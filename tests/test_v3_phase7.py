# tests/test_v3_phase7.py
#
# Phase 7 — prediction logger and calibration tests
#
# Run with:
#   .venv/bin/python tests/test_v3_phase7.py

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_prediction_logger_and_summary():
    print("\n" + "=" * 55)
    print("  TEST 1 — Prediction Logger Summary")
    print("=" * 55)

    import analysis.prediction_logger as logger

    with tempfile.TemporaryDirectory() as tmpdir:
        logger.PREDICTION_LOG_PATH = os.path.join(tmpdir, "prediction_log.json")
        logger.TRACK_RECORD_TABLE_PATH = os.path.join(tmpdir, "track_record_table.md")

        logger.log_prediction(
            event_id="rbi_rate_hike_2022",
            topic="RBI Rate Hike 2022",
            predicted_probs={"panic": 0.72, "cautious": 0.20, "optimistic": 0.05, "divided": 0.03},
            actual_outcome="panic",
            dominant_predicted="panic",
            brier_score=0.0284,
            interpretation="VERY GOOD — strong predictive accuracy",
            correct=True,
            event_type="rbi_rate_hike",
            event_date="2022-05-04",
            domain="macro",
            branch_count=3,
            agent_count=5,
            market_impact={
                "market_regime": "policy_shock",
                "sector_impacts": {
                    "nbfc": {"direction": "strong_negative"},
                    "banking_private": {"direction": "negative"},
                }
            },
            actual_sector_moves={
                "nbfc": "strong_negative",
                "banking_private": "negative",
            }
        )

        logger.log_prediction(
            event_id="budget_event_001",
            topic="Union Budget Expansion",
            predicted_probs={"panic": 0.10, "cautious": 0.25, "optimistic": 0.55, "divided": 0.10},
            actual_outcome="cautious",
            dominant_predicted="optimistic",
            brier_score=0.276,
            interpretation="ACCEPTABLE — moderate accuracy",
            correct=False,
            event_type="budget_fiscal_expansion",
            event_date="2024-02-01",
            domain="policy",
            branch_count=4,
            agent_count=6
        )

        summary = logger.compute_track_record_summary()

        total_ok = summary["total_predictions"] == 2
        accuracy_ok = abs(summary["accuracy"] - 0.5) < 0.0001
        avg_brier_ok = summary["average_brier_score"] is not None
        sector_accuracy_ok = summary["sector_direction_accuracy"] == 1.0

        print(f"\n  Total predictions         : {summary['total_predictions']}")
        print(f"  Accuracy                  : {summary['accuracy']}")
        print(f"  Avg Brier                 : {summary['average_brier_score']}")
        print(f"  Sector accuracy           : {summary['sector_direction_accuracy']}")

        passed = total_ok and accuracy_ok and avg_brier_ok and sector_accuracy_ok
        print(f"\n  {'✓ TEST 1 PASSED' if passed else '✗ TEST 1 FAILED'}")
        return passed


def test_track_record_markdown_generation():
    print("\n" + "=" * 55)
    print("  TEST 2 — Track Record Markdown")
    print("=" * 55)

    import analysis.prediction_logger as logger

    with tempfile.TemporaryDirectory() as tmpdir:
        logger.PREDICTION_LOG_PATH = os.path.join(tmpdir, "prediction_log.json")
        logger.TRACK_RECORD_TABLE_PATH = os.path.join(tmpdir, "track_record_table.md")

        logger.log_prediction(
            event_id="oil_case",
            topic="Oil Price Spike",
            predicted_probs={"panic": 0.20, "cautious": 0.50, "optimistic": 0.15, "divided": 0.15},
            actual_outcome="cautious",
            dominant_predicted="cautious",
            brier_score=0.18,
            interpretation="GOOD — reliable predictions",
            correct=True,
            event_type="oil_price_spike",
            event_date="2022-03-08",
            domain="global"
        )

        markdown = logger.build_track_record_table()
        file_exists = os.path.exists(logger.TRACK_RECORD_TABLE_PATH)
        has_header = "| Event | Date | Predicted | Actual | Brier Score | Sector Accuracy |" in markdown
        has_row = "Oil Price Spike" in markdown

        print(f"\n  Markdown file exists      : {'✓' if file_exists else '✗'}")
        print(f"  Header present            : {'✓' if has_header else '✗'}")
        print(f"  Event row present         : {'✓' if has_row else '✗'}")

        passed = file_exists and has_header and has_row
        print(f"\n  {'✓ TEST 2 PASSED' if passed else '✗ TEST 2 FAILED'}")
        return passed


