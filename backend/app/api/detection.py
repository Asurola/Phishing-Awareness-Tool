"""
app/api/detection.py — Detection (email analysis) API endpoint.

Handles incoming email submissions (raw text or .eml file upload) and
orchestrates the full analysis pipeline:
  1. Parse the raw email into structured components.
  2. Extract features (URL, header, content).
  3. Run the ML classifier.
  4. Generate human-readable explanation flags.
  5. Return the structured result to the frontend.

Endpoints:
    POST /api/analyse
        Body (JSON):          { "raw_email": "<string>" }
        Body (multipart):     file=<.eml file>
        Response:             { risk_score, verdict, flags, recommendations, feature_vector }
"""

from flask import Blueprint, request, jsonify

# TODO (Phase 2): Import service modules once implemented
# from ..services.email_parser import parse_email
# from ..services.feature_extractor import extract_features
# from ..services.ml_classifier import classify
# from ..services.explanation import generate_explanation
# from ..utils.validators import validate_email_input

detection_bp = Blueprint("detection", __name__)


@detection_bp.route("/analyse", methods=["POST"])
def analyse_email():
    """
    Analyse a submitted email for phishing indicators.

    Accepts either:
      - JSON body with 'raw_email' string key, or
      - multipart/form-data with an attached .eml file.

    Returns:
        JSON: {
            "risk_score": int (0–100),
            "verdict": str,
            "flags": list[dict],
            "summary_recommendations": list[str],
            "feature_vector": dict
        }

    Raises:
        400: If no email content is provided.
        500: If an internal error occurs during analysis.
    """
    try:
        raw_email: str | None = None

        # Handle JSON body
        if request.is_json:
            data = request.get_json()
            raw_email = data.get("raw_email", "").strip()

        # Handle .eml file upload
        elif "file" in request.files:
            file = request.files["file"]
            raw_email = file.read().decode("utf-8", errors="replace")

        if not raw_email:
            return jsonify({"error": "No email content provided."}), 400

        # ── Placeholder response (Phase 1 scaffold) ──────────────────────
        # The full pipeline will be implemented in Phase 2.
        # For now, return a stubbed response so the frontend can be built.
        placeholder_response = {
            "risk_score": 0,
            "verdict": "Analysis not yet implemented — Phase 2",
            "flags": [],
            "summary_recommendations": [
                "The detection engine will be implemented in Phase 2."
            ],
            "feature_vector": {},
        }
        return jsonify(placeholder_response), 200

    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500
