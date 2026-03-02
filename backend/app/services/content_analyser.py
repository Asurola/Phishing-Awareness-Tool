"""
app/services/content_analyser.py — Email body/content NLP feature extraction.

Analyses the plaintext and HTML body of an email to extract 11 content-based
features that are strong indicators of phishing attempts. These include
linguistic cues (urgency and threat language), structural cues (forms,
link-text mismatches), and presentation cues (generic greetings).

Feature list (11 total):
    urgency_word_count        — Count of urgency phrase matches
    threat_word_count         — Count of threat language matches
    reward_word_count         — Count of reward/lure language matches
    has_credential_request    — Body asks for passwords, SSNs, credit card info, etc.
    link_text_mismatch_count  — Hyperlinks where visible text URL ≠ href URL
    num_links                 — Total hyperlinks found in the body
    num_attachments           — Number of email attachments
    body_length               — Character count of the plaintext body
    has_html_form             — Body contains HTML <form> element
    greeting_is_generic       — Email uses generic greeting ("Dear Customer", etc.)
    has_spelling_errors       — Basic count of misspelled words

TODO (Phase 2): Implement the following functions.
"""

from __future__ import annotations
from typing import Any

# Urgency language patterns (case-insensitive)
URGENCY_WORDS: list[str] = [
    "immediately", "urgent", "urgently", "expires", "expiring",
    "suspend", "suspended", "verify now", "act now", "limited time",
    "action required", "important notice", "respond immediately",
]

# Threat language patterns
THREAT_WORDS: list[str] = [
    "locked", "compromised", "unauthorized", "suspended",
    "restricted", "blocked", "deactivated", "terminated",
    "illegal activity", "security breach",
]

# Reward / lure language patterns
REWARD_WORDS: list[str] = [
    "winner", "congratulations", "prize", "free", "gift",
    "reward", "bonus", "selected", "chosen", "lucky",
    "claim now", "won",
]

# Credential request patterns
CREDENTIAL_PATTERNS: list[str] = [
    "password", "passcode", "pin", "social security",
    "ssn", "credit card", "card number", "cvv", "bank account",
    "account number", "routing number", "date of birth",
]

# Generic greeting patterns
GENERIC_GREETINGS: list[str] = [
    "dear customer", "dear user", "dear account holder",
    "dear member", "dear valued customer", "dear client",
    "hello customer", "greetings",
]


def extract_content_features(
    body_text: str,
    body_html: str | None,
    links: list[dict],
    num_attachments: int,
) -> dict[str, Any]:
    """
    Compute all 11 content-based features from the email body.

    Args:
        body_text:       Plaintext version of the email body.
        body_html:       HTML version of the email body (may be None if
                         the email is plaintext only).
        links:           List of link dicts as produced by
                         email_parser.extract_urls_from_html(), each with
                         'url' and 'display_text' keys.
        num_attachments: Number of attachments reported by the email parser.

    Returns:
        dict[str, Any]: Feature dictionary with the 11 content features.

    Example:
        >>> features = extract_content_features(
        ...     body_text="Act now! Your account will be suspended.",
        ...     body_html=None, links=[], num_attachments=0)
        >>> features["urgency_word_count"]
        2
    """
    # TODO (Phase 2): Implement
    raise NotImplementedError("content_analyser.extract_content_features is not yet implemented.")


def count_keyword_matches(text: str, keywords: list[str]) -> int:
    """
    Count how many keywords from a list appear in the given text.

    Matching is case-insensitive. A keyword found multiple times is
    counted multiple times.

    Args:
        text:     Input text to search within.
        keywords: List of keyword strings or phrases to search for.

    Returns:
        int: Total number of keyword matches found.
    """
    # TODO (Phase 2): Implement with str.lower() + str.count()
    raise NotImplementedError("content_analyser.count_keyword_matches is not yet implemented.")
