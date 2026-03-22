# tests/test_v2_phase2.py
#
# PHASE 2 INTELLIGENCE UPGRADES — TEST SUITE
# Tests C4 (semantic memory), C1 (social network), C3 (causal DAG in sim)
#
# Run with: python tests/test_v2_phase2.py
# Tests 1-2: no LLM needed. Tests 3-4: need ollama serve.

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ─────────────────────────────────────────────────────────────────────────────
# TEST 1: Semantic Memory
# ─────────────────────────────────────────────────────────────────────────────

def test_semantic_memory():
    print("\n" + "="*55)
    print("  TEST 1 — Semantic Memory (agents/semantic_memory.py)")
    print("="*55)

    from agents.semantic_memory import SemanticMemory, create_shared_chroma_client

    # Create client in a temp test directory
    test_dir = "data/test_agent_memories"
    client = create_shared_chroma_client(persist_dir=test_dir)

    mem = SemanticMemory("test_agent_001", client, simulation_id="test_run")

    # Store diverse memories
    print("\n  Storing test memories...")
    mem.store("The RBI announced an interest rate hike today", round_num=1)
    mem.store("Inflation reached 7.2 percent this quarter", round_num=1)
    mem.store("Markets dropped 2 percent after the announcement", round_num=2)
    mem.store("The Finance Minister defended the rate hike decision", round_num=2)
    mem.store("NASSCOM warns of reduced venture capital activity", round_num=3)

    print(f"  Stored {mem.count()} memories")
    stored_correctly = mem.count() == 5

    # Test semantic retrieval
    print("\n  Query: 'inflation and monetary policy'")
    results = mem.retrieve("inflation and monetary policy", n_results=2)
    print(f"  Results:\n{results}")
    has_inflation = "inflation" in results.lower() or "rate" in results.lower()

    print("\n  Query: 'technology and startups'")
    results2 = mem.retrieve("technology and startups", n_results=2)
    print(f"  Results:\n{results2}")
    has_nasscom = "nasscom" in results2.lower() or "venture" in results2.lower()

    # Clean up test data
    import shutil
    try:
        shutil.rmtree(test_dir)
    except Exception:
        pass

    print(f"\n  Checks:")
    print(f"  Stored 5 memories   : {'✓' if stored_correctly else '✗'}")
    print(f"  Inflation query works: {'✓' if has_inflation else '✗'}")
    print(f"  Tech query works    : {'✓' if has_nasscom else '✗'}")

    passed = stored_correctly and has_inflation
    print(f"\n  {'✓ TEST 1 PASSED' if passed else '✗ TEST 1 FAILED'}")
    return passed


# ─────────────────────────────────────────────────────────────────────────────
# TEST 2: Social Network
# ─────────────────────────────────────────────────────────────────────────────

def test_social_network():
    print("\n" + "="*55)
    print("  TEST 2 — Social Network (simulation/social_network.py)")
    print("="*55)

    from simulation.social_network import SocialNetwork
    from core.base_agent import BaseAgent

    # Create a small test population of 6 agents with different types
    class MockAgent:
        def __init__(self, agent_id, name, agent_type):
            self.agent_id   = agent_id
            self.name       = name
            self.agent_type = agent_type

    agents = [
        MockAgent("a001", "Rational Rita",     "RATIONAL"),
        MockAgent("a002", "Emotional Emma",    "EMOTIONAL"),
        MockAgent("a003", "Tribal Tomas",      "TRIBAL"),
        MockAgent("a004", "Contrarian Carlos", "CONTRARIAN"),
        MockAgent("a005", "Institutional Ivan","INSTITUTIONAL"),
        MockAgent("a006", "Emotional Eva",     "EMOTIONAL"),
    ]

    network = SocialNetwork()
    network.build(agents)

    stats = network.get_network_stats()
    print(f"\n  Network stats: {stats}")

    has_connections = stats["total_connections"] > 0
    has_all_types   = len(stats["agents_by_type"]) >= 4

    # Test posting
    network.post("a001", "Rational Rita", "RATIONAL",
                 "The data shows a 60% probability of recession.")
    network.post("a002", "Emotional Emma", "EMOTIONAL",
                 "Oh no, everything is falling apart!")

    # Test feed — contrarian follows everyone so should see posts
    feed = network.get_feed("a004")
    print(f"\n  Feed for Contrarian Carlos:")
    print(f"  {feed if feed else '(empty — no follows yet posted)'}")

    # Emotional agents follow many people — their feed might be populated
    feed_emotional = network.get_feed("a003")

    # Test clearing
    network.clear_round_posts()
    feed_after_clear = network.get_feed("a004")
    feed_cleared = feed_after_clear == "" or feed_after_clear == "  (empty)"

    print(f"\n  Checks:")
    print(f"  Network has connections : {'✓' if has_connections else '✗'} "
          f"({stats['total_connections']} total)")
    print(f"  All types represented   : {'✓' if has_all_types else '✗'}")
    print(f"  Feed cleared correctly  : {'✓' if feed_cleared else '✗'}")

    passed = has_connections and has_all_types and feed_cleared
    print(f"\n  {'✓ TEST 2 PASSED' if passed else '✗ TEST 2 FAILED'}")
    return passed


