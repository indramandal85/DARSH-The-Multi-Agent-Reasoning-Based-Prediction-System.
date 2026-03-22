# analysis/batch_backtest.py
#
# HISTORICAL BACKTESTING ENGINE
#
# Runs DARSH against real historical events with known outcomes.
# Computes honest Brier scores — the scientific credibility layer
# that distinguishes DARSH from every other prediction demo.
#
# This is the research contribution MiroFish never made.
#
# How it works:
#   1. Load each historical event's document
#   2. Run a small simulation (3 branches, 4 agents, 3 rounds)
#   3. Compare predicted outcome to documented real outcome
#   4. Compute Brier score for this prediction
#   5. Accumulate across all events for aggregate accuracy stats
#
# Important: these are SHORT simulations for calibration testing.
# For serious prediction, use the full simulation with more branches/agents.

import sys
import os
import json
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis.backtest_engine import compute_brier_score, interpret_brier_score
from analysis.calibration import save_prediction, compute_calibration_summary


HISTORICAL_INDEX = "data/historical_events/index.json"
HISTORICAL_DOCS  = "data/historical_events/docs"
RESULTS_DIR      = "data/reports"


def load_historical_events(event_ids: list = None) -> list:
    """Load event definitions from the index file."""
    if not os.path.exists(HISTORICAL_INDEX):
        raise FileNotFoundError(
            f"Historical events index not found: {HISTORICAL_INDEX}\n"
            f"Run the setup step to create it."
        )
    with open(HISTORICAL_INDEX) as f:
        events = json.load(f)

    if event_ids:
        events = [e for e in events if e["event_id"] in event_ids]

    return events


def run_single_historical_event(event: dict, verbose: bool = False) -> dict:
    """
    Run one historical event through DARSH and score the prediction.

    Uses small simulation settings to keep runtime reasonable:
      - 2 branches (enough for basic probability estimation)
      - 4 agents per branch
      - 3 rounds

    Returns dict with prediction results and Brier score.
    """
    from simulation.parallel_branches import run_parallel_branches

    event_id   = event["event_id"]
    doc_path   = os.path.join(HISTORICAL_DOCS, event["document_file"])
    actual     = event["actual_outcome"]
    topic      = event["description"]

    if not os.path.exists(doc_path):
        return {
            "event_id": event_id,
            "error"   : f"Document not found: {doc_path}",
            "skipped" : True
        }

    # Read the historical document as the simulation input
    with open(doc_path) as f:
        situation = f.read()[:600]  # first 600 chars as initial situation

    print(f"\n  [{event_id}]")
    print(f"  Topic   : {topic[:70]}...")
    print(f"  Actual  : {actual}")

    start = time.time()

    try:
        results = run_parallel_branches(
            topic             = topic,
            initial_situation = situation,
            events_per_round  = [
                "Situation continues to develop with new reactions emerging.",
                "Expert analysis and public response published.",
                "Government and institutional responses observed."
            ],
            available_actions = [
                "wait and observe cautiously",
                "take immediate protective action",
                "spread information to network",
                "research and analyze the situation",
                "express optimism about recovery",
                "consult advisors for guidance"
            ],
            num_branches = 2,
            num_agents   = 4,
            num_rounds   = 3
        )

        elapsed = round(time.time() - start, 1)

        # Convert percentage probs to 0-1 scale for Brier scoring
        outcome_probs_01 = {
            k: v / 100.0
            for k, v in results["outcome_probs"].items()
        }

        brier = compute_brier_score(outcome_probs_01, actual)
        interp = interpret_brier_score(brier)

        # Determine if prediction was correct (dominant outcome matches actual)
        predicted = results["dominant_outcome"]
        correct   = predicted == actual

        # Save to calibration history
        actual_prob = outcome_probs_01.get(actual, 0.0)
        save_prediction(
            event_id       = event_id,
            predicted_prob = actual_prob,
            actual_outcome = True,
            outcome_type   = actual
        )

        result = {
            "event_id"         : event_id,
            "date"             : event["date"],
            "domain"           : event.get("domain", "unknown"),
            "predicted_probs"  : outcome_probs_01,
            "dominant_predicted": predicted,
            "actual_outcome"   : actual,
            "brier_score"      : brier,
            "brier_interpretation": interp,
            "prediction_correct": correct,
            "elapsed_seconds"  : elapsed,
            "skipped"          : False
        }

        status = "✓ CORRECT" if correct else "✗ WRONG"
        print(f"  Predicted: {predicted} | {status} | Brier: {brier}")

        return result

    except Exception as e:
        print(f"  ERROR: {e}")
        return {
            "event_id": event_id,
            "error"   : str(e),
            "skipped" : True
        }


