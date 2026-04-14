# Master Prompt - Phishing Detection & Awareness Tool (FYP)

> **Paste this into your agentic IDE (Cursor, Windsurf, Bolt, etc.) as the project-level system prompt or initial generation prompt.**

---

## 🎯 Project Overview

Build a **Phishing Detection and Awareness Tool** - a dual-function web application with two core components:

1. **Detection Engine**: Analyses user-submitted email content (pasted or uploaded) for phishing indicators using feature extraction and machine learning classification. Outputs a risk score, threat explanations, and actionable recommendations.
2. **Educational Platform**: Interactive simulation-based training that presents users with phishing scenarios of increasing difficulty, provides immediate feedback, and tracks learning progress.

This is an **academic Final Year Project (FYP)**, not a commercial product. Prioritise clean architecture, well-documented code, and demonstrable functionality over production polish.

---

## 🏗️ Technology Stack (Finalised)

```
Frontend:      React 18+ with Tailwind CSS
Backend:       Python Flask (with Flask-CORS, Flask-RESTful)
ML Framework:  scikit-learn (Random Forest primary classifier)
NLP:           NLTK or spaCy for text processing
Database:      SQLite (development) → PostgreSQL (production)
Email Parsing: Python `email` stdlib + `mailparser`
URL Analysis:  tldextract, urllib.parse, re
HTTP Client:   requests (for URL resolution/redirect chain checks)
Build Tools:   Vite (frontend), pip (backend)
```

---

## 📁 Project Structure

Generate the following monorepo structure:

```
phishing-awareness-tool/
├── README.md
├── .gitignore
├── .env.example
│
├── backend/
│   ├── app/
│   │   ├── __init__.py              # Flask app factory
│   │   ├── config.py                # Configuration (dev/prod/test)
│   │   ├── extensions.py            # DB, CORS, etc. initialisation
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py              # User model (optional auth)
│   │   │   ├── analysis.py          # Analysis result/history model
│   │   │   └── progress.py          # Educational progress model
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── detection.py         # POST /api/analyse - main detection endpoint
│   │   │   ├── education.py         # GET/POST /api/scenarios, /api/progress
│   │   │   └── health.py            # GET /api/health
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── email_parser.py      # Parse raw email → structured data
│   │   │   ├── feature_extractor.py # Extract features from parsed email
│   │   │   ├── url_analyser.py      # URL-specific feature extraction
│   │   │   ├── header_analyser.py   # Email header analysis (SPF/DKIM checks)
│   │   │   ├── content_analyser.py  # Body text NLP analysis
│   │   │   ├── ml_classifier.py     # Load model & predict
│   │   │   └── explanation.py       # Generate human-readable explanations
│   │   ├── ml/
│   │   │   ├── train_model.py       # Training script
│   │   │   ├── evaluate_model.py    # Evaluation metrics script
│   │   │   ├── models/              # Saved .pkl model files
│   │   │   └── data/                # Training datasets (gitignored)
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── validators.py        # Input validation helpers
│   ├── tests/
│   │   ├── test_detection.py
│   │   ├── test_email_parser.py
│   │   ├── test_feature_extractor.py
│   │   └── test_url_analyser.py
│   ├── requirements.txt
│   ├── run.py                       # Entry point: python run.py
│   └── seed_scenarios.py            # Seed DB with phishing scenarios
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx                  # Router setup
│   │   ├── api/
│   │   │   └── client.js            # Axios/fetch wrapper for backend API
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   ├── Navbar.jsx
│   │   │   │   ├── Footer.jsx
│   │   │   │   └── Layout.jsx
│   │   │   ├── detection/
│   │   │   │   ├── EmailInputForm.jsx    # Paste or upload email content
│   │   │   │   ├── AnalysisResults.jsx   # Risk score + breakdown display
│   │   │   │   ├── ThreatIndicator.jsx   # Individual threat flag component
│   │   │   │   ├── RiskScoreGauge.jsx    # Visual risk meter
│   │   │   │   └── Recommendations.jsx   # Actionable advice panel
│   │   │   ├── education/
│   │   │   │   ├── ScenarioCard.jsx      # Single phishing scenario
│   │   │   │   ├── SimulationView.jsx    # Interactive "is this phishing?" exercise
│   │   │   │   ├── FeedbackPanel.jsx     # Explains why correct/incorrect
│   │   │   │   ├── ProgressTracker.jsx   # User's learning progress
│   │   │   │   └── DifficultySelector.jsx
│   │   │   └── common/
│   │   │       ├── Button.jsx
│   │   │       ├── Card.jsx
│   │   │       └── LoadingSpinner.jsx
│   │   ├── pages/
│   │   │   ├── HomePage.jsx              # Landing page with tool overview
│   │   │   ├── DetectionPage.jsx         # Email analysis interface
│   │   │   ├── EducationPage.jsx         # Training module hub
│   │   │   ├── SimulationPage.jsx        # Active simulation exercise
│   │   │   └── ResultsPage.jsx           # Detailed analysis results
│   │   ├── hooks/
│   │   │   └── useAnalysis.js            # Custom hook for detection API calls
│   │   └── utils/
│   │       └── constants.js
│   ├── index.html
│   ├── tailwind.config.js
│   ├── vite.config.js
│   └── package.json
│
└── docs/
    ├── API.md                            # API endpoint documentation
    └── FEATURES.md                       # Feature checklist
```

