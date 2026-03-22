# tests/test_v3_phase5.py
#
# Phase 5 — population-weighted market cohort model tests
#
# Run with:
#   .venv/bin/python tests/test_v3_phase5.py

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _sample_branch(simulation_id, retail_outcome="optimistic", fund_outcome="cautious"):
    retail_distribution = {
        "panic": 0.08,
        "cautious": 0.22,
        "optimistic": 0.60 if retail_outcome == "optimistic" else 0.18,
        "divided": 0.10,
    }
    if retail_outcome != "optimistic":
        retail_distribution = {
            "panic": 0.18,
            "cautious": 0.56,
            "optimistic": 0.10,
            "divided": 0.16,
        }

    fund_distribution = {
        "panic": 0.06,
        "cautious": 0.68 if fund_outcome == "cautious" else 0.22,
        "optimistic": 0.16 if fund_outcome == "cautious" else 0.56,
        "divided": 0.10,
    }

    return {
        "simulation_id": simulation_id,
        "final_outcome": "cautious",
        "action_distribution": {"observe": 2, "rebalance": 1},
        "avg_final_confidence": 0.64,
        "round_summaries": [
            {
                "round": 3,
                "round_results": [
                    {
                        "market_role": "RETAIL_TRADER",
                        "confidence": 0.61,
                        "belief_distribution": retail_distribution,
                    },
                    {
                        "market_role": "DOMESTIC_MUTUAL_FUND",
                        "confidence": 0.73,
                        "belief_distribution": fund_distribution,
                    },
                    {
                        "market_role": "FII_ANALYST",
                        "confidence": 0.70,
                        "belief_distribution": {
                            "panic": 0.08,
                            "cautious": 0.64,
                            "optimistic": 0.16,
                            "divided": 0.12,
                        },
                    },
                    {
                        "market_role": "FINANCIAL_MEDIA_EDITOR",
                        "confidence": 0.55,
                        "belief_distribution": {
                            "panic": 0.14,
                            "cautious": 0.46,
                            "optimistic": 0.20,
                            "divided": 0.20,
                        },
                    },
                ],
            }
        ],
    }


def test_population_model_module():
    print("\n" + "=" * 55)
    print("  TEST 1 — Population Model Module")
    print("=" * 55)

    from analysis.india_market_population import compute_population_weighted_sentiment

    result = compute_population_weighted_sentiment(
        branch_results=[
            _sample_branch("phase5_branch_1"),
            _sample_branch("phase5_branch_2", retail_outcome="cautious"),
        ],
        topic="RBI surprise hike impact on Indian sectors",
        event_type="rbi_rate_hike",
    )

    distributions_sum_ok = abs(sum(result["blended_distribution"].values()) - 1.0) < 0.01
    lens_keys_ok = set(result["lens_views"].keys()) == {"participation", "capital", "velocity"}
    cohorts_ok = result["sampled_cohort_count"] >= 4 and len(result["cohort_breakdown"]) >= 4
    takeaways_ok = len(result["summary_takeaways"]) >= 2

    print(f"\n  Dominant population view  : {result['dominant_population_outcome']}")
    print(f"  Blended regime            : {result['blended_market_regime']}")
    print(f"  Represented base          : {result['represented_population']}")
    print(f"  Sampled cohorts           : {result['sampled_cohort_count']}")

    passed = distributions_sum_ok and lens_keys_ok and cohorts_ok and takeaways_ok
    print(f"\n  {'✓ TEST 1 PASSED' if passed else '✗ TEST 1 FAILED'}")
    return passed


