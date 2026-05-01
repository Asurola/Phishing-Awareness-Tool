"""
app/services/__init__.py - Services package initialiser.

The services layer contains the core business logic of the phishing
detection pipeline. Each module has a single, well-defined responsibility:

  email_parser.py       - Parse raw email text or .eml files into structured data
  feature_extractor.py  - Extract header, body, and URL features from parsed emails
  ml_classifier.py      - Load trained model and produce predictions
  explanation.py        - Convert ML output to human-readable explanations
"""