---

## 🔍 Detection Engine - Detailed Specification

### Email Input Methods
Users submit email content via:
1. **Paste raw email** (including headers) into a text area
2. **Upload .eml file** which is parsed server-side

### Feature Extraction Pipeline

The `feature_extractor.py` service should extract and return a feature dictionary from a parsed email. Features fall into three categories:

#### A. URL Features (from `url_analyser.py`)
For each URL found in the email body:
| Feature | Type | Description |
|---------|------|-------------|
| `url_length` | int | Total character length of URL |
| `has_ip_address` | bool | URL contains raw IP instead of domain |
| `has_https` | bool | Uses HTTPS scheme |
| `num_dots` | int | Number of dots in the URL |
| `num_hyphens` | int | Number of hyphens in the domain |
| `num_subdomains` | int | Number of subdomains |
| `has_at_symbol` | bool | Contains `@` symbol |
| `has_redirect` | bool | Contains `//` redirect pattern |
| `uses_shortener` | bool | Domain matches known shorteners (bit.ly, tinyurl, etc.) |
| `path_length` | int | Length of URL path |
| `has_suspicious_tld` | bool | TLD in suspicious list (.tk, .ml, .ga, .cf, .gq, .xyz, .top, .buzz) |
| `domain_age_days` | int or null | Days since domain registration (if checkable) |
| `has_prefix_suffix` | bool | Domain contains hyphen (e.g., `paypal-secure.com`) |

#### B. Header Features (from `header_analyser.py`)
| Feature | Type | Description |
|---------|------|-------------|
| `sender_domain_matches_from` | bool | Envelope sender matches `From` header domain |
| `has_spf_pass` | bool | SPF authentication result is pass |
| `has_dkim_pass` | bool | DKIM authentication result is pass |
| `has_reply_to_mismatch` | bool | Reply-To differs from From address |
| `received_hop_count` | int | Number of `Received` headers |
| `has_x_mailer` | bool | Presence of X-Mailer header |
| `from_domain_is_freemail` | bool | Sender uses gmail.com, yahoo.com, outlook.com, etc. |

#### C. Content Features (from `content_analyser.py`)
| Feature | Type | Description |
|---------|------|-------------|
| `urgency_word_count` | int | Count of urgency words ("immediately", "urgent", "expires", "suspend", "verify now", "act now", "limited time") |
| `threat_word_count` | int | Count of threat words ("locked", "compromised", "unauthorized", "suspended") |
| `reward_word_count` | int | Count of reward/lure words ("winner", "congratulations", "prize", "free", "gift") |
| `has_credential_request` | bool | Asks for password, SSN, credit card, PIN, etc. |
| `link_text_mismatch_count` | int | HTML links where display text URL ≠ actual href |
| `num_links` | int | Total hyperlinks in body |
| `num_attachments` | int | Number of email attachments |
| `body_length` | int | Character count of email body |
| `has_html_form` | bool | Email body contains `<form>` elements |
| `greeting_is_generic` | bool | Uses "Dear Customer", "Dear User" vs. personalised name |
| `has_spelling_errors` | int | Count of misspelled words (basic check) |

