"""
app/services/email_parser.py — Email parsing service.

Parses raw email content (either a pasted string or the contents of a .eml
file) into the structured dictionary format that the feature extractor
expects.

The output schema matches the row format used during training in the
ML notebook:

    {
        "sender":  "<From header or empty string>",
        "subject": "<Subject header or empty string>",
        "body":    "<plain-text body, HTML decoded where possible>",
        "urls":    "<space-separated URLs found in the body>",
    }

This schema is deliberately flat and string-valued so the feature
extraction functions (ported verbatim from the notebook) can consume
it without modification.
"""

from __future__ import annotations

import email
import re
from email import policy
from email.message import EmailMessage
from html import unescape
from typing import Any

# URL extraction pattern — matches http(s) URLs, excluding trailing punctuation
URL_REGEX = re.compile(r'https?://[^\s<>"\'\)]+')

# Simple HTML tag stripper — removes tags without parsing structure
HTML_TAG_REGEX = re.compile(r'<[^>]+>')


def parse_raw_email(raw: str) -> dict[str, Any]:
    """
    Parse a raw email string into the structured format used by the
    feature extractor.

    The parser handles three input shapes, in order of preference:
      1. A full RFC-822 email with headers and body (typical .eml content)
      2. A partial email with recognisable headers but no body separator
      3. A plain text blob with no headers at all — treated entirely as body

    Args:
        raw: The raw email content as a string. May be a full .eml file,
             a pasted email including headers, or just a body.

    Returns:
        dict with keys 'sender', 'subject', 'body', 'urls'. All values
        are strings; missing fields are returned as empty strings rather
        than None so downstream code can treat them uniformly.
    """
    if not raw or not raw.strip():
        return {"sender": "", "subject": "", "body": "", "urls": ""}

    # Try parsing as a proper RFC-822 email first. The modern policy
    # handles MIME multipart, header decoding, and charset conversion.
    try:
        msg: EmailMessage = email.message_from_string(raw, policy=policy.default)

        # If parsing yielded recognisable headers, treat it as structured email
        if msg.get("From") or msg.get("Subject"):
            return _extract_from_message(msg)
    except Exception:
        # Fall through to the plain-text fallback below
        pass

    # Fallback: no recognisable headers → treat entire input as body text
    body = _strip_html(raw)
    urls = _extract_urls(raw)
    return {
        "sender": "",
        "subject": "",
        "body": body,
        "urls": " ".join(urls),
    }


def _extract_from_message(msg: EmailMessage) -> dict[str, Any]:
    """Extract the four fields from a parsed EmailMessage object."""
    sender = str(msg.get("From", "")).strip()
    subject = str(msg.get("Subject", "")).strip()

    # Walk the MIME tree and collect body parts. Prefer text/plain,
    # fall back to text/html (stripped) if no plain text exists.
    plain_parts: list[str] = []
    html_parts: list[str] = []

    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            if ctype == "text/plain":
                plain_parts.append(_get_part_content(part))
            elif ctype == "text/html":
                html_parts.append(_get_part_content(part))
    else:
        ctype = msg.get_content_type()
        content = _get_part_content(msg)
        if ctype == "text/html":
            html_parts.append(content)
        else:
            plain_parts.append(content)

    if plain_parts:
        body = "\n".join(plain_parts)
    elif html_parts:
        body = _strip_html("\n".join(html_parts))
    else:
        body = ""

    urls = _extract_urls(body) + _extract_urls(" ".join(html_parts))
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique_urls: list[str] = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            unique_urls.append(u)

    return {
        "sender": sender,
        "subject": subject,
        "body": body.strip(),
        "urls": " ".join(unique_urls),
    }


def _get_part_content(part: EmailMessage) -> str:
    """Safely get a message part's string content, handling encoding errors."""
    try:
        content = part.get_content()
        if isinstance(content, bytes):
            return content.decode("utf-8", errors="replace")
        return str(content)
    except (LookupError, UnicodeDecodeError, AttributeError):
        # Fallback for parts with undeclared or unknown charsets
        try:
            payload = part.get_payload(decode=True)
            if isinstance(payload, bytes):
                return payload.decode("utf-8", errors="replace")
            return str(payload or "")
        except Exception:
            return ""


def _strip_html(text: str) -> str:
    """Remove HTML tags and decode HTML entities, collapsing whitespace."""
    text = HTML_TAG_REGEX.sub(" ", text)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _extract_urls(text: str) -> list[str]:
    """Find all http(s) URLs in a string."""
    if not text:
        return []
    return URL_REGEX.findall(text)
