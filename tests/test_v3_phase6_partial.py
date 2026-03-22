# tests/test_v3_phase6_partial.py
#
# Phase 6 partial — interactive analysis tests
#
# Run with:
#   .venv/bin/python tests/test_v3_phase6_partial.py

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


SAMPLE_MARKET_IMPACT = {
    "market_regime": "policy_shock",
    "volatility_expectation": "high",
    "triggers_that_strengthen": [
        "Bond yields move higher with bank-heavy weakness",
        "Broker notes stay hawkish on rate-sensitive sectors",
        "Pre-open cues confirm broad risk-off pricing",
    ],
    "triggers_that_weaken": [
        "RBI communication sounds softer than expected",
        "Global cues reverse sharply into the open",
        "Rate-sensitive sectors recover despite the headline shock",
    ],
    "monitoring_signals": [
        "Gift Nifty direction",
        "USD/INR and bond yield movement",
        "Opening breadth in banking and NBFC names",
    ],
    "second_order_effects": [
        "Funding-cost concerns deepen for rate-sensitive sectors",
        "Defensive sectors may attract relative allocation",
    ],
    "sector_impacts": {
        "banking_private": {
            "sector": "banking_private",
            "direction": "negative",
            "confidence": 0.71,
            "reasoning": "Private banks face funding-cost repricing and a tighter policy narrative.",
            "representative_stocks": ["HDFC Bank", "ICICI Bank", "Axis Bank"],
        },
        "nbfc": {
            "sector": "nbfc",
            "direction": "strong_negative",
            "confidence": 0.82,
            "reasoning": "NBFCs are more exposed to funding-cost pressure under a hawkish policy shock.",
            "representative_stocks": ["Bajaj Finance", "Muthoot Finance"],
        },
    },
}


def test_sector_chat_fallback():
    print("\n" + "=" * 55)
    print("  TEST 1 — Sector Chat Fallback")
    print("=" * 55)

    import simulation.simulation_chat as chat_module

    original_ask_llm = chat_module.ask_llm
    chat_module.ask_llm = lambda prompt, system_prompt=None: (_ for _ in ()).throw(RuntimeError("offline"))

    try:
        result = chat_module.answer_sector_question(
            question="Why is NBFC likely to lag here?",
            sector_key="nbfc",
            market_impact=SAMPLE_MARKET_IMPACT,
            topic="RBI surprise rate hike"
        )
    finally:
        chat_module.ask_llm = original_ask_llm

    answer_ok = "NBFC" in result.get("title", "") and "policy shock" in result.get("answer", "").lower()
    points_ok = len(result.get("supporting_points", [])) >= 2

    print(f"\n  Title returned            : {result.get('title')}")
    print(f"  Supporting points         : {len(result.get('supporting_points', []))}")
    print(f"  Fallback answer valid     : {'✓' if answer_ok else '✗'}")

    passed = answer_ok and points_ok
    print(f"\n  {'✓ TEST 1 PASSED' if passed else '✗ TEST 1 FAILED'}")
    return passed


def test_change_chat_fallback():
    print("\n" + "=" * 55)
    print("  TEST 2 — What Would Change Fallback")
    print("=" * 55)

    import simulation.simulation_chat as chat_module

    original_ask_llm = chat_module.ask_llm
    chat_module.ask_llm = lambda prompt, system_prompt=None: ""

    try:
        result = chat_module.answer_what_would_change(
            question="What would change this view before open?",
            market_impact=SAMPLE_MARKET_IMPACT,
            topic="RBI surprise rate hike"
        )
    finally:
        chat_module.ask_llm = original_ask_llm

    answer_ok = "strengthens" in result.get("answer", "").lower() or "what strengthens" in result.get("answer", "").lower()
    signals_ok = len(result.get("supporting_points", [])) == 3

    print(f"\n  Title returned            : {result.get('title')}")
    print(f"  Monitoring signals        : {len(result.get('supporting_points', []))}")
    print(f"  Fallback answer valid     : {'✓' if answer_ok else '✗'}")

    passed = answer_ok and signals_ok
    print(f"\n  {'✓ TEST 2 PASSED' if passed else '✗ TEST 2 FAILED'}")
    return passed


def test_simulation_chat_api():
    print("\n" + "=" * 55)
    print("  TEST 3 — Simulation Chat API")
    print("=" * 55)

    import simulation.simulation_chat as chat_module
    from app import app

    original_ask_llm = chat_module.ask_llm
    chat_module.ask_llm = lambda prompt, system_prompt=None: "This sector remains under pressure until early signals clearly reverse."

    try:
        app.testing = True
        client = app.test_client()

        sector_res = client.post("/api/simulation-chat", json={
            "mode": "ask_sector",
            "question": "Why is private banking weak here?",
            "sector": "banking_private",
            "topic": "RBI surprise rate hike",
            "market_impact": SAMPLE_MARKET_IMPACT
        })

        change_res = client.post("/api/simulation-chat", json={
            "mode": "what_would_change",
            "question": "What would change this forecast?",
            "topic": "RBI surprise rate hike",
            "market_impact": SAMPLE_MARKET_IMPACT
        })
    finally:
        chat_module.ask_llm = original_ask_llm

    sector_json = sector_res.get_json() or {}
    change_json = change_res.get_json() or {}
    sector_ok = sector_res.status_code == 200 and sector_json.get("mode") == "ask_sector"
    change_ok = change_res.status_code == 200 and change_json.get("mode") == "what_would_change"

    print(f"\n  Sector endpoint status    : {sector_res.status_code}")
    print(f"  Change endpoint status    : {change_res.status_code}")
    print(f"  Sector mode returned      : {sector_json.get('mode')}")
    print(f"  Change mode returned      : {change_json.get('mode')}")

    passed = sector_ok and change_ok
    print(f"\n  {'✓ TEST 3 PASSED' if passed else '✗ TEST 3 FAILED'}")
    return passed


def run_all_tests():
    print("\n" + "=" * 55)
    print("  DARSH v3 — PHASE 6 PARTIAL TEST SUITE")
    print("=" * 55)

    results = {}
    for name, func in [
        ("1_sector_fallback", test_sector_chat_fallback),
        ("2_change_fallback", test_change_chat_fallback),
        ("3_api", test_simulation_chat_api),
    ]:
        try:
            results[name] = func()
        except Exception as e:
            print(f"\n  ✗ {name} ERROR: {e}")
            import traceback
            traceback.print_exc()
            results[name] = False

    print("\n\n" + "=" * 55)
    print("  PHASE 6 PARTIAL RESULTS SUMMARY")
    print("=" * 55)

    all_passed = True
    for name, ok in results.items():
        print(f"  {'✓' if ok else '✗'}  {name}")
        if not ok:
            all_passed = False

    print("\n" + "=" * 55)
    if all_passed:
        print("  ✓  ALL PHASE 6 PARTIAL TESTS PASSED")
        print("  ✓  Sector analysis fallback works")
        print("  ✓  Forecast-change analysis fallback works")
        print("  ✓  Interactive analysis API is ready for the UI")
    else:
        print("  ✗  Some Phase 6 partial tests failed")
    print("=" * 55)


if __name__ == "__main__":
    run_all_tests()
