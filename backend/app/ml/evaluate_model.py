"""
app/ml/evaluate_model.py — Model evaluation and comparison script.

Loads all trained models from app/ml/models/ and evaluates them on a
held-out test set, producing a comparison table with key metrics
for inclusion in the FYP report.

Metrics computed per model:
  - Accuracy
  - Precision (macro-averaged)
  - Recall    (macro-averaged)
  - F1 Score  (macro-averaged)
  - ROC-AUC
  - Confusion matrix

Also generates:
  - ROC curves for all models on a single plot (matplotlib)
  - Feature importance bar chart for the Random Forest model
  - Confusion matrix heatmaps (one per model)

Usage:
    python app/ml/evaluate_model.py --test-data app/ml/data/test.csv

TODO (Phase 2): Implement after training script is complete.
"""

from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def load_all_models(models_dir: str) -> dict:
    """
    Load all trained model .pkl files from the models directory.

    Args:
        models_dir: Path to the directory containing saved .pkl files.

    Returns:
        dict: Mapping of model_name (str) → loaded model object.
    """
    # TODO (Phase 2): Implement with joblib.load() for each .pkl found
    raise NotImplementedError("evaluate_model.load_all_models is not yet implemented.")


def print_comparison_table(results: list[dict]) -> None:
    """
    Print a formatted comparison table of all model evaluation metrics.

    Args:
        results: List of metric dicts as returned by train_model.evaluate_model().
                 Each dict should have keys: model, accuracy, precision, recall,
                 f1, roc_auc.
    """
    # TODO (Phase 2): Implement with tabulate or manual string formatting
    raise NotImplementedError("evaluate_model.print_comparison_table is not yet implemented.")


def plot_roc_curves(models: dict, X_test, y_test, output_path: str) -> None:
    """
    Plot ROC curves for all models and save to a PNG file.

    Args:
        models:      Dict of model_name → model object.
        X_test:      Test feature matrix.
        y_test:      True test labels.
        output_path: Path to save the output PNG file.
    """
    # TODO (Phase 2): Implement with matplotlib + sklearn.metrics.roc_curve
    raise NotImplementedError("evaluate_model.plot_roc_curves is not yet implemented.")


if __name__ == "__main__":
    print("Evaluation script — Phase 2 implementation pending.")
