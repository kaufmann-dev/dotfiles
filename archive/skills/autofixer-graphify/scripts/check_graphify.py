#!/usr/bin/env python3
"""Check that Graphify is installed and callable."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys


INSTALL_GUIDANCE = (
    "Graphify is required but the `graphify` command is unavailable. "
    "Install the `graphifyy` package, for example with `uv tool install graphifyy` "
    "or `pipx install graphifyy`, and ensure `graphify` is on PATH."
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--command", default="graphify", help="Graphify command name or path")
    parser.add_argument(
        "--skip-version",
        action="store_true",
        help="Only check PATH lookup; do not try to execute the command.",
    )
    args = parser.parse_args()

    graphify = shutil.which(args.command)
    if graphify is None:
        print(INSTALL_GUIDANCE, file=sys.stderr)
        return 2

    if not args.skip_version:
        try:
            subprocess.run(
                [graphify, "--help"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
                timeout=20,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            print(f"Graphify was found at {graphify}, but it could not be executed: {exc}", file=sys.stderr)
            print(INSTALL_GUIDANCE, file=sys.stderr)
            return 2

    print(f"Graphify command found: {graphify}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