def run_historical_suite(
    event_ids: list = None,
    save_results: bool = True
) -> dict:
    """
    Run all historical events and produce aggregate accuracy report.

    event_ids   : optional list of specific event IDs to run.
                  If None, runs all events in the index.
    save_results: whether to save results JSON to data/reports/

    Returns dict with per-event results and aggregate statistics.
    """

    events = load_historical_events(event_ids)

    print(f"\n{'='*55}")
    print(f"  HISTORICAL BACKTESTING SUITE")
    print(f"  Events to test: {len(events)}")
    print(f"  Config: 2 branches × 4 agents × 3 rounds per event")
    print(f"  Est. time: ~{len(events) * 8} minutes")
    print(f"{'='*55}")

    per_event_results = []
    total_start = time.time()

    for i, event in enumerate(events, 1):
        print(f"\n  Event {i}/{len(events)}")
        result = run_single_historical_event(event)
        per_event_results.append(result)

    total_elapsed = round(time.time() - total_start, 1)

    # Compute aggregate statistics
    valid = [r for r in per_event_results if not r.get("skipped")]
    skipped = [r for r in per_event_results if r.get("skipped")]

    if not valid:
        print("\n  No valid results to aggregate.")
        return {"error": "No events completed successfully"}

    brier_scores = [r["brier_score"] for r in valid]
    correct      = [r for r in valid if r.get("prediction_correct")]

    avg_brier = round(sum(brier_scores) / len(brier_scores), 4)
    accuracy  = round(len(correct) / len(valid), 3)

    # Domain breakdown
    domain_results = {}
    for r in valid:
        domain = r.get("domain", "unknown")
        if domain not in domain_results:
            domain_results[domain] = {"correct": 0, "total": 0, "brier_sum": 0}
        domain_results[domain]["total"] += 1
        domain_results[domain]["brier_sum"] += r["brier_score"]
        if r.get("prediction_correct"):
            domain_results[domain]["correct"] += 1

    summary = {
        "total_events"  : len(events),
        "completed"     : len(valid),
        "skipped"       : len(skipped),
        "avg_brier_score": avg_brier,
        "accuracy"      : accuracy,
        "correct_count" : len(correct),
        "brier_interpretation": interpret_brier_score(avg_brier),
        "domain_breakdown": domain_results,
        "per_event"     : per_event_results,
        "total_elapsed_seconds": total_elapsed
    }

    # Print summary
    print(f"\n\n{'='*55}")
    print(f"  BACKTESTING RESULTS SUMMARY")
    print(f"{'='*55}")
    print(f"  Events completed   : {len(valid)}/{len(events)}")
    print(f"  Correct predictions: {len(correct)}/{len(valid)} "
          f"({accuracy*100:.0f}%)")
    print(f"  Average Brier score: {avg_brier} "
          f"({interpret_brier_score(avg_brier)})")
    print(f"  Total time         : {total_elapsed}s")
    print(f"\n  Per-event breakdown:")
    for r in valid:
        status = "✓" if r.get("prediction_correct") else "✗"
        print(f"  {status} [{r['event_id'][:30]:30}] "
              f"Brier={r['brier_score']:.3f} "
              f"pred={r['dominant_predicted']} "
              f"actual={r['actual_outcome']}")

    # Save results
    if save_results:
        os.makedirs(RESULTS_DIR, exist_ok=True)
        results_path = os.path.join(RESULTS_DIR, "historical_backtest_results.json")
        with open(results_path, "w") as f:
            json.dump(summary, f, indent=2)
        print(f"\n  Results saved to: {results_path}")

    return summary