### ML Classification (from `ml_classifier.py`)
- **Primary model**: Random Forest (scikit-learn `RandomForestClassifier`)
- **Also train & compare**: Logistic Regression, SVM, XGBoost (for the evaluation chapter of the report)
- **Output**: `{ "prediction": "phishing" | "legitimate", "confidence": 0.0-1.0, "feature_importances": {...} }`
- **Model persistence**: Save trained models with `joblib` to `backend/app/ml/models/`
- **Training script** (`train_model.py`): Load dataset, extract features, train model, output accuracy/precision/recall/F1, save model

### Explanation Engine (from `explanation.py`)
After classification, generate **human-readable explanations** for the user:
```python
# Example output structure
{
    "risk_score": 85,        # 0-100 scale
    "verdict": "High Risk - Likely Phishing",
    "flags": [
        {
            "category": "URL",
            "severity": "high",
            "finding": "Suspicious URL detected",
            "explanation": "The link 'paypa1-secure.com/verify' uses a lookalike domain that mimics PayPal. The '1' replaces 'l' - a common typo-squatting technique.",
            "recommendation": "Never click links in emails. Navigate to PayPal directly by typing paypal.com in your browser."
        },
        {
            "category": "Content",
            "severity": "medium",
            "finding": "Urgency language detected",
            "explanation": "This email contains 4 urgency phrases: 'act immediately', 'account will be suspended', 'within 24 hours', 'verify now'. Phishing emails create false urgency to pressure quick action.",
            "recommendation": "Legitimate organisations rarely threaten immediate account suspension via email."
        }
    ],
    "summary_recommendations": [
        "Do not click any links in this email",
        "Do not provide any personal information",
        "Report this email as phishing to your email provider",
        "If concerned about your account, visit the company's website directly"
    ]
}
```

This explanatory output is **critical** - it bridges the detection engine and educational platform by teaching users WHY something is flagged.

---

## 📚 Educational Platform - Detailed Specification

