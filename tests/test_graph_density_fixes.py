# tests/test_graph_density_fixes.py
#
# Targeted regression tests for dense knowledge-graph fixes.

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_numeric_entities_stay_distinct():
    print("\n" + "=" * 60)
    print("  TEST 1 — Numeric military entities stay distinct")
    print("=" * 60)

    from knowledge.entity_validator import validate_entities

    source = """
    The 56 Mountain Brigade coordinated with 79 Mountain Brigade.
    Indian troops attacked Point 5100 and later reinforced Point 5140.
    The Kargil War reshaped planning in Kargil district.
    """

    raw_entities = [
        {"name": "56 Mountain Brigade", "type": "ORGANIZATION", "description": "formation"},
        {"name": "79 Mountain Brigade", "type": "ORGANIZATION", "description": "formation"},
        {"name": "Point 5100", "type": "PLACE", "description": "feature"},
        {"name": "Point 5140", "type": "PLACE", "description": "feature"},
        {"name": "Kargil War", "type": "EVENT", "description": "conflict"},
        {"name": "Kargil", "type": "PLACE", "description": "district"},
    ]

    validated = validate_entities(raw_entities, source)
    kept = {entity["name"] for entity in validated}

    expectations = [
        "56 Mountain Brigade",
        "79 Mountain Brigade",
        "Point 5100",
        "Point 5140",
        "Kargil War",
        "Kargil",
    ]

    passed = all(name in kept for name in expectations)
    print(f"  Kept all distinct entities: {'✓' if passed else '✗'}")
    return passed


def test_relationship_canonicalization_and_graph_strictness():
    print("\n" + "=" * 60)
    print("  TEST 2 — Relationship endpoints are canonicalized cleanly")
    print("=" * 60)

    from knowledge.entity_validator import validate_relationships
    from knowledge.graph_builder import build_graph

    valid_entities = [
        {"name": "RBI", "type": "ORGANIZATION", "description": "central bank"},
        {"name": "Shaktikanta Das", "type": "PERSON", "description": "governor"},
    ]

    rels = [
        {"source": "the RBI", "target": "Shaktikanta Das", "relation": "LED_BY"},
        {"source": "Reserve Bank of India", "target": "Shaktikanta Das", "relation": "LED_BY"},
        {"source": "Unknown Entity", "target": "RBI", "relation": "MENTIONED"},
    ]

    cleaned = validate_relationships(rels, {entity["name"] for entity in valid_entities})
    graph = build_graph({"entities": valid_entities, "relationships": cleaned}, "validator_regression")

    edge_pairs = {(u, v) for u, v in graph.edges()}
    node_names = set(graph.nodes())

    passed = (
        ("RBI", "Shaktikanta Das") in edge_pairs and
        "Unknown Entity" not in node_names
    )

    print(f"  Canonical endpoint kept : {'✓' if ('RBI', 'Shaktikanta Das') in edge_pairs else '✗'}")
    print(f"  Unknown node not added  : {'✓' if 'Unknown Entity' not in node_names else '✗'}")
    return passed


def test_contextual_edge_augmentation():
    print("\n" + "=" * 60)
    print("  TEST 3 — Contextual augmentation adds density safely")
    print("=" * 60)

    from knowledge.entity_extractor import augment_contextual_relationships

    source = """
    India briefed the Indian Army, the Air Force, and the Vajpayee government in Dras.
    The Indian Army and the Air Force coordinated around Tiger Hill.
    Tiger Hill and Dras were repeatedly discussed by the Vajpayee government and the Air Force.
    """

    entities = [
        {"name": "India", "type": "PLACE", "description": ""},
        {"name": "Indian Army", "type": "ORGANIZATION", "description": ""},
        {"name": "Air Force", "type": "ORGANIZATION", "description": ""},
        {"name": "Vajpayee government", "type": "ORGANIZATION", "description": ""},
        {"name": "Dras", "type": "PLACE", "description": ""},
        {"name": "Tiger Hill", "type": "PLACE", "description": ""},
    ]

    relationships = [
        {"source": "India", "target": "Indian Army", "relation": "BRIEFED"},
    ]

    augmented = augment_contextual_relationships(source, entities, relationships)
    context_edges = [rel for rel in augmented if rel.get("relation") == "CONTEXT_NEAR"]

    passed = len(context_edges) >= 3
    print(f"  Added contextual edges: {len(context_edges)}")
    print(f"  {'✓ TEST 3 PASSED' if passed else '✗ TEST 3 FAILED'}")
    return passed


def run_all_tests():
    results = []
    for test_fn in [
        test_numeric_entities_stay_distinct,
        test_relationship_canonicalization_and_graph_strictness,
        test_contextual_edge_augmentation,
    ]:
        try:
            results.append(test_fn())
        except Exception as exc:
            print(f"  ✗ ERROR: {exc}")
            import traceback
            traceback.print_exc()
            results.append(False)

    all_passed = all(results)
    print("\n" + "=" * 60)
    print("  GRAPH DENSITY FIX SUMMARY")
    print("=" * 60)
    print(f"  {'✓' if all_passed else '✗'} All targeted density tests")
    print("=" * 60)
    return all_passed


if __name__ == "__main__":
    raise SystemExit(0 if run_all_tests() else 1)
