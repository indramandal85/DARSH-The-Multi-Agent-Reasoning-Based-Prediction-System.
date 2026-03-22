# tests/test_v3_phase4.py
#
# Phase 4 — Structured market rounds tests
#
# Run with:
#   .venv/bin/python tests/test_v3_phase4.py

import os
import sqlite3
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_market_timeline_module():
    print("\n" + "=" * 55)
    print("  TEST 1 — Market Timeline Module")
    print("=" * 55)

    from simulation.market_timeline import build_market_timeline, get_branch_narratives

    timeline = build_market_timeline(
        num_rounds=5,
        events_per_round=["Headline hits", "Funds react", "Media amplifies", "Rotation begins", "Policy clarifies"],
        topic="RBI surprise hike",
        event_type="rbi_rate_hike",
    )
    narratives = get_branch_narratives(5)

    labels = [round_info["label"] for round_info in timeline]
    label_ok = labels[:3] == [
        "Headline Shock",
        "Institutional Interpretation",
        "Social and Media Amplification",
    ]
    context_ok = all("Scenario type" in round_info["context_prompt"] for round_info in timeline)
    narratives_ok = len(narratives) == 5 and len({item["branch_id"] for item in narratives}) == 5

    print(f"\n  Timeline labels           : {labels}")
    print(f"  Narrative ids            : {[item['branch_id'] for item in narratives]}")
    print(f"  Round labels correct     : {'✓' if label_ok else '✗'}")
    print(f"  Context prompts ready    : {'✓' if context_ok else '✗'}")
    print(f"  Five branch narratives   : {'✓' if narratives_ok else '✗'}")

    passed = label_ok and context_ok and narratives_ok
    print(f"\n  {'✓ TEST 1 PASSED' if passed else '✗ TEST 1 FAILED'}")
    return passed


