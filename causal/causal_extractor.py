# causal/causal_extractor.py
#
# WHAT THIS DOES:
# Takes the knowledge graph from Module 2 and upgrades it to a Causal DAG.
#
# The knowledge graph knows: "RBI and inflation are related"
# The causal DAG knows:      "Inflation CAUSES RBI rate hikes (strength: 0.9)"
#
# For each relationship in the graph, we ask the LLM three questions:
#   1. Which direction does causation flow?
#   2. How strong is that causal link? (0.0 to 1.0)
#   3. What is the time lag? (immediate, days, weeks, months)
#
# The result is a DAG where every edge means "A causes B"
# and we know HOW strongly and HOW quickly.

import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import networkx as nx
from core.llm_caller import ask_llm_json

CAUSAL_GRAPHS_DIR = "data/graphs"


def determine_causal_direction(source: str, target: str,
                                relation: str, context: str) -> dict:
    """
    Ask the LLM whether A causes B, B causes A, both, or neither.

    source   : the source entity from the knowledge graph
    target   : the target entity from the knowledge graph
    relation : the relationship label e.g. "ANNOUNCED", "CAUSED_BY"
    context  : background context about what these entities are

    Returns dict with:
      direction  : "A_CAUSES_B", "B_CAUSES_A", "BIDIRECTIONAL", or "NONE"
      strength   : float 0.0–1.0 (how strong is the causal link)
      time_lag   : "immediate", "days", "weeks", "months", "years"
      explanation: one sentence explaining the reasoning
    """

    prompt = f"""
Analyze whether there is a CAUSAL relationship between these two entities.

Entity A: {source}
Entity B: {target}  
Relationship observed: {relation}
Context: {context}

Determine the causal direction:
- A_CAUSES_B: changes in A directly cause changes in B
- B_CAUSES_A: changes in B directly cause changes in A  
- BIDIRECTIONAL: they mutually cause each other
- NONE: they are correlated but neither causes the other

Return JSON with exactly these keys:
{{
  "direction": "A_CAUSES_B or B_CAUSES_A or BIDIRECTIONAL or NONE",
  "strength": 0.0 to 1.0 (0=no causal link, 1=direct certain cause),
  "time_lag": "immediate or days or weeks or months or years",
  "explanation": "one sentence explaining why"
}}

Think carefully. Correlation is not causation.
"""

    result = ask_llm_json(prompt)

    # Safe defaults if parsing failed
    if result.get("parse_error"):
        return {
            "direction": "NONE",
            "strength": 0.0,
            "time_lag": "unknown",
            "explanation": "Could not determine causal direction."
        }

    # Validate direction value
    valid_directions = ["A_CAUSES_B", "B_CAUSES_A", "BIDIRECTIONAL", "NONE"]
    if result.get("direction") not in valid_directions:
        result["direction"] = "NONE"

    # Clamp strength to 0.0–1.0
    try:
        result["strength"] = max(0.0, min(1.0, float(result.get("strength", 0.0))))
    except (ValueError, TypeError):
        result["strength"] = 0.0

    return result


def build_causal_dag(knowledge_graph_path: str, context_description: str = "") -> nx.DiGraph:
    """
    Load a knowledge graph and build a Causal DAG from it.

    Iterates over every edge in the knowledge graph.
    For each edge, asks the LLM to determine causal direction and strength.
    Builds a new directed graph where edges represent CAUSATION not just relation.

    knowledge_graph_path  : path to the JSON file saved by Module 2
    context_description   : brief description of the domain for LLM context
                           e.g. "Indian economic and monetary policy events"

    Returns: NetworkX DiGraph where edges mean "A causes B"
    """

    # Load the knowledge graph from Module 2
    if not os.path.exists(knowledge_graph_path):
        raise FileNotFoundError(
            f"Knowledge graph not found: {knowledge_graph_path}\n"
            f"Run Module 2 test first to generate the graph.\n"
        )

    with open(knowledge_graph_path, "r") as f:
        graph_data = json.load(f)

    edges = graph_data.get("edges", [])
    nodes = {n["id"]: n for n in graph_data.get("nodes", [])}

    print(f"  Loaded graph: {len(nodes)} nodes, {len(edges)} edges")
    print(f"  Analyzing {len(edges)} relationships for causal direction...")

    # Build the causal DAG
    causal_dag = nx.DiGraph()
    causal_dag.name = graph_data.get("name", "causal_dag")

    # Add all nodes from knowledge graph
    for node_id, node_data in nodes.items():
        causal_dag.add_node(
            node_id,
            type=node_data.get("type", "UNKNOWN"),
            description=node_data.get("description", "")
        )

    causal_edges_added = 0

    for i, edge in enumerate(edges):
        source = edge.get("source", "")
        target = edge.get("target", "")
        relation = edge.get("relation", "")

        if not source or not target:
            continue

        # Build context from node descriptions
        source_desc = nodes.get(source, {}).get("description", source)
        target_desc = nodes.get(target, {}).get("description", target)
        context = (
            f"{source} ({source_desc}) has relationship '{relation}' "
            f"with {target} ({target_desc}). "
            f"Domain: {context_description}"
        )

        print(f"  [{i+1}/{len(edges)}] {source} → {target}", end=" ... ")

        causal_info = determine_causal_direction(source, target, relation, context)
        direction = causal_info["direction"]
        strength = causal_info["strength"]
        time_lag = causal_info["time_lag"]
        explanation = causal_info["explanation"]

        print(f"{direction} (strength: {strength})")

        # Add causal edge(s) based on determined direction
        # Only add if strength > 0.1 (filter out very weak links)
        if direction == "A_CAUSES_B" and strength > 0.1:
            causal_dag.add_edge(
                source, target,
                relation=relation,
                strength=strength,
                time_lag=time_lag,
                explanation=explanation,
                causal_type="A_CAUSES_B"
            )
            causal_edges_added += 1

        elif direction == "B_CAUSES_A" and strength > 0.1:
            causal_dag.add_edge(
                target, source,
                relation=f"REVERSE_{relation}",
                strength=strength,
                time_lag=time_lag,
                explanation=explanation,
                causal_type="B_CAUSES_A"
            )
            causal_edges_added += 1

        elif direction == "BIDIRECTIONAL" and strength > 0.1:
            # Add both directions for bidirectional causation
            causal_dag.add_edge(
                source, target,
                relation=relation,
                strength=strength,
                time_lag=time_lag,
                explanation=explanation,
                causal_type="BIDIRECTIONAL"
            )
            causal_dag.add_edge(
                target, source,
                relation=f"REVERSE_{relation}",
                strength=strength * 0.8,  # slightly weaker reverse
                time_lag=time_lag,
                explanation=explanation,
                causal_type="BIDIRECTIONAL"
            )
            causal_edges_added += 2

        # direction == "NONE" — skip, no causal edge added

    print(f"\n  Causal DAG built:")
    print(f"    Original edges    : {len(edges)}")
    print(f"    Causal edges kept : {causal_edges_added}")
    print(f"    Filtered out      : {len(edges) - causal_edges_added} "
          f"(correlation only, not causation)")

    return causal_dag


