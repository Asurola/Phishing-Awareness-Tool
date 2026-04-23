"""
app/ml/train_model.py - ML model training script.

Trains phishing classifiers on labelled email/URL datasets and saves the
best-performing model to disk for use by the live detection service.

Training pipeline:
  1. Load dataset(s) from app/ml/data/
  2. Apply feature extraction (same functions as live detection)
  3. Stratified 80/20 train/test split
  4. Train: Random Forest, Logistic Regression, SVM, XGBoost
  5. Evaluate each with accuracy, precision, recall, F1, ROC-AUC
  6. Save best model + scaler with joblib
  7. Print comparison table (for final report)

Usage:
    python -m app.ml.train_model
    or
    python app/ml/train_model.py
"""

from __future__ import annotations
import os
import sys

# Ensure backend/ is on the Python path when run as a script
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def load_dataset(data_dir: str) -> tuple:
    """
    Load and combine phishing/legitimate labelled datasets.

    Expected files in data_dir:
      - phishing.csv  - Phishing samples with feature columns + 'label' column
      - legitimate.csv - Legitimate samples with same format

    Args:
        data_dir: Path to the directory containing training data files.

    Returns:
        tuple: (X, y) where X is a pandas DataFrame of features and
               y is a pandas Series of labels (1=phishing, 0=legitimate).
    """
    raise NotImplementedError("train_model.load_dataset is not yet implemented.")


def train_all_models(X_train, y_train) -> dict:
    """
    Train all four classifier models on the training data.

    Models trained:
      - RandomForestClassifier (primary)
      - LogisticRegression
      - SVC (Support Vector Machine)
      - XGBClassifier

    Args:
        X_train: Training feature matrix (numpy array or DataFrame).
        y_train: Training labels (numpy array or Series).

    Returns:
        dict: Mapping of model_name → fitted model instance.
    """
    raise NotImplementedError("train_model.train_all_models is not yet implemented.")


def evaluate_model(model, X_test, y_test, model_name: str) -> dict:
    """
    Evaluate a trained model on the test set and return metrics.

    Args:
        model:      Fitted scikit-learn compatible model.
        X_test:     Test feature matrix.
        y_test:     True test labels.
        model_name: Display name for the model (used in output table).

    Returns:
        dict: {
            "model": model_name,
            "accuracy": float,
            "precision": float,
            "recall": float,
            "f1": float,
            "roc_auc": float
        }
    """
    raise NotImplementedError("train_model.evaluate_model is not yet implemented.")


def save_model(model, scaler, output_path: str) -> None:
    """
    Persist the trained model and feature scaler to disk using joblib.

    Args:
        model:       Fitted classifier to save.
        scaler:      Fitted StandardScaler (or equivalent) to save.
        output_path: File path to save the model .pkl file (e.g.
                     'app/ml/models/phishing_classifier.pkl').
    """
    raise NotImplementedError("train_model.save_model is not yet implemented.")


if __name__ == "__main__":
    print("ML training script - Phase 2 implementation pending.")
    print("Run this script after implementing the training pipeline.")
