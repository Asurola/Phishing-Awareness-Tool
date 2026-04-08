"""
app/api/detection.py — Detection (email analysis) API endpoint.
"""

import email as email_lib
from flask import Blueprint, request, jsonify
from ..services.ml_classifier import predict, is_model_loaded
from ..services.explanation import generate_explanation

detection_bp = Blueprint('detection', __name__)


def _parse_raw_email(raw: str) -> tuple[str, str, dict]:
    """
    Parse a raw email string into (subject, body, headers).
    Falls back gracefully if the input is just body text with no headers.
    """
    try:
        msg = email_lib.message_from_string(raw)

        subject = msg.get('Subject', '') or ''
        headers = dict(msg.items())

        # Extract plain-text body
        body = ''
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                if ctype == 'text/plain':
                    body += part.get_payload(decode=True).decode('utf-8', errors='replace')
                    break
        else:
            payload = msg.get_payload(decode=True)
            if payload:
                body = payload.decode('utf-8', errors='replace')
            else:
                # Payload is already a string (no encoding)
                body = msg.get_payload() or ''

        # If body is empty the entire raw input is probably just body text
        if not body.strip():
            body = raw

        return subject.strip(), body.strip(), headers

    except Exception:
        # Fallback: treat entire input as body
        return '', raw.strip(), {}


@detection_bp.route('/analyse', methods=['POST'])
def analyse_email():
    """
    Analyse a submitted email for phishing indicators.

    Accepts JSON body { "raw_email": "..." } or multipart .eml file upload.

    Returns:
        JSON: { risk_score, verdict, prediction, confidence,
                flags, summary_recommendations, feature_vector }
    """
    try:
        raw_email: str | None = None

        if request.is_json:
            data = request.get_json()
            raw_email = (data.get('raw_email') or '').strip()
        elif 'file' in request.files:
            raw_email = request.files['file'].read().decode('utf-8', errors='replace')

        if not raw_email:
            return jsonify({'error': 'No email content provided.'}), 400

        # ── Parse ────────────────────────────────────────────────────────
        subject, body, headers = _parse_raw_email(raw_email)

        # ── Classify ─────────────────────────────────────────────────────
        if not is_model_loaded():
            # Rule-based fallback when model files are missing
            return jsonify(_rule_based_fallback(subject, body)), 200

        result = predict(subject, body, headers)

        # ── Explain ──────────────────────────────────────────────────────
        explanation = generate_explanation(result, subject, body)

        # Attach the feature vector for the frontend (raw view / debug)
        explanation['feature_vector'] = result.get('engineered_features', {})

        return jsonify(explanation), 200

    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500


def _rule_based_fallback(subject: str, body: str) -> dict:
    """
    Simple rule-based response when the ML model is unavailable.
    Ensures the API is always usable even without the pkl files.
    """
    body_lower    = body.lower()
    urgency_words = ['urgent', 'verify', 'suspend', 'click here', 'confirm', 'expire']
    urgency_count = sum(body_lower.count(w) for w in urgency_words)
    url_count     = len(__import__('re').findall(r'https?://', body_lower))

    score = min(urgency_count * 15 + url_count * 10, 95)

    return {
        'risk_score':  score,
        'verdict':     'High Risk — Likely Phishing' if score >= 65
                       else 'Medium Risk — Treat with Caution' if score >= 35
                       else 'Low Risk — Likely Legitimate',
        'prediction':  'phishing' if score >= 65 else 'legitimate',
        'confidence':  round(score / 100, 2),
        'flags': [{
            'category':       'System',
            'severity':       'low',
            'finding':        'Rule-based analysis (ML model not loaded)',
            'explanation':    'The ML model could not be loaded. Basic rule-based analysis was used instead.',
            'recommendation': 'Place phishing_model.pkl in backend/app/ml/models/ to enable full analysis.',
        }],
        'summary_recommendations': ['ML model not available — results are approximate.'],
        'feature_vector': {},
    }