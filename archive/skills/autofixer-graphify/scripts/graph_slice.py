#!/usr/bin/env python3
"""Create a schema-limited graph slice for autofixer-graphify prompts."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PURPOSES = {"audit", "fix", "adjudication", "verification"}


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        return list(value.values())
    return []


def pick(mapping: dict[str, Any], *keys: str, default: str = "") -> str:
    for key in keys:
        value = mapping.get(key)
        if value is not None:
            return str(value)
    return default


def confidence(value: Any) -> str:
    if value is None:
        return "unknown"
    if isinstance(value, (int, float)):
        if value >= 0.8:
            return "high"
        if value >= 0.5:
            return "medium"
        return "low"
    text = str(value).lower()
    return text if text in {"high", "medium", "low", "unknown"} else "unknown"


def normalize_nodes(raw_graph: dict[str, Any]) -> list[dict[str, Any]]:
    raw_nodes = as_list(raw_graph.get("nodes") or raw_graph.get("Vertices") or raw_graph.get("vertices"))
    nodes: list[dict[str, Any]] = []
    for index, raw in enumerate(raw_nodes):
        if not isinstance(raw, dict):
            continue
        node_id = pick(raw, "id", "node_id", "key", default=f"node:{index}")
        nodes.append(
            {
                "id": node_id,
                "kind": pick(raw, "kind", "type", "category", default="unknown"),
                "label": pick(raw, "label", "name", "title", default=node_id),
                "path": pick(raw, "path", "file", "filepath", "source", default=""),
                "summary": pick(raw, "summary", "description", "text", "doc", default=""),
                "confidence": confidence(raw.get("confidence")),
                "reasons": [str(item) for item in as_list(raw.get("reasons") or raw.get("evidence"))],
            }
        )
    return nodes


def normalize_edges(raw_graph: dict[str, Any]) -> list[dict[str, Any]]:
    raw_edges = as_list(raw_graph.get("edges") or raw_graph.get("links") or raw_graph.get("relationships"))
    edges: list[dict[str, Any]] = []
    for index, raw in enumerate(raw_edges):
        if not isinstance(raw, dict):
            continue
        source = pick(raw, "source", "from", "src")
        target = pick(raw, "target", "to", "dst")
        if not source or not target:
            continue
        edges.append(
            {
                "id": pick(raw, "id", "edge_id", default=f"edge:{index}"),
                "source": source,
                "target": target,
                "kind": pick(raw, "kind", "type", "relation", "relationship", default="related"),
                "confidence": confidence(raw.get("confidence")),
                "evidence": [str(item) for item in as_list(raw.get("evidence") or raw.get("reasons"))],
            }
        )
    return edges


def node_matches(node: dict[str, Any], paths: list[str], symbols: list[str], queries: list[str]) -> bool:
    haystack = " ".join(
        str(node.get(key, "")).lower() for key in ("id", "kind", "label", "path", "summary")
    )
    needles = [item.lower() for item in paths + symbols + queries if item]
    if not needles:
        return True
    return any(needle in haystack for needle in needles)


def select_slice(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    paths: list[str],
    symbols: list[str],
    queries: list[str],
    max_nodes: int,
    max_edges: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    selected = [node for node in nodes if node_matches(node, paths, symbols, queries)]
    selected_ids = {str(node["id"]) for node in selected}

    neighbor_ids = set(selected_ids)
    for edge in edges:
        source = str(edge["source"])
        target = str(edge["target"])
        if source in selected_ids or target in selected_ids:
            neighbor_ids.add(source)
            neighbor_ids.add(target)

    by_id = {str(node["id"]): node for node in nodes}
    expanded = [by_id[node_id] for node_id in by_id if node_id in neighbor_ids]
    if not expanded:
        expanded = nodes[:max_nodes]
    expanded = expanded[:max_nodes]
    expanded_ids = {str(node["id"]) for node in expanded}
    selected_edges = [
        edge
        for edge in edges
        if str(edge["source"]) in expanded_ids and str(edge["target"]) in expanded_ids
    ][:max_edges]
    return expanded, selected_edges


def build_neighborhoods(
    focus_items: list[str],
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    if not focus_items:
        focus_items = ["repository"]
    node_ids = [str(node["id"]) for node in nodes]
    edge_ids = [str(edge["id"]) for edge in edges]
    paths = sorted({str(node.get("path", "")) for node in nodes if node.get("path")})
    tests = [path for path in paths if "test" in path.lower() or "spec" in path.lower()]
    entrypoints = [
        path
        for path in paths
        if path.endswith(("main.py", "index.js", "index.ts", "main.go", "main.rs", "app.py"))
    ]

    return [
        {
            "focus": item,
            "node_ids": node_ids,
            "edge_ids": edge_ids,
            "likely_affected_files": paths,
            "callers": [],
            "dependents": [],
            "shared_tests": tests,
            "entrypoints": entrypoints,
        }
        for item in focus_items
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph-json", required=True, help="Graphify graph JSON")
    parser.add_argument("--purpose", required=True, choices=sorted(PURPOSES))
    parser.add_argument("--workspace-fingerprint", default="")
    parser.add_argument("--coverage-mode", default="code-oriented")
    parser.add_argument("--limitation", action="append", default=[])
    parser.add_argument("--excluded-path", action="append", default=[])
    parser.add_argument("--path", action="append", default=[], dest="paths")
    parser.add_argument("--symbol", action="append", default=[], dest="symbols")
    parser.add_argument("--query", action="append", default=[], dest="queries")
    parser.add_argument("--max-nodes", type=int, default=80)
    parser.add_argument("--max-edges", type=int, default=160)
    parser.add_argument("--output", help="Write slice JSON to this file instead of stdout")
    args = parser.parse_args()

    graph_path = Path(args.graph_json).resolve()
    try:
        raw_graph = json.loads(graph_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Could not read graph JSON: {exc}", file=sys.stderr)
        return 1
    if not isinstance(raw_graph, dict):
        print("Graph JSON must be an object", file=sys.stderr)
        return 1

    nodes = normalize_nodes(raw_graph)
    edges = normalize_edges(raw_graph)
    selected_nodes, selected_edges = select_slice(
        nodes,
        edges,
        args.paths,
        args.symbols,
        args.queries,
        args.max_nodes,
        args.max_edges,
    )
    focus_items = args.paths + args.symbols + args.queries
    output = {
        "schema_version": "autofixer-graphify.slice.v1",
        "purpose": args.purpose,
        "source": {
            "graph_path": str(graph_path),
            "workspace_fingerprint": args.workspace_fingerprint,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
        "coverage": {
            "mode": args.coverage_mode,
            "limitations": [str(item) for item in args.limitation],
            "excluded_paths": [str(item) for item in args.excluded_path],
        },
        "focus": {
            "paths": [str(item) for item in args.paths],
            "symbols": [str(item) for item in args.symbols],
            "queries": [str(item) for item in args.queries],
        },
        "nodes": selected_nodes,
        "edges": selected_edges,
        "neighborhoods": build_neighborhoods(focus_items, selected_nodes, selected_edges),
    }

    text = json.dumps(output, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
