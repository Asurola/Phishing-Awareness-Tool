"""
app/services/feature_extractor.py — Feature extraction orchestrator.

This module is the central coordinator for the feature extraction pipeline.
It accepts a parsed email dictionary (from email_parser.py) and calls
each sub-analyser in turn to produce a flat feature dictionary suitable
for input to the ML classifier.

The full feature set (31 features) is made up of:
  - 13 URL features       (from url_analyser.py)
  - 7  Header features    (from header_analyser.py)
  - 11 Content features   (from content_analyser.py)

The same extraction functions used here during live detection should be
applied to the training dataset (in ml/train_model.py) to ensure
consistency between training and inference.

TODO (Phase 2): Implement the following functions.
"""

from __future__ import annotations
from typing import Any

# TODO (Phase 2): Import sub-analysers
# from .url_analyser import extract_url_features
# from .header_analyser import extract_header_features
# from .content_analyser import extract_content_features


def extract_features(parsed_email: dict[str, Any]) -> dict[str, Any]:
    """
    Orchestrate feature extraction from a parsed email.

    Calls each sub-analyser module and merges their output into a single
    flat dictionary of named features. The resulting dict is used both
    for ML inference and for display in the frontend feature breakdown panel.

    Args:
        parsed_email: Structured email dictionary as produced by
                      email_parser.parse_raw_email(). Expected keys:
                      'headers', 'body_text', 'body_html', 'urls',
                      'from_address', 'reply_to', 'attachments'.

    Returns:
        dict[str, Any]: Flat dictionary of feature name → feature value.
            URL features will use the worst-case (most suspicious) values
            across all URLs found in the email.
            Example:
                {
                    "url_length": 87,
                    "has_ip_address": False,
                    "has_https": False,
                    "urgency_word_count": 4,
                    "has_spf_pass": False,
                    ...
                }

    Raises:
        ValueError: If parsed_email is missing required keys.
    """
    # TODO (Phase 2): Implement full pipeline
    raise NotImplementedError("feature_extractor.extract_features is not yet implemented.")


def get_feature_names() -> list[str]:
    """
    Return the ordered list of feature names used by the ML model.

    This list must match the column order used during training
    (see ml/train_model.py). Used by ml_classifier.py to construct
    the feature vector in the correct order.

    Returns:
        list[str]: Ordered list of feature name strings.
    """
    return [
        # URL features
        "url_length",
        "has_ip_address",
        "has_https",
        "num_dots",
        "num_hyphens",
        "num_subdomains",
        "has_at_symbol",
        "has_redirect",
        "uses_shortener",
        "path_length",
        "has_suspicious_tld",
        "domain_age_days",
        "has_prefix_suffix",
        # Header features
        "sender_domain_matches_from",
        "has_spf_pass",
        "has_dkim_pass",
        "has_reply_to_mismatch",
        "received_hop_count",
        "has_x_mailer",
        "from_domain_is_freemail",
        # Content features
        "urgency_word_count",
        "threat_word_count",
        "reward_word_count",
        "has_credential_request",
        "link_text_mismatch_count",
        "num_links",
        "num_attachments",
        "body_length",
        "has_html_form",
        "greeting_is_generic",
        "has_spelling_errors",
    ]
