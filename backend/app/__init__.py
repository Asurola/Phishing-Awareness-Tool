"""
app/__init__.py — Flask application factory.

Creates and configures the Flask app instance using the factory pattern.
This allows multiple app instances to be created for different environments
(development, testing, production) and makes testing easier.

Usage:
    from app import create_app
    app = create_app('development')
"""

from flask import Flask
from .config import config_map
from .extensions import db, cors


def create_app(env: str = "development") -> Flask:
    """
    Application factory function.

    Creates and returns a configured Flask application instance.

    Args:
        env: The environment name to load configuration for.
             One of 'development', 'testing', 'production'.
             Defaults to 'development'.

    Returns:
        Flask: A fully configured Flask application instance.
    """
    app = Flask(__name__)

    # Load configuration from the appropriate config class
    config_class = config_map.get(env, config_map["development"])
    app.config.from_object(config_class)

    # Initialise Flask extensions
    db.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config.get("CORS_ORIGINS", "*")}})

    # Register API blueprints
    from .api.health import health_bp
    from .api.detection import detection_bp
    from .api.education import education_bp

    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(detection_bp, url_prefix="/api")
    app.register_blueprint(education_bp, url_prefix="/api")

    # Load ML model into memory at startup
    from .services.ml_classifier import load_model
    load_model()

    with app.app_context():
        db.create_all()

    return app
