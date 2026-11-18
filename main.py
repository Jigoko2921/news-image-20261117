#!/usr/bin/env python3
"""make.fun bounty entry — news-image-20261117.

Copies ``entry.png`` (which sits beside this script) into the submission
output directory, creating that directory when it does not exist yet.

Output directory: ``$MAKEFUN_OUTPUT_DIR``, falling back to ``/output``.

The program is deterministic — the same input image always lands as the same
bytes — prints nothing on success and exits 0. Standard library only: no
network, no subprocesses, no third-party packages. Python 3.13.
"""

from __future__ import annotations

import os
import shutil
import sys

SOURCE_NAME = "entry.png"
OUTPUT_ENV_VAR = "MAKEFUN_OUTPUT_DIR"
DEFAULT_OUTPUT_DIR = "/output"


def source_path() -> str:
    """Absolute path of entry.png living next to this script."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, SOURCE_NAME)


def target_dir() -> str:
    """Absolute output directory, honouring $MAKEFUN_OUTPUT_DIR."""
    raw = os.environ.get(OUTPUT_ENV_VAR) or DEFAULT_OUTPUT_DIR
    return os.path.abspath(os.path.expanduser(raw))


def main() -> int:
    src = source_path()
    dst = os.path.join(target_dir(), SOURCE_NAME)

    if not os.path.isfile(src):
        print(f"main.py: source image not found: {src}", file=sys.stderr)
        return 1

    # Byte-exact copy of the payload; never rewrite the source in place.
    if os.path.realpath(src) == os.path.realpath(dst):
        return 0

    try:
        parent = os.path.dirname(dst)
        if parent:
            os.makedirs(parent, exist_ok=True)
        shutil.copyfile(src, dst)
    except OSError as exc:
        print(f"main.py: cannot write {dst}: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
