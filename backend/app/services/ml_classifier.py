"""
app/services/ml_classifier.py — Machine learning phishing classifier service.

Loads a pre-trained scikit-learn model (saved with joblib) and provides
functions to:
  1. Load the model into memory at application start.
  2. Accept a feature dictionary and return a classification prediction.
  3. Return per-feature importance scores for the explanation engine.

The model is trained by ml/train_model.py and saved to
app/ml/models/phishing_classifier.pkl (path configured via MODEL_PATH env var).

TODO (Phase 2): Implement the following functions after training the model.
"""

from __future__ import annotations
import os
from typing import Any

# Module-level model cache — loaded once at first use (lazy loading)
_model = None
_scaler = None


def load_model(model_path: str | None = None) -> bool:
    """
    Load the trained ML model and scaler from disk into module-level cache.

    Should be called once at application startup or on first prediction request.
    After loading, the model instance is cached at module level so subsequent
    calls are instant.

    Args:
        model_path: Absolute or relative path to the .pkl model file.
                    If None, reads from MODEL_PATH environment variable.
                    Defaults to 'app/ml/models/phishing_classifier.pkl'.

    Returns:
        bool: True if the model was successfully loaded, False otherwise.
    """
    global _model, _scaler
    # TODO (Phase 2): Implement with joblib.load()
    return False


def is_model_loaded() -> bool:
    """
    Check whether the ML model is currently loaded in memory.

    Returns:
        bool: True if the model cache is populated, False otherwise.
    """
    return _model is not None


def predict(feature_dict: dict[str, Any]) -> dict[str, Any]:
    """
    Classify an email as 'phishing' or 'legitimate' using the loaded model.

    Converts the feature dictionary to an ordered numpy array matching the
    training feature order (from feature_extractor.get_feature_names()),
    applies the saved scaler, and runs the classifier.

    Args:
        feature_dict: Feature dictionary as produced by
                      feature_extractor.extract_features().

    Returns:
        dict[str, Any]: Prediction result with keys:
            - "prediction" (str):         'phishing' or 'legitimate'
            - "confidence" (float):        Model confidence score (0.0–1.0)
            - "feature_importances" (dict): Feature name → importance score

    Raises:
        RuntimeError: If the model has not been loaded yet.
        ValueError:   If feature_dict is missing required features.

    Example:
        >>> load_model()
        True
        >>> result = predict({"url_length": 87, "has_https": False, ...})
        >>> result["prediction"]
        'phishing'
    """
    if not is_model_loaded():
        raise RuntimeError(
            "ML model is not loaded. Call load_model() first."
        )
    # TODO (Phase 2): Implement prediction pipeline
    raise NotImplementedError("ml_classifier.predict is not yet implemented.")
