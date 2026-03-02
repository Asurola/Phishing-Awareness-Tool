"""
app/extensions.py — Flask extension instances.

Centralises extension initialisation so that they can be imported anywhere
in the application without circular import issues.

Extensions are created here without an app instance (using the "deferred init"
pattern) and are bound to the app via `extension.init_app(app)` in the
application factory (app/__init__.py).
"""

from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Database ORM — used by all model files in app/models/
db: SQLAlchemy = SQLAlchemy()

# Cross-Origin Resource Sharing — allows the React frontend to call the API
cors: CORS = CORS()
