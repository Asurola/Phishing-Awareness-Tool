"""Flask extension instances (deferred init pattern)."""

from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Database ORM - used by all model files in app/models/
db: SQLAlchemy = SQLAlchemy()

# Cross-Origin Resource Sharing - allows the React frontend to call the API
cors: CORS = CORS()