### Scenario Database Schema
```sql
CREATE TABLE scenarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,               -- "Fake Bank Alert"
    difficulty TEXT NOT NULL,           -- "beginner", "intermediate", "advanced"
    category TEXT NOT NULL,             -- "credential_harvesting", "spear_phishing", "whaling", "clone_phishing", "legitimate"
    email_content TEXT NOT NULL,        -- Full simulated email (with headers if applicable)
    is_phishing BOOLEAN NOT NULL,      -- Ground truth
    indicators JSON,                   -- List of phishing indicators present (or empty for legit)
    explanation TEXT NOT NULL,          -- Detailed explanation of why phishing/legitimate
    learning_points JSON NOT NULL,     -- Key takeaways for the user
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,           -- Anonymous session tracking (no auth required)
    scenario_id INTEGER REFERENCES scenarios(id),
    user_answer TEXT NOT NULL,          -- "phishing" or "legitimate"
    is_correct BOOLEAN NOT NULL,
    time_taken_seconds INTEGER,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Scenario Content
Seed the database with **at least 15-20 scenarios** across difficulty levels:

**Beginner (5-7 scenarios):**
- Obviously fake "Nigerian prince" style scam
- Fake prize/lottery notification
- Blatant credential harvesting ("Your PayPal account is locked")
- Obvious spoofed sender (e.g., support@amaz0n-security.com)
- Legitimate email for contrast (e.g., genuine password reset from a real service pattern)

**Intermediate (5-7 scenarios):**
- Clone phishing (duplicated real email with swapped links)
- Fake invoice/payment notification
- Spoofed IT department email requesting credentials
- Phishing with URL shortener to hide destination
- Legitimate transactional email for contrast

**Advanced (5-7 scenarios):**
- Spear phishing targeting a specific role (e.g., "Hi [Name], re: Q3 budget review")
- Whaling attempt targeting executives
- Sophisticated clone with near-identical domain (paypa1.com)
- Multi-stage phishing (reply chain injection)
- Legitimate email with complex formatting for contrast

### Simulation Flow
1. User selects difficulty level (or "mixed" for all levels)
2. System presents a simulated email in a realistic email viewer component
3. User decides: **"Phishing"** or **"Legitimate"**
4. User can optionally **highlight specific suspicious elements** before answering
5. System reveals the correct answer with:
   - Whether the user was correct
   - Detailed explanation of each phishing indicator (or why it's legitimate)
   - Specific learning points
   - Tips to spot similar attacks in the future
6. Progress tracker updates (correct %, scenarios completed, difficulty breakdown)

### Progress Tracking
Track per-session (no login required - use localStorage session ID):
- Total scenarios attempted & completed
- Accuracy rate (overall and per difficulty level)
- Common mistakes (which indicator types the user misses most)
- Time spent per scenario
- Display as a dashboard with simple charts (bar chart for accuracy by difficulty, progress over scenarios)

---

## 🎨 Frontend Design Specification

### Design Principles
- **Clean, professional** - this is an academic cybersecurity tool, not a gaming app
- **Informative** - every screen should teach the user something
- **Colour scheme**: Use blue/navy tones for trust + red/amber for warning indicators
- **Responsive**: Must work on desktop and tablet (mobile is nice-to-have)

### Page Specifications

#### Home Page (`/`)
- Hero section: Tool name, one-line description, two CTAs: "Analyse an Email" and "Test Your Skills"
- Brief "How it works" section (3 cards: Submit → Analyse → Learn)
- Quick stats section if returning user (scenarios completed, last risk score)

#### Detection Page (`/detect`)
- **Input area**: Large text area for pasting raw email content + file upload button for .eml files
- **"Analyse" button**: Sends to backend, shows loading spinner
- **Results panel** (appears after analysis):
  - Risk score gauge (0-100, colour-coded: green/amber/red)
  - Verdict banner ("Low Risk - Likely Legitimate" / "High Risk - Likely Phishing")
  - Expandable threat flags grouped by category (URL / Headers / Content)
  - Each flag shows: severity icon, finding summary, detailed explanation, recommendation
  - Summary recommendations panel at the bottom

#### Education Hub (`/learn`)
- Difficulty selector (Beginner / Intermediate / Advanced / Mixed)
- Grid of scenario cards showing title, difficulty badge, category tag
- Progress summary bar at the top (X/Y completed, Z% accuracy)
- "Start Training" button → enters simulation mode

#### Simulation Page (`/learn/simulate`)
- **Email viewer component**: Renders the simulated email in a realistic-looking email client mockup (From, To, Subject, Date, Body)
- Two large buttons: "🚨 This is Phishing" / "✅ This is Legitimate"
- After answering → Feedback panel slides in:
  - Correct/Incorrect banner
  - Annotated email showing highlighted indicators
  - Explanation text
  - Learning points
  - "Next Scenario" button

#### Results/Progress Page (`/learn/progress`)
- Accuracy chart by difficulty
- Scenarios completed counter
- Weakest areas (which phishing indicator types user misses most)
- Encouragement messaging

---

## 🔌 API Endpoints

### Detection
```
POST /api/analyse
  Body: { "raw_email": "string" }  OR  multipart form with .eml file
  Response: { "risk_score": int, "verdict": string, "flags": [...], "recommendations": [...], "feature_vector": {...} }
```

### Education
```
GET  /api/scenarios?difficulty=beginner&limit=10
  Response: [{ "id": int, "title": string, "difficulty": string, "category": string }]

