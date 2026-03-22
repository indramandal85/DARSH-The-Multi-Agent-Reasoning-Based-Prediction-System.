# tests/test_v3_phase6_full.py
#
# Phase 6 full — cohort and counterfactual interaction tests
#
# Run with:
#   .venv/bin/python tests/test_v3_phase6_full.py

import json
import os
import sqlite3
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


SAMPLE_MARKET_IMPACT = {
    "market_regime": "policy_shock",
    "triggers_that_strengthen": [
        "Bond yields stay elevated",
        "Banking and NBFC weakness persists",
        "Broker notes remain hawkish"
    ],
    "triggers_that_weaken": [
        "RBI softens its communication",
        "Global cues reverse",
        "Rate-sensitive sectors recover quickly"
    ],
    "monitoring_signals": [
        "Gift Nifty direction",
        "USD/INR move",
        "Banking breadth at the open"
    ],
    "second_order_effects": [
        "Borrowing-sensitive sectors face earnings pressure",
        "Defensives could attract relative flows"
    ],
    "sector_impacts": {
        "nbfc": {
            "sector": "nbfc",
            "direction": "strong_negative",
            "confidence": 0.82,
            "reasoning": "NBFCs face higher funding-cost pressure under a hawkish rate shock.",
            "representative_stocks": ["Bajaj Finance", "Muthoot Finance"]
        }
    }
}


def _create_test_sim_db(sim_id: str):
    os.makedirs("data/simulations", exist_ok=True)
    db_path = os.path.join("data", "simulations", f"{sim_id}.db")
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE agent_actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            simulation_id TEXT,
            round_number INTEGER,
            agent_id TEXT,
            agent_name TEXT,
            agent_type TEXT,
            market_role TEXT,
            thought TEXT,
            action TEXT,
            confidence REAL,
            belief TEXT,
            timestamp TEXT
        )
    """)
    cursor.executemany("""
        INSERT INTO agent_actions
        (simulation_id, round_number, agent_id, agent_name, agent_type, market_role, thought, action, confidence, belief, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (sim_id, 2, "a1", "Fund Analyst 1", "RATIONAL", "FII_ANALYST", "We are focused on rates and currency spillover.", "reduce rate-sensitive exposure", 0.72, "belief", "2026-03-19T09:00:00"),
        (sim_id, 2, "a2", "Fund Analyst 2", "CONTRARIAN", "FII_ANALYST", "The street may still be underpricing second-order pressure.", "hedge cyclical exposure", 0.68, "belief", "2026-03-19T09:00:00"),
    ])
    conn.commit()
    conn.close()
    return db_path


def test_cohort_chat_fallback_and_loader():
    print("\n" + "=" * 55)
    print("  TEST 1 — Cohort Chat Loader")
    print("=" * 55)

    import simulation.simulation_chat as chat_module

    sim_id = "phase6_full_cohort_test"
    db_path = _create_test_sim_db(sim_id)
    original_ask_llm = chat_module.ask_llm
    chat_module.ask_llm = lambda prompt, system_prompt=None: ""

    try:
        result = chat_module.answer_cohort_question(
            question="How are FIIs reacting?",
            cohort_key="FII_ANALYST",
            simulation_ids=[sim_id],
            market_impact=SAMPLE_MARKET_IMPACT,
            topic="RBI surprise rate hike"
        )
    finally:
        chat_module.ask_llm = original_ask_llm

    sample_ok = result.get("sample_size") == 2
    title_ok = "FII Analyst" in result.get("title", "")
    points_ok = len(result.get("supporting_points", [])) >= 2

    print(f"\n  Cohort sample size        : {result.get('sample_size')}")
    print(f"  Title returned            : {result.get('title')}")
    print(f"  Supporting points         : {len(result.get('supporting_points', []))}")

    if os.path.exists(db_path):
        os.remove(db_path)

    passed = sample_ok and title_ok and points_ok
    print(f"\n  {'✓ TEST 1 PASSED' if passed else '✗ TEST 1 FAILED'}")
    return passed


def test_counterfactual_uses_causal_dag():
    print("\n" + "=" * 55)
    print("  TEST 2 — Counterfactual Uses DAG")
    print("=" * 55)

    import simulation.simulation_chat as chat_module
    import causal.counterfactual as cf_module

    with tempfile.TemporaryDirectory() as tmpdir:
        causal_path = os.path.join(tmpdir, "test_causal.json")
        with open(causal_path, "w", encoding="utf-8") as f:
            json.dump({
                "nodes": [
                    {"id": "RBI", "type": "ORG", "description": "Reserve Bank of India"},
                    {"id": "NBFC", "type": "SECTOR", "description": "Non-bank financial companies"}
                ],
                "causal_edges": [
                    {"cause": "RBI", "effect": "NBFC", "strength": 0.8, "time_lag": "days", "explanation": "Rates affect NBFC funding", "causal_type": "A_CAUSES_B"}
                ]
            }, f, indent=2)

        original_cf_ask = cf_module.ask_llm
        cf_module.ask_llm = lambda prompt: "Without RBI tightening, NBFC funding pressure would likely be lower. Confidence: HIGH"

        try:
            result = chat_module.answer_counterfactual_question(
                question="What if RBI had not tightened?",
                market_impact=SAMPLE_MARKET_IMPACT,
                topic="RBI surprise rate hike",
                causal_dag_path=causal_path,
                counterfactual_target="RBI"
            )
        finally:
            cf_module.ask_llm = original_cf_ask

    dag_ok = result.get("used_causal_dag") is True
    title_ok = "RBI Removed" in result.get("title", "")
    answer_ok = "NBFC" in result.get("answer", "") or "funding pressure" in result.get("answer", "").lower()

    print(f"\n  Used causal DAG           : {result.get('used_causal_dag')}")
    print(f"  Title returned            : {result.get('title')}")
    print(f"  Answer preview            : {result.get('answer', '')[:80]}")

    passed = dag_ok and title_ok and answer_ok
    print(f"\n  {'✓ TEST 2 PASSED' if passed else '✗ TEST 2 FAILED'}")
    return passed


