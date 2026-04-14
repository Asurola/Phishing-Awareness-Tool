"""
app/api/detection.py - Detection (email analysis) API endpoint.

Handles incoming email submissions (raw text or .eml file upload) and
orchestrates the full analysis pipeline:
  1. Parse the raw email into structured components.
  2. Extract features (header + body + URL + TF-IDF).
  3. Run the ML classifier.
  4. Generate human-readable explanation flags.
  5. Return the structured result to the frontend.

Endpoints:
    POST /api/analyse
        Body (JSON):      { "raw_email": "<string>" }
        Body (multipart): file=<.eml file>

        Response (200):
            {
                "risk_score":              int (0-100),
                "verdict":                 str,
                "phishing_probability":    float,
                "flags":                   list[dict],
                "summary_recommendations": list[str],
                "feature_vector":          dict
            }
"""

from flask import Blueprint, request, jsonify

from ..services.email_parser import parse_raw_email
from ..services.ml_classifier import classify, is_model_loaded
from ..services.explanation import (
    generate_flags,
    risk_score,
    verdict as compute_verdict,
    summary_recommendations,
)

detection_bp = Blueprint("detection", __name__)


@detection_bp.route("/analyse", methods=["POST"])
def analyse_email():
    """
    Analyse a submitted email for phishing indicators.

    Accepts either a JSON body with a `raw_email` string key, or a
    multipart/form-data request with an attached .eml file. Either way,
    the body is fed into the same parse → extract → classify → explain
    pipeline.

    Returns:
        JSON response with the full analysis result, or an error object
        with an appropriate HTTP status code.
    """
    try:
        raw_email: str = ""

        # Accept JSON body...
        if request.is_json:
            data = request.get_json() or {}
            raw_email = (data.get("raw_email") or "").strip()

        # ...or a multipart file upload
        elif "file" in request.files:
            file = request.files["file"]
            raw_bytes = file.read()
            raw_email = raw_bytes.decode("utf-8", errors="replace")

        if not raw_email:
            return jsonify({"error": "No email content provided."}), 400

        # Refuse to serve if the model never loaded (e.g. missing .pkl files)
        if not is_model_loaded():
            return jsonify({
                "error": (
                    "ML model is not loaded on the server. Ensure the four "
                    ".pkl files are present in app/ml/models/ and restart."
                )
            }), 503

        # 1. Parse → 2. Classify (includes feature extraction + TF-IDF)
        parsed = parse_raw_email(raw_email)
        result = classify(parsed)

        # 3. Explain
        flags = generate_flags(result["engineered"], result["probability"])
        response = {
            "risk_score":              risk_score(result["probability"]),
            "verdict":                 compute_verdict(result["probability"]),
            "phishing_probability":    round(result["probability"], 4),
            "flags":                   flags,
            "summary_recommendations": summary_recommendations(
                flags, result["probability"]
            ),
            "feature_vector":          result["feature_vector"],
            "parsed_email":            {
                # Echo back the parsed fields so the frontend can show
                # the user exactly what the model saw. Helpful for
                # debugging and for the educational aspect of the tool.
                "sender":  parsed.get("sender", ""),
                "subject": parsed.get("subject", ""),
                "body_preview": (parsed.get("body", "") or "")[:500],
                "url_count": len(
                    (parsed.get("urls", "") or "").split()
                ),
            },
        }
        return jsonify(response), 200

    except Exception as e:
        # Don't leak internals in production - but for the FYP demo it's
        # useful to see the actual error in the response body.
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500