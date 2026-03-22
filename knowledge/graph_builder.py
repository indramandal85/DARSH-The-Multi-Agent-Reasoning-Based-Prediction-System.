# knowledge/graph_builder.py
#
# WHAT THIS DOES:
# Takes extracted entities + relationships and:
#   1. Builds a NetworkX graph (nodes = entities, edges = relationships)
#   2. Saves the graph as JSON to data/graphs/
#   3. Stores everything in ChromaDB for semantic search
#
# After this runs, agents in Module 4 can ask:
#   "find everything related to inflation"
# and get relevant nodes back even if "inflation" isn't the exact word.

import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import networkx as nx
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions


# Path where graphs are saved
GRAPHS_DIR = "data/graphs"
CHROMA_DIR = "data/chroma"


def _get_chroma_client():
    return chromadb.PersistentClient(
        path=CHROMA_DIR,
        settings=Settings(anonymized_telemetry=False)
    )


def build_graph(extracted_data: dict, graph_name: str) -> nx.DiGraph:
    """
    Build a NetworkX directed graph from extracted entities and relationships.

    DiGraph = Directed Graph, meaning edges have direction:
    RBI --ANNOUNCED--> Rate Hike  (not the reverse)

    Returns the NetworkX graph object.
    """

    G = nx.DiGraph()
    G.name = graph_name

    entities = extracted_data.get("entities", [])
    relationships = extracted_data.get("relationships", [])

    # Add nodes (entities)
    for entity in entities:
        name = entity.get("name", "").strip()
        if name:
            G.add_node(
                name,
                type=entity.get("type", "UNKNOWN"),
                description=entity.get("description", "")
            )

    skipped_unresolved = 0

    # Add edges (relationships)
    for rel in relationships:
        source = rel.get("source", "").strip()
        target = rel.get("target", "").strip()
        relation = rel.get("relation", "").strip()

        if source and target and relation:
            # After validation, unresolved endpoints are cleaner to skip than
            # to silently add as UNKNOWN nodes, which makes the graph noisier
            # and visually sparser.
            if source not in G or target not in G:
                skipped_unresolved += 1
                continue

            G.add_edge(
                source,
                target,
                relation=relation,
                inferred=bool(rel.get("inferred", False)),
                weight=float(rel.get("weight", 1.0)),
            )

    print(f"\n  Graph built:")
    print(f"    Nodes (entities)      : {G.number_of_nodes()}")
    print(f"    Edges (relationships) : {G.number_of_edges()}")
    if skipped_unresolved:
        print(f"    Skipped unresolved    : {skipped_unresolved}")

    return G


def save_graph(G: nx.DiGraph, graph_name: str) -> str:
    """
    Save the graph to disk as a JSON file.
    Returns the filepath where it was saved.
    """

    os.makedirs(GRAPHS_DIR, exist_ok=True)
    filepath = os.path.join(GRAPHS_DIR, f"{graph_name}.json")

    # Convert graph to a JSON-serializable format
    graph_data = {
        "name": graph_name,
        "nodes": [
            {
                "id": node,
                "type": data.get("type", "UNKNOWN"),
                "description": data.get("description", "")
            }
            for node, data in G.nodes(data=True)
        ],
        "edges": [
            {
                "source": u,
                "target": v,
                "relation": data.get("relation", ""),
                "inferred": data.get("inferred", False),
                "weight": data.get("weight", 1.0),
            }
            for u, v, data in G.edges(data=True)
        ]
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(graph_data, f, indent=2, ensure_ascii=False)

    print(f"    Graph saved to: {filepath}")
    return filepath


def store_in_chromadb(G: nx.DiGraph, graph_name: str):
    """
    Store graph nodes in ChromaDB for semantic search.

    Each node gets stored as a text document like:
    "Shaktikanta Das is a PERSON. RBI Governor."

    Agents in Module 4 can then search: "find monetary policy decision makers"
    and ChromaDB returns Shaktikanta Das even without exact keyword match.
    """

    try:
        os.makedirs(CHROMA_DIR, exist_ok=True)

        # Create ChromaDB client — stores data locally in data/chroma/
        client = _get_chroma_client()

        # Use a local sentence-transformer model for embeddings
        # This runs on your Mac — no API needed when the model is cached.
        embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )

        # Get or create a collection for this graph
        collection_name = f"graph_{graph_name}".replace("-", "_").replace(" ", "_")

        # Delete existing collection if re-running (avoids duplicate errors)
        try:
            client.delete_collection(collection_name)
        except Exception:
            pass

        collection = client.create_collection(
            name=collection_name,
            embedding_function=embedding_fn
        )

        # Build documents for each node
        documents = []
        ids = []
        metadatas = []

        for node, data in G.nodes(data=True):
            node_type = data.get("type", "UNKNOWN")
            description = data.get("description", "")

            # Find this node's relationships for richer context
            outgoing = [
                f"{data_e.get('relation', '')} {v}"
                for _, v, data_e in G.out_edges(node, data=True)
            ]

            # Create a rich text description for semantic search
            doc_text = f"{node} is a {node_type}."
            if description:
                doc_text += f" {description}."
            if outgoing:
                doc_text += f" Connections: {', '.join(outgoing[:3])}."

            documents.append(doc_text)
            ids.append(f"node_{node[:50].replace(' ', '_')}")
            metadatas.append({
                "name": node,
                "type": node_type,
                "description": description
            })

        if documents:
            collection.add(
                documents=documents,
                ids=ids,
                metadatas=metadatas
            )
            print(f"    Stored {len(documents)} nodes in ChromaDB")
            print(f"    Collection: {collection_name}")
    except Exception as e:
        print(f"    Warning: ChromaDB storage skipped ({e})")


