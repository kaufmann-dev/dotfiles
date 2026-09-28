#!/usr/bin/env python3
"""Validate autofixer-graphify graph slices."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


TOP_LEVEL_KEYS = {
    "schema_version",
    "purpose",
    "source",
    "coverage",
    "focus",
    "nodes",
    "edges",
    "neighborhoods",
}
SOURCE_KEYS = {"graph_path", "workspace_fingerprint", "generated_at"}
COVERAGE_KEYS = {"mode", "limitations", "excluded_paths"}
FOCUS_KEYS = {"paths", "symbols", "queries"}
NODE_KEYS = {"id", "kind", "label", "path", "summary", "confidence", "reasons"}
EDGE_KEYS = {"id", "source", "target", "kind", "confidence", "evidence"}
NEIGHBORHOOD_KEYS = {
    "focus",
    "node_ids",
    "edge_ids",
    "likely_affected_files",
    "callers",
    "dependents",
    "shared_tests",
    "entrypoints",
}
PURPOSES = {"audit", "fix", "adjudication", "verification"}
CONFIDENCE = {"high", "medium", "low", "unknown"}

FORBIDDEN_KEY_PARTS = {
    "accepted_finding",
    "accepted_findings",
    "clean_confirmation",
    "clean_confirmation_count",
    "conclusion",
    "convergence",
    "coordinator",
    "failed_repair",
    "finding_fingerprint",
    "ledger",
    "needs_evidence",
    "previous_auditor",
    "previous_fixer",
    "prior_finding",
    "prior_findings",
    "rejected_finding",
    "rejected_findings",
    "repair_attempt",
    "repair_attempts",
    "unresolved_finding",
    "unresolved_findings",
}
FORBIDDEN_TEXT_PHRASES = {
    "accepted finding",
    "accepted findings",
    "clean-confirmation count",
    "clean confirmation count",
    "coordinator conclusion",
    "coordinator conclusions",
    "failed repair count",
    "finding fingerprint",
    "findings marked needs evidence",
    "previous auditor",
    "previous fixer",
    "prior finding",
    "prior findings",
    "rejected finding",
    "rejected findings",
    "repair attempt",
    "repair attempts",
    "unresolved finding",
    "unresolved findings",
}


def fail(message: str) -> None:
    raise ValueError(message)


def require_keys(obj: dict[str, Any], allowed: set[str], path: str) -> None:
    unknown = set(obj) - allowed
    if unknown:
        fail(f"{path} contains unknown field(s): {', '.join(sorted(unknown))}")


def require_string_list(value: Any, path: str) -> None:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        fail(f"{path} must be an array of strings")


def scan_forbidden(value: Any, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = key.lower().replace("-", "_")
            if normalized in FORBIDDEN_KEY_PARTS:
                fail(f"{path}.{key} contains forbidden autofixer state")
            scan_forbidden(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            scan_forbidden(child, f"{path}[{index}]")
    elif isinstance(value, str):
        normalized = value.lower()
        for phrase in FORBIDDEN_TEXT_PHRASES:
            if phrase in normalized:
                fail(f"{path} contains forbidden autofixer state")


def validate_slice(data: dict[str, Any]) -> None:
    scan_forbidden(data)
    require_keys(data, TOP_LEVEL_KEYS, "$")
    if data.get("schema_version") != "autofixer-graphify.slice.v1":
        fail("$.schema_version must be autofixer-graphify.slice.v1")
    if data.get("purpose") not in PURPOSES:
        fail("$.purpose must be one of audit, fix, adjudication, verification")

    source = data.get("source")
    if not isinstance(source, dict):
        fail("$.source must be an object")
    require_keys(source, SOURCE_KEYS, "$.source")
    for key in SOURCE_KEYS:
        if not isinstance(source.get(key), str):
            fail(f"$.source.{key} must be a string")

    coverage = data.get("coverage")
    if not isinstance(coverage, dict):
        fail("$.coverage must be an object")
    require_keys(coverage, COVERAGE_KEYS, "$.coverage")
    if not isinstance(coverage.get("mode"), str):
        fail("$.coverage.mode must be a string")
    require_string_list(coverage.get("limitations"), "$.coverage.limitations")
    require_string_list(coverage.get("excluded_paths"), "$.coverage.excluded_paths")

    focus = data.get("focus")
    if not isinstance(focus, dict):
        fail("$.focus must be an object")
    require_keys(focus, FOCUS_KEYS, "$.focus")
    for key in FOCUS_KEYS:
        require_string_list(focus.get(key), f"$.focus.{key}")

    nodes = data.get("nodes")
    if not isinstance(nodes, list):
        fail("$.nodes must be an array")
    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            fail(f"$.nodes[{index}] must be an object")
        require_keys(node, NODE_KEYS, f"$.nodes[{index}]")
        for key in {"id", "kind", "label", "path", "summary", "confidence"}:
            if not isinstance(node.get(key), str):
                fail(f"$.nodes[{index}].{key} must be a string")
        if node.get("confidence") not in CONFIDENCE:
            fail(f"$.nodes[{index}].confidence must be high, medium, low, or unknown")
        require_string_list(node.get("reasons"), f"$.nodes[{index}].reasons")

    edges = data.get("edges")
    if not isinstance(edges, list):
        fail("$.edges must be an array")
    for index, edge in enumerate(edges):
        if not isinstance(edge, dict):
            fail(f"$.edges[{index}] must be an object")
        require_keys(edge, EDGE_KEYS, f"$.edges[{index}]")
        for key in EDGE_KEYS - {"evidence"}:
            if not isinstance(edge.get(key), str):
                fail(f"$.edges[{index}].{key} must be a string")
        if edge.get("confidence") not in CONFIDENCE:
            fail(f"$.edges[{index}].confidence must be high, medium, low, or unknown")
        require_string_list(edge.get("evidence"), f"$.edges[{index}].evidence")

    neighborhoods = data.get("neighborhoods")
    if not isinstance(neighborhoods, list):
        fail("$.neighborhoods must be an array")
    for index, neighborhood in enumerate(neighborhoods):
        if not isinstance(neighborhood, dict):
            fail(f"$.neighborhoods[{index}] must be an object")
        require_keys(neighborhood, NEIGHBORHOOD_KEYS, f"$.neighborhoods[{index}]")
        if not isinstance(neighborhood.get("focus"), str):
            fail(f"$.neighborhoods[{index}].focus must be a string")
        for key in NEIGHBORHOOD_KEYS - {"focus"}:
            require_string_list(neighborhood.get(key), f"$.neighborhoods[{index}].{key}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slice_json", help="Slice JSON file to validate")
    args = parser.parse_args()

    try:
        data = json.loads(Path(args.slice_json).read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            fail("slice must be a JSON object")
        validate_slice(data)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Invalid slice: {exc}", file=sys.stderr)
        return 1

    print("Slice is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
