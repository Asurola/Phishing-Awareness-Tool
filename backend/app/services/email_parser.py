"""
app/services/email_parser.py — Raw email parser service.

Responsible for accepting raw email content (either as a plaintext string
copied from an email client, or as the bytes of a .eml file) and returning
a structured dictionary of its components — sender, recipients, subject,
headers, body text, HTML body, and attachment metadata.

This structured representation is then passed to the feature extractor,
which delegates to the URL, header, and content analysers.

TODO (Phase 2): Implement the following functions.
"""

from __future__ import annotations
import email as email_lib
from email.message import Message
from typing import Any


def parse_raw_email(raw_email: str) -> dict[str, Any]:
    """
    Parse a raw email string into a structured dictionary.

    Handles both plaintext emails and RFC 822/MIME formatted emails
    (including those with headers, multipart bodies, and attachments).

    Args:
        raw_email: The full raw email content as a string. May include
                   full headers (Received, From, To, etc.) or just the body.

    Returns:
        dict: Parsed email components with the following keys:
            - "from_address" (str | None): Sender email address.
            - "to_addresses" (list[str]): List of recipient addresses.
            - "reply_to" (str | None): Reply-To header value.
            - "subject" (str | None): Email subject line.
            - "date" (str | None): Date header value.
            - "headers" (dict[str, str]): All raw header key-value pairs.
            - "body_text" (str): Plaintext body content.
            - "body_html" (str | None): HTML body content if present.
            - "urls" (list[str]): All URLs extracted from the body.
            - "attachments" (list[dict]): Attachment metadata dicts with
              "filename" and "content_type" keys.

    Raises:
        ValueError: If raw_email is empty or unparseable.

    Example:
        >>> result = parse_raw_email("From: phisher@evil.com\\n\\nClick here!")
        >>> result["from_address"]
        'phisher@evil.com'
    """
    # TODO (Phase 2): Implement full parser using Python email stdlib
    raise NotImplementedError("email_parser.parse_raw_email is not yet implemented.")


def extract_urls_from_text(text: str) -> list[str]:
    """
    Extract all URLs found in a block of text using a regular expression.

    Args:
        text: Plain text (or stripped HTML) to search for URLs.

    Returns:
        list[str]: Deduplicated list of URL strings found in the text.
    """
    # TODO (Phase 2): Implement with re module
    raise NotImplementedError("email_parser.extract_urls_from_text is not yet implemented.")


def extract_urls_from_html(html: str) -> list[str]:
    """
    Extract all href and src URLs from an HTML email body.

    Parses the HTML DOM to retrieve both the href attribute values
    (actual destinations) and the visible link text, which are then
    used by the content analyser to detect link-text mismatches.

    Args:
        html: Raw HTML string (the HTML body part of the email).

    Returns:
        list[dict]: List of dicts with "url" (href) and "display_text" keys.
    """
    # TODO (Phase 2): Implement with html.parser or BeautifulSoup
    raise NotImplementedError("email_parser.extract_urls_from_html is not yet implemented.")