GET  /api/scenarios/:id
  Response: { "id": int, "email_content": string, "difficulty": string, "category": string }
  Note: Does NOT include is_phishing or explanation (that's revealed after answering)

POST /api/scenarios/:id/answer
  Body: { "session_id": "string", "answer": "phishing" | "legitimate", "time_taken_seconds": int }
  Response: { "correct": bool, "is_phishing": bool, "explanation": string, "indicators": [...], "learning_points": [...] }

GET  /api/progress/:session_id
  Response: { "total_attempted": int, "total_correct": int, "accuracy": float, "by_difficulty": {...}, "weak_areas": [...] }
```

### Health
```
GET  /api/health
  Response: { "status": "ok", "model_loaded": bool, "scenarios_count": int }
```

---

## 🗃️ Datasets for ML Training

Use these publicly available datasets:

1. **PhishTank** (https://phishtank.org/developer_info.php) - Verified phishing URLs
2. **UNB URL Dataset 2016** - Balanced URL features dataset (benign + phishing)
3. **Kaggle Phishing Email Dataset** - Labelled email corpus
4. **UCI Phishing Websites Dataset** - 30 features, 11,055 instances

For the training script, structure the pipeline as:
1. Load dataset(s)
2. Apply feature extraction functions (same ones used in live detection)
3. Split: 80% train / 20% test (stratified)
4. Train: Random Forest, Logistic Regression, SVM, XGBoost
5. Evaluate each: Accuracy, Precision, Recall, F1, Confusion Matrix, ROC-AUC
6. Save best model + scaler with `joblib`
7. Output comparison table (needed for the final report)

---

## ⚙️ Implementation Priorities

Build in this order:

### Phase 1 - Foundation (Week 1-2)
- [ ] Project scaffolding (both frontend and backend)
- [ ] Flask app factory with config, CORS, SQLite
- [ ] Database models & migrations
- [ ] Basic React app with routing and layout components
- [ ] Health check endpoint working end-to-end

### Phase 2 - Detection Engine Core (Week 3-5)
- [ ] Email parser service (handles raw text paste and .eml upload)
- [ ] URL analyser (all 13 URL features)
- [ ] Header analyser (all 7 header features)
- [ ] Content analyser (all 11 content features)
- [ ] Feature extractor orchestrator
- [ ] ML model training script + initial model
- [ ] Classification endpoint (`POST /api/analyse`)
- [ ] Explanation engine (generates human-readable flags)

### Phase 3 - Detection Frontend (Week 5-6)
- [ ] Email input form (paste + file upload)
- [ ] API integration with loading states
- [ ] Risk score gauge component
- [ ] Threat flags display (expandable cards)
- [ ] Recommendations panel

### Phase 4 - Educational Platform (Week 6-8)
- [ ] Scenario database seeding script (15-20 scenarios)
- [ ] Scenario API endpoints
- [ ] Education hub page with difficulty selector
- [ ] Email viewer simulation component
- [ ] Answer & feedback flow
- [ ] Progress tracking (backend + frontend dashboard)

### Phase 5 - Integration & Polish (Week 8-9)
- [ ] Cross-link detection results → related educational scenarios
- [ ] Error handling and input validation throughout
- [ ] Loading states, empty states, error states
- [ ] Responsive design pass

### Phase 6 - Testing & Evaluation (Week 9-10)
- [ ] Unit tests for feature extractors
- [ ] Integration tests for API endpoints
- [ ] ML model evaluation (comparison table with metrics)
- [ ] Manual testing with real phishing email samples

---

## 🚫 Out of Scope (Do Not Build)

- User authentication/registration (use anonymous session IDs)
- Live email client integration (Gmail/Outlook plugins)
- Automatic email blocking or quarantine
- Real-time email monitoring
- Anti-virus or malware scanning
- Mobile-native apps
- Payment or subscription features

---

## 📝 Code Quality Standards

- **Comments**: Every function should have a docstring explaining purpose, parameters, and return value
- **Error handling**: All API endpoints should have try/catch with meaningful error responses
- **Separation of concerns**: Business logic in `services/`, routing in `api/`, data in `models/`
- **Environment variables**: All config (DB path, model path, debug mode) via `.env`
- **No hardcoded secrets**: Use `.env.example` as a template
- **Type hints**: Use Python type hints in all function signatures
- **Constants**: Magic strings/numbers go in a constants file

---

## 🏁 Getting Started Command

After generating the project:
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python seed_scenarios.py
python run.py

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

Both should run concurrently - frontend on port 5173 (Vite default), backend on port 5000.

---

## Key Reminder

This is a **university Final Year Project**. The code needs to be:
1. **Well-documented** - I need to explain every design decision in my report
2. **Modular** - each component should be independently testable and demonstrable
3. **Demonstrable** - I need to demo this live during a viva presentation
4. **Evaluable** - I need to collect metrics (accuracy, F1, etc.) for my report

Prioritise a **working, demonstrable system** over feature completeness. A polished core that works well is far more impressive than a sprawling system that's half-broken.
