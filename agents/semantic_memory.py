# agents/semantic_memory.py
#
# PER-AGENT SEMANTIC MEMORY BACKED BY CHROMADB
#
# v1 problem: each agent had a Python list of the last 8 strings.
#   - No relevance ranking — the agent always sees the most RECENT memories
#     not the most RELEVANT ones.
#   - If an agent learned about inflation in Round 1 and is now in Round 10
#     discussing monetary policy, that Round 1 memory is long gone.
#
# v2 solution: each agent gets their own ChromaDB collection.
#   - Unlimited storage — every observation persists the entire simulation.
#   - Semantic retrieval — "what do I know about inflation?" returns the
#     most conceptually relevant memories regardless of when they occurred.
#   - Uses the same all-MiniLM-L6-v2 embedding model already installed.
#
# One shared ChromaDB client is passed to all agents at creation time.
# This avoids opening 50 separate database connections.

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import chromadb
from chromadb.utils import embedding_functions


# Shared embedding function — created once, reused across all agents.
# all-MiniLM-L6-v2 is already installed from Module 2.
# It's fast (22ms per query on M4) and good enough for our use case.
_EMBEDDING_FN = None

def _get_embedding_fn():
    """Lazy-initialize the embedding function (loads model on first call)."""
    global _EMBEDDING_FN
    if _EMBEDDING_FN is None:
        _EMBEDDING_FN = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
    return _EMBEDDING_FN


def create_shared_chroma_client(persist_dir: str = "data/agent_memories") -> chromadb.ClientAPI:
    """
    Create one ChromaDB client shared across all agents in a simulation.

    All agent memory collections live inside persist_dir.
    Pass this client to SemanticMemory() for each agent.

    persist_dir: where agent memories are stored on disk.
                 Separate from data/chroma/ which stores knowledge graphs.
    """
    os.makedirs(persist_dir, exist_ok=True)
    return chromadb.PersistentClient(path=persist_dir)


class SemanticMemory:
    """
    ChromaDB-backed semantic memory for one agent.

    Usage in BaseAgent:
        self.memory = SemanticMemory(agent_id, shared_client)
        self.memory.store("RBI raised rates", round_num=1)
        relevant = self.memory.retrieve("what do I know about inflation?")

    The retrieve() method returns the semantically closest stored memories
    to the query — not just the most recent ones.
    """

    def __init__(self, agent_id: str, chroma_client, simulation_id: str = "default"):
        """
        agent_id      : unique agent ID — becomes the collection name
        chroma_client : shared ChromaDB client from create_shared_chroma_client()
        simulation_id : which simulation this memory belongs to
                        (prevents memory bleeding across simulation runs)
        """
        self.agent_id      = agent_id
        self.simulation_id = simulation_id
        self._client       = chroma_client
        self._memory_count = 0

        # Collection name: agent_simid_agentid (alphanumeric + underscore only)
        safe_agent_id = agent_id.replace("-", "_").replace(" ", "_")
        safe_sim_id   = simulation_id.replace("-", "_").replace(" ", "_")
        self._collection_name = f"mem_{safe_sim_id}_{safe_agent_id}"

        # Get or create the collection for this agent
        try:
            self._collection = self._client.get_collection(
                name=self._collection_name,
                embedding_function=_get_embedding_fn()
            )
            # Count existing memories if collection already exists
            self._memory_count = self._collection.count()
        except Exception:
            self._collection = self._client.create_collection(
                name=self._collection_name,
                embedding_function=_get_embedding_fn()
            )

    def store(self, content: str, round_num: int = 0, category: str = "observation"):
        """
        Store a memory. The embedding is computed automatically by ChromaDB.

        content  : the text to remember
        round_num: which simulation round this memory came from
        category : "observation", "belief", "decision", "social_feed"
        """
        if not content or not content.strip():
            return

        self._memory_count += 1
        memory_id = f"{self._collection_name}_{self._memory_count}"

        try:
            self._collection.add(
                documents=[content.strip()],
                ids=[memory_id],
                metadatas=[{
                    "round"    : round_num,
                    "category" : category,
                    "agent_id" : self.agent_id
                }]
            )
        except Exception as e:
            # Memory storage failure is non-fatal — simulation continues
            print(f"    Warning: memory storage failed for {self.agent_id}: {e}")

    def retrieve(self, query: str, n_results: int = 3, category: str = None) -> str:
        """
        Semantic search: return the most relevant memories for this query.

        query     : what to search for (e.g. "inflation and interest rates")
        n_results : how many memories to return
        category  : optionally filter by category ("belief", "observation" etc.)

        Returns formatted string ready for insertion into LLM prompts.
        Returns "No relevant memories." if collection is empty.
        """
        if self._memory_count == 0:
            return "No memories yet."

        actual_n = min(n_results, self._memory_count)

        try:
            query_params = {
                "query_texts": [query],
                "n_results"  : actual_n
            }
            if category:
                query_params["where"] = {"category": category}

            results = self._collection.query(**query_params)

            if not results["documents"] or not results["documents"][0]:
                return "No relevant memories found."

            memories = []
            for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
                round_label = f"[Round {meta.get('round', '?')}]"
                memories.append(f"  {round_label} {doc}")

            return "\n".join(memories)

        except Exception as e:
            return f"Memory retrieval error: {e}"

    def count(self) -> int:
        """Return number of stored memories."""
        return self._memory_count

    def clear(self):
        """Clear all memories (used between simulation runs)."""
        try:
            self._client.delete_collection(self._collection_name)
            self._collection = self._client.create_collection(
                name=self._collection_name,
                embedding_function=_get_embedding_fn()
            )
            self._memory_count = 0
        except Exception:
            pass

    def clear_old_agent_memories(keep_recent_n: int = 3):
        """
        Delete ChromaDB collections from old simulation runs.
        Keeps only the N most recent simulation memory namespaces.
        Prevents disk from filling up and eliminates cross-run contamination.

        Called once at the start of each new parallel branch run.
        """
        try:
            client = create_shared_chroma_client()
            collections = client.list_collections()

            # Extract simulation timestamps from collection names
            # Format: mem_{sim_id}_{timestamp}_{agent_id}
            sim_timestamps = {}
            for col in collections:
                name = col.name
                if not name.startswith("mem_"):
                    continue
                parts = name.split("_")
                # Find the timestamp part (6-digit number)
                for part in parts:
                    if part.isdigit() and len(part) == 6:
                        ts = int(part)
                        if ts not in sim_timestamps:
                            sim_timestamps[ts] = []
                        sim_timestamps[ts].append(name)
                        break

            # Keep only the N most recent timestamps
            sorted_ts = sorted(sim_timestamps.keys(), reverse=True)
            old_timestamps = sorted_ts[keep_recent_n:]

            deleted = 0
            for ts in old_timestamps:
                for col_name in sim_timestamps[ts]:
                    try:
                        client.delete_collection(col_name)
                        deleted += 1
                    except Exception:
                        pass

            if deleted > 0:
                print(f"  Cleared {deleted} old agent memory collections")

        except Exception as e:
            pass   # non-fatal — cleanup failure should not stop simulation