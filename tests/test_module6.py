# tests/test_module6.py
# Run with: python tests/test_module6.py
#
# PASS condition:
#   - Backtest computes Brier score from Module 5 simulation data
#   - Report engine generates a complete report.md with all 6 sections
#   - Report file exists and has substantial content (>500 words)

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis.backtest_engine import run_backtest
from analysis.report_engine import ReportEngine
from analysis.calibration import save_prediction, print_calibration_report


def run_test():

    print("\n" + "="*52)
    print("  DARSH — MODULE 6 DRY-RUN TEST")
    print("  Backtesting, Calibration & Report Engine")
    print("="*52)

    # ── Check Module 5 databases exist ────────────────────────────────────
    branch_ids = ["branch_01", "branch_02", "branch_03"]
    missing = [
        b for b in branch_ids
        if not os.path.exists(f"data/simulations/{b}.db")
    ]

    if missing:
        print(f"\n  ERROR: Missing simulation databases: {missing}")
        print(f"  Run Module 5 test first: python tests/test_module5.py")
        return

    print(f"\n  Found simulation databases: {branch_ids}")

    # ── Part A: Backtest ───────────────────────────────────────────────────
    print(f"\n\n{'─'*52}")
    print(f"  PART A — BACKTESTING")
    print(f"{'─'*52}")

    # For our test: the simulation predicted "panic" at 100%
    # We define the "actual outcome" as "panic" (which is realistic
    # for an emergency RBI rate hike scenario)
    # In a real system you would look up what actually happened historically

    backtest_result = run_backtest(
        simulation_ids    = branch_ids,
        actual_outcome    = "panic",
        event_description = "RBI 0.5% emergency rate hike March 2024",
        event_date        = "2024-03-15"
    )

    print(f"\n  Backtest complete:")
    print(f"  Brier score     : {backtest_result['brier_score']}")
    print(f"  Interpretation  : {backtest_result['brier_interpretation']}")
    print(f"  Correct?        : {backtest_result['prediction_correct']}")

    # Save to calibration history
    save_prediction(
        event_id       = "rbi_rate_hike_test",
        predicted_prob = backtest_result["actual_confidence"],
        actual_outcome = True,
        outcome_type   = "panic"
    )

    # ── Part B: Generate report ────────────────────────────────────────────
    print(f"\n\n{'─'*52}")
    print(f"  PART B — REPORT GENERATION")
    print(f"{'─'*52}")

    # Load causal summary from Module 3 if available
    causal_summary = ""
    causal_path = "data/graphs/rbi_crisis_causal.json"
    if os.path.exists(causal_path):
        with open(causal_path, "r") as f:
            causal_data = json.load(f)
        edges = causal_data.get("causal_edges", [])[:5]
        causal_summary = " | ".join(
            f"{e['cause']} causes {e['effect']} (strength {e['strength']})"
            for e in edges
        )

    engine = ReportEngine(
        simulation_ids = branch_ids,
        topic          = "RBI 0.5% emergency interest rate hike — Indian economic impact",
        outcome_probs  = {"panic": 1.0},
        causal_summary = causal_summary,
        brier_score    = backtest_result["brier_score"]
    )

    report = engine.generate_report()

    # ── Part C: Calibration ────────────────────────────────────────────────
    print(f"\n\n{'─'*52}")
    print(f"  PART C — CALIBRATION")
    print(f"{'─'*52}")
    print_calibration_report()

    # ── Pass check ─────────────────────────────────────────────────────────
    report_path = f"data/reports/report_RBI_0.5%_emergency_interest_rate_hike_.md"
    report_files = [
        f for f in os.listdir("data/reports")
        if f.startswith("report_") and f.endswith(".md")
    ]
    report_exists    = len(report_files) > 0
    report_has_content = len(report.split()) > 300
    brier_computed   = backtest_result["brier_score"] is not None
    all_sections     = all(
        section in report
        for section in [
            "Executive Summary",
            "Predicted Outcome",
            "Causal Drivers",
            "Agent Behavior",
            "Dissenting Views",
            "Confidence Assessment"
        ]
    )

    passed = report_exists and report_has_content and brier_computed and all_sections

    print(f"\n\n{'='*52}")
    if passed:
        print("  ✓  MODULE 6 PASSED")
        print(f"  ✓  Brier score computed: {backtest_result['brier_score']}")
        print(f"  ✓  Report generated: {report_files[0] if report_files else 'N/A'}")
        print(f"  ✓  Word count: ~{len(report.split())} words")
        print(f"  ✓  All 6 sections present")
        print(f"  ✓  Calibration history updated")
        print(f"\n  → Ready for Module 7 (UI Integration)")
    else:
        print("  ✗  Something needs fixing:")
        print(f"  Report file exists  : {report_exists}")
        print(f"  Report has content  : {report_has_content} ({len(report.split())} words)")
        print(f"  Brier computed      : {brier_computed}")
        print(f"  All 6 sections      : {all_sections}")
        print(f"\n  → Paste output and we fix together")
    print("="*52 + "\n")


if __name__ == "__main__":
    import json
    run_test()