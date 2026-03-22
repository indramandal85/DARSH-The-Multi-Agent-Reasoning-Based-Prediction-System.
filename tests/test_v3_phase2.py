# tests/test_v3_phase2.py
#
# Phase 2 — Market ontology, event templates, and render flow tests
#
# Run with:
#   .venv/bin/python tests/test_v3_phase2.py

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_ontology_and_template_registry():
    print("\n" + "=" * 55)
    print("  TEST 1 — Ontology and Template Registry")
    print("=" * 55)

    from market.template_renderer import load_market_ontology, list_event_templates

    ontology = load_market_ontology()
    templates = list_event_templates()

    event_classes = set(ontology.get("event_classes", {}).keys())
    template_ids = {template["template_id"] for template in templates}

    required_classes = {"monetary_policy", "fiscal_policy", "global_shock"}
    required_templates = {"rbi_rate_hike", "union_budget_expansion", "oil_price_spike"}

    classes_ok = required_classes.issubset(event_classes)
    templates_ok = required_templates.issubset(template_ids)

    print(f"\n  Event classes found       : {sorted(event_classes)}")
    print(f"  Template ids found        : {sorted(template_ids)}")
    print(f"  Core classes present      : {'✓' if classes_ok else '✗'}")
    print(f"  Core templates present    : {'✓' if templates_ok else '✗'}")

    passed = classes_ok and templates_ok
    print(f"\n  {'✓ TEST 1 PASSED' if passed else '✗ TEST 1 FAILED'}")
    return passed


def test_template_render_derivations():
    print("\n" + "=" * 55)
    print("  TEST 2 — Template Render Derivations")
    print("=" * 55)

    from market.template_renderer import render_event_template

    rendered = render_event_template("rbi_rate_hike", {
        "hike_magnitude_bps": 40,
        "current_repo_rate_percent": 6.5,
        "was_off_cycle": True,
        "current_inflation_percent": 6.8,
        "sensex_immediate_move": -1200,
        "market_consensus_expected": False,
    })

    new_rate_ok = rendered["derived_inputs"].get("new_rate") == 6.9
    event_type_ok = rendered.get("event_type") == "rbi_rate_hike"
    topic_ok = "RBI Rate Hike" in rendered.get("topic", "")
    round_events_ok = all("{" not in event for event in rendered.get("round_events", []))
    situation_ok = "6.9%" in rendered.get("situation", "") and "off-cycle" in rendered.get("situation", "")

    print(f"\n  Derived new rate          : {rendered['derived_inputs'].get('new_rate')}")
    print(f"  Event type                : {rendered.get('event_type')}")
    print(f"  Round events formatted    : {'✓' if round_events_ok else '✗'}")
    print(f"  Situation rendered        : {'✓' if situation_ok else '✗'}")

    passed = all([new_rate_ok, event_type_ok, topic_ok, round_events_ok, situation_ok])
    print(f"\n  {'✓ TEST 2 PASSED' if passed else '✗ TEST 2 FAILED'}")
    return passed


def test_template_api_endpoints():
    print("\n" + "=" * 55)
    print("  TEST 3 — Template API Endpoints")
    print("=" * 55)

    from app import app

    app.testing = True
    client = app.test_client()

    list_res = client.get("/api/event-templates")
    detail_res = client.get("/api/event-templates/rbi_rate_hike")
    render_res = client.post("/api/event-templates/render", json={
        "template_id": "oil_price_spike",
        "inputs": {
            "brent_price_usd": 99,
            "one_day_spike_percent": 8.1,
            "usd_inr_level": 83.4,
            "shipping_disruption": True,
            "opec_supply_signal": True,
        }
    })

    list_ok = list_res.status_code == 200 and (list_res.get_json() or {}).get("count", 0) >= 3
    detail_json = detail_res.get_json() or {}
    detail_ok = detail_res.status_code == 200 and detail_json.get("template_id") == "rbi_rate_hike"
    render_json = render_res.get_json() or {}
    render_ok = (
        render_res.status_code == 200 and
        render_json.get("event_type") == "oil_price_spike" and
        len(render_json.get("round_events", [])) == 3
    )

    print(f"\n  List endpoint             : {list_res.status_code}")
    print(f"  Detail endpoint           : {detail_res.status_code}")
    print(f"  Render endpoint           : {render_res.status_code}")
    print(f"  Returned template count   : {(list_res.get_json() or {}).get('count', 0)}")
    print(f"  Rendered event type       : {render_json.get('event_type')}")

    passed = list_ok and detail_ok and render_ok
    print(f"\n  {'✓ TEST 3 PASSED' if passed else '✗ TEST 3 FAILED'}")
    return passed


def run_all_tests():
    print("\n" + "=" * 55)
    print("  DARSH v3 — PHASE 2 TEST SUITE")
    print("=" * 55)

    results = {}
    for name, func in [
        ("1_registry", test_ontology_and_template_registry),
        ("2_renderer", test_template_render_derivations),
        ("3_api", test_template_api_endpoints),
    ]:
        try:
            results[name] = func()
        except Exception as e:
            print(f"\n  ✗ {name} ERROR: {e}")
            import traceback
            traceback.print_exc()
            results[name] = False

    print("\n\n" + "=" * 55)
    print("  PHASE 2 RESULTS SUMMARY")
    print("=" * 55)

    all_passed = True
    for name, ok in results.items():
        print(f"  {'✓' if ok else '✗'}  {name}")
        if not ok:
            all_passed = False

    print("\n" + "=" * 55)
    if all_passed:
        print("  ✓  ALL PHASE 2 TESTS PASSED")
        print("  ✓  Ontology and templates load correctly")
        print("  ✓  Template derivation and rendering works")
        print("  ✓  Template API flow is ready for the frontend")
    else:
        print("  ✗  Some Phase 2 tests failed")
    print("=" * 55)


if __name__ == "__main__":
    run_all_tests()