def test_parallel_branches_population_integration():
    print("\n" + "=" * 55)
    print("  TEST 2 — Parallel Branch Population Integration")
    print("=" * 55)

    import simulation.parallel_branches as pb

    original_runner = pb.run_single_branch
    original_narratives = pb.get_branch_narratives

    def fake_run_single_branch(config):
        idx = config["simulation_id"].split("_")[-1]
        return _sample_branch(
            simulation_id=config["simulation_id"],
            retail_outcome="optimistic" if idx == "01" else "cautious",
        )

    pb.run_single_branch = fake_run_single_branch
    pb.get_branch_narratives = lambda n: [
        {"branch_id": f"branch_{i+1:02d}", "label": "Base Case", "summary": "Reference scenario"}
        for i in range(n)
    ]

    try:
        results = pb.run_parallel_branches(
            topic="RBI surprise hike",
            initial_situation="The market is digesting a rate shock.",
            events_per_round=["Banks react", "Funds rebalance", "Media amplifies"],
            available_actions=["observe", "rebalance"],
            num_branches=2,
            num_agents=4,
            num_rounds=3,
            event_type="rbi_rate_hike",
        )
    finally:
        pb.run_single_branch = original_runner
        pb.get_branch_narratives = original_narratives

    population_model = results.get("population_model") or {}
    integration_ok = (
        results.get("num_branches") == 2 and
        population_model.get("population_method") == "population_weighted_market_cohort_model" and
        population_model.get("represented_population", 0) > 0
    )

    print(f"\n  Population model present  : {'✓' if population_model else '✗'}")
    print(f"  Represented population    : {population_model.get('represented_population')}")
    print(f"  Blended regime            : {population_model.get('blended_market_regime')}")

    passed = integration_ok
    print(f"\n  {'✓ TEST 2 PASSED' if passed else '✗ TEST 2 FAILED'}")
    return passed


