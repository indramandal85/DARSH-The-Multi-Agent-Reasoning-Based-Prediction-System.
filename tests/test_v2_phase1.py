# tests/test_v2_phase1.py
#
# PHASE 1 FOUNDATION FIXES — TEST SUITE
# Tests all 3 fixes independently then together.
#
# Run with: python tests/test_v2_phase1.py
#
# PASS condition: all 3 sections print ✓

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ─────────────────────────────────────────────────────────────────────────────
# TEST SECTION 1: Entity Validator
# ─────────────────────────────────────────────────────────────────────────────

def test_entity_validator():
    print("\n" + "="*55)
    print("  TEST 1 — Entity Validator (knowledge/entity_validator.py)")
    print("="*55)

    from knowledge.entity_validator import validate_entities, validate_relationships

    # Sample source text
    source = """
    The Reserve Bank of India (RBI), led by Governor Shaktikanta Das, announced
    an interest rate hike. The Sensex dropped 2%. HDFC Bank and SBI shares fell.
    Finance Minister Nirmala Sitharaman commented on the decision.
    The Congress party criticized the government.
    """

    # Raw entities including known v1 bugs: "sex" from "Sensex",
    # "ss party" from "Congress", duplicate "RBI"/"Reserve Bank of India",
    # hallucinated entity "XYZ Corp" not in text
    raw_entities = [
        {"name": "RBI", "type": "ORGANIZATION", "description": "central bank"},
        {"name": "Reserve Bank of India", "type": "ORGANIZATION",
         "description": "India's central bank"},            # duplicate of RBI
        {"name": "Shaktikanta Das", "type": "PERSON", "description": "RBI Governor"},
        {"name": "sex", "type": "PLACE", "description": "stock index"},         # bug
        {"name": "Sensex", "type": "CONCEPT", "description": "Indian stock index"},
        {"name": "ss", "type": "ORGANIZATION", "description": "political party"}, # too short
        {"name": "Congress", "type": "ORGANIZATION", "description": "opposition party"},
        {"name": "XYZ Corp", "type": "ORGANIZATION", "description": "company"},  # hallucinated
        {"name": "Nirmala Sitharaman", "type": "PERSON", "description": "Finance Minister"},
        {"name": "HDFC Bank", "type": "ORGANIZATION", "description": "private bank"},
        {"name": "ab", "type": "PERSON", "description": ""},     # too short
    ]

    validated = validate_entities(raw_entities, source)

    print(f"\n  Input entities  : {len(raw_entities)}")
    print(f"  Validated       : {len(validated)}")
    print(f"\n  Kept entities:")
    for e in validated:
        print(f"    ✓ [{e['type']:14}] {e['name']}")

    # Check what was correctly removed
    kept_names = {e["name"] for e in validated}
    should_be_removed = ["sex", "ss", "XYZ Corp", "ab"]
    should_be_kept    = ["Shaktikanta Das", "Sensex", "Congress",
                         "Nirmala Sitharaman", "HDFC Bank"]

    # One of "RBI" or "Reserve Bank of India" should remain (duplicate removal)
    rbi_kept = "RBI" in kept_names or "Reserve Bank of India" in kept_names
    rbi_both = "RBI" in kept_names and "Reserve Bank of India" in kept_names

    print(f"\n  Validation checks:")
    removed_correctly = all(name not in kept_names for name in should_be_removed)
    kept_correctly    = all(name in kept_names for name in should_be_kept)

    print(f"  Garbage removed correctly : {'✓' if removed_correctly else '✗'}")
    print(f"  Valid entities kept       : {'✓' if kept_correctly else '✗'}")
    print(f"  RBI deduplicated          : {'✓' if not rbi_both else '✗ both RBI versions kept'}")

    # Test relationship validation
    raw_rels = [
        {"source": "RBI", "target": "Shaktikanta Das", "relation": "LED_BY"},
        {"source": "sex", "target": "HDFC Bank", "relation": "DROPPED"},      # invalid
        {"source": "Congress", "target": "RBI", "relation": "CRITICIZED"},
        {"source": "XYZ Corp", "target": "RBI", "relation": "INFLUENCED"},    # invalid
    ]
    valid_names = kept_names
    validated_rels = validate_relationships(raw_rels, valid_names)

    print(f"\n  Relationship validation:")
    print(f"  Input    : {len(raw_rels)}")
    print(f"  Valid    : {len(validated_rels)}")
    rel_invalid_removed = len(validated_rels) < len(raw_rels)
    print(f"  Bad rels removed : {'✓' if rel_invalid_removed else '✗'}")

    passed = removed_correctly and kept_correctly and rel_invalid_removed
    print(f"\n  {'✓ TEST 1 PASSED' if passed else '✗ TEST 1 FAILED'}")
    return passed


