"""
app/api/education.py - Educational platform API endpoints.

Handles all endpoints related to the training/simulation module:
  - Listing scenarios filtered by difficulty
  - Fetching a single scenario (without revealing the answer)
  - Submitting a user's answer and receiving feedback
  - Retrieving a user's progress statistics

Endpoints:
    GET  /api/scenarios                      List scenarios (filterable by difficulty)
    GET  /api/scenarios/<id>                 Get one scenario (answer withheld)
    POST /api/scenarios/<id>/answer          Submit answer, receive result + explanation
    GET  /api/progress/<session_id>          Get user's learning progress
"""

import json
from flask import Blueprint, request, jsonify
from ..models.progress import Scenario, UserProgress
from ..extensions import db

education_bp = Blueprint("education", __name__)


@education_bp.route("/scenarios", methods=["GET"])
def list_scenarios():
    """
    List available training scenarios, optionally filtered by difficulty.

    Query Parameters:
        difficulty (str): Filter by 'beginner', 'intermediate', or 'advanced'.
        limit (int):      Maximum number of results to return (default: 10).

    Returns:
        JSON: List of scenario summaries (id, title, difficulty).
    """
    try:
        difficulty = request.args.get("difficulty")
        limit = int(request.args.get("limit", 10))

        query = Scenario.query
        if difficulty:
            query = query.filter_by(difficulty=difficulty)

        scenarios = query.limit(limit).all()
        return jsonify([s.to_dict(include_answer=False) for s in scenarios]), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@education_bp.route("/scenarios/<int:scenario_id>", methods=["GET"])
def get_scenario(scenario_id: int):
    """
    Retrieve a single scenario by ID (answer withheld).

    Args:
        scenario_id: The primary key of the scenario.

    Returns:
        JSON: Scenario data without is_phishing, indicators, or explanation.

    Raises:
        404: If the scenario does not exist.
    """
    try:
        scenario = Scenario.query.get_or_404(scenario_id)
        return jsonify(scenario.to_dict(include_answer=False)), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@education_bp.route("/scenarios/<int:scenario_id>/answer", methods=["POST"])
def submit_answer(scenario_id: int):
    """
    Submit a user's answer to a scenario and receive feedback.

    Args:
        scenario_id: The primary key of the scenario.

    Request Body (JSON):
        session_id (str):          Anonymous session identifier.
        answer (str):              'phishing' or 'legitimate'.
        time_taken_seconds (int):  How long the user spent (optional).

    Returns:
        JSON: {
            "correct": bool,
            "is_phishing": bool,
            "explanation": str,
            "indicators": list,
            "learning_points": list
        }

    Raises:
        400: If request body is invalid.
        404: If scenario does not exist.
    """
    try:
        scenario = Scenario.query.get_or_404(scenario_id)
        data = request.get_json()

        session_id: str = data.get("session_id", "")
        user_answer: str = data.get("answer", "").lower()
        time_taken: int | None = data.get("time_taken_seconds")

        if user_answer not in ("phishing", "legitimate"):
            return jsonify({"error": "answer must be 'phishing' or 'legitimate'"}), 400

        correct_label = "phishing" if scenario.is_phishing else "legitimate"
        is_correct = user_answer == correct_label

        # Persist the attempt
        progress_record = UserProgress(
            session_id=session_id,
            scenario_id=scenario_id,
            user_answer=user_answer,
            is_correct=is_correct,
            time_taken_seconds=time_taken,
        )
        db.session.add(progress_record)
        db.session.commit()

        return jsonify({
            "correct": is_correct,
            "is_phishing": scenario.is_phishing,
            "explanation": scenario.explanation,
            "indicators": json.loads(scenario.indicators) if scenario.indicators else [],
            "learning_points": json.loads(scenario.learning_points) if scenario.learning_points else [],
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@education_bp.route("/progress/<string:session_id>", methods=["GET"])
def get_progress(session_id: str):
    """
    Retrieve a user's learning progress for a given session.

    Args:
        session_id: The anonymous session identifier.

    Returns:
        JSON: {
            "total_attempted": int,
            "total_correct": int,
            "accuracy": float,
            "by_difficulty": { "beginner": {...}, "intermediate": {...}, "advanced": {...} },
            "weak_areas": list[str]
        }
    """
    try:
        attempts = (
            UserProgress.query
            .filter_by(session_id=session_id)
            .all()
        )

        total_attempted = len(attempts)
        total_correct = sum(1 for a in attempts if a.is_correct)
        accuracy = (total_correct / total_attempted) if total_attempted > 0 else 0.0

        # Break down accuracy by difficulty
        by_difficulty: dict = {}
        for diff in ("Beginner", "Intermediate", "Advanced"):
            diff_attempts = [
                a for a in attempts if a.scenario and a.scenario.difficulty == diff
            ]
            diff_correct = sum(1 for a in diff_attempts if a.is_correct)
            by_difficulty[diff] = {
                "attempted": len(diff_attempts),
                "correct": diff_correct,
                "accuracy": (diff_correct / len(diff_attempts)) if diff_attempts else 0.0,
            }

        # TODO (Phase 4): Implement weak_areas computation based on missed indicators
        weak_areas: list = []

        return jsonify({
            "total_attempted": total_attempted,
            "total_correct": total_correct,
            "accuracy": round(accuracy, 3),
            "by_difficulty": by_difficulty,
            "weak_areas": weak_areas,
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