def search_graph(query: str, graph_name: str, n_results: int = 5) -> list:
    """
    Semantic search over the knowledge graph.
    Returns the most relevant nodes for a given query.

    This is what agents call in Module 4 when they need context:
    agent.search_knowledge("what caused the inflation crisis")
    """

    client = _get_chroma_client()
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    collection_name = f"graph_{graph_name}".replace("-", "_").replace(" ", "_")

    try:
        collection = client.get_collection(
            name=collection_name,
            embedding_function=embedding_fn
        )
    except Exception:
        return []

    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, collection.count())
    )

    # Format results as clean list
    found = []
    if results and results["metadatas"]:
        for meta in results["metadatas"][0]:
            found.append(meta)

    return found


def build_knowledge_graph(filepath: str, graph_name: str) -> dict:
    """
    MAIN FUNCTION — runs the full pipeline:
    document → extract → build graph → save → store in ChromaDB

    filepath   : path to input document
    graph_name : name for this graph (used for saving and searching)

    Returns dict with graph object and saved filepath.
    """

    from knowledge.document_parser import parse_document
    from knowledge.entity_extractor import extract_from_document

    print(f"\n{'='*50}")
    print(f"  Building knowledge graph: {graph_name}")
    print(f"{'='*50}")

    # Step 1: Parse document
    print("\n[1/4] Parsing document...")
    doc = parse_document(filepath)

    # Step 2: Extract entities and relationships
    print("\n[2/4] Extracting entities and relationships...")
    extracted = extract_from_document(doc["chunks"])

    # Step 3: Build NetworkX graph
    print("\n[3/4] Building graph...")
    G = build_graph(extracted, graph_name)

    # Step 4: Save and store
    print("\n[4/4] Saving graph and storing in ChromaDB...")
    saved_path = save_graph(G, graph_name)
    store_in_chromadb(G, graph_name)

    print(f"\n  Knowledge graph complete.")

    return {
        "graph": G,
        "saved_path": saved_path,
        "graph_name": graph_name,
        "entity_count": G.number_of_nodes(),
        "relationship_count": G.number_of_edges()
    }


# ── SELF TEST ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":

    print("\n" + "="*45)
    print("  TESTING graph_builder.py — search only")
    print("="*45)
    print("  (Run test_module2.py for the full pipeline test)")
    print("\n  If you've already run test_module2.py, testing search:")

    results = search_graph("monetary policy decision", "rbi_crisis")
    if results:
        print("\n  Search results for 'monetary policy decision':")
        for r in results:
            print(f"    [{r.get('type')}] {r.get('name')} — {r.get('description')}")
    else:
        print("\n  No results yet — run test_module2.py first.")