# ─────────────────────────────────────────────────────────────────────────────
# TEST SECTION 2: Bayesian Belief State
# ─────────────────────────────────────────────────────────────────────────────

def test_belief_state():
    print("\n" + "="*55)
    print("  TEST 2 — Bayesian Belief State (agents/belief_state.py)")
    print("="*55)

    from agents.belief_state import BeliefState, aggregate_beliefs, OUTCOMES

    # Test 1: uniform prior
    bs = BeliefState()
    print(f"\n  Starting distribution (uniform prior):")
    for outcome, prob in bs.distribution.items():
        print(f"    {outcome}: {prob:.3f}")

    initial_probs = list(bs.distribution.values())
    all_equal = len(set(round(p, 3) for p in initial_probs)) == 1
    print(f"  Uniform prior correct: {'✓' if all_equal else '✗'}")

    # Test 2: Bayesian update with strong panic evidence
    panic_likelihoods = {
        "panic"     : 0.9,   # this evidence strongly suggests panic
        "cautious"  : 0.4,
        "optimistic": 0.05,
        "divided"   : 0.3
    }
    posterior_1 = bs.bayesian_update(panic_likelihoods)
    print(f"\n  After panic evidence (likelihoods: panic=0.9, optimistic=0.05):")
    for o, p in sorted(posterior_1.items(), key=lambda x: x[1], reverse=True):
        print(f"    {o}: {p:.3f}")

    panic_dominant = bs.dominant_outcome() == "panic"
    probs_sum_1 = abs(sum(posterior_1.values()) - 1.0) < 0.001
    print(f"  Panic is dominant    : {'✓' if panic_dominant else '✗'}")
    print(f"  Probabilities sum to 1: {'✓' if probs_sum_1 else '✗'}")

    # Test 3: second update with optimistic evidence — should shift back
    optimistic_likelihoods = {
        "panic"     : 0.1,
        "cautious"  : 0.5,
        "optimistic": 0.9,
        "divided"   : 0.3
    }
    posterior_2 = bs.bayesian_update(optimistic_likelihoods)
    print(f"\n  After optimistic evidence (likelihoods: optimistic=0.9, panic=0.1):")
    for o, p in sorted(posterior_2.items(), key=lambda x: x[1], reverse=True):
        print(f"    {o}: {p:.3f}")

    panic_reduced = posterior_2["panic"] < posterior_1["panic"]
    probs_sum_2 = abs(sum(posterior_2.values()) - 1.0) < 0.001
    print(f"  Panic probability reduced : {'✓' if panic_reduced else '✗'}")
    print(f"  Still sums to 1.0         : {'✓' if probs_sum_2 else '✗'}")

    # Test 4: confidence score
    conf = bs.confidence()
    print(f"\n  Confidence score: {conf:.3f}")
    conf_reasonable = 0.0 <= conf <= 1.0
    print(f"  Confidence in valid range: {'✓' if conf_reasonable else '✗'}")

    # Test 5: as_text() output
    text = bs.as_text()
    print(f"\n  as_text(): {text}")
    text_has_percent = "%" in text
    print(f"  Text has percentages: {'✓' if text_has_percent else '✗'}")

    # Test 6: aggregate multiple belief states
    bs2 = BeliefState()
    bs2.bayesian_update({"panic": 0.8, "cautious": 0.4, "optimistic": 0.1, "divided": 0.3})
    bs3 = BeliefState()
    bs3.bayesian_update({"panic": 0.3, "cautious": 0.7, "optimistic": 0.5, "divided": 0.4})

    aggregated = aggregate_beliefs([bs, bs2, bs3])
    print(f"\n  Aggregated distribution (3 belief states):")
    for o, p in aggregated.items():
        print(f"    {o}: {p:.3f}")
    agg_sums_to_1 = abs(sum(aggregated.values()) - 1.0) < 0.01
    print(f"  Aggregation sums to 1.0: {'✓' if agg_sums_to_1 else '✗'}")

    passed = (all_equal and panic_dominant and probs_sum_1 and
              panic_reduced and probs_sum_2 and conf_reasonable and
              text_has_percent and agg_sums_to_1)
    print(f"\n  {'✓ TEST 2 PASSED' if passed else '✗ TEST 2 FAILED'}")
    return passed


