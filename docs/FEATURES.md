# Feature Checklist

> Tracks implementation status of all planned features across project phases.

---

## Phase 1 - Foundation

- [ ] Flask app factory with config, CORS, SQLite
- [ ] Database models (Analysis, Progress/UserProgress)
- [ ] Basic React app with routing
- [ ] Layout components (Navbar, Footer)
- [ ] Health check endpoint (`GET /api/health`) working end-to-end

---

## Phase 2 - Detection Engine

### Feature Extraction
- [ ] Email parser service (raw text + .eml upload)
- [ ] URL analyser - 13 URL features
- [ ] Header analyser - 7 header features
- [ ] Content analyser - 11 content features
- [ ] Feature extractor orchestrator

### ML Pipeline
- [ ] Training script (`train_model.py`)
- [ ] Evaluation script (`evaluate_model.py`) - accuracy, F1, ROC-AUC
- [ ] Random Forest classifier
- [ ] Logistic Regression (comparison)
- [ ] SVM (comparison)
- [ ] XGBoost (comparison)
- [ ] Model persistence with `joblib`

### API
- [ ] `POST /api/analyse` endpoint
- [ ] Explanation engine (human-readable flags)

---

## Phase 3 - Detection Frontend

- [ ] Email input form (paste + .eml upload)
- [ ] API integration with loading states
- [ ] Risk score gauge (0–100, colour-coded)
- [ ] Threat flags display (expandable cards by category)
- [ ] Recommendations panel

---

## Phase 4 - Educational Platform

- [ ] Scenario database seeding script (15–20 scenarios)
- [ ] `GET /api/scenarios` endpoint
- [ ] `POST /api/scenarios/:id/answer` endpoint
- [ ] Education hub page with difficulty selector
- [ ] Email viewer simulation component
- [ ] Answer & feedback flow
- [ ] `GET /api/progress/:session_id` endpoint
- [ ] Progress dashboard with charts

---

## Phase 5 - Integration & Polish

- [ ] Cross-link detection results → related educational scenarios
- [ ] Error handling and input validation throughout
- [ ] Loading / empty / error states
- [ ] Responsive design pass (desktop + tablet)

---

## Phase 6 - Testing & Evaluation

- [ ] Unit tests: `test_email_parser.py`
- [ ] Unit tests: `test_feature_extractor.py`
- [ ] Unit tests: `test_url_analyser.py`
- [ ] Integration tests: `test_detection.py`
- [ ] ML evaluation comparison table
- [ ] Manual testing with real phishing samples

---

## URL Features (13 total)

| Feature | Status |
|---------|--------|
| `url_length` | [ ] |
| `has_ip_address` | [ ] |
| `has_https` | [ ] |
| `num_dots` | [ ] |
| `num_hyphens` | [ ] |
| `num_subdomains` | [ ] |
| `has_at_symbol` | [ ] |
| `has_redirect` | [ ] |
| `uses_shortener` | [ ] |
| `path_length` | [ ] |
| `has_suspicious_tld` | [ ] |
| `domain_age_days` | [ ] |
| `has_prefix_suffix` | [ ] |

## Header Features (7 total)

| Feature | Status |
|---------|--------|
| `sender_domain_matches_from` | [ ] |
| `has_spf_pass` | [ ] |
| `has_dkim_pass` | [ ] |
| `has_reply_to_mismatch` | [ ] |
| `received_hop_count` | [ ] |
| `has_x_mailer` | [ ] |
| `from_domain_is_freemail` | [ ] |

## Content Features (11 total)

| Feature | Status |
|---------|--------|
| `urgency_word_count` | [ ] |
| `threat_word_count` | [ ] |
| `reward_word_count` | [ ] |
| `has_credential_request` | [ ] |
| `link_text_mismatch_count` | [ ] |
| `num_links` | [ ] |
| `num_attachments` | [ ] |
| `body_length` | [ ] |
| `has_html_form` | [ ] |
| `greeting_is_generic` | [ ] |
| `has_spelling_errors` | [ ] |
