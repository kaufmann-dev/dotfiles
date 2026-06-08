#!/usr/bin/env python3
"""Build or refresh a transient Graphify snapshot for a workspace."""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


DEEP_EXTENSIONS = {
    ".pdf",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".svg",
    ".mp4",
    ".mov",
    ".avi",
    ".mkv",
    ".mp3",
    ".wav",
    ".flac",
    ".ogg",
}
DOCUMENTATION_EXTENSIONS = {
    ".adoc",
    ".md",
    ".mdx",
    ".org",
    ".rst",
    ".text",
    ".txt",
}
DOCUMENTATION_PATH_PARTS = {
    "doc",
    "docs",
    "documentation",
}

DEFAULT_SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    "graphify-out",
    ".graphify",
}


def load_epoch(path: Path | None) -> dict[str, object] | None:
    if path is None:
        return None
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def listed_paths(epoch: dict[str, object] | None, workspace: Path) -> list[Path]:
    if epoch is not None:
        files = epoch.get("files", [])
        return [Path(str(item["path"])) for item in files if isinstance(item, dict) and "path" in item]

    paths: list[Path] = []
    for root, dirs, files in os.walk(workspace):
        dirs[:] = [item for item in dirs if item not in DEFAULT_SKIP_DIRS]
        root_path = Path(root)
        for name in files:
            paths.append((root_path / name).relative_to(workspace))
    return paths


def matches_any(path: Path, patterns: list[str]) -> bool:
    text = path.as_posix()
    return any(fnmatch.fnmatch(text, pattern) for pattern in patterns)


def is_deep_semantic_path(path: Path) -> bool:
    suffix = path.suffix.lower()
    if suffix in DEEP_EXTENSIONS:
        return True
    if suffix in DOCUMENTATION_EXTENSIONS:
        return True
    return any(part.lower() in DOCUMENTATION_PATH_PARTS for part in path.parts)


def partition_paths(paths: list[Path], excludes: list[str]) -> tuple[list[Path], list[Path]]:
    included: list[Path] = []
    deep: list[Path] = []
    for path in paths:
        if matches_any(path, excludes):
            continue
        if is_deep_semantic_path(path):
            deep.append(path)
        else:
            included.append(path)
    return included, deep


def mirror_workspace(workspace: Path, mirror: Path, paths: list[Path], reset: bool) -> None:
    if reset and mirror.exists():
        shutil.rmtree(mirror)
    mirror.mkdir(parents=True, exist_ok=True)
    expected = {path.as_posix() for path in paths}
    if not reset:
        for existing in sorted(mirror.rglob("*"), reverse=True):
            if existing.is_dir():
                if existing.name == "graphify-out":
                    continue
                try:
                    existing.rmdir()
                except OSError:
                    pass
                continue
            rel = existing.relative_to(mirror).as_posix()
            if rel.startswith("graphify-out/"):
                continue
            if rel not in expected:
                existing.unlink()
    for rel_path in paths:
        src = workspace / rel_path
        if not src.exists() and not src.is_symlink():
            continue
        dst = mirror / rel_path
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.is_symlink():
            target = os.readlink(src)
            dst.symlink_to(target)
        else:
            shutil.copy2(src, dst)


def find_graph_json(cache_dir: Path) -> Path | None:
    candidates = sorted(cache_dir.rglob("graph.json"))
    if candidates:
        return candidates[0]
    candidates = sorted(cache_dir.rglob("*graph*.json"))
    return candidates[0] if candidates else None


def cache_matches_previous(cache_dir: Path, previous_fingerprint: str | None) -> bool:
    if not previous_fingerprint:
        return False
    metadata_path = cache_dir / "autofixer-graphify-snapshot.json"
    if not metadata_path.exists():
        return False
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    return metadata.get("workspace_fingerprint") == previous_fingerprint


def run_graphify(
    graphify: str,
    source_dir: Path,
    output_dir: Path,
    include_deep: bool,
) -> subprocess.CompletedProcess[str]:
    if include_deep:
        command = [graphify, "extract", str(source_dir), "--out", str(output_dir), "--no-cluster"]
    else:
        command = [graphify, "update", str(source_dir), "--no-cluster"]
    return subprocess.run(command, cwd=output_dir, check=False, capture_output=True, text=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=".", help="Workspace root")
    parser.add_argument("--epoch-json", help="Current epoch JSON from graph_epoch.py")
    parser.add_argument("--cache-dir", help="Transient cache directory. Defaults to a temp directory.")
    parser.add_argument("--previous-fingerprint", help="Fingerprint from the prior graph epoch")
    parser.add_argument("--include-deep", action="store_true", help="Include files requiring deep semantic extraction")
    parser.add_argument(
        "--require-approval-for-deep",
        action="store_true",
        help="Fail when deep semantic files are in scope and --include-deep is not set.",
    )
    parser.add_argument("--exclude", action="append", default=[], help="Glob to exclude from the mirrored source")
    parser.add_argument("--command", default="graphify", help="Graphify command name or path")
    args = parser.parse_args()

    graphify = shutil.which(args.command)
    if graphify is None:
        print(
            "Graphify is required but the `graphify` command is unavailable. "
            "Install the `graphifyy` package and ensure `graphify` is on PATH.",
            file=sys.stderr,
        )
        return 2

    workspace = Path(args.workspace).resolve()
    epoch = load_epoch(Path(args.epoch_json).resolve() if args.epoch_json else None)
    fingerprint = str(epoch.get("fingerprint", "")) if epoch else ""

    cache_dir = Path(args.cache_dir).resolve() if args.cache_dir else Path(
        tempfile.mkdtemp(prefix="autofixer-graphify-")
    )
    cache_dir.mkdir(parents=True, exist_ok=True)

    paths = listed_paths(epoch, workspace)
    included, deep = partition_paths(paths, args.exclude)
    if deep and args.require_approval_for_deep and not args.include_deep:
        print("Deep semantic extraction requires explicit approval for:", file=sys.stderr)
        for path in deep:
            print(f"- {path.as_posix()}", file=sys.stderr)
        return 3
    if args.include_deep:
        included = included + deep

    source_dir = cache_dir / "source"
    output_dir = cache_dir / "graphify"
    output_dir.mkdir(parents=True, exist_ok=True)

    incremental = cache_matches_previous(cache_dir, args.previous_fingerprint) and not args.include_deep
    if not incremental and output_dir.exists():
        shutil.rmtree(output_dir)
        output_dir.mkdir(parents=True)

    mirror_workspace(workspace, source_dir, included, reset=not incremental)
    result = run_graphify(graphify, source_dir, output_dir, args.include_deep)
    if result.returncode != 0:
        print(result.stderr or result.stdout, file=sys.stderr)
        return result.returncode

    graph_json = find_graph_json(cache_dir)
    metadata = {
        "schema_version": "autofixer-graphify.snapshot.v1",
        "workspace": str(workspace),
        "workspace_fingerprint": fingerprint,
        "cache_dir": str(cache_dir),
        "source_dir": str(source_dir),
        "output_dir": str(output_dir),
        "graph_json": str(graph_json) if graph_json else None,
        "mode": "code-oriented" if not args.include_deep else "deep-approved",
        "incremental": incremental,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "coverage_limitations": [] if args.include_deep or not deep else ["deep semantic files excluded"],
        "excluded_paths": [path.as_posix() for path in ([] if args.include_deep else deep)],
    }
    metadata_path = cache_dir / "autofixer-graphify-snapshot.json"
    metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(metadata, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
