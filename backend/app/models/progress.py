"""
app/models/progress.py — Educational progress and scenario database models.

Contains two models:
  - Scenario:      A seeded phishing or legitimate email scenario used in the
                   educational simulation module.
  - UserProgress:  Records each attempt by a user (identified by session_id)
                   on a specific scenario, including their answer and whether
                   it was correct.
"""

from datetime import datetime
from typing import Optional
from ..extensions import db


class Scenario(db.Model):
    """
    SQLAlchemy model representing a training scenario.

    Scenarios are seeded via seed_scenarios.py and presented to users
    in the educational simulation module.

    Attributes:
        id:             Primary key, auto-incremented.
        title:          Short descriptive title (e.g. "Fake Bank Alert").
        difficulty:     Difficulty level: 'beginner', 'intermediate', or 'advanced'.
        category:       Scenario type: 'credential_harvesting', 'spear_phishing',
                        'whaling', 'clone_phishing', or 'legitimate'.
        email_content:  Full simulated email text (including headers where applicable).
        is_phishing:    Ground truth label — True if phishing, False if legitimate.
        indicators:     JSON string listing the phishing indicators present (empty if legitimate).
        explanation:    Detailed explanation of why this is phishing or legitimate.
        learning_points: JSON string containing key takeaways for the user.
        created_at:     UTC timestamp when the scenario was seeded.
    """

    __tablename__ = "scenarios"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title: str = db.Column(db.String(128), nullable=False)
    difficulty: str = db.Column(db.String(16), nullable=False)   # beginner|intermediate|advanced
    category: str = db.Column(db.String(32), nullable=False)
    email_content: str = db.Column(db.Text, nullable=False)
    is_phishing: bool = db.Column(db.Boolean, nullable=False)
    indicators: Optional[str] = db.Column(db.Text, nullable=True)      # JSON string
    explanation: str = db.Column(db.Text, nullable=False)
    learning_points: str = db.Column(db.Text, nullable=False)           # JSON string
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationship to user attempts
    attempts = db.relationship("UserProgress", backref="scenario", lazy=True)

    def to_dict(self, include_answer: bool = False) -> dict:
        """
        Serialise the model to a dictionary.

        Args:
            include_answer: If False (default), omits is_phishing, indicators,
                            and explanation so the answer is not revealed
                            before the user submits their guess.

        Returns:
            dict: Serialised scenario data.
        """
        data = {
            "id": self.id,
            "title": self.title,
            "difficulty": self.difficulty,
            "category": self.category,
            "email_content": self.email_content,
        }
        if include_answer:
            data.update({
                "is_phishing": self.is_phishing,
                "indicators": self.indicators,
                "explanation": self.explanation,
                "learning_points": self.learning_points,
            })
        return data

    def __repr__(self) -> str:
        return f"<Scenario id={self.id} title='{self.title}' difficulty='{self.difficulty}'>"


class UserProgress(db.Model):
    """
    SQLAlchemy model recording a user's attempt on a scenario.

    Uses anonymous session IDs (stored in browser localStorage) so no
    user authentication is required.

    Attributes:
        id:                  Primary key, auto-incremented.
        session_id:          Anonymous session identifier from the frontend.
        scenario_id:         Foreign key referencing scenarios.id.
        user_answer:         The user's submitted answer: 'phishing' or 'legitimate'.
        is_correct:          Whether the user's answer matched the ground truth.
        time_taken_seconds:  How long the user spent on this scenario (seconds).
        completed_at:        UTC timestamp of submission.
    """

    __tablename__ = "user_progress"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    session_id: str = db.Column(db.String(64), nullable=False, index=True)
    scenario_id: int = db.Column(
        db.Integer, db.ForeignKey("scenarios.id"), nullable=False
    )
    user_answer: str = db.Column(db.String(16), nullable=False)   # 'phishing' | 'legitimate'
    is_correct: bool = db.Column(db.Boolean, nullable=False)
    time_taken_seconds: Optional[int] = db.Column(db.Integer, nullable=True)
    completed_at: datetime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self) -> dict:
        """
        Serialise the model instance to a dictionary for JSON API responses.

        Returns:
            dict: Serialised user progress record.
        """
        return {
            "id": self.id,
            "session_id": self.session_id,
            "scenario_id": self.scenario_id,
            "user_answer": self.user_answer,
            "is_correct": self.is_correct,
            "time_taken_seconds": self.time_taken_seconds,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }

    def __repr__(self) -> str:
        return (
            f"<UserProgress id={self.id} session='{self.session_id}' "
            f"scenario={self.scenario_id} correct={self.is_correct}>"
        )
