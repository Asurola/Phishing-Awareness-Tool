"""
app/services/__init__.py — Services package initialiser.

The services layer contains the core business logic of the phishing
detection pipeline. Each module has a single, well-defined responsibility:

  email_parser.py       — Parse raw email text or .eml files into structured data
  feature_extractor.py  — Orchestrate feature extraction across all analysers
  url_analyser.py       — Extract URL-based phishing features
  header_analyser.py    — Extract email header authentication features
  content_analyser.py   — NLP-based content feature extraction
  ml_classifier.py      — Load trained model and produce predictions
  explanation.py        — Convert ML output to human-readable explanations
"""
