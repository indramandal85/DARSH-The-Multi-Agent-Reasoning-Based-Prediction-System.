# tests/test_v3_phase3.py
#
# Phase 3 — Market role agents tests
#
# Run with:
#   .venv/bin/python tests/test_v3_phase3.py

import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_market_role_registry():
    print("\n" + "=" * 55)
    print("  TEST 1 — Market Role Registry")
    print("=" * 55)

    from agents.market_roles import MARKET_ROLES, ROLE_COGNITION_WEIGHTS

    role_count_ok = len(MARKET_ROLES) == 12
    required_fields_ok = all(
        all(field in role_meta for field in ["label", "background_template", "constraints", "information_sources", "reaction_speed"])
        for role_meta in MARKET_ROLES.values()
    )
    weight_keys_ok = set(MARKET_ROLES.keys()) == set(ROLE_COGNITION_WEIGHTS.keys())

    print(f"\n  Role count                : {len(MARKET_ROLES)}")
    print(f"  All required fields       : {'✓' if required_fields_ok else '✗'}")
    print(f"  Cognition weights aligned : {'✓' if weight_keys_ok else '✗'}")

    passed = role_count_ok and required_fields_ok and weight_keys_ok
    print(f"\n  {'✓ TEST 1 PASSED' if passed else '✗ TEST 1 FAILED'}")
    return passed


def test_market_agent_population():
    print("\n" + "=" * 55)
    print("  TEST 2 — Market Agent Population")
    print("=" * 55)

    from agents.agent_factory import create_agent_population

    population = create_agent_population(
        count=10,
        topic="RBI surprise hike and sector impact",
        event_type="rbi_rate_hike",
        use_semantic_memory=False,
        simulation_id="phase3_population_test"
    )

    roles_present = [getattr(agent, "market_role", "") for agent in population]
    unique_roles = {role for role in roles_present if role}
    unique_types = {getattr(agent, "agent_type", "") for agent in population if getattr(agent, "agent_type", "")}
    role_context_ok = all(
        "Market role:" in getattr(agent, "background", "") and getattr(agent, "reaction_speed", "")
        for agent in population
    )

    print(f"\n  Agents created            : {len(population)}")
    print(f"  Unique market roles       : {len(unique_roles)}")
    print(f"  Unique cognition types    : {len(unique_types)}")
    print(f"  Role context attached     : {'✓' if role_context_ok else '✗'}")

    passed = (
        len(population) == 10 and
        len(unique_roles) >= 6 and
        len(unique_types) >= 4 and
        role_context_ok
    )
    print(f"\n  {'✓ TEST 2 PASSED' if passed else '✗ TEST 2 FAILED'}")
    return passed


def test_runner_and_api_market_role_persistence():
    print("\n" + "=" * 55)
    print("  TEST 3 — Runner and API Market Role Persistence")
    print("=" * 55)

    import simulation.runner as runner_module
    from app import app

    class DummyAgent:
        def __init__(self, idx, role_key):
            self.agent_id = f"phase3_dummy_{idx}"
            self.name = f"Dummy {idx}"
            self.agent_type = "RATIONAL" if idx == 1 else "INSTITUTIONAL"
            self.market_role = role_key

        def run_round(self, world_context, new_information, available_actions, social_feed=""):
            return {
                "agent_id": self.agent_id,
                "name": self.name,
                "thought": f"Role-aware reaction from {self.market_role}.",
                "action": available_actions[0],
                "confidence": 0.67,
                "belief": "Current belief distribution: cautious: 55%, optimistic: 20%, panic: 15%, divided: 10%",
                "belief_distribution": {
                    "cautious": 0.55,
                    "optimistic": 0.20,
                    "panic": 0.15,
                    "divided": 0.10,
                }
            }

    original_factory = runner_module.create_agent_population
    runner_module.create_agent_population = lambda count, topic, event_type="general", use_semantic_memory=True, simulation_id="default": [
        DummyAgent(1, "FII_ANALYST"),
        DummyAgent(2, "REGULATOR_POLICY_DESK"),
    ]

    sim_id = "phase3_role_test"
    db_path = os.path.join("data", "simulations", f"{sim_id}.db")

    try:
        runner_module.run_simulation(
            simulation_id=sim_id,
            topic="RBI surprise hike",
            initial_situation="An RBI policy surprise has hit the market.",
            events_per_round=["Banks react first.", "Institutions publish notes."],
            available_actions=["observe", "hedge"],
            num_agents=2,
            num_rounds=2,
            event_type="rbi_rate_hike",
            verbose=False
        )
    finally:
        runner_module.create_agent_population = original_factory

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT market_role FROM agent_actions ORDER BY market_role")
    stored_roles = [row[0] for row in cursor.fetchall()]
    conn.close()

    app.testing = True
    client = app.test_client()
    api_res = client.get(f"/api/simulations/{sim_id}/round/1")
    api_json = api_res.get_json() or {}
    api_roles = {agent.get("market_role") for agent in api_json.get("agents", [])}

    print(f"\n  Stored roles              : {stored_roles}")
    print(f"  API roles                 : {sorted(role for role in api_roles if role)}")
    print(f"  API status                : {api_res.status_code}")

    if os.path.exists(db_path):
        os.remove(db_path)

    passed = (
        api_res.status_code == 200 and
        "FII_ANALYST" in stored_roles and
        "REGULATOR_POLICY_DESK" in stored_roles and
        "FII_ANALYST" in api_roles and
        "REGULATOR_POLICY_DESK" in api_roles
    )
    print(f"\n  {'✓ TEST 3 PASSED' if passed else '✗ TEST 3 FAILED'}")
    return passed


def run_all_tests():
    print("\n" + "=" * 55)
    print("  DARSH v3 — PHASE 3 TEST SUITE")
    print("=" * 55)

    results = {}
    for name, func in [
        ("1_registry", test_market_role_registry),
        ("2_population", test_market_agent_population),
        ("3_runner_api", test_runner_and_api_market_role_persistence),
    ]:
        try:
            results[name] = func()
        except Exception as e:
            print(f"\n  ✗ {name} ERROR: {e}")
            import traceback
            traceback.print_exc()
            results[name] = False

    print("\n\n" + "=" * 55)
    print("  PHASE 3 RESULTS SUMMARY")
    print("=" * 55)

    all_passed = True
    for name, ok in results.items():
        print(f"  {'✓' if ok else '✗'}  {name}")
        if not ok:
            all_passed = False

    print("\n" + "=" * 55)
    if all_passed:
        print("  ✓  ALL PHASE 3 TESTS PASSED")
        print("  ✓  Market role registry is complete")
        print("  ✓  Agent factory now produces role-aware market participants")
        print("  ✓  Role metadata persists through simulation and API history")
    else:
        print("  ✗  Some Phase 3 tests failed")
    print("=" * 55)


if __name__ == "__main__":
    run_all_tests()