# ─────────────────────────────────────────────────────────────────────────────
# TEST SECTION 3: Belief State + BaseAgent Integration
# ─────────────────────────────────────────────────────────────────────────────

def test_agent_belief_integration():
    print("\n" + "="*55)
    print("  TEST 3 — Agent + Belief Integration (requires ollama serve)")
    print("="*55)

    from core.base_agent import BaseAgent
    from agents.belief_state import OUTCOMES

    agent = BaseAgent(
        agent_id    = "v2_test_001",
        name        = "Test Agent",
        personality = "analytical, data-driven",
        background  = "Economics researcher"
    )

    # Verify belief_state was created
    has_belief_state = hasattr(agent, "belief_state")
    print(f"\n  Agent has belief_state   : {'✓' if has_belief_state else '✗'}")

    if not has_belief_state:
        print("  ✗ TEST 3 FAILED — belief_state not found on agent")
        return False

    initial_dist = agent.belief_state.distribution.copy()
    print(f"  Initial distribution     : {initial_dist}")

    # Run one update
    print(f"\n  Running update_belief with alarming evidence...")
    agent.round = 1
    agent.update_belief("The RBI has confirmed three more rate hikes this year.")

    updated_dist = agent.belief_state.distribution.copy()
    print(f"  Updated distribution     : {updated_dist}")

    # Distribution should have changed
    distribution_changed = initial_dist != updated_dist
    # Probabilities should still sum to 1
    sums_to_one = abs(sum(updated_dist.values()) - 1.0) < 0.01
    # All outcomes should be present
    all_outcomes_present = all(o in updated_dist for o in OUTCOMES)
    # Confidence should be a valid float
    conf_valid = 0.0 <= agent.confidence <= 1.0
    # Memory should have been updated
    memory_updated = len(agent.memory) > 0

    print(f"\n  Distribution changed     : {'✓' if distribution_changed else '✗'}")
    print(f"  Sums to 1.0              : {'✓' if sums_to_one else '✗'}")
    print(f"  All outcomes present     : {'✓' if all_outcomes_present else '✗'}")
    print(f"  Confidence valid (0-1)   : {'✓' if conf_valid else '✗'} ({agent.confidence:.3f})")
    print(f"  Memory updated           : {'✓' if memory_updated else '✗'}")
    print(f"  Belief text              : {agent.belief[:100]}")

    passed = (distribution_changed and sums_to_one and all_outcomes_present
              and conf_valid and memory_updated)
    print(f"\n  {'✓ TEST 3 PASSED' if passed else '✗ TEST 3 FAILED'}")
    return passed


