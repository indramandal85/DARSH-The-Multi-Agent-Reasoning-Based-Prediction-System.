# tests/test_v3_phase1.py
#
# Phase 1 — Pre-Market Behavioral Intelligence foundation tests
#
# Run with:
#   python tests/test_v3_phase1.py

import os
import sqlite3
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_sector_matrix_consistency():
    print("\n" + "=" * 55)
    print("  TEST 1 — Sector Matrix Consistency")
    print("=" * 55)

    from analysis.market_output_schema import INDIA_SECTORS
    from analysis.market_impact_mapper import (
        SECTOR_REPRESENTATIVE_STOCKS,
        load_sector_matrix,
    )

    matrix = load_sector_matrix()
    known = set(INDIA_SECTORS)
    stock_keys = set(SECTOR_REPRESENTATIVE_STOCKS.keys())

    unknown = []
    for event_type, mappings in matrix.get("event_type_mappings", {}).items():
        for sector in mappings:
            if sector not in known:
                unknown.append((event_type, sector))

    has_aviation = "aviation" in known and "aviation" in stock_keys

    print(f"\n  Known sectors in schema  : {len(known)}")
    print(f"  Stock map entries        : {len(stock_keys)}")
    print(f"  Unknown matrix sectors   : {len(unknown)}")
    print(f"  Aviation supported       : {'✓' if has_aviation else '✗'}")

    if unknown:
        for event_type, sector in unknown[:5]:
            print(f"    Unknown: {event_type} -> {sector}")

    passed = not unknown and has_aviation
    print(f"\n  {'✓ TEST 1 PASSED' if passed else '✗ TEST 1 FAILED'}")
    return passed


def test_market_impact_generation():
    print("\n" + "=" * 55)
    print("  TEST 2 — Market Impact Mapper")
    print("=" * 55)

    import analysis.market_impact_mapper as mim

    original_ask_llm_json = mim.ask_llm_json
    mim.ask_llm_json = lambda prompt, system_prompt=None: {"parse_error": True}

    try:
        result = mim.generate_full_market_impact(
            behavioral_distribution={
                "panic": 72.0,
                "cautious": 20.0,
                "optimistic": 5.0,
                "divided": 3.0,
            },
            event_type="rbi_rate_hike",
            topic="RBI emergency off-cycle repo rate hike shocks market",
            branch_count=3,
        )
    finally:
        mim.ask_llm_json = original_ask_llm_json

    total_prob = sum(result.get("behavioral_distribution", {}).values())
    regime_ok = result.get("market_regime") in {"policy_shock", "risk_off"}
    sums_to_one = abs(total_prob - 1.0) < 0.01
    has_watchlists = all(
        key in result for key in
        ["likely_laggards", "likely_resilient", "likely_beneficiaries"]
    )
    nbfc_negative = (
        result.get("sector_impacts", {})
        .get("nbfc", {})
        .get("direction") == "strong_negative"
    )

    print(f"\n  Market regime            : {result.get('market_regime')}")
    print(f"  Probability total        : {total_prob:.4f}")
    print(f"  Sector count             : {len(result.get('sector_impacts', {}))}")
    print(f"  Watchlists present       : {'✓' if has_watchlists else '✗'}")
    print(f"  NBFC mapped correctly    : {'✓' if nbfc_negative else '✗'}")
    print(f"  Normalized to 1.0        : {'✓' if sums_to_one else '✗'}")

    passed = regime_ok and sums_to_one and has_watchlists and nbfc_negative
    print(f"\n  {'✓ TEST 2 PASSED' if passed else '✗ TEST 2 FAILED'}")
    return passed


def test_market_role_schema_migration():
    print("\n" + "=" * 55)
    print("  TEST 3 — SQLite market_role Migration")
    print("=" * 55)

    from simulation.environment import SimulationEnvironment

    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "legacy_sim.db")

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
                thought TEXT,
                action TEXT,
                confidence REAL,
                belief TEXT,
                timestamp TEXT
            )
        """)
        conn.commit()
        conn.close()

        env = SimulationEnvironment(
            simulation_id="phase1_schema_test",
            topic="schema test",
            initial_situation="test",
            agents=[],
            db_path=db_path
        )

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(agent_actions)")
        columns = [row[1] for row in cursor.fetchall()]
        has_market_role = "market_role" in columns

        env.log_action(1, {
            "agent_id": "agent_001",
            "name": "Test Agent",
            "agent_type": "RATIONAL",
            "thought": "Testing schema migration",
            "action": "observe",
            "confidence": 0.5,
            "belief": "Current belief distribution: cautious: 50%, panic: 20%, optimistic: 20%, divided: 10%"
        })

        cursor.execute("SELECT market_role FROM agent_actions LIMIT 1")
        row = cursor.fetchone()
        stored_default = row and row[0] == "RETAIL_TRADER"
        conn.close()

    print(f"\n  market_role column exists : {'✓' if has_market_role else '✗'}")
    print(f"  Default role stored       : {'✓' if stored_default else '✗'}")

    passed = has_market_role and stored_default
    print(f"\n  {'✓ TEST 3 PASSED' if passed else '✗ TEST 3 FAILED'}")
    return passed


def run_all_tests():
    print("\n" + "=" * 55)
    print("  DARSH v3 — PHASE 1 TEST SUITE")
    print("=" * 55)

    results = {}
    for name, func in [
        ("1_sector_matrix", test_sector_matrix_consistency),
        ("2_market_mapper", test_market_impact_generation),
        ("3_market_role_schema", test_market_role_schema_migration),
    ]:
        try:
            results[name] = func()
        except Exception as e:
            print(f"\n  ✗ {name} ERROR: {e}")
            import traceback
            traceback.print_exc()
            results[name] = False

    print("\n\n" + "=" * 55)
    print("  PHASE 1 RESULTS SUMMARY")
    print("=" * 55)

    all_passed = True
    for name, ok in results.items():
        print(f"  {'✓' if ok else '✗'}  {name}")
        if not ok:
            all_passed = False

    print("\n" + "=" * 55)
    if all_passed:
        print("  ✓  ALL PHASE 1 TESTS PASSED")
        print("  ✓  Market output layer working")
        print("  ✓  Sector mapping consistent")
        print("  ✓  SQLite schema prepped for market roles")
    else:
        print("  ✗  Some Phase 1 tests failed")
    print("=" * 55)


if __name__ == "__main__":
    run_all_tests()
