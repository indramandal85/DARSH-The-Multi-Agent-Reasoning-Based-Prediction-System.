# knowledge/graph_densifier.py
#
# Post-process an existing saved graph into a denser visualization graph by
# adding grounded context-proximity edges from the original source document.

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def densify_saved_graph(graph_path: str, source_path: str, output_name: str | None = None) -> dict:
    """
    Load an existing graph JSON, add grounded CONTEXT_NEAR edges based on the
    original document text, and save a denser graph JSON for visualization.
    """

    from knowledge.entity_extractor import augment_contextual_relationships

    if not os.path.exists(graph_path):
        raise FileNotFoundError(f"Graph not found: {graph_path}")
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Source document not found: {source_path}")

    with open(graph_path, "r", encoding="utf-8") as f:
        graph_data = json.load(f)

    with open(source_path, "r", encoding="utf-8") as f:
        source_text = f.read()

    nodes = graph_data.get("nodes", [])
    edges = graph_data.get("edges", [])

    entities = [
        {
            "name": node.get("id", ""),
            "type": node.get("type", "UNKNOWN"),
            "description": node.get("description", ""),
        }
        for node in nodes
        if node.get("id") and node.get("type") != "UNKNOWN"
    ]

    relationships = [
        {
            "source": edge.get("source", ""),
            "target": edge.get("target", ""),
            "relation": edge.get("relation", ""),
            "inferred": edge.get("inferred", False),
            "weight": edge.get("weight", 1.0),
        }
        for edge in edges
        if edge.get("source") and edge.get("target") and edge.get("relation")
    ]

    augmented = augment_contextual_relationships(source_text, entities, relationships)

    densified_name = output_name or (
        os.path.splitext(os.path.basename(graph_path))[0] + "_dense_view"
    )
    output_path = os.path.join("data", "graphs", f"{densified_name}.json")

    payload = {
        "name": densified_name,
        "nodes": nodes,
        "edges": augmented,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print("\n  Dense graph view generated:")
    print(f"    Input graph  : {graph_path}")
    print(f"    Source text  : {source_path}")
    print(f"    Saved to     : {output_path}")
    print(f"    Nodes        : {len(nodes)}")
    print(f"    Base edges   : {len(edges)}")
    print(f"    Dense edges  : {len(augmented)}")
    print(f"    Added edges  : {len(augmented) - len(edges)}")

    return {
        "graph_name": densified_name,
        "saved_path": output_path,
        "node_count": len(nodes),
        "edge_count": len(augmented),
        "added_edges": len(augmented) - len(edges),
    }


if __name__ == "__main__":
    raise SystemExit(
        "Use from Python: densify_saved_graph(graph_path, source_path, output_name=None)"
    )