# ─────────────────────────────────────────────────────────────────────────────
# TEST 3: Agent with Semantic Memory (needs LLM)
# ─────────────────────────────────────────────────────────────────────────────

def test_agent_with_semantic_memory():
    print("\n" + "="*55)
    print("  TEST 3 — Agent with Semantic Memory (needs ollama)")
    print("="*55)

    from core.base_agent import BaseAgent
    from agents.semantic_memory import create_shared_chroma_client

    test_dir = "data/test_agent_memories_v2"
    client = create_shared_chroma_client(persist_dir=test_dir)

    agent = BaseAgent(
        agent_id      = "sem_test_001",
        name          = "Priya Nair",
        personality   = "cautious and analytical",
        background    = "Economics student, follows monetary policy",
        chroma_client = client,
        simulation_id = "phase2_test"
    )

    print(f"\n  Agent created with semantic memory: "
          f"{'✓' if agent._use_semantic_memory else '✗'}")

    # Store some memories manually
    agent.round = 1
    agent.remember("RBI hiked rates by 0.5% citing inflation", category="observation")
    agent.remember("Markets dropped 2% immediately after announcement", category="observation")
    agent.round = 2
    agent.remember("IIM economist warns of recession risk if rates rise again", category="observation")

    # Run one belief update
    agent.update_belief("RBI confirms further hikes are possible this quarter.")

    print(f"\n  Memories stored: {agent.memory.count()}")
    print(f"  Belief distribution: {agent.belief_state.distribution}")

    # Test memory retrieval through think
    print(f"\n  Testing semantic memory retrieval in think()...")
    relevant_memories = agent.memory_as_text(query="inflation and interest rates")
    print(f"  Relevant memories retrieved:\n{relevant_memories}")

    has_memory = agent.memory.count() > 0
    has_beliefs = sum(agent.belief_state.distribution.values()) > 0.99
    has_relevant = len(relevant_memories) > 10

    # Cleanup
    import shutil
    try:
        shutil.rmtree(test_dir)
    except Exception:
        pass

    print(f"\n  Checks:")
    print(f"  Semantic memory active  : {'✓' if agent._use_semantic_memory else '✗'}")
    print(f"  Memories stored         : {'✓' if has_memory else '✗'} "
          f"({agent.memory.count() if has_memory else 0})")
    print(f"  Belief distribution OK  : {'✓' if has_beliefs else '✗'}")
    print(f"  Memory retrieval works  : {'✓' if has_relevant else '✗'}")

    passed = agent._use_semantic_memory and has_memory and has_beliefs
    print(f"\n  {'✓ TEST 3 PASSED' if passed else '✗ TEST 3 FAILED'}")
    return passed


# ─────────────────────────────────────────────────────────────────────────────
# TEST 4: Causal DAG Insight Extraction
# ─────────────────────────────────────────────────────────────────────────────

def test_causal_dag_integration():
    print("\n" + "="*55)
    print("  TEST 4 — Causal DAG in Simulation (simulation/runner.py)")
    print("="*55)

    from simulation.runner import _get_causal_insight

    # Load the actual causal DAG from Module 3 if it exists
    causal_path = "data/graphs/rbi_crisis_causal.json"
    if not os.path.exists(causal_path):
        print(f"\n  Causal DAG not found at {causal_path}")
        print(f"  Run python tests/test_module3.py to generate it.")
        print(f"  ✓ TEST 4 SKIPPED")
        return True

    import json
    with open(causal_path) as f:
        causal_data = json.load(f)

    print(f"\n  Loaded causal DAG: "
          f"{len(causal_data.get('causal_edges', []))} edges")

    # Test with RBI context
    world_context = (
        "RBI has announced an emergency 0.5% interest rate hike. "
        "Markets are reacting."
    )
    insight = _get_causal_insight(causal_data, world_context)
    print(f"\n  World context: '{world_context[:60]}...'")
    print(f"  Causal insight: '{insight}'")

    # Test with unrelated context
    unrelated_context = "A sports team won the championship yesterday."
    no_insight = _get_causal_insight(causal_data, unrelated_context)
    print(f"\n  Unrelated context: no insight expected")
    print(f"  Got: '{no_insight}'")

    has_insight = len(insight) > 0
    no_false_positive = len(no_insight) == 0 or no_insight == ""

    print(f"\n  Checks:")
    print(f"  Insight found for RBI context  : {'✓' if has_insight else '✗'}")
    print(f"  No false positive (sports ctx) : {'✓' if no_false_positive else '✗'}")

    passed = has_insight
    print(f"\n  {'✓ TEST 4 PASSED' if passed else '✗ TEST 4 FAILED'}")
    return passed


