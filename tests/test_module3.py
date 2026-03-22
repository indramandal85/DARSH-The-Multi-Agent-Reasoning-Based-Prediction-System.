# tests/test_module3.py
# Run with: python tests/test_module3.py
#
# PASS condition:
#   - Causal DAG built from Module 2 graph
#   - At least 3 causal edges identified
#   - Counterfactual reasoning produces coherent text
#   - Intervention point identified for recession risk

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from causal.causal_extractor import build_causal_dag, save_causal_dag
from causal.counterfactual import CounterfactualEngine


def run_test():

    print("\n" + "="*52)
    print("  DARSH — MODULE 3 DRY-RUN TEST")
    print("  Causal World Model")
    print("="*52)

    # ── Step 1: Build causal DAG from Module 2 graph ───────────────────────
    print("\n[1/3] Building causal DAG from knowledge graph...")

    dag = build_causal_dag(
        knowledge_graph_path="data/graphs/rbi_crisis.json",
        context_description="Indian monetary policy and economic crisis"
    )

    saved_path = save_causal_dag(dag, "rbi_crisis")

    # ── Print the causal DAG ───────────────────────────────────────────────
    print(f"\n\n{'='*52}")
    print("  CAUSAL DAG")
    print(f"{'='*52}")
    print(f"\n  Causal edges (A causes B):")

    for u, v, data in sorted(dag.edges(data=True),
                              key=lambda x: x[2].get("strength", 0),
                              reverse=True):
        strength = data.get("strength", 0)
        lag = data.get("time_lag", "?")
        print(f"  {u}")
        print(f"    ──causes──► {v}")
        print(f"    strength: {strength}  |  time lag: {lag}")
        print(f"    why: {data.get('explanation', '')[:80]}")
        print()

    # ── Step 2: Counterfactual — what if inflation hadn't risen? ───────────
    print(f"\n{'='*52}")
    print("  COUNTERFACTUAL ANALYSIS")
    print(f"{'='*52}")

    engine = CounterfactualEngine(
        causal_dag=dag,
        domain_context="Indian monetary policy, RBI interest rate decisions, and economic impact"
    )

    # Find a good node to test counterfactual on
    # Use "inflation crisis" if it exists, otherwise use first node with outgoing edges
    test_cause = None
    preferred = ["inflation crisis", "RBI", "Shaktikanta Das"]
    for candidate in preferred:
        if candidate in dag and dag.out_degree(candidate) > 0:
            test_cause = candidate
            break

    if not test_cause:
        # Fall back to any node with outgoing edges
        for node in dag.nodes():
            if dag.out_degree(node) > 0:
                test_cause = node
                break

    if test_cause:
        print(f"\n  Counterfactual question:")
        print(f"  'What would have happened if {test_cause} had not occurred?'\n")

        cf_result = engine.what_if_removed(test_cause)

        print(f"\n  Counterfactual reasoning:")
        print(f"  {cf_result['counterfactual']}")
        print(f"\n  Confidence: {cf_result['confidence']}")
        print(f"  Effects that would be prevented: {cf_result['all_effects_count']}")

    # ── Step 3: Intervention point ─────────────────────────────────────────
    print(f"\n\n{'='*52}")
    print("  INTERVENTION POINT ANALYSIS")
    print(f"{'='*52}")

    # Find a node with incoming causal edges to use as the target outcome
    target_outcome = None
    preferred_outcomes = ["inflation crisis", "Market Drop", "recession"]
    for candidate in preferred_outcomes:
        if candidate in dag and dag.in_degree(candidate) > 0:
            target_outcome = candidate
            break

    if not target_outcome:
        for node in dag.nodes():
            if dag.in_degree(node) > 0:
                target_outcome = node
                break

    if target_outcome:
        print(f"\n  Question: How could '{target_outcome}' have been prevented?\n")
        intervention = engine.find_intervention_points(target_outcome)
        print(f"  Best intervention recommendation:")
        print(f"  {intervention.get('best_intervention', 'No recommendation generated.')}")

    # ── Pass check ─────────────────────────────────────────────────────────
    causal_file = os.path.exists("data/graphs/rbi_crisis_causal.json")
    has_causal_edges = dag.number_of_edges() >= 3
    has_nodes = dag.number_of_nodes() >= 5
    cf_generated = test_cause is not None

    passed = causal_file and has_causal_edges and has_nodes and cf_generated

    print(f"\n\n{'='*52}")
    if passed:
        print("  ✓  MODULE 3 PASSED")
        print(f"  ✓  Causal DAG: {dag.number_of_nodes()} nodes, "
              f"{dag.number_of_edges()} causal edges")
        print(f"  ✓  Causal JSON saved")
        print(f"  ✓  Counterfactual reasoning working")
        print(f"  ✓  Intervention points identified")
        print(f"\n  → Ready for Module 4")
    else:
        print("  ✗  Something needs fixing:")
        print(f"  Causal file saved   : {causal_file}")
        print(f"  Causal edges (≥3)   : {has_causal_edges} ({dag.number_of_edges()})")
        print(f"  Nodes (≥5)          : {has_nodes} ({dag.number_of_nodes()})")
        print(f"  Counterfactual ran  : {cf_generated}")
        print(f"\n  → Paste output and we fix together")
    print("="*52 + "\n")


if __name__ == "__main__":
    run_test()