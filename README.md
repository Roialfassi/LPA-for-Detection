# LPA for Detection

Domain-based **Latent Personal Analysis (LPA)** and its use for impersonation /
AI-text detection.

LPA characterises how an author (or document) differs from the "typical" author
of a domain by comparing a per-document distribution against a **Domain
Vector Representation (DVR)**, using a symmetrised Kullback–Leibler divergence.
The resulting **signatures** and **sockpuppet distances** are used here to detect
impersonation and to distinguish human- from machine-generated text.

> Please cite:
> Mokryn, O., Ben-Shoshan, H. *Domain-based Latent Personal Analysis and its use
> for impersonation detection in social media.* User Model User-Adap Inter 31,
> 785–828.

## Repository layout

```
LPA-for-Detection/
├── src/                 # Core library (importable as LPA, algo, helpers, visualize)
│   ├── LPA.py           #   Matrix / Corpus, signatures, sockpuppet distance, PCA
│   ├── algo.py          #   KL-divergence / distance primitives
│   ├── helpers.py       #   IO + timing utilities
│   └── visualize.py     #   Altair charts (timelines, sockpuppet matrix, PCA)
├── scripts/             # Runnable scripts (e.g. run_lpa.py)
├── notebooks/           # Jupyter notebooks, grouped by purpose
│   ├── tutorial/        #   Walk-through of the method
│   ├── detection/       #   Impersonation / prompt-in-real detection
│   ├── experiments/     #   Experiment wrappers and runs
│   ├── preprocessing/   #   Data preparation
│   ├── political/       #   Political-speech case study
│   ├── generation/      #   Synthetic story generation
│   └── exploratory/     #   Scratch / idea testing
├── tests/               # pytest suite + fixtures (tests/test_data/)
├── docs/                # Documentation (see docs/STRUCTURE.md)
├── data/                # Local data archives (git-ignored)
├── archive/             # Old scratch notebooks kept for reference (git-ignored)
├── pyproject.toml       # Packaging + tooling config
├── requirements.txt
└── README.md
```

The large datasets (`Dataset/`, `Data-For-Model/`, `Idea-Dataset/`,
`Experiments/`) are **not** committed — they live at the repo root locally and
are git-ignored. They are kept at the root (rather than under `data/`) so the
notebooks' existing relative paths (e.g. `pd.read_csv("Dataset/...")`) keep
working. See [docs/STRUCTURE.md](docs/STRUCTURE.md) for details.

## Setup

```bash
python -m pip install -e .       # installs deps and the LPA modules (editable)
# or, without installing the package:
python -m pip install -r requirements.txt
```

Installing with `-e .` makes `from LPA import Corpus`, `import algo`, etc. work
from anywhere (including the notebooks) without path hacks.

## Running the notebooks

The notebooks were moved into `notebooks/<topic>/`. Each one now starts with a
small **path-bootstrap cell** that walks up to the repository root, `chdir`s
there, and adds `src/` to `sys.path`. Because of this:

- Run the **first cell first** (or "Run All"). After it runs, all the original
  relative imports and data paths resolve as before.
- Data is read relative to the repo root, so keep the local data folders
  (`Dataset/`, `Data-For-Model/`, …) at the root.

## Running the tests

```bash
pytest
```

`tests/conftest.py` puts `src/` on the path, and fixtures load from
`tests/test_data/`, so the suite is discoverable from the repo root without an
install.

> Note: `tests/test_LPA.py` is **legacy** — it predates the current code (it
> imports an `LPA` class that the `Corpus`-based design replaced, and asserts a
> natural-log result where `algo.KLD_distance` now uses `log2`). It was already
> failing before this reorganization and is kept only for reference. The
> reorganization fixed its import/data paths but not its outdated logic.
