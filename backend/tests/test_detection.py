"""
tests/test_detection.py - Integration tests for the detection API endpoint.

Tests the POST /api/analyse endpoint with various email inputs,
verifying the HTTP response structure and field types.
"""

import pytest
from app import create_app


@pytest.fixture
def client():
    """Create a test client using the testing configuration."""
    app = create_app("testing")
    with app.test_client() as client:
        with app.app_context():
            from app.extensions import db
            db.create_all()
            yield client


def test_health_endpoint(client):
    """Health endpoint should return status 'ok'."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"


def test_analyse_returns_400_with_no_body(client):
    """Analyse endpoint should return 400 when no email is provided."""
    response = client.post("/api/analyse", json={})
    assert response.status_code == 400


def test_analyse_accepts_raw_email(client):
    """Analyse endpoint should accept a raw_email string and return 200."""
    response = client.post(
        "/api/analyse",
        json={"raw_email": "From: test@example.com\n\nThis is a test email."},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "risk_score" in data
    assert "verdict" in data
    assert "flags" in data

