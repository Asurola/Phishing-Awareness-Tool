"""
tests/test_feature_extractor.py — Unit tests for the feature extractor service.

Tests that extract_features() returns a dict with all expected feature keys
and that feature values are within the correct type/range constraints.

TODO (Phase 6): Implement once feature_extractor.py is implemented.
"""

import pytest

EXPECTED_FEATURE_COUNT = 31  # 13 URL + 7 Header + 11 Content


class TestGetFeatureNames:
    """Tests for get_feature_names() — available even in Phase 1."""

    def test_returns_31_features(self):
        """Feature names list should have exactly 31 entries."""
        from app.services.feature_extractor import get_feature_names
        names = get_feature_names()
        assert len(names) == EXPECTED_FEATURE_COUNT

    def test_all_names_are_strings(self):
        """All feature names should be non-empty strings."""
        from app.services.feature_extractor import get_feature_names
        names = get_feature_names()
        assert all(isinstance(n, str) and len(n) > 0 for n in names)

    def test_no_duplicate_names(self):
        """Feature name list should contain no duplicates."""
        from app.services.feature_extractor import get_feature_names
        names = get_feature_names()
        assert len(names) == len(set(names))


class TestExtractFeatures:
    """Tests for extract_features() — to be implemented in Phase 6."""

    def test_raises_not_implemented(self):
        """Function raises NotImplementedError until Phase 2."""
        with pytest.raises(NotImplementedError):
            from app.services.feature_extractor import extract_features
            extract_features({})

    # TODO (Phase 6): Add tests after Phase 2 implementation
    # def test_returns_all_feature_keys(self): ...
    # def test_boolean_features_are_bool_type(self): ...
    # def test_integer_features_are_non_negative(self): ...
