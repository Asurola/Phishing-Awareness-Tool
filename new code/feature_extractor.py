"""
app/services/feature_extractor.py — Feature extraction for the ML pipeline.

This module is ported directly from the training notebook
(`phishing_detection_pipeline_v2.ipynb`) to guarantee that the features
produced at inference time are byte-identical to those used during model
training. Any divergence between training and serving features would
silently break predictions, so the three core extractors below must
mirror the notebook exactly.

Feature groups (25 engineered features total):
  - Header features (5):  sender/reply mismatch, SPF/DKIM, received hops,
                          display-name spoofing
  - Body features (11):   urgency keywords, HTML signals, URL counts,
                          vocabulary stats, credential/financial keywords
  - URL features (8):     IP-based URLs, @ symbol, length, dot count,
                          HTTPS, subdomain depth, suspicious TLD,
                          unique external domain count

On top of these, the ML classifier also appends 100 TF-IDF subject
features and 200 TF-IDF body features, for a total of 322 features —
but those are applied in `ml_classifier.py` using the pre-fitted
vectorizers, not here.
"""

from __future__ import annotations

import re
from typing import Any

import numpy as np
import pandas as pd
import tldextract

# ─────────────────────────────────────────────────────────────────────────
# Shared constants — must exactly match the training notebook
# ─────────────────────────────────────────────────────────────────────────

URGENCY_WORDS: list[str] = [
    "verify", "immediately", "urgent", "suspended", "limited", "expire",
    "confirm", "update", "validate", "click here", "act now",
    "account locked", "unusual activity", "security alert",
    "unauthorised", "unauthorized", "compromised", "blocked", "unusual",
    "restricted",
]

CREDENTIAL_WORDS: list[str] = [
    "password", "username", "login", "sign in", "credentials", "ssn",
    "credit card",
]

FINANCIAL_WORDS: list[str] = [
    "bank account", "wire transfer", "western union", "inheritance",
    "lottery", "prize",
]

BRAND_DOMAINS: dict[str, str] = {
    "paypal": "paypal.com",
    "amazon": "amazon.com",
    "apple": "apple.com",
    "microsoft": "microsoft.com",
    "google": "google.com",
    "facebook": "facebook.com",
    "netflix": "netflix.com",
}

SUSPICIOUS_TLDS: set[str] = {
    "tk", "ml", "ga", "cf", "gq", "xyz", "top", "club", "work",
}

URL_REGEX = re.compile(r'https?://[^\s<>"\']+')
HTML_TAG_REGEX = re.compile(r"<[^>]+>")


# ─────────────────────────────────────────────────────────────────────────
# Shared helpers
# ─────────────────────────────────────────────────────────────────────────

def _extract_urls_from_text(text: Any) -> list[str]:
    """Find all http(s) URLs in a string; returns [] for null/empty input."""
    if text is None or (isinstance(text, float) and pd.isnull(text)):
        return []
    return URL_REGEX.findall(str(text))


def _safe_str(value: Any) -> str:
    """Coerce any value (including NaN / None) to a string."""
    if value is None:
        return ""
    try:
        if pd.isnull(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value)


# ─────────────────────────────────────────────────────────────────────────
# Header features (ported from notebook Cell 7)
# ─────────────────────────────────────────────────────────────────────────

def extract_header_features(row: dict[str, Any]) -> dict[str, int]:
    """
    Compute the 5 header-derived features from a parsed email row.

    Args:
        row: Dictionary with at least 'sender' and 'body' keys.

    Returns:
        Dictionary of feature name → integer value. All header features
        are 0/1 flags except `received_hops` which counts occurrences.
    """
    features: dict[str, int] = {}
    sender = _safe_str(row.get("sender", ""))
    body_raw = _safe_str(row.get("body", ""))

    # Extract the sender domain by matching against '@domain.tld'
    sender_domain = ""
    match = re.search(r"@([\w\.-]+)", sender)
    if match:
        sender_domain = match.group(1).lower()

    # Reply-To domain mismatch — only triggers if both domains parseable
    # and differ (a common phishing indicator where a spoofed From header
    # is paired with an attacker-controlled Reply-To address)
    reply_to_match = re.search(
        r"Reply-To:.*?@([\w\.-]+)", body_raw, re.IGNORECASE
    )
    reply_domain = reply_to_match.group(1).lower() if reply_to_match else ""
    features["sender_reply_mismatch"] = int(
        bool(sender_domain and reply_domain and sender_domain != reply_domain)
    )

    # SPF / DKIM pass indicators — looked up in body text because the
    # training dataset stored these as quoted strings within the body
    features["has_spf"] = int(
        bool(re.search(r"spf=pass", body_raw, re.IGNORECASE))
    )
    features["has_dkim"] = int(
        bool(re.search(r"dkim=pass", body_raw, re.IGNORECASE))
    )

    # Routing depth — more hops sometimes correlate with relayed phish
    features["received_hops"] = len(
        re.findall(r"^Received:", body_raw, re.MULTILINE)
    )

    # Display name spoofing — brand keyword present in sender name but
    # the corresponding legit domain is NOT in the actual sender domain
    spoofed = 0
    for brand, legit_domain in BRAND_DOMAINS.items():
        if brand in sender.lower() and legit_domain not in sender_domain:
            spoofed = 1
            break
    features["display_name_spoofed"] = spoofed

    return features


# ─────────────────────────────────────────────────────────────────────────
# Body features (ported from notebook Cell 7)
# ─────────────────────────────────────────────────────────────────────────