def test_phase6_full_api_modes():
    print("\n" + "=" * 55)
    print("  TEST 3 — Phase 6 Full API Modes")
    print("=" * 55)

    import simulation.simulation_chat as chat_module
    import causal.counterfactual as cf_module
    from app import app

    sim_id = "phase6_full_api_test"
    db_path = _create_test_sim_db(sim_id)

    with tempfile.TemporaryDirectory() as tmpdir:
        causal_path = os.path.join(tmpdir, "api_causal.json")
        with open(causal_path, "w", encoding="utf-8") as f:
            json.dump({
                "nodes": [{"id": "RBI"}, {"id": "NBFC"}],
                "causal_edges": [{"cause": "RBI", "effect": "NBFC", "strength": 0.8, "time_lag": "days"}]
            }, f)

        original_chat_ask = chat_module.ask_llm
        original_cf_ask = cf_module.ask_llm
        chat_module.ask_llm = lambda prompt, system_prompt=None: "This cohort is focused on rates, flows, and confirmation signals."
        cf_module.ask_llm = lambda prompt: "Without RBI tightening, downstream funding pressure would likely be lower."

        try:
            app.testing = True
            client = app.test_client()

            cohort_res = client.post("/api/simulation-chat", json={
                "mode": "ask_cohort",
                "question": "How are FIIs reacting?",
                "cohort": "FII_ANALYST",
                "simulation_ids": [sim_id],
                "topic": "RBI surprise rate hike",
                "market_impact": SAMPLE_MARKET_IMPACT
            })

            cf_res = client.post("/api/simulation-chat", json={
                "mode": "counterfactual",
                "question": "What if RBI had not tightened?",
                "counterfactual_target": "RBI",
                "causal_dag_path": causal_path,
                "topic": "RBI surprise rate hike",
                "market_impact": SAMPLE_MARKET_IMPACT
            })
        finally:
            chat_module.ask_llm = original_chat_ask
            cf_module.ask_llm = original_cf_ask

    cohort_json = cohort_res.get_json() or {}
    cf_json = cf_res.get_json() or {}
    cohort_ok = cohort_res.status_code == 200 and cohort_json.get("mode") == "ask_cohort"
    cf_ok = cf_res.status_code == 200 and cf_json.get("mode") == "counterfactual"

    print(f"\n  Cohort endpoint status    : {cohort_res.status_code}")
    print(f"  Counterfactual status     : {cf_res.status_code}")
    print(f"  Cohort title              : {cohort_json.get('title')}")
    print(f"  Counterfactual title      : {cf_json.get('title')}")

    if os.path.exists(db_path):
        os.remove(db_path)

    passed = cohort_ok and cf_ok
    print(f"\n  {'✓ TEST 3 PASSED' if passed else '✗ TEST 3 FAILED'}")
    return passed


def run_all_tests():
    print("\n" + "=" * 55)
    print("  DARSH v3 — PHASE 6 FULL TEST SUITE")
    print("=" * 55)

    results = {}
    for name, func in [
        ("1_cohort", test_cohort_chat_fallback_and_loader),
        ("2_counterfactual", test_counterfactual_uses_causal_dag),
        ("3_api", test_phase6_full_api_modes),
    ]:
        try:
            results[name] = func()
        except Exception as e:
            print(f"\n  ✗ {name} ERROR: {e}")
            import traceback
            traceback.print_exc()
            results[name] = False

    print("\n\n" + "=" * 55)
    print("  PHASE 6 FULL RESULTS SUMMARY")
    print("=" * 55)

    all_passed = True
    for name, ok in results.items():
        print(f"  {'✓' if ok else '✗'}  {name}")
        if not ok:
            all_passed = False

    print("\n" + "=" * 55)
    if all_passed:
        print("  ✓  ALL PHASE 6 FULL TESTS PASSED")
        print("  ✓  Cohort analysis works from persisted market-role data")
        print("  ✓  Counterfactual mode uses causal DAG when available")
        print("  ✓  Full interactive API modes are ready for the UI")
    else:
        print("  ✗  Some Phase 6 full tests failed")
    print("=" * 55)


if __name__ == "__main__":
    run_all_tests()
