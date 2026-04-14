# API Documentation

> **Status:** Placeholder - to be completed during Phase 2 implementation.

## Base URL

```
http://localhost:5000/api
```

---

## Endpoints

### Health

#### `GET /health`

Returns the current status of the backend service and ML model.

**Response:**
```json
{
  "status": "ok",
  "model_loaded": true,
  "scenarios_count": 20
}
```

---

### Detection

#### `POST /analyse`

Analyse a raw email for phishing indicators.

**Request Body (JSON):**
```json
{
  "raw_email": "<full raw email content including headers>"
}
```

**Request Body (multipart/form-data):**
```
file: <.eml file upload>
```

**Response:**
```json
{
  "risk_score": 85,
  "verdict": "High Risk - Likely Phishing",
  "flags": [
    {
      "category": "URL",
      "severity": "high",
      "finding": "Suspicious lookalike domain",
      "explanation": "...",
      "recommendation": "..."
    }
  ],
  "summary_recommendations": ["..."],
  "feature_vector": {}
}
```

---

### Education

#### `GET /scenarios`

List available training scenarios.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `difficulty` | string | Filter by `beginner`, `intermediate`, `advanced` |
| `limit` | int | Max results to return (default: 10) |

**Response:**
```json
[
  {
    "id": 1,
    "title": "Fake Bank Alert",
    "difficulty": "beginner",
    "category": "credential_harvesting"
  }
]
```

---

#### `GET /scenarios/:id`

Retrieve a single scenario for display (answer is withheld).

**Response:**
```json
{
  "id": 1,
  "email_content": "...",
  "difficulty": "beginner",
  "category": "credential_harvesting"
}
```

---

#### `POST /scenarios/:id/answer`

Submit a user's answer to a scenario.

**Request Body:**
```json
{
  "session_id": "abc123",
  "answer": "phishing",
  "time_taken_seconds": 45
}
```

**Response:**
```json
{
  "correct": true,
  "is_phishing": true,
  "explanation": "...",
  "indicators": ["..."],
  "learning_points": ["..."]
}
```

---

#### `GET /progress/:session_id`

Retrieve a user's learning progress.

**Response:**
```json
{
  "total_attempted": 10,
  "total_correct": 7,
  "accuracy": 0.70,
  "by_difficulty": {
    "beginner": { "attempted": 5, "correct": 5 },
    "intermediate": { "attempted": 3, "correct": 2 },
    "advanced": { "attempted": 2, "correct": 0 }
  },
  "weak_areas": ["URL analysis", "Header spoofing"]
}
```
