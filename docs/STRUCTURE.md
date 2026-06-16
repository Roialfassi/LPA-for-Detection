# Repository structure & reorganization notes

This file documents how the repository is organised and the decisions made when
it was restructured from a flat layout (everything in the root) into the current
folders.

## Goals of the reorganization

1. Clean up a root directory that held ~30 mixed files (source, notebooks, data,
   scratch).
2. Group files by role without breaking the existing notebooks, which import the
   local modules and read data via **relative paths**.

## Where things went

| Area | Location | Notes |
| --- | --- | --- |
| Core library | `src/` | `LPA.py`, `algo.py`, `helpers.py`, `visualize.py` |
| Scripts | `scripts/` | `run_lpa.py`, plus `_add_notebook_bootstrap.py` (the one-off used during the reorg) |
| Notebooks | `notebooks/<topic>/` | grouped by purpose — see below |
| Tests | `tests/` | `test_LPA.py`, fixtures in `tests/test_data/`, `conftest.py` |
| Docs | `docs/` | this file |
| Local data archives | `data/` | git-ignored |
| Old scratch | `archive/` | `Untitled.ipynb`, `new.ipynb`, `P.txt` — git-ignored, kept not deleted |

### Notebook grouping

- `notebooks/tutorial/` — `LPA - Tutorial.ipynb`
- `notebooks/detection/` — `Detector.ipynb`, `LPA-Detection-FindPromptinReal.ipynb`,
  `LPA-Detection-FindPromptinReal-WithStemmingAndStopwords.ipynb`,
  `LPA-DetectionFoodBlogs.ipynb`
- `notebooks/experiments/` — the `LPA_Experiment - Wrapper*` notebooks and
  `LPA_Experiment - real in prompts.ipynb`
- `notebooks/preprocessing/` — `PreProcess Data LPA2 .ipynb`,
  `PresidentialSpeeches - PreProcess.ipynb`
- `notebooks/political/` — `LPA-Political.ipynb`
- `notebooks/generation/` — `Generate tons of stories.ipynb`
- `notebooks/exploratory/` — `Testing-Ideas.ipynb`

## How the notebooks still work after moving

Two things change when a notebook moves into `notebooks/<topic>/`: its imports of
the local modules, and its relative data paths (Jupyter sets a kernel's working
directory to the notebook's own folder).

Both are handled by a **path-bootstrap cell** inserted at the top of every
notebook:

```python
# --- LPA repo path bootstrap (added during repository reorganization) ---
import os, sys
_root = os.path.abspath(os.getcwd())
while not os.path.exists(os.path.join(_root, "pyproject.toml")) and os.path.dirname(_root) != _root:
    _root = os.path.dirname(_root)
os.chdir(_root)                       # relative data paths (e.g. "Dataset/...") resolve
_src = os.path.join(_root, "src")
if _src not in sys.path:
    sys.path.insert(0, _src)          # `from LPA import ...` works without installing
```

It finds the repo root by looking for `pyproject.toml`, `chdir`s there, and puts
`src/` on `sys.path`. **Run it first** (or "Run All"). The helper that inserted
it is `scripts/_add_notebook_bootstrap.py` and is idempotent.

## Data location

The bulky datasets are git-ignored and intentionally kept at the **repo root**
(`Dataset/`, `Data-For-Model/`, `Idea-Dataset/`, `Experiments/`, plus
`frequency.csv`) so that the many relative paths inside the notebooks keep
resolving after the bootstrap `chdir`s to the root. Moving them under `data/`
would require rewriting those paths inside every notebook.

If you want a fully consolidated `data/` directory later, the follow-up is:
move the folders under `data/` and update the `pd.read_csv("Dataset/...")`-style
strings in the notebooks (or define a `DATA_DIR` and prefix paths with it).
