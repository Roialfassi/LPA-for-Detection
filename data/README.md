# data/

Local data archives. **Everything in this folder except this README is
git-ignored** (see the repo `.gitignore`).

Use this directory for downloaded/derived data archives (e.g. zipped datasets).

## Note on the active datasets

The datasets the notebooks read at runtime are kept at the **repository root**,
not here, so the notebooks' relative paths keep working:

- `Dataset/`
- `Data-For-Model/`
- `Idea-Dataset/`
- `Experiments/`
- `frequency.csv`

See [../docs/STRUCTURE.md](../docs/STRUCTURE.md) for the reasoning and how to
fully consolidate data under `data/` later if desired.
