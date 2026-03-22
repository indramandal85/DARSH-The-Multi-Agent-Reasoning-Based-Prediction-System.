# knowledge/graph_merger.py
#
# MULTI-DOCUMENT GRAPH FUSION
#
# Takes multiple knowledge graph JSON files and merges them into
# one richer combined graph with source provenance labels.
#
# Use case: feed 5 news articles about the same topic for a
# much richer world model than any single article provides.
#
# Merging rules:
#   1. Nodes with same name → merge (keep best description)
#   2. Nodes with similar names (fuzzy match > 0.85) → merge
#   3. Relationships: deduplicate by source+target+relation
#   4. Add "sources" field to every node tracking which document it came from

import os
import sys
import json
import difflib

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

GRAPHS_DIR = "data/graphs"


def load_graph_json(graph_name: str) -> dict:
    """Load a saved knowledge graph JSON file."""
    path = os.path.join(GRAPHS_DIR, f"{graph_name}.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Graph not found: {path}")
    with open(path) as f:
        return json.load(f)


def _find_canonical(name: str, seen: dict, threshold: float = 0.85) -> str | None:
    """Find if this name is a fuzzy duplicate of an existing node."""
    name_lower = name.lower()
    for existing in seen:
        existing_lower = existing.lower()
        if name_lower in existing_lower or existing_lower in name_lower:
            if len(min(name_lower, existing_lower, key=len)) >= 3:
                return existing
        ratio = difflib.SequenceMatcher(None, name_lower, existing_lower).ratio()
        if ratio >= threshold:
            return existing
    return None


def merge_graphs(graph_names: list, merged_name: str = None) -> dict:
    """
    Merge multiple knowledge graphs into one combined graph.

    graph_names  : list of graph names (without .json extension)
    merged_name  : name for the output graph (auto-generated if None)

    Returns dict with merged graph data and saves to data/graphs/.
    """

    if len(graph_names) < 2:
        raise ValueError("Need at least 2 graphs to merge")

    print(f"\n  Merging {len(graph_names)} graphs:")
    for name in graph_names:
        print(f"    - {name}")

    # Load all source graphs
    source_graphs = {}
    for name in graph_names:
        try:
            source_graphs[name] = load_graph_json(name)
            node_count = len(source_graphs[name].get("nodes", []))
            edge_count = len(source_graphs[name].get("edges", []))
            print(f"    {name}: {node_count} nodes, {edge_count} edges")
        except FileNotFoundError as e:
            print(f"    Warning: {e} — skipping")

    if not source_graphs:
        raise ValueError("No graphs could be loaded")

    # ── Merge nodes ──────────────────────────────────────────────────────
    merged_nodes = {}    # canonical_name → node dict

    for graph_name, graph_data in source_graphs.items():
        for node in graph_data.get("nodes", []):
            node_id = node.get("id", "").strip()
            if not node_id:
                continue

            canonical = _find_canonical(node_id, merged_nodes)

            if canonical:
                # Merge into existing node
                existing = merged_nodes[canonical]
                # Keep longer/better description
                if len(node.get("description", "")) > len(existing.get("description", "")):
                    existing["description"] = node["description"]
                # Track all source graphs
                if graph_name not in existing.get("sources", []):
                    existing.setdefault("sources", []).append(graph_name)
            else:
                # New node
                new_node = {
                    "id"         : node_id,
                    "type"       : node.get("type", "UNKNOWN"),
                    "description": node.get("description", ""),
                    "sources"    : [graph_name]
                }
                merged_nodes[node_id] = new_node

    # ── Merge edges ──────────────────────────────────────────────────────
    merged_edges = {}    # (source, target, relation) → edge dict

    for graph_name, graph_data in source_graphs.items():
        for edge in graph_data.get("edges", []):
            src = edge.get("source", "").strip()
            tgt = edge.get("target", "").strip()
            rel = edge.get("relation", "").strip()

            if not src or not tgt:
                continue

            # Resolve to canonical names
            canonical_src = _find_canonical(src, merged_nodes) or src
            canonical_tgt = _find_canonical(tgt, merged_nodes) or tgt

            # Only keep edges where both nodes exist in merged graph
            if canonical_src not in merged_nodes or canonical_tgt not in merged_nodes:
                continue

            edge_key = (canonical_src, canonical_tgt, rel)
            if edge_key not in merged_edges:
                merged_edges[edge_key] = {
                    "source"  : canonical_src,
                    "target"  : canonical_tgt,
                    "relation": rel,
                    "sources" : [graph_name]
                }
            else:
                if graph_name not in merged_edges[edge_key]["sources"]:
                    merged_edges[edge_key]["sources"].append(graph_name)

    # ── Build final structure ────────────────────────────────────────────
    merged = {
        "nodes"          : list(merged_nodes.values()),
        "edges"          : list(merged_edges.values()),
        "source_graphs"  : list(source_graphs.keys()),
        "merged_from"    : len(source_graphs)
    }

    # ── Save ─────────────────────────────────────────────────────────────
    if merged_name is None:
        merged_name = "merged_" + "_".join(graph_names[:2])

    save_path = os.path.join(GRAPHS_DIR, f"{merged_name}.json")
    with open(save_path, "w") as f:
        json.dump(merged, f, indent=2)

    print(f"\n  Merged graph:")
    print(f"    Total nodes  : {len(merged['nodes'])} "
          f"(from {sum(len(g.get('nodes',[])) for g in source_graphs.values())} raw)")
    print(f"    Total edges  : {len(merged['edges'])} "
          f"(from {sum(len(g.get('edges',[])) for g in source_graphs.values())} raw)")
    print(f"    Saved to     : {save_path}")

    return {"merged": merged, "saved_path": save_path, "merged_name": merged_name}