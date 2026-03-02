"""
app/services/url_analyser.py — URL feature extraction service.

Analyses URLs extracted from an email body and computes 13 phishing-related
features per URL. When multiple URLs are present, the feature_extractor
selects the worst-case (most suspicious) values across all URLs.

Feature list (13 total):
    url_length          — Total character length of URL
    has_ip_address      — URL contains a raw IP address instead of a domain
    has_https           — URL uses HTTPS scheme
    num_dots            — Number of dots in the URL
    num_hyphens         — Number of hyphens in the domain component
    num_subdomains      — Number of subdomains (dot-separated labels before the TLD+1)
    has_at_symbol       — URL contains '@' symbol (can redirect to a different host)
    has_redirect        — URL contains '//' redirect pattern within the path
    uses_shortener      — Domain matches known URL shortener list
    path_length         — Character length of the URL path component
    has_suspicious_tld  — TLD is in suspicious list (.tk, .ml, .ga, .cf, .gq, .xyz, etc.)
    domain_age_days     — Days since domain registration (int or None if unavailable)
    has_prefix_suffix   — Domain contains a hyphen (e.g. paypal-secure.com)

TODO (Phase 2): Implement the following functions.
"""

from __future__ import annotations
from typing import Any

# Known URL shortener domains
SHORTENER_DOMAINS: set[str] = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly",
    "is.gd", "buff.ly", "adf.ly", "shorte.st", "cutt.ly",
}

# Suspicious top-level domains associated with phishing
SUSPICIOUS_TLDS: set[str] = {
    ".tk", ".ml", ".ga", ".cf", ".gq", ".xyz", ".top", ".buzz",
    ".click", ".link", ".work", ".party",
}


def extract_url_features(url: str) -> dict[str, Any]:
    """
    Compute all 13 URL features for a single URL string.

    Args:
        url: A URL string extracted from the email body (e.g. from an
             href attribute or plain-text hyperlink).

    Returns:
        dict[str, Any]: Feature dictionary with keys matching the
                        feature names listed in the module docstring.
                        Boolean features are Python bool (not 0/1 int).

    Example:
        >>> features = extract_url_features("http://paypa1-secure.com/login")
        >>> features["has_https"]
        False
        >>> features["has_prefix_suffix"]
        True
    """
    # TODO (Phase 2): Implement using tldextract, urllib.parse, re
    raise NotImplementedError("url_analyser.extract_url_features is not yet implemented.")


def analyse_urls(urls: list[str]) -> dict[str, Any]:
    """
    Analyse a list of URLs and return the worst-case feature values.

    For boolean features, 'worst case' means True if any URL has that
    feature. For integer features, 'worst case' means the maximum value
    across all URLs.

    Args:
        urls: List of URL strings extracted from the email.

    Returns:
        dict[str, Any]: Merged worst-case feature dictionary.
                        Returns all-zero/False defaults if urls is empty.
    """
    # TODO (Phase 2): Implement
    raise NotImplementedError("url_analyser.analyse_urls is not yet implemented.")