def save_causal_dag(dag: nx.DiGraph, name: str) -> str:
    """Save the causal DAG to disk as JSON."""

    os.makedirs(CAUSAL_GRAPHS_DIR, exist_ok=True)
    filepath = os.path.join(CAUSAL_GRAPHS_DIR, f"{name}_causal.json")

    dag_data = {
        "name": name,
        "type": "causal_dag",
        "nodes": [
            {
                "id": node,
                "type": data.get("type", "UNKNOWN"),
                "description": data.get("description", "")
            }
            for node, data in dag.nodes(data=True)
        ],
        "causal_edges": [
            {
                "cause": u,
                "effect": v,
                "strength": data.get("strength", 0.0),
                "time_lag": data.get("time_lag", "unknown"),
                "explanation": data.get("explanation", ""),
                "causal_type": data.get("causal_type", "")
            }
            for u, v, data in dag.edges(data=True)
        ]
    }

    with open(filepath, "w") as f:
        json.dump(dag_data, f, indent=2)

    print(f"    Causal DAG saved to: {filepath}")
    return filepath


def get_root_causes(dag: nx.DiGraph, effect: str) -> list:
    """
    Find the root causes of a given effect by walking backwards
    through the causal DAG.

    Root causes are nodes with no incoming causal edges —
    they cause other things but nothing causes them.

    Returns list of (cause_name, strength, path) tuples.
    """

    if effect not in dag:
        return []

    root_causes = []

    # Walk backwards using DFS
    def trace_back(node, path, accumulated_strength):
        predecessors = list(dag.predecessors(node))

        if not predecessors:
            # This is a root cause — nothing causes it
            root_causes.append({
                "root_cause": node,
                "path": path.copy(),
                "accumulated_strength": round(accumulated_strength, 3),
                "type": dag.nodes[node].get("type", "UNKNOWN")
            })
            return

        for pred in predecessors:
            if pred not in path:  # avoid cycles
                edge_data = dag.edges[pred, node]
                edge_strength = edge_data.get("strength", 0.5)
                path.append(pred)
                # Multiply strengths along the path (like probability chain)
                trace_back(pred, path, accumulated_strength * edge_strength)
                path.pop()

    trace_back(effect, [effect], 1.0)

    # Sort by accumulated strength — strongest causal chains first
    root_causes.sort(key=lambda x: x["accumulated_strength"], reverse=True)
    return root_causes


def get_downstream_effects(dag: nx.DiGraph, cause: str,
                           min_strength: float = 0.3) -> list:
    """
    Find all downstream effects of a given cause.
    Used by the counterfactual engine to answer
    "if we remove this cause, what effects disappear?"

    Returns list of (effect_name, strength, hops) tuples.
    """

    if cause not in dag:
        return []

    effects = []
    visited = set()

    def trace_forward(node, hops, accumulated_strength):
        successors = list(dag.successors(node))

        for succ in successors:
            if succ not in visited:
                visited.add(succ)
                edge_data = dag.edges[node, succ]
                edge_strength = edge_data.get("strength", 0.5)
                combined = accumulated_strength * edge_strength

                if combined >= min_strength:
                    effects.append({
                        "effect": succ,
                        "hops_from_cause": hops,
                        "strength": round(combined, 3),
                        "time_lag": edge_data.get("time_lag", "unknown"),
                        "type": dag.nodes[succ].get("type", "UNKNOWN")
                    })
                    trace_forward(succ, hops + 1, combined)

    visited.add(cause)
    trace_forward(cause, 1, 1.0)

    effects.sort(key=lambda x: x["strength"], reverse=True)
    return effects