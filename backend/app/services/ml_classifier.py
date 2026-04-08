"""
app/services/ml_classifier.py — ML phishing classifier service.
Loads the trained Random Forest model and pkl artifacts, then
provides a predict() function that mirrors the training pipeline.
"""

import os
import re
import joblib
import pandas as pd

# Module-level cache — loaded once at app startup
_model = None
_tfidf_body = None
_tfidf_subject = None
_feature_names = None

# Resolve path to models directory relative to this file
_MODELS_DIR = os.path.join(os.path.dirname(__file__), '..', 'ml', 'models')

# Urgency keywords used during training (must match notebook exactly)
_URGENCY_WORDS = [
    'urgent', 'immediately', 'verify', 'suspend',
    'confirm', 'click', 'limited', 'expire', 'warning'
]


def load_model(models_dir: str | None = None) -> bool:
    """
    Load all pkl artifacts into module-level cache.
    Called once at application startup from the app factory.

    Returns True if successful, False otherwise.
    """
    global _model, _tfidf_body, _tfidf_subject, _feature_names
    base = models_dir or _MODELS_DIR
    try:
        _model         = joblib.load(os.path.join(base, 'phishing_model.pkl'))
        _tfidf_body    = joblib.load(os.path.join(base, 'tfidf_body.pkl'))
        _tfidf_subject = joblib.load(os.path.join(base, 'tfidf_subject.pkl'))
        _feature_names = joblib.load(os.path.join(base, 'feature_names.pkl'))
        print(f"[ml_classifier] Model loaded — {len(_feature_names)} features")
        return True
    except Exception as e:
        print(f"[ml_classifier] WARNING: Model load failed — {e}")
        return False


def is_model_loaded() -> bool:
    return _model is not None


def _clean_text(text: str) -> str:
    """Mirror the text cleaning applied during training."""
    text = re.sub(r'[^a-zA-Z\s]', ' ', str(text))
    text = re.sub(r'\s+', ' ', text).strip().lower()
    return text


def _extract_engineered_features(subject: str, body: str, headers: dict) -> dict:
    """
    Reproduce the engineered (non-TF-IDF) features from the training pipeline.
    When real header data is available it is used; otherwise safe defaults apply.
    """
    body_lower = body.lower()
    url_count  = len(re.findall(r'https?://', body_lower))
    word_count = max(len(body.split()), 1)

    # SPF / DKIM from Authentication-Results header (if present)
    auth_header = headers.get('Authentication-Results', '').lower()
    has_spf     = int('spf=pass' in auth_header)
    has_dkim    = int('dkim=pass' in auth_header)

    # Reply-To mismatch
    from_addr    = headers.get('From', '')
    reply_to     = headers.get('Reply-To', '')
    sender_reply = int(bool(reply_to) and reply_to.strip() != from_addr.strip())

    # Received hops
    received_hops = len([k for k in headers if k.lower() == 'received'])
    if received_hops == 0:
        received_hops = 1  # default when no headers provided

    # Display name spoofing (name contains a domain-like string but differs from address)
    display_spoofed = 0
    if '<' in from_addr:
        display_part = from_addr.split('<')[0].strip().lower()
        if '.' in display_part and '@' not in display_part:
            display_spoofed = 1

    return {
        'sender_reply_mismatch': sender_reply,
        'has_spf':               has_spf,
        'has_dkim':              has_dkim,
        'received_hops':         received_hops,
        'display_name_spoofed':  display_spoofed,
        'urgency_keyword_count': sum(body_lower.count(w) for w in _URGENCY_WORDS),
        'has_html':              int('<a href' in body_lower or '<html' in body_lower),
        'html_to_text_ratio':    0.0,
        'url_count':             url_count,
        'body_url_ratio':        url_count / word_count,
    }


def predict(subject: str, body: str, headers: dict | None = None) -> dict:
    if not is_model_loaded():
        raise RuntimeError("ML model is not loaded. Call load_model() first.")

    headers = headers or {}

    # --- Engineered features ---
    eng_features = _extract_engineered_features(subject, body, headers)
    all_features = dict(eng_features)

    # --- TF-IDF features ---
    # Use the vectorizer's own feature names to avoid index misalignment
    body_vec = _tfidf_body.transform([_clean_text(body)]).toarray()[0]
    subj_vec = _tfidf_subject.transform([_clean_text(subject)]).toarray()[0]

    for name, val in zip(_tfidf_body.get_feature_names_out(), body_vec):
        all_features[f'body_{name}'] = float(val)

    for name, val in zip(_tfidf_subject.get_feature_names_out(), subj_vec):
        all_features[f'subj_{name}'] = float(val)

    # --- Build ordered feature vector matching training order ---
    feat_series = pd.Series(all_features).reindex(_feature_names).fillna(0)
    X_input = feat_series.values.reshape(1, -1)

    # --- Predict ---
    prob  = _model.predict_proba(X_input)[0]
    label = int(_model.predict(X_input)[0])

    # --- Top feature importances ---
    top_features = {}
    if hasattr(_model, 'feature_importances_'):
        imp_series = pd.Series(_model.feature_importances_, index=_feature_names)
        top_features = {k: float(v) for k, v in imp_series.nlargest(15).items()}

    return {
        'prediction':            'phishing' if label == 1 else 'legitimate',
        'confidence':            float(prob[1] if label == 1 else prob[0]),
        'phishing_probability':  float(prob[1]),
        'top_features':          top_features,
        'engineered_features':   eng_features,
    }