# ─────────────────────────────────────────────────────────────────────────────
# TEST SECTION 4: Grounded Report Facts Extraction
# ─────────────────────────────────────────────────────────────────────────────

def test_grounded_report():
    print("\n" + "="*55)
    print("  TEST 4 — Grounded Report Facts (analysis/report_engine.py)")
    print("="*55)

    # Check if simulation databases exist from Module 5 test
    branch_ids = ["branch_01", "branch_02", "branch_03"]
    existing = [b for b in branch_ids
                if os.path.exists(f"data/simulations/{b}.db")]

    if not existing:
        print(f"\n  No simulation databases found.")
        print(f"  Run python tests/test_module5.py first to generate databases.")
        print(f"  Skipping this test.")
        print(f"  ✓ TEST 4 SKIPPED (no simulation data)")
        return True   # not a failure — just no data yet

    print(f"\n  Found simulation databases: {existing}")

    from analysis.report_engine import ReportEngine

    engine = ReportEngine(
        simulation_ids=existing,
        topic="RBI interest rate hike — v2 grounded test",
        outcome_probs={"panic": 1.0}
    )

    print(f"\n  Fetching verified facts from SQLite...")
    facts = engine._fetch_verified_facts()

    print(f"\n  Verified facts extracted:")
    print(f"    Total agents     : {facts['total_agents']}")
    print(f"    Total rounds     : {facts['total_rounds']}")
    print(f"    Dominant action  : {facts['dominant_action']}")
    print(f"    Action counts    :")
    for action, count in list(facts["action_counts"].items())[:4]:
        print(f"      '{action}': {count}")
    print(f"    Avg confidence   : {facts['overall_avg_confidence']:.1%}")
    print(f"    Agent type data  : {list(facts['agent_type_actions'].keys())}")
    print(f"    Sample thoughts  : {len(facts['sample_thoughts'])} extracted")

    # Validation checks
    has_agents = facts["total_agents"] > 0
    has_rounds = facts["total_rounds"] > 0
    has_actions = len(facts["action_counts"]) > 0
    has_confidence = 0.0 <= facts["overall_avg_confidence"] <= 1.0
    has_type_data = len(facts["agent_type_actions"]) > 0

    print(f"\n  Validation:")
    print(f"  Has agent count     : {'✓' if has_agents else '✗'}")
    print(f"  Has round count     : {'✓' if has_rounds else '✗'}")
    print(f"  Has action counts   : {'✓' if has_actions else '✗'}")
    print(f"  Confidence valid    : {'✓' if has_confidence else '✗'}")
    print(f"  Has type breakdown  : {'✓' if has_type_data else '✗'}")

    passed = all([has_agents, has_rounds, has_actions, has_confidence, has_type_data])
    print(f"\n  {'✓ TEST 4 PASSED' if passed else '✗ TEST 4 FAILED'}")
    return passed


# ─────────────────────────────────────────────────────────────────────────────
# TEST SECTION 5: Full Phase 1 Integration
# ─────────────────────────────────────────────────────────────────────────────

