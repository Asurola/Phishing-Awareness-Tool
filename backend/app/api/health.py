"""
app/api/health.py - Health check endpoint.

Provides a simple `GET /api/health` endpoint that returns the operational
status of the backend service including whether the ML model is loaded
and how many training scenarios are available in the database.

Endpoint:
    GET /api/health
    Response: { "status": "ok", "model_loaded": bool, "scenarios_count": int }
"""

from flask import Blueprint, jsonify
from ..models.progress import Scenario

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health_check():
    """
    Health check endpoint.

    Returns the operational status of the backend service.

    Returns:
        JSON: {
            "status": "ok",
            "model_loaded": bool - True if the ML classifier is loaded,
            "scenarios_count": int - Number of seeded scenarios in the database
        }
    """
    try:
        # Check how many scenarios are in the database
        scenarios_count = Scenario.query.count()

        from ..services.ml_classifier import is_model_loaded
        model_loaded = is_model_loaded()

        return jsonify({
            "status": "ok",
            "model_loaded": model_loaded,
            "scenarios_count": scenarios_count,
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
        }), 500
