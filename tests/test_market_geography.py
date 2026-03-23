# tests/test_market_geography.py
#
# Targeted regression checks for geography-aware market scope.
#
# Run with:
#   .venv/bin/python tests/test_market_geography.py

import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _sample_branch(simulation_id: str) -> dict:
    return {
        "simulation_id": simulation_id,
        "round_summaries": [
            {
                "round": 3,
                "round_results": [
                    {
                        "market_role": "RETAIL_TRADER",
                        "confidence": 0.61,
                        "belief_distribution": {
                            "panic": 0.08,
                            "cautious": 0.22,
                            "optimistic": 0.60,
                            "divided": 0.10,
                        },
                    },
                    {
                        "market_role": "HEDGE_FUND_PM",
                        "confidence": 0.73,
                        "belief_distribution": {
                            "panic": 0.12,
                            "cautious": 0.48,
                            "optimistic": 0.28,
                            "divided": 0.12,
                        },
                    },
                    {
                        "market_role": "FINANCIAL_MEDIA_EDITOR",
                        "confidence": 0.58,
                        "belief_distribution": {
                            "panic": 0.16,
                            "cautious": 0.36,
                            "optimistic": 0.20,
                            "divided": 0.28,
                        },
                    },
                ],
            }
        ],
    }


def test_graph_detection():
    print("\n" + "=" * 55)
    print("  TEST 1 — Geography Detection From Graph")
    print("=" * 55)

    from analysis.market_geography import detect_geography_from_graph

    with tempfile.TemporaryDirectory() as tmpdir:
        graph_path = os.path.join(tmpdir, "fed_graph.json")
        with open(graph_path, "w", encoding="utf-8") as handle:
            json.dump(
                {
                    "nodes": [
                        {"id": "Federal Reserve", "description": "US central bank guides rates"},
                        {"id": "NASDAQ", "description": "US technology-heavy exchange"},
                        {"id": "USD", "description": "US dollar index and treasury moves"},
                    ],
                    "edges": [],
                },
                handle,
            )

        geography = detect_geography_from_graph(graph_path)

    print(f"\n  Detected geography       : {geography}")
    passed = geography == "us"
    print(f"\n  {'✓ TEST 1 PASSED' if passed else '✗ TEST 1 FAILED'}")
    return passed


def test_population_model_detection():
    print("\n" + "=" * 55)
    print("  TEST 2 — Population Model Auto Scope")
    print("=" * 55)

    from analysis.india_market_population import compute_population_weighted_sentiment

    with tempfile.TemporaryDirectory() as tmpdir:
        graph_path = os.path.join(tmpdir, "fed_graph.json")
        with open(graph_path, "w", encoding="utf-8") as handle:
            json.dump(
                {
                    "nodes": [
                        {"id": "Federal Reserve", "description": "US central bank"},
                        {"id": "NYSE", "description": "US equity exchange"},
                    ],
                    "edges": [],
                },
                handle,
            )

        result = compute_population_weighted_sentiment(
            branch_results=[_sample_branch("geo_branch_1")],
            topic="Federal Reserve surprise rate cut and US equity reaction",
            event_type="general",
            graph_path=graph_path,
        )

    geography_ok = result.get("market_geography") == "us"
    represented_ok = result.get("represented_population", 0) > 0
    scope_ok = "US equity market" in result.get("market_scope_description", "")

    print(f"\n  Market geography         : {result.get('market_geography')}")
    print(f"  Scope description        : {result.get('market_scope_description')}")
    print(f"  Represented population   : {result.get('represented_population')}")

    passed = geography_ok and represented_ok and scope_ok
    print(f"\n  {'✓ TEST 2 PASSED' if passed else '✗ TEST 2 FAILED'}")
    return passed


def test_market_impact_schema_switch():
    print("\n" + "=" * 55)
    print("  TEST 3 — Market Impact Schema Switch")
    print("=" * 55)

    import analysis.market_impact_mapper as mim

    original_ask_llm_json = mim.ask_llm_json
    mim.ask_llm_json = lambda prompt, system_prompt=None: {"parse_error": True}

    try:
        result = mim.generate_full_market_impact(
            behavioral_distribution={
                "panic": 62.0,
                "cautious": 24.0,
                "optimistic": 8.0,
                "divided": 6.0,
            },
            event_type="general",
            topic="Federal Reserve signals a sharper path for US rates",
            branch_count=3,
            geography="us",
        )
    finally:
        mim.ask_llm_json = original_ask_llm_json

    sector_impacts = result.get("sector_impacts", {})
    geography_ok = result.get("market_geography") == "us"
    us_schema_ok = "banks" in sector_impacts and "software" in sector_impacts
    india_schema_gone = "nbfc" not in sector_impacts and "banking_private" not in sector_impacts

    print(f"\n  Market geography         : {result.get('market_geography')}")
    print(f"  Sector sample            : {list(sector_impacts.keys())[:5]}")

    passed = geography_ok and us_schema_ok and india_schema_gone
    print(f"\n  {'✓ TEST 3 PASSED' if passed else '✗ TEST 3 FAILED'}")
    return passed


def run_all_tests():
    print("\n" + "=" * 55)
    print("  DARSH — MARKET GEOGRAPHY TESTS")
    print("=" * 55)

    results = {}
    for name, func in [
        ("1_graph_detection", test_graph_detection),
        ("2_population_scope", test_population_model_detection),
        ("3_market_schema", test_market_impact_schema_switch),
    ]:
        try:
            results[name] = func()
        except Exception as e:
            print(f"\n  ✗ {name} ERROR: {e}")
            import traceback
            traceback.print_exc()
            results[name] = False

    print("\n\n" + "=" * 55)
    print("  MARKET GEOGRAPHY SUMMARY")
    print("=" * 55)

    all_passed = True
    for name, ok in results.items():
        print(f"  {'✓' if ok else '✗'}  {name}")
        if not ok:
            all_passed = False

    print("\n" + "=" * 55)
    if all_passed:
        print("  ✓  ALL MARKET GEOGRAPHY TESTS PASSED")
    else:
        print("  ✗  Some market geography tests failed")
    print("=" * 55)


if __name__ == "__main__":
    run_all_tests()
