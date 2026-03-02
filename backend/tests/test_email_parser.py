"""
tests/test_email_parser.py — Unit tests for the email parser service.

Tests parse_raw_email() and URL extraction functions with various
email formats including plain text, MIME multipart, and malformed inputs.

TODO (Phase 6): Implement once email_parser.py is implemented.
"""

import pytest

# TODO (Phase 6): Uncomment imports when parser is implemented
# from app.services.email_parser import (
#     parse_raw_email,
#     extract_urls_from_text,
#     extract_urls_from_html,
# )

SAMPLE_PLAIN_EMAIL = """From: attacker@evil.com
To: victim@example.com
Subject: Urgent: Verify your account

Dear Customer,

Click here to verify: http://evil.com/login

Regards,
Support Team
"""

SAMPLE_MIME_EMAIL = """MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="boundary"
From: spoof@paypal.com
To: user@example.com
Subject: Account suspended

--boundary
Content-Type: text/plain

Your account has been suspended. Visit http://paypa1.com/verify
--boundary--
"""


class TestParseRawEmail:
    """Tests for parse_raw_email() function."""

    def test_raises_not_implemented(self):
        """Parser raises NotImplementedError until Phase 2."""
        with pytest.raises(NotImplementedError):
            from app.services.email_parser import parse_raw_email
            parse_raw_email(SAMPLE_PLAIN_EMAIL)

    # TODO (Phase 6): Add these tests after Phase 2 implementation
    # def test_parses_from_address(self): ...
    # def test_parses_subject(self): ...
    # def test_extracts_urls_from_plaintext_body(self): ...
    # def test_extracts_urls_from_html_body(self): ...
    # def test_handles_empty_input(self): ...
    # def test_parses_multipart_mime(self): ...


class TestExtractUrlsFromText:
    """Tests for extract_urls_from_text() function."""

    def test_raises_not_implemented(self):
        """Function raises NotImplementedError until Phase 2."""
        with pytest.raises(NotImplementedError):
            from app.services.email_parser import extract_urls_from_text
            extract_urls_from_text("Visit http://example.com")

    # TODO (Phase 6): Add tests after Phase 2 implementation
