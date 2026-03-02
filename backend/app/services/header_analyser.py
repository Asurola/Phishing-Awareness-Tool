"""
app/services/header_analyser.py — Email header feature extraction service.

Analyses the headers of a parsed email to extract 7 authentication and
routing features commonly used to identify phishing attempts.

Feature list (7 total):
    sender_domain_matches_from — Envelope sender domain == From header domain
    has_spf_pass               — SPF authentication result is 'pass'
    has_dkim_pass              — DKIM authentication result is 'pass'
    has_reply_to_mismatch      — Reply-To address differs from From address
    received_hop_count         — Number of 'Received' headers (routing depth)
    has_x_mailer               — Presence of X-Mailer header (bulk mailer indicator)
    from_domain_is_freemail    — Sender uses a free email provider (gmail, yahoo, etc.)

TODO (Phase 2): Implement the following functions.
"""

from __future__ import annotations
from typing import Any

# Well-known free email provider domains
FREEMAIL_DOMAINS: set[str] = {
    "gmail.com", "yahoo.com", "outlook.com", "hotmail.com",
    "live.com", "msn.com", "aol.com", "icloud.com",
    "protonmail.com", "zoho.com", "mail.com",
}


def extract_header_features(headers: dict[str, str]) -> dict[str, Any]:
    """
    Compute all 7 header features from the email headers dictionary.

    Args:
        headers: Dictionary of email header key-value pairs as returned
                 by email_parser.parse_raw_email() under the 'headers' key.
                 Header names are expected to be in their original mixed case
                 (e.g. 'Received', 'Authentication-Results', 'From').

    Returns:
        dict[str, Any]: Feature dictionary with the 7 header features.
                        Boolean features are Python bool.

    Example:
        >>> features = extract_header_features({"Reply-To": "evil@attacker.com",
        ...                                      "From": "support@bank.com"})
        >>> features["has_reply_to_mismatch"]
        True
    """
    # TODO (Phase 2): Implement with re module + string parsing
    raise NotImplementedError("header_analyser.extract_header_features is not yet implemented.")


def parse_authentication_results(auth_results_header: str) -> dict[str, str]:
    """
    Parse the 'Authentication-Results' email header to extract SPF and DKIM results.

    The Authentication-Results header is added by receiving mail servers and
    contains the results of SPF and DKIM verification checks.

    Args:
        auth_results_header: Raw value of the 'Authentication-Results' header
                             (e.g. "mx.google.com; spf=pass ... dkim=fail ...").

    Returns:
        dict[str, str]: Dictionary with keys 'spf' and 'dkim', each mapped
                        to their result string ('pass', 'fail', 'neutral',
                        'none', 'softfail', 'temperror', 'permerror', or
                        'unknown' if not found).
    """
    # TODO (Phase 2): Implement with re module
    raise NotImplementedError("header_analyser.parse_authentication_results is not yet implemented.")
