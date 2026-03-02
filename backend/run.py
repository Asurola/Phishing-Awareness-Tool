"""
run.py — Application entry point.

Imports the Flask app factory and starts the development server.
Run with: python run.py
"""

import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables from .env file
load_dotenv()

# Determine environment (default to development)
env = os.getenv("FLASK_ENV", "development")

# Create the Flask app using the factory
app = create_app(env)

if __name__ == "__main__":
    print(f"Starting Phishing Awareness Tool backend — environment: {env}")
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=(env == "development"),
    )
