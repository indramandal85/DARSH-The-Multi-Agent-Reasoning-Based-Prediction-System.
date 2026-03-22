# analysis/backtest_engine.py
#
# WHAT THIS DOES:
# Measures how accurate DARSH's predictions actually are.
#
# The core problem with MiroFish: it generates compelling stories
# but never checks if they were right. We fix that here.
#
# How it works:
#   1. You run a simulation on a historical event (one where outcome is known)
#   2. The simulation produces probability estimates per outcome type
#   3. You tell the engine what actually happened
#   4. It computes a Brier score — a proper accuracy metric
#
# Brier score explained in ML terms you already know:
#   It's Mean Squared Error for probability predictions.
#   prediction = [0.8 panic, 0.2 cautious]
#   reality    = [1.0 panic, 0.0 cautious]  (panic actually happened)
#   brier      = mean((0.8-1.0)² + (0.2-0.0)²) = mean(0.04 + 0.04) = 0.04
#   → Excellent score (0.0 = perfect, 1.0 = worst possible)

import sys
import os
import json
import sqlite3
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np


RESULTS_DIR = "data/reports"


def load_simulation_results(simulation_ids: list) -> dict:
    """
    Load aggregated results from one or more simulation branch databases.

    Reads the SQLite databases saved by Module 5's runner.
    Returns a summary of what happened across all branches.

    simulation_ids : list of simulation IDs e.g. ["branch_01", "branch_02"]
    """

    all_actions = []
    all_beliefs = []
    outcome_counts = {}

    for sim_id in simulation_ids:
        db_path = f"data/simulations/{sim_id}.db"

        if not os.path.exists(db_path):
            print(f"  Warning: database not found: {db_path}")
            continue

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Get all agent actions from final round
        cursor.execute("""
            SELECT action, belief, confidence, agent_type
            FROM agent_actions
            WHERE round_number = (SELECT MAX(round_number) FROM agent_actions)
        """)
        rows = cursor.fetchall()

        for action, belief, confidence, agent_type in rows:
            all_actions.append(action or "")
            all_beliefs.append(belief or "")

        # Get world states
        cursor.execute("""
            SELECT world_state, dominant_action, avg_confidence
            FROM world_states
            ORDER BY round_number DESC
            LIMIT 1
        """)
        final_state = cursor.fetchone()

        conn.close()

        # Classify outcome for this branch
        if final_state:
            world_text = (final_state[0] or "").lower()
            beliefs_text = " ".join(all_beliefs).lower()
            combined = world_text + " " + beliefs_text

            panic_score = sum(combined.count(w) for w in
                ["panic", "recession", "crisis", "crash", "catastrophic",
                 "devastating", "disaster", "doom", "terrible"])
            cautious_score = sum(combined.count(w) for w in
                ["cautious", "wait", "observe", "uncertain", "careful", "monitor"])
            optimistic_score = sum(combined.count(w) for w in
                ["recover", "stable", "opportunity", "growth", "positive",
                 "confident", "improve", "optimistic"])

            if panic_score > cautious_score and panic_score > optimistic_score:
                outcome = "panic"
            elif cautious_score > optimistic_score:
                outcome = "cautious"
            elif optimistic_score > 0:
                outcome = "optimistic"
            else:
                outcome = "divided"

            outcome_counts[outcome] = outcome_counts.get(outcome, 0) + 1

    total = sum(outcome_counts.values())
    outcome_probs = {}
    if total > 0:
        outcome_probs = {k: round(v / total, 3) for k, v in outcome_counts.items()}

    return {
        "simulation_ids"  : simulation_ids,
        "total_branches"  : len(simulation_ids),
        "outcome_counts"  : outcome_counts,
        "outcome_probs"   : outcome_probs,
        "dominant_outcome": max(outcome_counts, key=outcome_counts.get) if outcome_counts else "unknown"
    }


