"""
app/models/analysis.py — AnalysisResult database model.

Stores the results of phishing analysis requests so that users can
review their history and so that aggregate statistics can be computed.

Each row represents one analysis of one email submission, including
the extracted feature vector and the final classification result.
"""

from datetime import datetime
from typing import Optional
from ..extensions import db


class AnalysisResult(db.Model):
    """
    SQLAlchemy model representing a single phishing analysis result.

    Attributes:
        id:              Primary key, auto-incremented.
        session_id:      Anonymous session identifier (stored in browser localStorage).
        raw_email_hash:  SHA-256 hash of the submitted email (for deduplication, not the raw text).
        risk_score:      Integer risk score 0–100 produced by the explanation engine.
        verdict:         Human-readable verdict string (e.g. "High Risk — Likely Phishing").
        prediction:      Raw ML prediction: 'phishing' or 'legitimate'.
        confidence:      ML model confidence score (0.0–1.0).
        feature_vector:  JSON-serialised dict of extracted features.
        flags_json:      JSON-serialised list of threat flag dicts from the explanation engine.
        analysed_at:     UTC timestamp of the analysis.
    """

    __tablename__ = "analysis_results"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    session_id: str = db.Column(db.String(64), nullable=True, index=True)
    raw_email_hash: str = db.Column(db.String(64), nullable=True)
    risk_score: int = db.Column(db.Integer, nullable=True)
    verdict: str = db.Column(db.String(128), nullable=True)
    prediction: str = db.Column(db.String(16), nullable=True)  # 'phishing' | 'legitimate'
    confidence: float = db.Column(db.Float, nullable=True)
    feature_vector: Optional[str] = db.Column(db.Text, nullable=True)  # JSON string
    flags_json: Optional[str] = db.Column(db.Text, nullable=True)       # JSON string
    analysed_at: datetime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self) -> dict:
        """
        Serialise the model instance to a dictionary for JSON API responses.

        Returns:
            dict: Serialised representation of this analysis result.
        """
        return {
            "id": self.id,
            "session_id": self.session_id,
            "risk_score": self.risk_score,
            "verdict": self.verdict,
            "prediction": self.prediction,
            "confidence": self.confidence,
            "analysed_at": self.analysed_at.isoformat() if self.analysed_at else None,
        }

    def __repr__(self) -> str:
        return f"<AnalysisResult id={self.id} prediction='{self.prediction}' score={self.risk_score}>"
