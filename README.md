# PhishGuard — Phishing Detection and Awareness Tool

PhishGuard is a web-based platform that combines machine-learning email analysis with interactive training scenarios to help users identify and defend against phishing attacks.

The tool serves two purposes:

1. **Detection** — Users paste raw email content (or upload `.eml` files) and receive an instant risk assessment with human-readable explanations of every threat indicator found.
2. **Education** — Users work through curated phishing and legitimate email scenarios at varying difficulty levels, building practical detection skills with immediate feedback.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 19, Vite, Tailwind CSS v4, React Router v7 |
| Backend | Flask, Flask-SQLAlchemy, Flask-CORS |
| ML Pipeline | scikit-learn (Random Forest), XGBoost, NLTK, TF-IDF vectorisation |
| Database | SQLite (development), PostgreSQL-ready (production) |
| Model Serving | joblib serialisation, loaded at startup |

## Architecture

```
┌──────────────┐       /api/analyse        ┌──────────────────┐
│   React SPA  │  ◄──────────────────────►  │   Flask Backend  │
│  (Vite dev)  │       /api/scenarios       │                  │
│  port 5173   │       /api/progress        │    port 5000     │
└──────────────┘                            └────────┬─────────┘
                                                     │
                                          ┌──────────┴─────────┐
                                          │                    │
                                    ┌─────▼─────┐     ┌───────▼───────┐
                                    │  SQLite   │     │  ML Pipeline  │
                                    │ (scenarios │     │ (322 features,│
                                    │  progress) │     │  Random Forest│
                                    └───────────┘     │  classifier)  │
                                                      └───────────────┘
```

The ML pipeline extracts 22 engineered features (header, body, and URL analysis) plus 300 TF-IDF features from the email subject and body, feeding a 322-feature vector into a trained Random Forest classifier.

## Prerequisites

- Python 3.10+
- Node.js 18+
- npm 9+

## Setup

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

pip install -r requirements.txt
```

Copy the environment file and adjust values as needed:

```bash
cp .env.example .env
```

The ML model files (`.pkl`) must be placed in `backend/app/ml/models/`. Four files are required:

- `phishing_model.pkl` — trained Random Forest classifier
- `tfidf_subject.pkl` — subject line TF-IDF vectoriser
- `tfidf_body.pkl` — body text TF-IDF vectoriser
- `feature_names.pkl` — ordered feature column names

These are produced by the training notebook and are not included in version control due to file size.

### Frontend

```bash
cd frontend
npm install
```

## Running the Application

Start the backend:

```bash
cd backend
python run.py
```

In a separate terminal, start the frontend:

```bash
cd frontend
npm run dev
```

The frontend runs at `http://localhost:5173` and proxies API requests to the Flask backend on port 5000.

### Seeding the Database

The education module requires training scenarios to be seeded into the database:

```bash
cd backend
python seed_scenarios.py
```

This populates the database with phishing and legitimate email scenarios across beginner, intermediate, and advanced difficulty levels. Run with `--force` to clear and re-seed.

## Project Structure

```
Phishing-awareness-tool/
├── backend/
│   ├── app/
│   │   ├── api/               # REST endpoints (health, detection, education)
│   │   ├── models/            # SQLAlchemy models (Scenario, UserProgress)
│   │   ├── services/          # Business logic
│   │   │   ├── email_parser.py        # RFC-822 / .eml parsing
│   │   │   ├── feature_extractor.py   # 22 engineered features
│   │   │   ├── ml_classifier.py       # Model loading and inference
│   │   │   └── explanation.py         # Human-readable flag generation
│   │   ├── ml/models/         # Trained .pkl artefacts (git-ignored)
│   │   ├── config.py          # Environment-specific configuration
│   │   └── extensions.py      # Flask extension instances
│   ├── tests/                 # Integration tests
│   ├── seed_scenarios.py      # Database seeder for training scenarios
│   ├── run.py                 # Application entry point
│   ├── requirements.txt
│   └── .env.example
│
└── frontend/
    ├── src/
    │   ├── pages/             # Route-level components
    │   │   ├── HomePage.jsx
    │   │   ├── DetectionPage.jsx
    │   │   ├── EducationPage.jsx
    │   │   ├── SimulationPage.jsx
    │   │   └── ResultsPage.jsx
    │   ├── components/        # Reusable UI components
    │   │   ├── detection/     # Analysis result display components
    │   │   └── layout/        # Navbar, Footer, Layout wrapper
    │   ├── api/client.js      # HTTP client for backend communication
    │   ├── hooks/             # Custom React hooks
    │   └── utils/             # Constants and helpers
    ├── index.html
    ├── vite.config.js
    └── package.json
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check with model and scenario status |
| `POST` | `/api/analyse` | Submit email for phishing analysis |
| `GET` | `/api/scenarios` | List training scenarios (filterable by difficulty) |
| `GET` | `/api/scenarios/:id` | Get a single scenario (answer withheld) |
| `POST` | `/api/scenarios/:id/answer` | Submit answer and receive feedback |
| `GET` | `/api/progress/:session_id` | Retrieve session learning progress |
