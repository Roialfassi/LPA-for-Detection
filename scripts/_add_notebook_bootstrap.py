"""One-off helper used during the repository reorganization.

Inserts a small "path bootstrap" cell at the top of every notebook under
``notebooks/`` so each notebook can still import the project code (``src/``)
and read the data folders at the repository root, even though the notebooks now
live in ``notebooks/<topic>/`` subfolders.

Idempotent: running it twice will not add the cell twice.

Usage:  python scripts/_add_notebook_bootstrap.py
"""
from __future__ import annotations

from pathlib import Path

import nbformat

MARKER = "LPA repo path bootstrap"

BOOTSTRAP = """\
# --- LPA repo path bootstrap (added during repository reorganization) ---
# Makes this notebook find the project source (src/) and the data folders at the
# repository root, no matter which notebooks/<topic>/ subfolder it lives in.
# Run this cell first.
import os, sys

_root = os.path.abspath(os.getcwd())
while not os.path.exists(os.path.join(_root, "pyproject.toml")) and os.path.dirname(_root) != _root:
    _root = os.path.dirname(_root)
os.chdir(_root)                       # so relative data paths (e.g. "Dataset/...") resolve
_src = os.path.join(_root, "src")
if _src not in sys.path:
    sys.path.insert(0, _src)          # so `from LPA import ...` works without installing
print("working dir set to repo root:", _root)
"""


def already_has_bootstrap(nb) -> bool:
    return bool(nb.cells) and MARKER in nb.cells[0].get("source", "")


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    notebooks = sorted((root / "notebooks").rglob("*.ipynb"))
    changed, skipped = 0, 0
    for path in notebooks:
        nb = nbformat.read(path, as_version=4)
        if already_has_bootstrap(nb):
            skipped += 1
            print(f"skip (already has bootstrap): {path.relative_to(root)}")
            continue
        nb.cells.insert(0, nbformat.v4.new_code_cell(BOOTSTRAP))
        nbformat.write(nb, path)
        changed += 1
        print(f"added bootstrap: {path.relative_to(root)}")
    print(f"\nDone. {changed} updated, {skipped} already had it.")


if __name__ == "__main__":
    main()
