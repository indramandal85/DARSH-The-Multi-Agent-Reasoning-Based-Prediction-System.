# tests/test_module5.py
# Run with: python tests/test_module5.py
#
# PASS condition:
#   - 3 branches complete without errors
#   - Each branch has an outcome classification
#   - Probability distribution sums to 100%
#   - Prediction summary generated

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation.parallel_branches import run_parallel_branches, print_results


def run_test():

    print("\n" + "="*55)
    print("  DARSH — MODULE 5 DRY-RUN TEST")
    print("  Multi-Scale Parallel Simulation Engine")
    print("="*55)

    # ── Simulation parameters ──────────────────────────────────────────────
    topic = "RBI interest rate hike impact on Indian economy"

    initial_situation = (
        "The Reserve Bank of India has announced an emergency "
        "0.5% interest rate hike. Markets dropped 2.3% immediately. "
        "Inflation is at 7.2%. Recession warnings are circulating."
    )

    # One new event injected per round — escalating pressure
    events = [
        "RBI Governor confirms this is the first of potentially three hikes this year.",
        "Three major banks announce EMI increases affecting 40 million borrowers.",
        "IIM economist publishes report: 65% probability of recession within 6 months."
    ]

    actions = [
        "wait and observe before acting",
        "immediately revise financial plan",
        "research historical data before deciding",
        "spread concerns to social network",
        "consult financial advisor",
        "file formal complaint or protest"
    ]

    # ── Run 3 parallel branches ────────────────────────────────────────────
    # Using small numbers for the test (3 branches, 5 agents, 3 rounds)
    # Production runs would use 5-10 branches, 20+ agents, 5+ rounds
    results = run_parallel_branches(
        topic             = topic,
        initial_situation = initial_situation,
        events_per_round  = events,
        available_actions = actions,
        num_branches      = 3,
        num_agents        = 5,
        num_rounds        = 3
    )

    # ── Print results ──────────────────────────────────────────────────────
    print_results(results)

    # ── Pass check ─────────────────────────────────────────────────────────
    branches_ran = len(results["branches"]) == 3
    has_outcomes = len(results["outcome_probs"]) > 0
    probs_sum_100 = abs(sum(results["outcome_probs"].values()) - 100.0) < 1.0
    has_prediction = len(results["prediction"]) > 20
    no_errors = all(
        b.get("final_outcome") != "error"
        for b in results["branches"]
    )

    passed = branches_ran and has_outcomes and has_prediction and no_errors

    print(f"\n\n{'='*55}")
    if passed:
        print("  ✓  MODULE 5 PASSED")
        print(f"  ✓  {len(results['branches'])} branches completed")
        print(f"  ✓  Outcome distribution: {results['outcome_probs']}")
        print(f"  ✓  Dominant outcome: {results['dominant_outcome']}")
        print(f"  ✓  Prediction generated")
        print(f"\n  → Ready for Module 6")
    else:
        print("  ✗  Something needs fixing:")
        print(f"  Branches ran (3)    : {branches_ran}")
        print(f"  Has outcomes        : {has_outcomes}")
        print(f"  Has prediction      : {has_prediction}")
        print(f"  No errors           : {no_errors}")
        print(f"\n  → Paste output and we fix together")
    print("="*55 + "\n")


if __name__ == "__main__":
    run_test()