def test_phase7_api_integration():
    print("\n" + "=" * 55)
    print("  TEST 3 — Phase 7 API Integration")
    print("=" * 55)

    import analysis.prediction_logger as logger
    from app import app

    with tempfile.TemporaryDirectory() as tmpdir:
        logger.PREDICTION_LOG_PATH = os.path.join(tmpdir, "prediction_log.json")
        logger.TRACK_RECORD_TABLE_PATH = os.path.join(tmpdir, "track_record_table.md")

        app.testing = True
        client = app.test_client()

        score_res = client.post("/api/score-prediction", json={
            "predicted_probs": {"panic": 75, "cautious": 15, "optimistic": 5, "divided": 5},
            "actual_outcome": "panic",
            "event_id": "api_rbi_case",
            "topic": "API RBI Backtest",
            "event_type": "rbi_rate_hike",
            "event_date": "2022-05-04",
            "domain": "macro",
            "model_version": "v3",
            "phase_config": ["phase1", "phase2", "phase4", "phase3", "phase6_partial", "phase7"],
            "branch_count": 3,
            "agent_count": 5,
            "used_market_roles": True,
            "market_impact": {
                "market_regime": "policy_shock",
                "sector_impacts": {"nbfc": {"direction": "strong_negative"}}
            },
            "actual_sector_moves": {"nbfc": "strong_negative"}
        })

        track_res = client.get("/api/prediction-track-record")

        score_json = score_res.get_json() or {}
        track_json = track_res.get_json() or {}
        score_ok = score_res.status_code == 200 and "track_record_summary" in score_json
        track_ok = track_res.status_code == 200 and track_json.get("total_predictions") == 1

        print(f"\n  Score endpoint status     : {score_res.status_code}")
        print(f"  Track endpoint status     : {track_res.status_code}")
        print(f"  Logged predictions        : {track_json.get('total_predictions')}")

        passed = score_ok and track_ok
        print(f"\n  {'✓ TEST 3 PASSED' if passed else '✗ TEST 3 FAILED'}")
        return passed


def run_all_tests():
    print("\n" + "=" * 55)
    print("  DARSH v3 — PHASE 7 TEST SUITE")
    print("=" * 55)

    results = {}
    for name, func in [
        ("1_logger", test_prediction_logger_and_summary),
        ("2_markdown", test_track_record_markdown_generation),
        ("3_api", test_phase7_api_integration),
    ]:
        try:
            results[name] = func()
        except Exception as e:
            print(f"\n  ✗ {name} ERROR: {e}")
            import traceback
            traceback.print_exc()
            results[name] = False

    print("\n\n" + "=" * 55)
    print("  PHASE 7 RESULTS SUMMARY")
    print("=" * 55)

    all_passed = True
    for name, ok in results.items():
        print(f"  {'✓' if ok else '✗'}  {name}")
        if not ok:
            all_passed = False

    print("\n" + "=" * 55)
    if all_passed:
        print("  ✓  ALL PHASE 7 TESTS PASSED")
        print("  ✓  Prediction logging is persistent")
        print("  ✓  Track record markdown is generated")
        print("  ✓  Calibration summary is exposed through the API")
    else:
        print("  ✗  Some Phase 7 tests failed")
    print("=" * 55)


if __name__ == "__main__":
    run_all_tests()
