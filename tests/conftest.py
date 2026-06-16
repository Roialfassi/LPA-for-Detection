"""Pytest configuration: make the project modules in ``src/`` importable.

This lets the test suite run with a plain ``pytest`` from the repo root without
requiring an editable install (`pip install -e .`).
"""
import os
import sys

SRC = os.path.join(os.path.dirname(__file__), "..", "src")
if SRC not in sys.path:
    sys.path.insert(0, os.path.abspath(SRC))
