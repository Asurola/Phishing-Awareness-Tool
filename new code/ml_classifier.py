"""
app/services/ml_classifier.py - ML model loader and prediction service.

Loads the trained Random Forest classifier and both TF-IDF vectorizers
once at application startup using a singleton pattern, then exposes a
`classify()` function that takes a parsed email and returns the model's
prediction plus the full feature vector used for that prediction.

The four artefacts required (all produced by
`phishing_detection_pipeline_v2.ipynb`):
  - phishing_model.pkl    : RandomForestClassifier, 322 input features
  - tfidf_subject.pkl     : TfidfVectorizer, 100-term vocabulary
  - tfidf_body.pkl        : TfidfVectorizer, 200-term vocabulary
  - feature_names.pkl     : ordered list of 322 feature names

Feature column order is authoritative - the model was trained with a
specific column ordering, and inference vectors MUST be built in that
same order. We read this from `feature_names.pkl` rather than hardcoding
it so retraining automatically propagates.
"""

from __future__ import annotations

import os
from typing import Any

import joblib
import numpy as np
import pandas as pd

from .feature_extractor import (
    extract_all_engineered_features,
    clean_body_for_tfidf,
)


# ─────────────────────────────────────────────────────────────────────────
# Singleton state - populated once by load_model()
# ─────────────────────────────────────────────────────────────────────────

_model: Any = None
_tfidf_subject: Any = None
_tfidf_body: Any = None
_feature_columns: list[str] | None = None
_subject_tfidf_cols: list[str] = []
_body_tfidf_cols: list[str] = []


# ─────────────────────────────────────────────────────────────────────────
# Loading
# ─────────────────────────────────────────────────────────────────────────

def load_model(models_dir: str) -> None:
    """
    Load all four ML artefacts from disk into module-level singletons.

    Called once at application startup from the app factory. Safe to call
    repeatedly - subsequent calls are no-ops unless artefacts have changed.

    Args:
        models_dir: Absolute path to the directory containing the four
                    .pkl files. Typically `<app>/ml/models/`.

    Raises:
        FileNotFoundError: If any of the four required files is missing.
        RuntimeError:      If the loaded model's expected feature count
                           does not match the length of feature_names.pkl.
    """
    global _model, _tfidf_subject, _tfidf_body, _feature_columns
    global _subject_tfidf_cols, _body_tfidf_cols

    model_path = os.path.join(models_dir, "phishing_model.pkl")
    subject_path = os.path.join(models_dir, "tfidf_subject.pkl")
    body_path = os.path.join(models_dir, "tfidf_body.pkl")
    features_path = os.path.join(models_dir, "feature_names.pkl")

    for path in (model_path, subject_path, body_path, features_path):
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Required ML artefact not found: {path}. "
                f"Copy the four .pkl files from the training notebook into "
                f"{models_dir}."
            )

    _model = joblib.load(model_path)
    _tfidf_subject = joblib.load(subject_path)
    _tfidf_body = joblib.load(body_path)
    _feature_columns = list(joblib.load(features_path))

    # Derive the TF-IDF column name lists from the loaded vectorizers.
    # These must use the same 'subj_' / 'body_' prefixes the notebook used
    # when building the feature matrix, otherwise reindex() will drop them.
    _subject_tfidf_cols = [
        f"subj_{t}" for t in _tfidf_subject.get_feature_names_out()
    ]
    _body_tfidf_cols = [
        f"body_{t}" for t in _tfidf_body.get_feature_names_out()
    ]

    # Sanity check: model's expected input width must match feature_names
    expected = getattr(_model, "n_features_in_", None)
    if expected is not None and expected != len(_feature_columns):
        raise RuntimeError(
            f"Model/feature mismatch: model expects {expected} features but "
            f"feature_names.pkl has {len(_feature_columns)}. The .pkl files "
            f"are out of sync - re-export all four from the notebook."
        )


def is_model_loaded() -> bool:
    """Return True if load_model() has been called successfully."""
    return _model is not None and _feature_columns is not None


# ─────────────────────────────────────────────────────────────────────────
# Inference
# ─────────────────────────────────────────────────────────────────────────

def classify(parsed_email: dict[str, Any]) -> dict[str, Any]:
    """
    Run the full inference pipeline on a parsed email.

    Pipeline:
      1. Extract 25 engineered features (header/body/URL).
      2. Transform subject and body through the pre-fitted TF-IDF
         vectorizers (100 + 200 features).
      3. Reindex into the training column order.
      4. Predict class and probability.

    Args:
        parsed_email: Output of `email_parser.parse_raw_email()`.

    Returns:
        Dictionary with:
          - 'prediction':   int (0 = legitimate, 1 = phishing)
          - 'probability':  float (model's P(phishing))
          - 'engineered':   dict of the 25 engineered features with their
                            active values (for the explanation engine)
          - 'feature_vector': dict of ALL 322 features (for diagnostics)

    Raises:
        RuntimeError: If load_model() has not been called first.
    """
    if not is_model_loaded():
        raise RuntimeError(
            "ML model is not loaded. Call load_model() at application "
            "startup before invoking classify()."
        )

    # Step 1: engineered features
    engineered = extract_all_engineered_features(parsed_email)

    # Step 2: TF-IDF features
    feats: dict[str, Any] = dict(engineered)

    subject_text = parsed_email.get("subject", "") or ""
    body_text = parsed_email.get("body", "") or ""

    subj_vec = _tfidf_subject.transform([subject_text]).toarray()[0]
    for col, val in zip(_subject_tfidf_cols, subj_vec):
        feats[col] = val

    body_vec = _tfidf_body.transform([clean_body_for_tfidf(body_text)]).toarray()[0]
    for col, val in zip(_body_tfidf_cols, body_vec):
        feats[col] = val

    # Step 3: reindex into training column order, filling missing with 0.
    # This is defensive: if any engineered feature somehow didn't get
    # computed (e.g. extractor raised an exception for an edge case),
    # reindex will insert a zero rather than crashing.
    x_series = pd.Series(feats).reindex(_feature_columns).fillna(0)
    x_array = x_series.values.reshape(1, -1)

    # Step 4: predict
    prediction = int(_model.predict(x_array)[0])
    probability = float(_model.predict_proba(x_array)[0][1])

    return {
        "prediction": prediction,
        "probability": probability,
        "engineered": engineered,
        "feature_vector": {k: _jsonable(v) for k, v in feats.items()},
    }


def _jsonable(value: Any) -> Any:
    """Convert numpy types to native Python so jsonify() doesn't choke."""
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, np.ndarray):
        return value.tolist()
    return value
