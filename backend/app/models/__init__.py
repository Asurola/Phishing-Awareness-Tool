"""
app/models/__init__.py — Models package initialiser.

Imports all model classes so they are registered with SQLAlchemy
when `db.create_all()` is called in the app factory.
"""

from .analysis import AnalysisResult  # noqa: F401
from .progress import UserProgress, Scenario  # noqa: F401