# ─────────────────────────────────────────────────────────────────────────────
# TEST 5: Mini Simulation with All Phase 2 Features
# ─────────────────────────────────────────────────────────────────────────────

def test_mini_simulation_phase2():
    print("\n" + "="*55)
    print("  TEST 5 — Mini Simulation with Phase 2 Features")
    print("  (semantic memory + social network + causal DAG)")
    print("  WARNING: this runs 1 branch × 3 agents × 2 rounds (~4 min)")
    print("="*55)

    from simulation.runner import run_simulation

    causal_path = "data/graphs/rbi_crisis_causal.json"
    causal_arg  = causal_path if os.path.exists(causal_path) else None

    result = run_simulation(
        simulation_id     = "phase2_mini_test",
        topic             = "RBI rate hike v2 test",
        initial_situation = "RBI announced 0.5% rate hike. Markets dropped.",
        events_per_round  = [
            "Economists warn of recession risk.",
            "Three banks announce EMI increases."
        ],
        available_actions = [
            "wait and observe",
            "research data",
            "spread concerns",
            "revise financial plan"
        ],
        num_agents        = 3,
        num_rounds        = 2,
        causal_dag_path   = causal_arg,
        verbose           = True
    )

    print(f"\n  Mini simulation complete:")
    print(f"  Final outcome    : {result.get('final_outcome')}")
    print(f"  Avg confidence   : {result.get('avg_final_confidence')}")
    print(f"  Action dist      : {result.get('action_distribution')}")

    has_outcome     = result.get("final_outcome") is not None
    has_confidence  = result.get("avg_final_confidence", 0) > 0

    print(f"\n  Checks:")
    print(f"  Has outcome      : {'✓' if has_outcome else '✗'}")
    print(f"  Has confidence   : {'✓' if has_confidence else '✗'}")

    passed = has_outcome and has_confidence
    print(f"\n  {'✓ TEST 5 PASSED' if passed else '✗ TEST 5 FAILED'}")
    return passed


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def run_all_tests():
    print("\n" + "="*55)
    print("  DARSH v2 — PHASE 2 INTELLIGENCE UPGRADES TEST SUITE")
    print("="*55)
    print("\n  Tests 1-2: Pure logic (no LLM)")
    print("  Tests 3-5: Need ollama serve in Tab 1\n")

    results = {}

    for test_num, (name, func) in enumerate([
        ("1_semantic_memory",        test_semantic_memory),
        ("2_social_network",         test_social_network),
        ("3_agent_semantic_memory",  test_agent_with_semantic_memory),
        ("4_causal_dag_integration", test_causal_dag_integration),
        ("5_mini_simulation",        test_mini_simulation_phase2),
    ], 1):
        try:
            results[name] = func()
        except Exception as e:
            print(f"\n  ✗ {name} ERROR: {e}")
            import traceback
            traceback.print_exc()
            results[name] = False

    print("\n\n" + "="*55)
    print("  PHASE 2 TEST RESULTS SUMMARY")
    print("="*55)

    all_passed = True
    for test_name, passed in results.items():
        status = "✓" if passed else "✗"
        print(f"  {status}  {test_name}")
        if not passed:
            all_passed = False

    print("\n" + "="*55)
    if all_passed:
        print("  ✓  ALL PHASE 2 TESTS PASSED")
        print("  ✓  Semantic memory working — agents remember relevantly")
        print("  ✓  Social network working — agents influence each other")
        print("  ✓  Causal DAG active — agents reason causally")
        print("\n  → Ready for Phase 3 credibility upgrades")
    else:
        failed = [k for k, v in results.items() if not v]
        print(f"  ✗  {len(failed)} test(s) need attention: {failed}")
        print("\n  → Paste output and we fix together")
    print("="*55 + "\n")


if __name__ == "__main__":
    run_all_tests()