def test_phase5_api_integration():
    print("\n" + "=" * 55)
    print("  TEST 3 — Phase 5 API Integration")
    print("=" * 55)

    from app import app
    import simulation.parallel_branches as pb
    import analysis.report_engine as report_engine
    import analysis.market_impact_mapper as mim

    dummy_results = {
        "topic": "RBI surprise hike",
        "num_branches": 2,
        "event_type": "rbi_rate_hike",
        "branches": [_sample_branch("api_phase5_branch_1"), _sample_branch("api_phase5_branch_2")],
        "outcome_probs": {"panic": 12.0, "cautious": 62.0, "optimistic": 18.0, "divided": 8.0},
        "outcome_std": {"panic": 5.0, "cautious": 12.0, "optimistic": 6.0, "divided": 4.0},
        "outcome_counts": {"cautious": 2},
        "dominant_outcome": "cautious",
        "consensus_action": "observe",
        "overall_confidence": 0.66,
        "prediction": "Weighted branches suggest a cautious market response.",
        "population_model": {
            "population_method": "population_weighted_market_cohort_model",
            "represented_population": 87013200,
            "sampled_agent_count": 8,
            "sampled_cohort_count": 4,
            "coverage_ratio": 0.999,
            "dominant_population_outcome": "cautious",
            "blended_market_regime": "risk_off",
            "blended_regime_confidence": 0.22,
            "lens_views": {
                "participation": {
                    "distribution": {"panic": 0.1, "cautious": 0.56, "optimistic": 0.22, "divided": 0.12},
                    "dominant_outcome": "cautious",
                    "market_regime": "risk_off",
                    "regime_confidence": 0.22,
                },
                "capital": {
                    "distribution": {"panic": 0.08, "cautious": 0.62, "optimistic": 0.20, "divided": 0.10},
                    "dominant_outcome": "cautious",
                    "market_regime": "risk_off",
                    "regime_confidence": 0.30,
                },
                "velocity": {
                    "distribution": {"panic": 0.12, "cautious": 0.48, "optimistic": 0.24, "divided": 0.16},
                    "dominant_outcome": "cautious",
                    "market_regime": "risk_off",
                    "regime_confidence": 0.18,
                },
            },
            "cohort_breakdown": [
                {
                    "role_key": "DOMESTIC_MUTUAL_FUND",
                    "label": "Domestic Mutual Fund Manager",
                    "sampled_agents": 2,
                    "represented_population": 47000000,
                    "dominant_outcome": "cautious",
                }
            ],
            "summary_takeaways": ["Institutional caution is dominating the weighted cohort view."],
        },
        "elapsed_seconds": 1.5,
    }

    class DummyReportEngine:
        def __init__(self, simulation_ids, topic, outcome_probs):
            self.simulation_ids = simulation_ids
            self.topic = topic
            self.outcome_probs = outcome_probs

        def generate_executive_summary(self):
            return "Exec"

        def generate_predicted_outcome(self):
            return "Predicted"

        def generate_causal_drivers(self):
            return "Causal"

        def generate_agent_behavior(self):
            return "Agents"

        def generate_dissenting_views(self):
            return "Dissent"

        def generate_confidence_assessment(self):
            return "Confidence"

        def _assemble_report(self, *sections):
            return "\n".join(sections)

    original_parallel = pb.run_parallel_branches
    original_engine = report_engine.ReportEngine
    original_market_impact = mim.generate_full_market_impact

    pb.run_parallel_branches = lambda **kwargs: dummy_results
    report_engine.ReportEngine = DummyReportEngine
    mim.generate_full_market_impact = lambda **kwargs: {
        "market_regime": "risk_off",
        "regime_confidence": 0.22,
        "sector_impacts": {},
        "volatility_expectation": "moderate",
        "vix_direction": "rising",
        "likely_laggards": [],
        "likely_resilient": [],
        "likely_beneficiaries": [],
        "triggers_that_strengthen": [],
        "triggers_that_weaken": [],
        "monitoring_signals": [],
        "retail_narrative": "",
        "institutional_narrative": "",
        "media_narrative": "",
        "expected_price_discovery_hours": 18,
        "second_order_effects": [],
        "behavioral_distribution": {"panic": 0.12, "cautious": 0.62, "optimistic": 0.18, "divided": 0.08},
        "branch_count": 2,
        "simulation_confidence": 0.62,
        "dominant_outcome": "cautious",
        "event_type": "rbi_rate_hike",
    }

    app.testing = True
    client = app.test_client()

    try:
        start_res = client.post("/api/run-simulation", json={
            "topic": "RBI surprise hike",
            "situation": "The market is digesting the policy shock.",
            "event_type": "rbi_rate_hike",
            "events": ["Banks react", "Funds publish notes", "Media amplifies"],
            "actions": ["observe", "rebalance"],
            "num_agents": 4,
            "num_branches": 2,
            "num_rounds": 3,
        })
        job_id = (start_res.get_json() or {}).get("job_id")

        status_json = {}
        for _ in range(60):
            time.sleep(0.05)
            status_res = client.get(f"/api/status/{job_id}")
            status_json = status_res.get_json() or {}
            if status_json.get("status") in {"complete", "error"}:
                break
    finally:
        pb.run_parallel_branches = original_parallel
        report_engine.ReportEngine = original_engine
        mim.generate_full_market_impact = original_market_impact

    population_model = status_json.get("population_model") or {}
    api_ok = (
        status_json.get("status") == "complete" and
        population_model.get("population_method") == "population_weighted_market_cohort_model" and
        population_model.get("blended_market_regime") == "risk_off"
    )

    print(f"\n  Job completed             : {status_json.get('status')}")
    print(f"  Population model present  : {'✓' if population_model else '✗'}")
    print(f"  Blended regime            : {population_model.get('blended_market_regime')}")

    passed = api_ok
    print(f"\n  {'✓ TEST 3 PASSED' if passed else '✗ TEST 3 FAILED'}")
    return passed


def run_all_tests():
    print("\n" + "=" * 55)
    print("  DARSH v3 — PHASE 5 TEST SUITE")
    print("=" * 55)

    results = {}
    for name, func in [
        ("1_population_module", test_population_model_module),
        ("2_parallel_integration", test_parallel_branches_population_integration),
        ("3_api", test_phase5_api_integration),
    ]:
        try:
            results[name] = func()
        except Exception as e:
            print(f"\n  ✗ {name} ERROR: {e}")
            import traceback
            traceback.print_exc()
            results[name] = False

    print("\n\n" + "=" * 55)
    print("  PHASE 5 RESULTS SUMMARY")
    print("=" * 55)

    all_passed = True
    for name, ok in results.items():
        print(f"  {'✓' if ok else '✗'}  {name}")
        if not ok:
            all_passed = False

    print("\n" + "=" * 55)
    if all_passed:
        print("  ✓  ALL PHASE 5 TESTS PASSED")
        print("  ✓  Population-weighted cohort math is active")
        print("  ✓  Branch aggregation exposes the Phase 5 layer")
        print("  ✓  API responses now include the weighted population model")
    else:
        print("  ✗  Some Phase 5 tests failed")
    print("=" * 55)


if __name__ == "__main__":
    run_all_tests()