def extract_body_features(row: dict[str, Any]) -> dict[str, Any]:
    """
    Compute the 11 body-text features from a parsed email row.

    Args:
        row: Dictionary with at least 'body' and 'subject' keys.

    Returns:
        Dictionary of feature name → value. Mix of int flags, counts,
        and float ratios.
    """
    features: dict[str, Any] = {}
    body = _safe_str(row.get("body", ""))
    subject = _safe_str(row.get("subject", ""))
    full_text = (subject + " " + body).lower()

    # Urgency keyword count — summed across all phrases in URGENCY_WORDS
    features["urgency_keyword_count"] = sum(
        full_text.count(kw) for kw in URGENCY_WORDS
    )

    # HTML detection — simple substring check for common tags
    body_lower = body.lower()
    features["has_html"] = int(
        "<html" in body_lower or "<a href" in body_lower
    )

    # HTML-to-text ratio — fraction of the body that is markup characters.
    # Phishing emails with heavy styling and hidden spans skew high.
    html_chars = sum(len(tag) for tag in HTML_TAG_REGEX.findall(body))
    total_chars = len(body)
    features["html_to_text_ratio"] = (
        round(html_chars / total_chars, 4) if total_chars > 0 else 0
    )

    # URL count in body
    body_urls = _extract_urls_from_text(body)
    features["url_count"] = len(body_urls)

    # Body-URL ratio — what fraction of body text is URL text. Emails
    # that are mostly links are suspicious.
    url_chars = sum(len(u) for u in body_urls)
    features["body_url_ratio"] = (
        round(url_chars / total_chars, 4) if total_chars > 0 else 0
    )

    # Vocabulary: average word length (phishing often uses simpler words)
    words = re.findall(r"\b[a-zA-Z]+\b", body)
    features["avg_word_length"] = (
        round(float(np.mean([len(w) for w in words])), 2) if words else 0
    )

    # Exclamation marks — crude proxy for emotional manipulation
    features["exclamation_count"] = body.count("!")

    # Credential / financial keyword flags (0/1)
    features["credential_request"] = int(
        any(w in full_text for w in CREDENTIAL_WORDS)
    )
    features["financial_threat"] = int(
        any(w in full_text for w in FINANCIAL_WORDS)
    )

    return features


# ─────────────────────────────────────────────────────────────────────────
# URL features (ported from notebook Cell 7)
# ─────────────────────────────────────────────────────────────────────────

def extract_url_features(row: dict[str, Any]) -> dict[str, int]:
    """
    Compute the 8 URL-based features from a parsed email row.

    When multiple URLs are present, most features describe only the FIRST
    URL (matching the training notebook's behaviour), except
    `external_domain_count` which counts unique domains across all URLs.

    Args:
        row: Dictionary with 'urls' and/or 'body' keys. URLs may appear in
             either field; both are scanned.

    Returns:
        Dictionary of feature name → integer value.
    """
    features: dict[str, int] = {
        "url_uses_ip": 0,
        "url_has_at_symbol": 0,
        "url_length": 0,
        "url_dot_count": 0,
        "url_has_https": 0,
        "url_subdomain_depth": 0,
        "url_suspicious_tld": 0,
        "external_domain_count": 0,
    }

    urls_col = _safe_str(row.get("urls", ""))
    body_urls = _extract_urls_from_text(row.get("body", ""))
    col_urls = _extract_urls_from_text(urls_col)
    all_urls = col_urls + body_urls

    if not all_urls:
        return features

    # Features describing the first URL only (notebook convention)
    url = all_urls[0]
    features["url_length"] = len(url)
    features["url_has_at_symbol"] = int("@" in url)
    features["url_has_https"] = int(url.startswith("https"))
    features["url_uses_ip"] = int(
        bool(re.search(r"https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", url))
    )

    try:
        extracted = tldextract.extract(url)
        subdomain = extracted.subdomain
        features["url_subdomain_depth"] = (
            len(subdomain.split(".")) if subdomain else 0
        )
        features["url_dot_count"] = url.count(".")
        features["url_suspicious_tld"] = int(
            extracted.suffix in SUSPICIOUS_TLDS
        )
    except Exception:
        # tldextract failures are swallowed — leave defaults in place
        pass

    # Count unique external domains across ALL URLs in the email
    unique_domains: set[str] = set()
    for u in all_urls:
        try:
            ext = tldextract.extract(u)
            if ext.domain:
                unique_domains.add(f"{ext.domain}.{ext.suffix}")
        except Exception:
            pass
    features["external_domain_count"] = len(unique_domains)

    return features


# ─────────────────────────────────────────────────────────────────────────
# Orchestrator
# ─────────────────────────────────────────────────────────────────────────

def extract_all_engineered_features(parsed_email: dict[str, Any]) -> dict[str, Any]:
    """
    Run all three extractors and merge their outputs into one flat dict.

    This is the single entry point called by the ML classifier at
    inference time. TF-IDF features are added separately in
    `ml_classifier.py` because they require the pre-fitted vectorizers.

    Args:
        parsed_email: Output of `email_parser.parse_raw_email()`.

    Returns:
        Flat dictionary of 25 engineered features.
    """
    features: dict[str, Any] = {}
    features.update(extract_header_features(parsed_email))
    features.update(extract_body_features(parsed_email))
    features.update(extract_url_features(parsed_email))
    return features


def clean_body_for_tfidf(text: Any) -> str:
    """
    Prepare body text for the body TF-IDF vectorizer.

    Matches the notebook's `clean_body_for_tfidf` function exactly:
    strips HTML, replaces URLs with a sentinel 'URL' token, collapses
    whitespace, and lowercases.
    """
    if text is None:
        return ""
    try:
        if pd.isnull(text):
            return ""
    except (TypeError, ValueError):
        pass

    s = HTML_TAG_REGEX.sub(" ", str(text))
    s = re.sub(r"https?://\S+", " URL ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s.lower()
