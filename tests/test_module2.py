# tests/test_module2.py
# Run with: python tests/test_module2.py
#
# PASS condition:
#   - Graph has at least 5 nodes and 3 edges
#   - JSON file saved in data/graphs/
#   - ChromaDB search returns relevant results

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from knowledge.graph_builder import build_knowledge_graph, search_graph


def run_test():

    print("\n" + "="*52)
    print("  DARSH — MODULE 2 DRY-RUN TEST")
    print("  Knowledge Graph Builder")
    print("="*52)

    # ── Run full pipeline ──────────────────────────────────────────────────
    result = build_knowledge_graph(
        filepath="data/inputs/rbi_article.txt",
        graph_name="rbi_crisis"
    )

    G = result["graph"]

    # ── Print the graph ────────────────────────────────────────────────────
    print(f"\n\n{'='*52}")
    print("  EXTRACTED KNOWLEDGE GRAPH")
    print(f"{'='*52}")

    print(f"\n  NODES ({G.number_of_nodes()} entities):")
    for node, data in G.nodes(data=True):
        print(f"    [{data.get('type', '?'):14}] {node}")
        if data.get("description"):
            print(f"                     → {data['description']}")

    print(f"\n  EDGES ({G.number_of_edges()} relationships):")
    for u, v, data in G.edges(data=True):
        print(f"    {u} --{data.get('relation', '?')}--> {v}")

    # ── Test semantic search ───────────────────────────────────────────────
    print(f"\n\n{'='*52}")
    print("  SEMANTIC SEARCH TESTS")
    print(f"{'='*52}")

    test_queries = [
        "who leads monetary policy decisions",
        "what caused the economic crisis",
        "stock market and financial institutions"
    ]

    for query in test_queries:
        print(f"\n  Query: '{query}'")
        results = search_graph(query, "rbi_crisis", n_results=3)
        for r in results:
            print(f"    → [{r.get('type')}] {r.get('name')}")

    # ── Pass check ─────────────────────────────────────────────────────────
    graph_file_exists = os.path.exists("data/graphs/rbi_crisis.json")
    has_nodes = G.number_of_nodes() >= 5
    has_edges = G.number_of_edges() >= 3
    search_works = len(search_graph("inflation", "rbi_crisis")) > 0

    passed = graph_file_exists and has_nodes and has_edges and search_works

    print(f"\n\n{'='*52}")
    if passed:
        print("  ✓  MODULE 2 PASSED")
        print(f"  ✓  Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
        print(f"  ✓  JSON saved to data/graphs/rbi_crisis.json")
        print(f"  ✓  ChromaDB semantic search working")
        print("\n  → Ready for Module 3")
    else:
        print("  ✗  Something needs attention:")
        print(f"  Graph file saved : {graph_file_exists}")
        print(f"  Enough nodes (≥5): {has_nodes} ({G.number_of_nodes()} found)")
        print(f"  Enough edges (≥3): {has_edges} ({G.number_of_edges()} found)")
        print(f"  Search working   : {search_works}")
        print("\n  → Paste this output and we fix together")
    print("="*52 + "\n")


if __name__ == "__main__":
    run_test()