def compute_brier_score(predicted_probs: dict, actual_outcome: str) -> float:
    """
    Compute the Brier score for a set of predictions.

    Brier score = mean of (predicted_prob - actual)² across all outcome types
    Range: 0.0 (perfect) to 1.0 (worst possible)
    Good score: < 0.2
    Acceptable: 0.2 – 0.4
    Poor: > 0.4

    predicted_probs : dict of {outcome_type: probability}
                      e.g. {"panic": 0.8, "cautious": 0.2}
    actual_outcome  : what actually happened e.g. "panic"

    Returns: float Brier score
    """

    if not predicted_probs:
        return 1.0

    squared_errors = []

    for outcome, predicted_prob in predicted_probs.items():
        actual = 1.0 if outcome == actual_outcome else 0.0
        squared_errors.append((predicted_prob - actual) ** 2)

    brier = sum(squared_errors) / len(squared_errors)
    return round(brier, 4)


def interpret_brier_score(brier: float) -> str:
    """Human-readable interpretation of a Brier score."""
    if brier <= 0.05:
        return "EXCELLENT — near-perfect calibration"
    elif brier <= 0.10:
        return "VERY GOOD — strong predictive accuracy"
    elif brier <= 0.20:
        return "GOOD — reliable predictions"
    elif brier <= 0.30:
        return "ACCEPTABLE — moderate accuracy"
    elif brier <= 0.40:
        return "POOR — weak predictions"
    else:
        return "VERY POOR — worse than random"


def run_backtest(
    simulation_ids: list,
    actual_outcome: str,
    event_description: str,
    event_date: str = None
) -> dict:
    """
    Run a full backtest: load simulation results, compare to real outcome,
    compute accuracy metrics.

    simulation_ids   : list of branch simulation IDs to evaluate
    actual_outcome   : what actually happened in reality
                       must be one of: "panic", "cautious", "optimistic", "divided"
    event_description: what the simulation was predicting
    event_date       : when the real event occurred (for records)

    Returns dict with full backtest results.
    """

    print(f"\n{'='*50}")
    print(f"  BACKTEST: {event_description}")
    print(f"  Real outcome: {actual_outcome}")
    print(f"{'='*50}")

    # Load simulation results
    print(f"\n  Loading {len(simulation_ids)} simulation branches...")
    sim_results = load_simulation_results(simulation_ids)

    predicted_probs = sim_results["outcome_probs"]
    dominant_predicted = sim_results["dominant_outcome"]

    print(f"  Predicted probabilities: {predicted_probs}")
    print(f"  Dominant predicted     : {dominant_predicted}")
    print(f"  Actual outcome         : {actual_outcome}")

    # Compute Brier score
    brier = compute_brier_score(predicted_probs, actual_outcome)
    interpretation = interpret_brier_score(brier)

    # Was the dominant prediction correct?
    prediction_correct = dominant_predicted == actual_outcome

    print(f"\n  Brier score     : {brier}")
    print(f"  Interpretation  : {interpretation}")
    print(f"  Prediction hit  : {'YES ✓' if prediction_correct else 'NO ✗'}")

    # Confidence in the actual outcome
    actual_confidence = predicted_probs.get(actual_outcome, 0.0)

    result = {
        "event_description"  : event_description,
        "event_date"         : event_date or datetime.now().strftime("%Y-%m-%d"),
        "simulation_ids"     : simulation_ids,
        "predicted_probs"    : predicted_probs,
        "dominant_predicted" : dominant_predicted,
        "actual_outcome"     : actual_outcome,
        "brier_score"        : brier,
        "brier_interpretation": interpretation,
        "prediction_correct" : prediction_correct,
        "actual_confidence"  : actual_confidence
    }

    # Save backtest result
    os.makedirs(RESULTS_DIR, exist_ok=True)
    result_path = os.path.join(
        RESULTS_DIR,
        f"backtest_{event_description[:30].replace(' ', '_')}.json"
    )
    with open(result_path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"  Saved to: {result_path}")
    return result