# analysis/calibration.py
#
# CALIBRATION TRACKER
#
# Tracks prediction accuracy over multiple backtests.
# Answers: "When DARSH says 80% confident, does it happen 80% of the time?"
# A well-calibrated system should have predicted probability ≈ actual frequency.
#
# This is what transforms DARSH from a demo into a scientific tool.

import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


CALIBRATION_FILE = "data/reports/calibration_history.json"


def save_prediction(
    event_id: str,
    predicted_prob: float,
    actual_outcome: bool,
    outcome_type: str
):
    """
    Save one prediction to the calibration history.

    event_id       : unique ID for this prediction event
    predicted_prob : what probability was predicted (0.0–1.0)
    actual_outcome : did the predicted outcome actually happen? (True/False)
    outcome_type   : what was being predicted e.g. "panic"
    """

    os.makedirs("data/reports", exist_ok=True)

    history = []
    if os.path.exists(CALIBRATION_FILE):
        with open(CALIBRATION_FILE, "r") as f:
            history = json.load(f)

    history.append({
        "event_id"      : event_id,
        "predicted_prob": predicted_prob,
        "actual"        : 1.0 if actual_outcome else 0.0,
        "outcome_type"  : outcome_type,
        "correct"       : actual_outcome
    })

    with open(CALIBRATION_FILE, "w") as f:
        json.dump(history, f, indent=2)


def compute_calibration_summary() -> dict:
    """
    Compute calibration statistics from all saved predictions.
    Returns summary with accuracy metrics.
    """

    if not os.path.exists(CALIBRATION_FILE):
        return {"message": "No calibration data yet. Run backtests first."}

    with open(CALIBRATION_FILE, "r") as f:
        history = json.load(f)

    if not history:
        return {"message": "No predictions recorded yet."}

    total = len(history)
    correct = sum(1 for p in history if p["correct"])
    accuracy = round(correct / total, 3)

    # Brier score across all predictions
    brier = sum(
        (p["predicted_prob"] - p["actual"]) ** 2
        for p in history
    ) / total

    return {
        "total_predictions": total,
        "correct"          : correct,
        "accuracy"         : accuracy,
        "brier_score"      : round(brier, 4),
        "interpretation"   : (
            "Well calibrated" if brier < 0.2
            else "Moderately calibrated" if brier < 0.35
            else "Needs improvement"
        )
    }


def print_calibration_report():
    """Print a human-readable calibration summary."""

    summary = compute_calibration_summary()

    print("\n" + "="*45)
    print("  CALIBRATION REPORT")
    print("="*45)

    if "message" in summary:
        print(f"  {summary['message']}")
        return

    print(f"  Total predictions : {summary['total_predictions']}")
    print(f"  Correct           : {summary['correct']}")
    print(f"  Accuracy          : {summary['accuracy']*100:.1f}%")
    print(f"  Brier score       : {summary['brier_score']}")
    print(f"  Status            : {summary['interpretation']}")
    print("="*45)