def test_world_state_schema_and_round_metadata():
    print("\n" + "=" * 55)
    print("  TEST 2 — World State Schema Migration")
    print("=" * 55)

    from simulation.environment import SimulationEnvironment

    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "legacy_world_states.db")

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE world_states (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                simulation_id TEXT,
                round_number INTEGER,
                world_state TEXT,
                dominant_action TEXT,
                avg_confidence REAL,
                timestamp TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE agent_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                simulation_id TEXT,
                round_number INTEGER,
                agent_id TEXT,
                agent_name TEXT,
                agent_type TEXT,
                thought TEXT,
                action TEXT,
                confidence REAL,
                belief TEXT,
                timestamp TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE outcomes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                simulation_id TEXT,
                outcome_type TEXT,
                description TEXT,
                confidence REAL,
                supporting_agents INTEGER,
                timestamp TEXT
            )
        """)
        conn.commit()
        conn.close()

        env = SimulationEnvironment(
            simulation_id="phase4_schema_test",
            topic="schema test",
            initial_situation="Initial market state.",
            agents=[],
            db_path=db_path
        )

        env.update_world_state(
            round_results=[],
            new_event="Analysts react to the policy move.",
            round_context={
                "label": "Headline Shock",
                "time_window": "0-2 hours",
                "focus": "Immediate reaction",
            }
        )

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(world_states)")
        columns = {row[1] for row in cursor.fetchall()}
        cursor.execute("""
            SELECT round_label, time_window
            FROM world_states
            WHERE round_number = 1
        """)
        row = cursor.fetchone()
        conn.close()

    labels_ok = {"round_label", "time_window"}.issubset(columns)
    stored_ok = row == ("Headline Shock", "0-2 hours")

    print(f"\n  New columns present      : {'✓' if labels_ok else '✗'}")
    print(f"  Stored round metadata    : {'✓' if stored_ok else '✗'}")

    passed = labels_ok and stored_ok
    print(f"\n  {'✓ TEST 2 PASSED' if passed else '✗ TEST 2 FAILED'}")
    return passed


def test_runner_and_api_round_labels():
    print("\n" + "=" * 55)
    print("  TEST 3 — Runner and API Round Labels")
    print("=" * 55)

    import simulation.runner as runner_module
    from app import app

    class DummyAgent:
        def __init__(self, idx):
            self.agent_id = f"dummy_{idx}"
            self.name = f"Dummy {idx}"
            self.agent_type = "RATIONAL"
            self.market_role = "RETAIL_TRADER"

        def run_round(self, world_context, new_information, available_actions, social_feed=""):
            return {
                "agent_id": self.agent_id,
                "name": self.name,
                "thought": f"Tracking stage context. {world_context[:70]}",
                "action": available_actions[0],
                "confidence": 0.62,
                "belief": "Current belief distribution: cautious: 55%, optimistic: 25%, panic: 15%, divided: 5%",
                "belief_distribution": {
                    "cautious": 0.55,
                    "optimistic": 0.25,
                    "panic": 0.15,
                    "divided": 0.05,
                }
            }

    original_factory = runner_module.create_agent_population
    runner_module.create_agent_population = lambda count, topic, event_type="general", use_semantic_memory=True, simulation_id="default": [
        DummyAgent(i + 1) for i in range(count)
    ]

    sim_id = "phase4_runner_test"
    db_path = os.path.join("data", "simulations", f"{sim_id}.db")

    try:
        result = runner_module.run_simulation(
            simulation_id=sim_id,
            topic="RBI surprise hike",
            initial_situation="The market is digesting an RBI surprise rate hike.",
            events_per_round=[
                "Banks and NBFCs move first.",
                "Fund managers publish sector notes.",
                "Financial media amplifies the debate.",
            ],
            available_actions=["observe", "rebalance"],
            num_agents=2,
            num_rounds=3,
            event_type="rbi_rate_hike",
            verbose=False
        )
    finally:
        runner_module.create_agent_population = original_factory

    round_label_ok = result["round_summaries"][0]["round_label"] == "Headline Shock"
    timeline_ok = result["market_timeline"][1]["label"] == "Institutional Interpretation"

    app.testing = True
    client = app.test_client()
    api_res = client.get(f"/api/simulations/{sim_id}/round/1")
    api_json = api_res.get_json() or {}
    api_ok = (
        api_res.status_code == 200 and
        (api_json.get("world_state") or {}).get("round_label") == "Headline Shock"
    )

    print(f"\n  Runner round label       : {result['round_summaries'][0]['round_label']}")
    print(f"  Timeline second stage    : {result['market_timeline'][1]['label']}")
    print(f"  API round label exposed  : {'✓' if api_ok else '✗'}")

    if os.path.exists(db_path):
        os.remove(db_path)

    passed = round_label_ok and timeline_ok and api_ok
    print(f"\n  {'✓ TEST 3 PASSED' if passed else '✗ TEST 3 FAILED'}")
    return passed


def run_all_tests():
    print("\n" + "=" * 55)
    print("  DARSH v3 — PHASE 4 TEST SUITE")
    print("=" * 55)

    results = {}
    for name, func in [
        ("1_timeline", test_market_timeline_module),
        ("2_schema", test_world_state_schema_and_round_metadata),
        ("3_runner_api", test_runner_and_api_round_labels),
    ]:
        try:
            results[name] = func()
        except Exception as e:
            print(f"\n  ✗ {name} ERROR: {e}")
            import traceback
            traceback.print_exc()
            results[name] = False

    print("\n\n" + "=" * 55)
    print("  PHASE 4 RESULTS SUMMARY")
    print("=" * 55)

    all_passed = True
    for name, ok in results.items():
        print(f"  {'✓' if ok else '✗'}  {name}")
        if not ok:
            all_passed = False

    print("\n" + "=" * 55)
    if all_passed:
        print("  ✓  ALL PHASE 4 TESTS PASSED")
        print("  ✓  Structured market rounds are active")
        print("  ✓  Round metadata is persisted and queryable")
        print("  ✓  API exposes the new timeline labels cleanly")
    else:
        print("  ✗  Some Phase 4 tests failed")
    print("=" * 55)


if __name__ == "__main__":
    run_all_tests()
