"""
app/config.py - Application configuration classes.

Defines configuration for different environments (development, testing, production)
using a base class with environment-specific subclasses.

Usage:
    from app.config import config_map
    app.config.from_object(config_map['development'])
"""

import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    """
    Base configuration with settings common to all environments.

    All environment-specific configs inherit from this class and can
    override individual settings as needed.
    """

    # Flask secret key - must be set via environment variable in production
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

    # SQLAlchemy settings
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    # Path to the saved ML model file
    MODEL_PATH: str = os.getenv("MODEL_PATH", "app/ml/models/phishing_classifier.pkl")

    # Allowed CORS origins (comma-separated list)
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "http://localhost:5173")

    # Maximum upload file size (16 MB)
    MAX_CONTENT_LENGTH: int = 16 * 1024 * 1024


class DevelopmentConfig(BaseConfig):
    """
    Development configuration.

    Uses SQLite for simplicity and enables debug mode.
    """

    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "DATABASE_URI", "sqlite:///phishing_tool_dev.db"
    )


class TestingConfig(BaseConfig):
    """
    Testing configuration.

    Uses an in-memory SQLite database so tests are fast and isolated.
    """

    TESTING: bool = True
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"

    # Disable CSRF protection in tests
    WTF_CSRF_ENABLED: bool = False


class ProductionConfig(BaseConfig):
    """
    Production configuration.

    Reads database URI from the DATABASE_URI environment variable.
    Debug mode is disabled. Raises an error if required env vars are missing.
    """

    DEBUG: bool = False
    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URI", "")

    def __init__(self) -> None:
        if not self.SQLALCHEMY_DATABASE_URI:
            raise ValueError(
                "DATABASE_URI environment variable must be set for production."
            )


# Mapping of environment name → configuration class
# Used by the application factory in app/__init__.py
config_map: dict = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
