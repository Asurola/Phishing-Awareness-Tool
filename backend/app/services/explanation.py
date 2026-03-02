"""
app/services/explanation.py — Human-readable explanation engine.

Takes the raw ML classification output (prediction + confidence +
feature importances) and the full feature dictionary, and generates a
structured, human-readable explanation that bridges the technical
detection result and the user-facing educational content.

The explanation includes:
  - A 0–100 risk score derived from the confidence and prediction.
  - A verdict string.
  - A list of individual threat flags grouped by category (URL, Header, Content),
    each with a severity level, finding summary, plain-English explanation,
    and a specific recommendation.
  - A list of summary recommendations for the user.

TODO (Phase 2): Implement the following functions.
"""

from __future__ import annotations
from typing import Any

# Severity thresholds for risk score
RISK_LOW_THRESHOLD: int = 35      # 0–34   → Low Risk
RISK_MEDIUM_THRESHOLD: int = 65   # 35–64  → Medium Risk
                                   # 65–100 → High Risk


def generate_explanation(
    prediction_result: dict[str, Any],
    feature_dict: dict[str, Any],
) -> dict[str, Any]:
    """
    Generate a structured, human-readable phishing analysis explanation.

    Converts ML binary prediction + confidence + feature importances into
    a structured result that the frontend can render directly, including
    individual threat flag cards and summary recommendations.

    Args:
        prediction_result: Dictionary as returned by ml_classifier.predict():
            {
                "prediction": "phishing" | "legitimate",
                "confidence": float,
                "feature_importances": { feature_name: importance_score, ... }
            }
        feature_dict: Full feature dictionary as returned by
                      feature_extractor.extract_features().

    Returns:
        dict[str, Any]: Explanation result with keys:
            - "risk_score" (int):                  0–100 risk score
            - "verdict" (str):                     Human-readable verdict
            - "flags" (list[dict]):                Threat flag cards
            - "summary_recommendations" (list[str]): High-level recommendations

        Each flag dict has:
            {
                "category": "URL" | "Header" | "Content",
                "severity": "high" | "medium" | "low",
                "finding": str,     — Short summary of the finding
                "explanation": str, — Detailed plain-English explanation
                "recommendation": str — Specific action the user should take
            }

    Example:
        >>> explain = generate_explanation(
        ...     {"prediction": "phishing", "confidence": 0.91, ...},
        ...     {"urgency_word_count": 4, "has_https": False, ...})
        >>> explain["risk_score"]
        91
    """
    # TODO (Phase 2): Implement
    raise NotImplementedError("explanation.generate_explanation is not yet implemented.")


def confidence_to_risk_score(prediction: str, confidence: float) -> int:
    """
    Convert ML prediction + confidence to a 0–100 integer risk score.

    For phishing predictions: risk_score = round(confidence * 100)
    For legitimate predictions: risk_score = round((1 - confidence) * 100)

    Args:
        prediction: 'phishing' or 'legitimate'
        confidence: Model confidence (0.0–1.0)

    Returns:
        int: Risk score from 0 (no risk) to 100 (certain phishing).
    """
    # TODO (Phase 2): Implement
    raise NotImplementedError("explanation.confidence_to_risk_score is not yet implemented.")


def get_verdict(risk_score: int) -> str:
    """
    Return a human-readable verdict string based on the risk score.

    Args:
        risk_score: Integer risk score from 0 to 100.

    Returns:
        str: One of:
            'Low Risk — Likely Legitimate'
            'Medium Risk — Treat with Caution'
            'High Risk — Likely Phishing'
    """
    if risk_score < RISK_LOW_THRESHOLD:
        return "Low Risk — Likely Legitimate"
    elif risk_score < RISK_MEDIUM_THRESHOLD:
        return "Medium Risk — Treat with Caution"
    else:
        return "High Risk — Likely Phishing"
