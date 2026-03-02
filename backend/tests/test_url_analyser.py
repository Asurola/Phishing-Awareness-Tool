"""
tests/test_url_analyser.py — Unit tests for the URL analyser service.

Tests extract_url_features() and analyse_urls() with known URL examples
that should produce predictable feature values.

TODO (Phase 6): Implement once url_analyser.py is implemented.
"""

import pytest

# Sample URLs for testing (known expected outcomes)
SHORTENER_URL = "http://bit.ly/abc123"
IP_URL = "http://192.168.1.1/phish"
SUSPICIOUS_TLD_URL = "http://login.paypal.tk/verify"
HYPHEN_DOMAIN_URL = "http://paypal-secure-login.com/account"
HTTPS_URL = "https://legitimate-bank.com/login"
LONG_URL = "http://" + "a" * 200 + ".com/path"


class TestExtractUrlFeatures:
    """Unit tests for extract_url_features() — to be implemented in Phase 6."""

    def test_raises_not_implemented(self):
        """Function raises NotImplementedError until Phase 2."""
        with pytest.raises(NotImplementedError):
            from app.services.url_analyser import extract_url_features
            extract_url_features("http://example.com")

    # TODO (Phase 6): Implement after Phase 2:
    # def test_detects_ip_address(self): ...
    # def test_detects_shortener(self): ...
    # def test_detects_suspicious_tld(self): ...
    # def test_detects_prefix_suffix_domain(self): ...
    # def test_https_detection(self): ...
    # def test_url_length_calculation(self): ...
    # def test_counts_subdomains(self): ...


class TestAnalyseUrls:
    """Tests for analyse_urls() worst-case aggregation."""

    def test_raises_not_implemented(self):
        """Function raises NotImplementedError until Phase 2."""
        with pytest.raises(NotImplementedError):
            from app.services.url_analyser import analyse_urls
            analyse_urls([])

    # TODO (Phase 6): Add tests after Phase 2 implementation