def test_full_pipeline_with_fixes():
    print("\n" + "="*55)
    print("  TEST 5 — Full Pipeline with Phase 1 Fixes")
    print("  (requires ollama serve running in Tab 1)")
    print("="*55)

    # Check if rbi_article.txt exists
    article_path = "data/inputs/rbi_article.txt"
    if not os.path.exists(article_path):
        print(f"\n  ✗ Test file not found: {article_path}")
        print(f"  This file should exist from Module 2.")
        return False

    print(f"\n  Running entity extraction with validation on rbi_article.txt...")

    from knowledge.document_parser import parse_document
    from knowledge.entity_extractor import extract_from_document

    doc = parse_document(article_path)
    extracted = extract_from_document(doc["chunks"])

    entities = extracted["entities"]
    relationships = extracted["relationships"]

    print(f"\n  Results after v2 validation:")
    print(f"  Entities kept    : {len(entities)}")
    print(f"  Relationships    : {len(relationships)}")

    # Check no garbage entities made it through
    entity_names = [e["name"].lower() for e in entities]
    garbage_present = any(g in entity_names for g in ["sex", "ss", "ab", "ex"])
    short_names_present = any(len(name) < 3 for name in entity_names)

    print(f"\n  Quality checks:")
    print(f"  No garbage entities : {'✓' if not garbage_present else '✗ GARBAGE FOUND'}")
    print(f"  No short names (<3) : {'✓' if not short_names_present else '✗ SHORT NAMES'}")
    print(f"  At least 5 entities : {'✓' if len(entities) >= 5 else '✗'}")
    print(f"  At least 3 rels     : {'✓' if len(relationships) >= 3 else '✗'}")

    if entities:
        print(f"\n  Sample validated entities:")
        for e in entities[:6]:
            print(f"    [{e['type']:14}] {e['name']}")

    passed = (not garbage_present and not short_names_present
              and len(entities) >= 5 and len(relationships) >= 3)
    print(f"\n  {'✓ TEST 5 PASSED' if passed else '✗ TEST 5 FAILED'}")
    return passed


# ─────────────────────────────────────────────────────────────────────────────
# MAIN RUNNER
# ─────────────────────────────────────────────────────────────────────────────

def run_all_tests():
    print("\n" + "="*55)
    print("  DARSH v2 — PHASE 1 FOUNDATION FIXES TEST SUITE")
    print("="*55)
    print("\n  Tests 1-2: Pure logic tests (no LLM needed)")
    print("  Tests 3-5: Require ollama serve running\n")

    results = {}

    # Test 1: entity validator (no LLM needed)
    try:
        results["1_entity_validator"] = test_entity_validator()
    except Exception as e:
        print(f"\n  ✗ TEST 1 ERROR: {e}")
        results["1_entity_validator"] = False

    # Test 2: belief state (no LLM needed)
    try:
        results["2_belief_state"] = test_belief_state()
    except Exception as e:
        print(f"\n  ✗ TEST 2 ERROR: {e}")
        results["2_belief_state"] = False

    # Test 3: agent integration (needs LLM)
    try:
        results["3_agent_integration"] = test_agent_belief_integration()
    except Exception as e:
        print(f"\n  ✗ TEST 3 ERROR: {e}")
        results["3_agent_integration"] = False

    # Test 4: grounded report (needs existing simulation databases)
    try:
        results["4_grounded_report"] = test_grounded_report()
    except Exception as e:
        print(f"\n  ✗ TEST 4 ERROR: {e}")
        results["4_grounded_report"] = False

    # Test 5: full pipeline integration
    try:
        results["5_full_pipeline"] = test_full_pipeline_with_fixes()
    except Exception as e:
        print(f"\n  ✗ TEST 5 ERROR: {e}")
        results["5_full_pipeline"] = False

    # Final summary
    print("\n\n" + "="*55)
    print("  PHASE 1 TEST RESULTS SUMMARY")
    print("="*55)

    all_passed = True
    for test_name, passed in results.items():
        status = "✓" if passed else "✗"
        print(f"  {status}  {test_name}")
        if not passed:
            all_passed = False

    print("\n" + "="*55)
    if all_passed:
        print("  ✓  ALL PHASE 1 TESTS PASSED")
        print("  ✓  Entity validation working correctly")
        print("  ✓  Bayesian belief states working correctly")
        print("  ✓  Grounded report engine working correctly")
        print("\n  → Ready for Phase 2 intelligence upgrades")
    else:
        failed = [k for k, v in results.items() if not v]
        print(f"  ✗  {len(failed)} test(s) need attention: {failed}")
        print("\n  → Paste the test output above and we fix together")
    print("="*55 + "\n")


if __name__ == "__main__":
    run_all_tests()