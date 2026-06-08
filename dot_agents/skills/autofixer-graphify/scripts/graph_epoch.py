#!/usr/bin/env python3
"""Compute a deterministic content fingerprint for a workspace."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


DEFAULT_EXCLUDES = {
    ".git",
    ".hg",
    ".svn",
    ".DS_Store",
    "graphify-out",
    ".graphify",
}


def run_git_files(workspace: Path) -> list[Path] | None:
    try:
        inside = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=workspace,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return None
    if inside.returncode != 0 or inside.stdout.strip() != "true":
        return None

    result = subprocess.run(
        ["git", "ls-files", "-co", "--exclude-standard", "-z"],
        cwd=workspace,
        check=True,
        capture_output=True,
    )
    paths = [Path(item.decode()) for item in result.stdout.split(b"\0") if item]
    return paths


def walk_files(workspace: Path) -> list[Path]:
    paths: list[Path] = []
    for root, dirs, files in os.walk(workspace):
        dirs[:] = [item for item in dirs if item not in DEFAULT_EXCLUDES]
        root_path = Path(root)
        for file_name in files:
            if file_name in DEFAULT_EXCLUDES:
                continue
            paths.append((root_path / file_name).relative_to(workspace))
    return paths


def should_exclude(path: Path, excludes: set[str]) -> bool:
    parts = set(path.parts)
    return any(exclude in parts or path.match(exclude) for exclude in excludes)


def hash_file(path: Path) -> tuple[str, int, str]:
    if path.is_symlink():
        target = os.readlink(path)
        return hashlib.sha256(f"symlink:{target}".encode()).hexdigest(), len(target), "symlink"

    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            size += len(chunk)
            digest.update(chunk)
    return digest.hexdigest(), size, "file"


def build_epoch(workspace: Path, excludes: set[str]) -> dict[str, object]:
    git_paths = run_git_files(workspace)
    paths = git_paths if git_paths is not None else walk_files(workspace)
    entries: list[dict[str, object]] = []
    aggregate = hashlib.sha256()

    for rel_path in sorted(set(paths), key=lambda item: item.as_posix()):
        if should_exclude(rel_path, excludes):
            continue
        abs_path = workspace / rel_path
        if not abs_path.exists() and not abs_path.is_symlink():
            continue
        if abs_path.is_dir():
            continue
        file_hash, size, kind = hash_file(abs_path)
        rel = rel_path.as_posix()
        aggregate.update(rel.encode())
        aggregate.update(b"\0")
        aggregate.update(kind.encode())
        aggregate.update(b"\0")
        aggregate.update(str(size).encode())
        aggregate.update(b"\0")
        aggregate.update(file_hash.encode())
        aggregate.update(b"\0")
        stat = abs_path.lstat()
        entries.append(
            {
                "path": rel,
                "kind": kind,
                "sha256": file_hash,
                "size": size,
                "mode": stat.st_mode & 0o777,
            }
        )

    return {
        "schema_version": "autofixer-graphify.epoch.v1",
        "workspace": str(workspace),
        "algorithm": "sha256(path,kind,size,content)",
        "fingerprint": aggregate.hexdigest(),
        "file_count": len(entries),
        "files": entries,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=".", help="Workspace root to fingerprint")
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Additional path component or glob to exclude. Can be repeated.",
    )
    parser.add_argument("--output", help="Write epoch JSON to this file instead of stdout")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    if not workspace.exists():
        print(f"Workspace does not exist: {workspace}", file=sys.stderr)
        return 1

    epoch = build_epoch(workspace, DEFAULT_EXCLUDES | set(args.exclude))
    text = json.dumps(epoch, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
