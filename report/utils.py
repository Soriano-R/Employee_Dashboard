"""Shared utilities for the report layer (model loading, paths, etc.)."""
import pickle
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent      # repo root
model_path   = project_root / "assets" / "model.pkl"       # <root>/assets/model.pkl

def load_model():
    """Return the un-pickled scikit-learn model."""
    with model_path.open("rb") as fh:
        return pickle.load(fh)