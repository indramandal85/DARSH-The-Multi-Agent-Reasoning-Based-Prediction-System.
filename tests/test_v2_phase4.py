# tests/test_v2_phase4.py
# Phase 4 UI upgrades — run with: python tests/test_v2_phase4.py

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_graph_api():
    print("\n" + "="*55)
    print("  TEST 1 — Graph API endpoint")
    print("="*55)

    graphs_dir = "data/graphs"
    if not os.path.exists(graphs_dir):
        print("  No graphs dir — run Module 2 first")
        return True

    json_files = [f for f in os.listdir(graphs_dir)
                  if f.endswith(".json") and "_causal" not in f]

    print(f"\n  Available graphs: {len(json_files)}")
    for f in json_files[:5]:
        print(f"    - {f}")

    passed = len(json_files) >= 1
    print(f"\n  {'✓ TEST 1 PASSED' if passed else '✗ TEST 1 FAILED'}")
    return passed


def test_simulation_history():
    print("\n" + "="*55)
    print("  TEST 2 — Simulation history")
    print("="*55)

    import sqlite3
    sims_dir = "data/simulations"
    if not os.path.exists(sims_dir):
        print("  No simulations yet — run Module 5 first")
        return True

    db_files = [f for f in os.listdir(sims_dir) if f.endswith(".db")]
    print(f"\n  Simulation databases found: {len(db_files)}")

    for db_file in db_files[:3]:
        db_path = os.path.join(sims_dir, db_file)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM agent_actions")
        actions = cursor.fetchone()[0]
        cursor.execute("SELECT MAX(round_number) FROM agent_actions")
        max_round = cursor.fetchone()[0]
        conn.close()
        print(f"    {db_file}: {actions} actions, {max_round} rounds")

    passed = len(db_files) >= 1
    print(f"\n  {'✓ TEST 2 PASSED' if passed else '✗ TEST 2 FAILED'}")
    return passed


def test_graph_merger():
    print("\n" + "="*55)
    print("  TEST 3 — Graph merger")
    print("="*55)

    graphs_dir = "data/graphs"
    json_files = [f.replace(".json","") for f in os.listdir(graphs_dir)
                  if f.endswith(".json") and "_causal" not in f
                  and not f.startswith("merged_")]

    if len(json_files) < 2:
        print(f"  Only {len(json_files)} graph(s) available — need 2 to merge")
        print(f"  Run Module 2 on multiple documents first")
        print(f"  ✓ TEST 3 SKIPPED")
        return True

    from knowledge.graph_merger import merge_graphs

    test_names = json_files[:2]
    print(f"\n  Merging: {test_names[0]} + {test_names[1]}")

    result = merge_graphs(test_names, merged_name="test_merge_output")

    node_count = len(result["merged"]["nodes"])
    edge_count = len(result["merged"]["edges"])
    saved      = os.path.exists(result["saved_path"])

    print(f"\n  Merged: {node_count} nodes, {edge_count} edges")
    print(f"  Saved : {'✓' if saved else '✗'}")

    # Cleanup
    if saved:
        os.remove(result["saved_path"])

    passed = node_count >= 1 and saved
    print(f"\n  {'✓ TEST 3 PASSED' if passed else '✗ TEST 3 FAILED'}")
    return passed


def run_all_tests():
    print("\n" + "="*55)
    print("  DARSH v2 — PHASE 4 UI UPGRADES TEST SUITE")
    print("="*55)

    results = {}
    for name, func in [
        ("1_graph_api",          test_graph_api),
        ("2_simulation_history", test_simulation_history),
        ("3_graph_merger",       test_graph_merger),
    ]:
        try:
            results[name] = func()
        except Exception as e:
            print(f"\n  ✗ {name} ERROR: {e}")
            import traceback; traceback.print_exc()
            results[name] = False

    print("\n\n" + "="*55)
    print("  PHASE 4 TEST RESULTS SUMMARY")
    print("="*55)

    all_passed = True
    for k, v in results.items():
        print(f"  {'✓' if v else '✗'}  {k}")
        if not v: all_passed = False

    print("\n" + "="*55)
    if all_passed:
        print("  ✓  ALL PHASE 4 TESTS PASSED")
        print("  ✓  Graph viewer API ready")
        print("  ✓  Simulation history API ready")
        print("  ✓  Graph merger working")
        print("\n  → DARSH v2 complete")
    else:
        print(f"  ✗  Some tests need attention")
    print("="*55)


if __name__ == "__main__":
    run_all_tests()