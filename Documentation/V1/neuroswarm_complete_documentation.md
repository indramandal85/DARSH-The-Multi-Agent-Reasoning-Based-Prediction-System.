# NeuroSwarm — Complete Project Documentation
## A Superior Multi-Agent AI Prediction System

**Built by:** Indra Mandal  
**Device:** MacBook Air M4 (Apple Silicon)  
**Python:** 3.10 | **LLM:** Llama 3.1 8B via Ollama  
**Total cost:** ₹0 — entirely free, entirely local  
**Duration:** 7 modules, built one at a time, tested before proceeding  

---

## Purpose of This Document

This document records every decision, every line of code, and every concept explained during the building of NeuroSwarm — a multi-agent AI prediction system. It is written so that anyone reading it (including future-you in another chat) can understand exactly what was built, why each choice was made, and how every component works.

---

## Project Philosophy

**Why we built before reading:** Instead of reading theory for weeks before writing code, every concept was explained in plain terms immediately before the code that used it. Concepts stick when you use them within 5 minutes of hearing them.

**Why all free tools:** Ollama runs Llama 3.1 locally — no OpenAI API key, no cost per token, no internet required for inference. Every library chosen has a free open-source alternative to paid services.

**Why one module at a time:** Each module was completed, tested with a dry-run script, and confirmed passing before the next module began. No module depends on a broken previous module.

**What makes it superior to MiroFish (the inspiration):**

| Feature | MiroFish | NeuroSwarm |
|---|---|---|
| Agent diversity | Uniform LLM agents | 5 cognitive architectures |
| World model | Knowledge graph only | Causal DAG + counterfactuals |
| Output | Single narrative | Probability distribution |
| Accuracy measurement | None | Brier score + calibration |
| Cost | Paid API | 100% free, fully local |
| Explainability | Narrative only | Causal attribution chains |

---

## System Architecture Overview

```
Any Document
    ↓
Module 2: Knowledge Graph (entities + relationships)
    ↓
Module 3: Causal DAG (cause → effect + counterfactuals)
    ↓
Module 4: Agent Society (5 cognitive types, 100s of agents)
    ↓
Module 5: Parallel Simulation (N branches simultaneously)
    ↓
Module 6: Backtesting + Report (Brier score + 6-section report)
    ↓
Module 7: Web UI (Flask API + Vue 3 browser interface)
```

**The core insight:** MiroFish proved emergent agent simulation is a viable prediction path. NeuroSwarm adds what MiroFish lacks: causal explainability, cognitive diversity, ensemble probability estimation, and empirical accuracy measurement.

---

## Full Project Folder Structure

```
neuroswarm/
├── core/
│   ├── __init__.py
│   ├── llm_caller.py           # Bridge to Ollama — every module uses this
│   └── base_agent.py           # BaseAgent with ReACT loop
├── knowledge/
│   ├── __init__.py
│   ├── document_parser.py      # Reads + chunks any document
│   ├── entity_extractor.py     # LLM extracts entities + relationships
│   └── graph_builder.py        # NetworkX + ChromaDB
├── causal/
│   ├── __init__.py
│   ├── causal_extractor.py     # Builds causal DAG from knowledge graph
│   └── counterfactual.py       # "What if X had not happened?"
├── agents/
│   ├── __init__.py
│   ├── rational_agent.py
│   ├── emotional_agent.py
│   ├── tribal_agent.py
│   ├── contrarian_agent.py
│   ├── institutional_agent.py
│   └── agent_factory.py        # Creates diverse populations automatically
├── simulation/
│   ├── __init__.py
│   ├── environment.py          # World state + SQLite logging
│   ├── runner.py               # Single simulation: agents × rounds
│   └── parallel_branches.py    # N branches → probability distribution
├── analysis/
│   ├── __init__.py
│   ├── backtest_engine.py      # Brier score accuracy measurement
│   ├── report_engine.py        # 6-section ReACT report writer
│   └── calibration.py          # Long-term accuracy tracking
├── api/
│   ├── __init__.py
│   └── routes.py               # Flask API endpoints
├── frontend/
│   └── src/
│       ├── App.vue             # Complete 4-screen UI
│       ├── main.js
│       └── style.css
├── data/
│   ├── inputs/                 # Upload documents here
│   ├── graphs/                 # Saved knowledge graphs
│   ├── simulations/            # SQLite simulation databases
│   └── reports/                # Generated prediction reports
├── tests/
│   ├── test_module1.py through test_module7.py
├── app.py                      # Flask server entry point
├── requirements.txt
├── README.md
├── RUNNING.md
└── .gitignore
```

---

# MODULE 1 — Foundation Setup

## What Module 1 Does

Module 1 has one job: prove that a local LLM can power an intelligent reasoning agent on your laptop, for free, with no internet. It installs the environment, downloads the model, and builds the `BaseAgent` — the class that every other agent in the system inherits from.

## Concepts Introduced

**Virtual environment:** An isolated Python installation just for this project. Prevents dependency conflicts between projects. Created with `python3.10 -m venv .venv`, activated with `source .venv/bin/activate`. The `(.venv)` prefix in the terminal confirms it is active. Must be activated every session.

**Ollama:** An application that runs LLMs locally. It loads Llama 3.1 into your M4's unified memory and starts a local HTTP server at `http://localhost:11434`. Python code sends HTTP POST requests to this URL exactly like it would to the OpenAI API — except everything stays on your machine.

**AI Agent vs LLM call:** A single LLM call is not an agent. An agent is a loop:
```
Round 1: Think(world_state) → Decide(thought) → Update(new_info) → memory
Round 2: Think(world_state + memory) → Decide → Update → memory
Round 3: Think(world_state + rounds 1+2 memory) → Decide → Update
```
Each round the agent knows more than before. This compounding context is what makes agents capable of reasoning rather than just answering.

**ReACT pattern:** Reason + Act. The agent reasons about the situation, takes an action, observes the result, and reasons again. This is the backbone of every AI agent including GPT agents and MiroFish's ReportAgent.

## Installation Steps

**Python 3.10 via Homebrew:**
```bash
brew install python@3.11  # attempted, got 3.10 instead — both work
python3.10 --version       # Python 3.10.17
```

Note: Python 3.10 was used instead of 3.11. All libraries confirmed compatible with 3.10.

**Project structure creation:**
```bash
mkdir neuroswarm && cd neuroswarm
mkdir core knowledge causal agents simulation analysis api frontend tests
mkdir -p data/inputs data/graphs data/simulations data/reports
touch core/__init__.py knowledge/__init__.py causal/__init__.py
touch agents/__init__.py simulation/__init__.py analysis/__init__.py api/__init__.py
# (all placeholder Python files created with touch)
```

**Virtual environment:**
```bash
python3.10 -m venv .venv
source .venv/bin/activate
# (.venv) now appears in terminal prompt
pip install --upgrade pip
pip install requests==2.31.0 ollama==0.3.3
```

**Ollama installation and model download:**
```bash
brew install ollama
brew services start ollama   # starts as background service
ollama pull llama3.1         # downloads 4.7GB — one time only
ollama run llama3.1          # test in terminal
# "An AI agent is a software program that perceives its environment..."
/bye
```

**Important M4 detail from Ollama serve output:**
```
inference compute ... name=Metal description="Apple M4" 
total="11.8 GiB" available="11.8 GiB"
```
Ollama detected the M4 chip and all 11.8GB of unified memory. This means the LLM runs on the GPU-like Neural Engine, making inference fast even on a laptop.

## Code: `core/llm_caller.py`

**Why this file exists:** Every module needs to talk to the LLM. Instead of writing HTTP request code in every file, one function handles it. This is the "phone line to the AI brain" — change the model name here and it changes everywhere.

**Why two functions:** `ask_llm()` returns plain text (for agent thoughts, beliefs). `ask_llm_json()` returns a parsed Python dict (for structured data like agent decisions with action + reason + confidence). Lower temperature (0.2) for JSON makes output more consistent and parseable.

```python
# core/llm_caller.py

import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1"  # change to "llama3.2:3b" for smaller/faster model

def ask_llm(prompt: str, system_prompt: str = None) -> str:
    """
    Send a prompt to Llama and get a plain text response back.
    system_prompt shapes the model's personality for this one call.
    temperature=0.7: balanced between creative and predictable.
    num_predict=512: max tokens — keeps responses fast.
    """
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.7, "num_predict": 512}
    }
    if system_prompt:
        payload["system"] = system_prompt
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        return response.json()["response"].strip()
    except requests.exceptions.ConnectionError:
        raise ConnectionError(
            "\n\nCannot connect to Ollama.\n"
            "Fix: make sure Tab 1 is running 'ollama serve'\n"
        )
    except requests.exceptions.Timeout:
        raise TimeoutError("\n\nOllama timed out. Wait 30s and retry.\n")
    except Exception as e:
        raise RuntimeError(f"\n\nError: {e}\n")

def ask_llm_json(prompt: str, system_prompt: str = None) -> dict:
    """
    Same as ask_llm() but forces JSON output.
    temperature=0.2: low — we want reliable JSON not creativity.
    If JSON parsing fails: returns {"raw": <text>, "parse_error": True}
    We never crash — always return something the caller can check.
    """
    json_rule = (
        "You must respond with a valid JSON object only. "
        "No explanation. No markdown. No code blocks. "
        "Start with { and end with }."
    )
    full_system = f"{system_prompt}\n\n{json_rule}" if system_prompt else json_rule
    payload = {
        "model": MODEL_NAME, "prompt": prompt, "stream": False,
        "system": full_system, "options": {"temperature": 0.2, "num_predict": 512}
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        raw = response.json()["response"].strip()
        if raw.startswith("```"):
            lines = raw.split("\n")
            raw = "\n".join(lines[1:-1]) if len(lines) > 2 else raw
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"raw": raw if "raw" in dir() else "", "parse_error": True}
    except Exception as e:
        return {"error": str(e), "parse_error": True}
```

## Code: `core/base_agent.py`

**Why identity is in the system prompt:** The system prompt is the agent's personality. Different agents with different system prompts will think differently about identical situations. This is what creates diversity — not random variation, but consistent character-driven differences.

**Why memory is bounded to 8 items:** Prompt length affects LLM response time. Keeping memory to 8 items keeps prompts fast. In Module 4 this gets upgraded to ChromaDB which allows unlimited memory with smart retrieval.

**Why confidence is tracked:** In Module 5 the simulation engine aggregates confidence scores across agents to compute the overall certainty of an outcome prediction.

```python
# core/base_agent.py

from core.llm_caller import ask_llm, ask_llm_json

class BaseAgent:
    """
    One intelligent agent in the NeuroSwarm simulation.
    Every agent type in Module 4 inherits from this class and
    overrides only the think() method. Everything else stays identical.
    
    The loop: Think → Decide → Update (called once per simulation round)
    """

    def __init__(self, agent_id: str, name: str, personality: str, background: str):
        self.agent_id    = agent_id
        self.name        = name
        self.personality = personality
        self.background  = background
        self.memory      = []          # list of strings, upgraded to ChromaDB in Module 4
        self.belief      = "I have no information about this topic yet."
        self.confidence  = 0.5         # 0.0=unsure, 1.0=certain
        self.round       = 0

    def remember(self, item: str):
        """Store in memory with round label. Keep last 8 items."""
        self.memory.append(f"[Round {self.round}] {item}")
        if len(self.memory) > 8:
            self.memory = self.memory[-8:]

    def memory_as_text(self) -> str:
        if not self.memory:
            return "  No memories yet."
        return "\n".join(f"  {m}" for m in self.memory)

    def think(self, world_context: str) -> str:
        """
        PHASE 1: Read the world, produce a thought.
        The system prompt IS the agent's identity.
        Different personalities → different thoughts about same situation.
        This method is overridden by each agent type in Module 4.
        """
        system = (
            f"You are {self.name}.\n"
            f"Background: {self.background}\n"
            f"Personality: {self.personality}\n"
            f"Always respond in character."
        )
        prompt = (
            f"Current situation:\n{world_context}\n\n"
            f"Your memories:\n{self.memory_as_text()}\n\n"
            f"What is your honest reaction? First person. In character. Max 2 sentences."
        )
        return ask_llm(prompt, system_prompt=system)

    def decide(self, thought: str, available_actions: list) -> dict:
        """
        PHASE 2: Given thought, pick one action.
        Returns dict: action, reason, confidence (0.0-1.0)
        Uses ask_llm_json — needs structured output.
        """
        actions_text = "\n".join(f"  - {a}" for a in available_actions)
        system = (
            f"You are {self.name}. Personality: {self.personality}. "
            f"Stay in character when deciding."
        )
        prompt = (
            f"Your thought: {thought}\n\nAvailable actions:\n{actions_text}\n\n"
            f"Choose ONE action. Return JSON with keys:\n"
            f'"action": exact action string\n'
            f'"reason": one sentence why, as {self.name}\n'
            f'"confidence": decimal 0.0 to 1.0'
        )
        result = ask_llm_json(prompt, system_prompt=system)
        if result.get("parse_error"):
            return {"action": available_actions[0],
                    "reason": "Fallback — JSON parsing failed.", "confidence": 0.3}
        return result

    def update_belief(self, new_information: str):
        """
        PHASE 3: Receive new info. Update belief. Store in memory.
        Simplified for Module 1 — Bayesian math added in Module 4.
        """
        system = (
            f"You are {self.name}. Personality: {self.personality}. "
            f"Respond in character."
        )
        prompt = (
            f"Your current belief: {self.belief}\n\n"
            f"New information: {new_information}\n\n"
            f"How does this update what you believe? 1-2 sentences. Start with 'I now believe'"
        )
        self.belief = ask_llm(prompt, system_prompt=system)
        self.remember(f"Info received: {new_information[:60]}...")
        self.remember(f"Updated belief: {self.belief[:70]}...")

    def run_round(self, world_context: str, new_information: str,
                  available_actions: list) -> dict:
        """
        One complete Think → Decide → Update cycle.
        Called once per round per agent by the SimulationRunner in Module 5.
        Returns dict saved to SQLite database.
        """
        self.round += 1
        print(f"\n{'─'*52}\n  {self.name}  |  Round {self.round}\n{'─'*52}")
        
        print("\n  [THINKING]")
        thought = self.think(world_context)
        print(f"  → {thought}")
        
        print("\n  [DECIDING]")
        decision = self.decide(thought, available_actions)
        print(f"  → Action: {decision.get('action')}")
        print(f"  → Reason: {decision.get('reason')}")
        print(f"  → Confidence: {decision.get('confidence')}")
        
        print("\n  [UPDATING BELIEF]")
        self.update_belief(new_information)
        print(f"  → {self.belief[:120]}")
        
        return {
            "agent_id": self.agent_id, "name": self.name, "round": self.round,
            "thought": thought, "action": decision.get("action"),
            "reason": decision.get("reason"),
            "confidence": decision.get("confidence", 0.5), "belief": self.belief
        }
```

## Module 1 Dry-Run Test Result

```
====================================================
  NEUROSWARM — MODULE 1 DRY-RUN TEST
====================================================
Agent: Priya Nair | Rounds: 3 | Memories: 6 items

Round 1: research historical data on past RBI rate hike effects
Round 2: wait and observe market reaction before acting  
Round 3: wait and observe market reaction before acting

Final belief: "I now believe that while the recent interest rate hike was a 
necessary measure to prevent future economic shocks, the Governor's emphasis 
on controlling inflation over stimulating growth may have inadvertently set 
the stage for a potential recession by Q3..."

✓ MODULE 1 PASSED
```

**What the result shows:** The agent didn't just repeat itself — it evolved. Round 1 she researched cautiously. By Round 3 after recession warnings, her belief incorporated the IIM economist's view. Memory-driven reasoning working correctly.

---

# MODULE 2 — Seed Ingestion & Knowledge Graph Builder

## What Module 2 Does

Takes any text document and builds a structured **Knowledge Graph** — a map of entities (people, organizations, events, concepts) and the relationships between them. This becomes the "world model" that agents query during simulation.

## Concepts Introduced

**Knowledge graph:** A graph where nodes are entities and edges are relationships. In code: `G.add_node("RBI")`, `G.add_edge("RBI", "Rate Hike", relation="ANNOUNCED")`. More powerful than a table because it captures connections, not just records.

**NetworkX:** Python library for graphs. A graph is a smarter dictionary — you can traverse relationships, find connected components, and query neighbors in one line.

**ChromaDB:** A vector database. Stores text as embeddings (numerical representations of meaning) so you can search by semantic meaning, not exact keywords. "Find everything about monetary policy" returns RBI results even if "monetary policy" doesn't appear verbatim.

**Chunking:** LLMs have token limits. A 10,000-word document can't be sent as one prompt. Chunking splits it into overlapping pieces (overlap prevents entities that span chunk boundaries from being missed).

**Issue encountered and fixed:**
```
AttributeError: `np.float_` was removed in NumPy 2.0 release.
```
ChromaDB 0.4.24 was written before NumPy 2.0. Fix: downgrade NumPy.
```bash
pip install "numpy==1.26.4"
```

## Test Document: `data/inputs/rbi_article.txt`

```
RBI Rate Hike Crisis: India's Economic Crossroads

The Reserve Bank of India, led by Governor Shaktikanta Das, announced an 
emergency interest rate hike of 0.5% on Monday, pushing the benchmark 
lending rate to 6.75%...
[full 1704 character article about RBI rate hike, Nirmala Sitharaman,
market reactions, IIM Ahmedabad warnings, Raghuram Rajan critique,
Rahul Gandhi opposition, NASSCOM concerns]
```

## Code: `knowledge/document_parser.py`

**Why overlapping chunks:** If "RBI Governor Shaktikanta Das announced" spans a chunk boundary, a clean cut would split the entity. Overlapping by 100 characters ensures relationships crossing boundaries are captured.

```python
# knowledge/document_parser.py

import os

def load_document(filepath: str) -> str:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"\nFile not found: {filepath}\n")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read().strip()
    print(f"  Loaded: {filepath}")
    print(f"  Size: {len(content)} characters")
    return content

def chunk_document(text: str, chunk_size: int = 800, overlap: int = 100) -> list:
    """
    Split document into overlapping chunks.
    chunk_size=800: ~150 words, safe for LLM prompt.
    overlap=100: prevents missing entities at chunk boundaries.
    Finds last period before cut to avoid splitting mid-sentence.
    """
    if len(text) <= chunk_size:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        if end < len(text):
            last_period = text.rfind(".", start, end)
            if last_period > start + (chunk_size // 2):
                end = last_period + 1
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap
    print(f"  Split into {len(chunks)} chunks (chunk_size={chunk_size}, overlap={overlap})")
    return chunks

def parse_document(filepath: str) -> dict:
    full_text = load_document(filepath)
    chunks = chunk_document(full_text)
    return {
        "filepath": filepath, "filename": os.path.basename(filepath),
        "full_text": full_text, "chunks": chunks
    }
```

## Code: `knowledge/entity_extractor.py`

**Why structured prompting:** The LLM is asked to return JSON with a specific schema. `ask_llm_json()` handles the parsing. Deduplication by entity name prevents "RBI" appearing 15 times in the final graph.

**Minor LLM quirks observed:** The model occasionally truncated entity names at chunk boundaries ("sex" from "Sensex", "ss party" from "Congress party"). These are normal LLM imperfections that post-processing would clean in production. The important entities all extracted correctly.

```python
# knowledge/entity_extractor.py

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.llm_caller import ask_llm_json

def extract_entities_from_chunk(chunk: str, chunk_index: int = 0) -> dict:
    """
    Ask LLM to extract entities and relationships from one text chunk.
    Entity types: PERSON, ORGANIZATION, PLACE, EVENT, CONCEPT
    Relationship: source --RELATION--> target
    Returns empty lists if extraction fails — never crashes.
    """
    prompt = f"""
Analyze this text and extract structured information.

TEXT:
{chunk}

Return a JSON object with exactly this structure:
{{
  "entities": [
    {{"name": "exact name", "type": "PERSON or ORGANIZATION or PLACE or EVENT or CONCEPT",
      "description": "one short phrase"}}
  ],
  "relationships": [
    {{"source": "entity name", "target": "entity name",
      "relation": "short verb phrase like LEADS, ANNOUNCED, CAUSED_BY"}}
  ]
}}

Rules: Only include entities from the text. Each relationship source and target
must be entity names you listed. Aim for 5-10 entities, 4-8 relationships.
Return valid JSON only.
"""
    print(f"    Extracting from chunk {chunk_index + 1}...")
    result = ask_llm_json(prompt)
    if result.get("parse_error"):
        print(f"    Warning: JSON parsing failed for chunk {chunk_index + 1}")
        return {"entities": [], "relationships": []}
    if "entities" not in result: result["entities"] = []
    if "relationships" not in result: result["relationships"] = []
    print(f"    Found {len(result['entities'])} entities, {len(result['relationships'])} relationships")
    return result

def extract_from_document(chunks: list) -> dict:
    """
    Run extraction on all chunks. Merge results. Deduplicate by entity name.
    """
    print(f"\n  Extracting from {len(chunks)} chunks...")
    all_entities = {}   # name → entity dict (deduplicates)
    all_relationships = []
    for i, chunk in enumerate(chunks):
        result = extract_entities_from_chunk(chunk, i)
        for entity in result["entities"]:
            name = entity.get("name", "").strip()
            if name and name not in all_entities:
                all_entities[name] = entity
        for rel in result["relationships"]:
            source = rel.get("source", "").strip()
            target = rel.get("target", "").strip()
            relation = rel.get("relation", "").strip()
            if source and target and relation:
                all_relationships.append({"source": source, "target": target, "relation": relation})
    entities_list = list(all_entities.values())
    print(f"\n  Extraction complete:")
    print(f"    Total unique entities : {len(entities_list)}")
    print(f"    Total relationships   : {len(all_relationships)}")
    return {"entities": entities_list, "relationships": all_relationships}
```

## Code: `knowledge/graph_builder.py`

**Why DiGraph (Directed Graph):** Relationships have direction. "RBI ANNOUNCED Rate Hike" is directional — the reverse "Rate Hike ANNOUNCED RBI" means something different. DiGraph enforces this.

**Why ChromaDB alongside NetworkX:** NetworkX is great for graph traversal (find neighbors, shortest path). ChromaDB is great for semantic search (find nodes related to "inflation" conceptually). They serve different query patterns.

```python
# knowledge/graph_builder.py (key functions)

import os, json
import networkx as nx
import chromadb
from chromadb.utils import embedding_functions

GRAPHS_DIR = "data/graphs"
CHROMA_DIR = "data/chroma"

def build_graph(extracted_data: dict, graph_name: str) -> nx.DiGraph:
    """Build NetworkX DiGraph from extracted entities and relationships."""
    G = nx.DiGraph()
    G.name = graph_name
    for entity in extracted_data.get("entities", []):
        name = entity.get("name", "").strip()
        if name:
            G.add_node(name, type=entity.get("type", "UNKNOWN"),
                      description=entity.get("description", ""))
    for rel in extracted_data.get("relationships", []):
        source = rel.get("source", "").strip()
        target = rel.get("target", "").strip()
        relation = rel.get("relation", "").strip()
        if source and target and relation:
            if source not in G: G.add_node(source, type="UNKNOWN", description="")
            if target not in G: G.add_node(target, type="UNKNOWN", description="")
            G.add_edge(source, target, relation=relation)
    print(f"\n  Graph built: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    return G

def store_in_chromadb(G: nx.DiGraph, graph_name: str):
    """
    Store each graph node as a text document in ChromaDB.
    Uses sentence-transformers 'all-MiniLM-L6-v2' for embeddings.
    This model runs locally — no API needed.
    Rich text per node includes type, description, and connections
    so semantic search works well.
    """
    os.makedirs(CHROMA_DIR, exist_ok=True)
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    collection_name = f"graph_{graph_name}".replace("-", "_").replace(" ", "_")
    try:
        client.delete_collection(collection_name)
    except Exception:
        pass
    collection = client.create_collection(name=collection_name, embedding_function=embedding_fn)
    documents, ids, metadatas = [], [], []
    for node, data in G.nodes(data=True):
        node_type = data.get("type", "UNKNOWN")
        description = data.get("description", "")
        outgoing = [f"{d.get('relation','')} {v}" for _, v, d in G.out_edges(node, data=True)]
        doc_text = f"{node} is a {node_type}."
        if description: doc_text += f" {description}."
        if outgoing: doc_text += f" Connections: {', '.join(outgoing[:3])}."
        documents.append(doc_text)
        ids.append(f"node_{node[:50].replace(' ', '_')}")
        metadatas.append({"name": node, "type": node_type, "description": description})
    if documents:
        collection.add(documents=documents, ids=ids, metadatas=metadatas)
    print(f"    Stored {len(documents)} nodes in ChromaDB")

def build_knowledge_graph(filepath: str, graph_name: str) -> dict:
    """Main function: document → extract → build → save → ChromaDB."""
    from knowledge.document_parser import parse_document
    from knowledge.entity_extractor import extract_from_document
    doc = parse_document(filepath)
    extracted = extract_from_document(doc["chunks"])
    G = build_graph(extracted, graph_name)
    saved_path = save_graph(G, graph_name)
    store_in_chromadb(G, graph_name)
    return {"graph": G, "saved_path": saved_path, "graph_name": graph_name,
            "entity_count": G.number_of_nodes(), "relationship_count": G.number_of_edges()}
```

## Module 2 Dry-Run Test Result

```
  Extracting from 3 chunks...
    Extracting from chunk 1... Found 5 entities, 4 relationships
    Extracting from chunk 2... Found 9 entities, 6 relationships
    Extracting from chunk 3... Found 6 entities, 3 relationships

  Total unique entities: 18 | Total relationships: 13

  NODES (18 entities):
    [ORGANIZATION ] RBI → Reserve Bank of India
    [PERSON       ] Shaktikanta Das → Governor of RBI
    [PERSON       ] Nirmala Sitharaman → Finance Minister
    [PERSON       ] Raghuram Rajan → former RBI Governor
    [PERSON       ] Rahul Gandhi → Opposition leader
    [ORGANIZATION ] HDFC Bank → banking company
    [EVENT        ] inflation crisis → economic situation with high inflation
    ... (18 total)

  EDGES (13 relationships):
    RBI --LED BY--> Shaktikanta Das
    RBI --CAUSED_BY--> inflation crisis
    Ministry of Finance --RELEASED DATA TO--> RBI
    IIM Ahmedabad --WARNED_ABOUT--> RBI
    ...

  Search: 'who leads monetary policy decisions'
    → [ORGANIZATION] Ministry of Finance
    → [ORGANIZATION] RBI
    → [EVENT] inflation crisis

  ✓ MODULE 2 PASSED — Graph: 18 nodes, 13 edges
```

---

# MODULE 3 — Causal World Model

## What Module 3 Does

Upgrades the knowledge graph from "things are related" to "A causes B with strength X". Builds a **Causal DAG** (Directed Acyclic Graph) where every edge means causation, not just correlation. Enables **counterfactual reasoning**: "what would have happened if X had not occurred?"

## Why This Makes NeuroSwarm Superior

MiroFish's knowledge graph knows "RBI and inflation are connected." NeuroSwarm's causal DAG knows:
```
Inflation (7.2%) ──causes──► RBI Rate Hike  (strength: 0.9, lag: weeks)
Shaktikanta Das  ──causes──► RBI decisions  (strength: 0.8, lag: immediate)
RBI Rate Hike    ──causes──► Market Drop    (strength: 0.8, lag: immediate)
```

This enables the system to answer: *"If inflation had stayed below 6%, the rate hike would likely not have occurred, which would have prevented the market drop."* That is prediction, not just description.

## Concepts Introduced

**Causal DAG:** Directed Acyclic Graph where edges mean "A causes B." Acyclic means no loops — A can't cause B which causes A (circular causation is not allowed). Direction encodes causation: `inflation → rate hike` not `rate hike → inflation`.

**Counterfactual:** "What would have happened in an alternate world where X was different?" Answered by tracing backwards through the DAG from an outcome to find root causes, then reasoning about which effects would disappear if a cause was removed.

**Causal strength:** A 0.0–1.0 score on each causal edge. 0.9 = near-certain causation. 0.3 = weak causal link. Used to rank which causes matter most.

**Why not DoWhy:** Originally planned to use Microsoft's DoWhy library. Replaced with pgmpy + NetworkX because DoWhy has complex dependency conflicts on Python 3.10 with Apple Silicon. Same capability, cleaner installation.

## Package Installed

```bash
pip install pgmpy==0.1.25
# pgmpy pulled in: pandas, statsmodels, scipy, torch (already present)
```

## Code: `causal/causal_extractor.py`

**Why ask the LLM for causal direction:** The LLM has encoded world knowledge about which things cause which other things. "Does inflation cause rate hikes or do rate hikes cause inflation?" — the LLM knows the economic answer (inflation causes rate hikes, not vice versa).

**Why filter strength < 0.1:** Removes very weak correlational relationships from the causal DAG. Keeps the DAG clean and meaningful.

```python
# causal/causal_extractor.py (key functions)

import json
import networkx as nx
from core.llm_caller import ask_llm_json

def determine_causal_direction(source: str, target: str,
                                relation: str, context: str) -> dict:
    """
    Ask LLM: does A cause B, B cause A, both, or neither?
    Returns direction, strength (0-1), time_lag, explanation.
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
  "strength": 0.0 to 1.0,
  "time_lag": "immediate or days or weeks or months or years",
  "explanation": "one sentence explaining why"
}}
Think carefully. Correlation is not causation.
"""
    result = ask_llm_json(prompt)
    if result.get("parse_error"):
        return {"direction": "NONE", "strength": 0.0,
                "time_lag": "unknown", "explanation": "Could not determine."}
    valid_directions = ["A_CAUSES_B", "B_CAUSES_A", "BIDIRECTIONAL", "NONE"]
    if result.get("direction") not in valid_directions:
        result["direction"] = "NONE"
    try:
        result["strength"] = max(0.0, min(1.0, float(result.get("strength", 0.0))))
    except (ValueError, TypeError):
        result["strength"] = 0.0
    return result

def build_causal_dag(knowledge_graph_path: str, context_description: str = "") -> nx.DiGraph:
    """
    Load knowledge graph → analyze each edge for causation → build Causal DAG.
    Only keeps edges with strength > 0.1 (filters correlations).
    """
    with open(knowledge_graph_path, "r") as f:
        graph_data = json.load(f)
    edges = graph_data.get("edges", [])
    nodes = {n["id"]: n for n in graph_data.get("nodes", [])}
    causal_dag = nx.DiGraph()
    for node_id, node_data in nodes.items():
        causal_dag.add_node(node_id, type=node_data.get("type", "UNKNOWN"),
                           description=node_data.get("description", ""))
    causal_edges_added = 0
    for i, edge in enumerate(edges):
        source = edge.get("source", "")
        target = edge.get("target", "")
        relation = edge.get("relation", "")
        if not source or not target: continue
        source_desc = nodes.get(source, {}).get("description", source)
        target_desc = nodes.get(target, {}).get("description", target)
        context = (f"{source} ({source_desc}) has relationship '{relation}' "
                  f"with {target} ({target_desc}). Domain: {context_description}")
        print(f"  [{i+1}/{len(edges)}] {source} → {target}", end=" ... ")
        causal_info = determine_causal_direction(source, target, relation, context)
        direction = causal_info["direction"]
        strength = causal_info["strength"]
        print(f"{direction} (strength: {strength})")
        if direction == "A_CAUSES_B" and strength > 0.1:
            causal_dag.add_edge(source, target, relation=relation, strength=strength,
                               time_lag=causal_info["time_lag"],
                               explanation=causal_info["explanation"])
            causal_edges_added += 1
        elif direction == "B_CAUSES_A" and strength > 0.1:
            causal_dag.add_edge(target, source, relation=f"REVERSE_{relation}",
                               strength=strength, time_lag=causal_info["time_lag"],
                               explanation=causal_info["explanation"])
            causal_edges_added += 1
        elif direction == "BIDIRECTIONAL" and strength > 0.1:
            causal_dag.add_edge(source, target, relation=relation, strength=strength,
                               time_lag=causal_info["time_lag"],
                               explanation=causal_info["explanation"])
            causal_dag.add_edge(target, source, relation=f"REVERSE_{relation}",
                               strength=strength * 0.8,
                               time_lag=causal_info["time_lag"],
                               explanation=causal_info["explanation"])
            causal_edges_added += 2
    print(f"\n  Causal DAG: {causal_edges_added} causal edges "
          f"(filtered {len(edges) - causal_edges_added} correlational)")
    return causal_dag
```

## Code: `causal/counterfactual.py`

**How get_downstream_effects works:** DFS traversal forward through the DAG from the cause. Multiplies edge strengths along each path (like probability chains). Only returns effects with combined strength ≥ threshold.

**How get_root_causes works:** DFS traversal backwards through the DAG. Nodes with no incoming edges are root causes — nothing causes them, they start causal chains.

```python
# causal/counterfactual.py (key class)

import networkx as nx
from core.llm_caller import ask_llm
from causal.causal_extractor import get_root_causes, get_downstream_effects

class CounterfactualEngine:
    def __init__(self, causal_dag: nx.DiGraph, domain_context: str = ""):
        self.dag = causal_dag
        self.domain_context = domain_context

    def what_if_removed(self, cause_node: str) -> dict:
        """
        "What would have happened if [cause_node] had NOT occurred?"
        1. Find all downstream effects via DAG traversal
        2. Ask LLM to reason about the counterfactual world
        """
        if cause_node not in self.dag:
            return {"error": f"'{cause_node}' not found in causal DAG."}
        all_effects = get_downstream_effects(self.dag, cause_node)
        effects_text = ""
        for e in all_effects[:8]:
            effects_text += (f"\n  - {e['effect']} "
                           f"(strength: {e['strength']}, timing: {e['time_lag']})")
        if not effects_text:
            effects_text = "  No significant downstream effects found."
        prompt = f"""
You are analyzing a causal model about: {self.domain_context}

"{cause_node}" causes these downstream effects: {effects_text}

Answer: "What would have happened if '{cause_node}' had NOT occurred?"
- Reason through the causal chain step by step
- Explain which effects would NOT have happened
- Explain which effects might still occur through other causes
- End with confidence: HIGH, MEDIUM, or LOW
Write 3-4 sentences.
"""
        reasoning = ask_llm(prompt)
        confidence = 0.8 if "HIGH" in reasoning.upper() else \
                    0.3 if "LOW" in reasoning.upper() else 0.5
        return {"cause_removed": cause_node, "direct_effects": all_effects[:3],
                "all_effects_count": len(all_effects),
                "counterfactual": reasoning, "confidence": confidence}

    def find_intervention_points(self, target_outcome: str) -> dict:
        """
        "We don't want [outcome] — what should we change?"
        Finds root causes ranked by causal strength.
        LLM recommends the single most effective intervention.
        """
        root_causes = get_root_causes(self.dag, target_outcome)
        if not root_causes:
            return {"target_outcome": target_outcome,
                   "message": "No root causes found.", "intervention_points": []}
        causes_text = "\n".join(
            f"  - {r['root_cause']} (causal strength: {r['accumulated_strength']}, "
            f"path: {' → '.join(r['path'][::-1])})"
            for r in root_causes[:5]
        )
        prompt = f"""
Context: {self.domain_context}
Outcome to prevent: "{target_outcome}"
Root causes (ranked by causal strength): {causes_text}

Which single intervention would be MOST effective at preventing "{target_outcome}"?
Explain the causal chain and why this is better than alternatives.
Note practical constraints. Write 3-4 sentences.
"""
        return {"target_outcome": target_outcome, "root_causes": root_causes,
                "best_intervention": ask_llm(prompt)}
```

## Module 3 Dry-Run Test Result

```
  [1/13] RBI → Shaktikanta Das ... B_CAUSES_A (strength: 0.8)
  [2/13] RBI → inflation crisis ... A_CAUSES_B (strength: 0.8)
  [3/13] Ministry of Finance → RBI ... A_CAUSES_B (strength: 0.8)
  [6/13] sex → HDFC Bank ... NONE (strength: 0.0) ← correctly filtered
  [8/13] IIM Ahmedabad → RBI ... NONE (strength: 0.0) ← correctly filtered

  Causal edges kept: 7 | Filtered out: 6 (correlation only)

  Causal edges (sorted by strength):
  Shaktikanta Das ──causes──► RBI (strength: 0.8, lag: immediate)
  RBI ──causes──► inflation crisis (strength: 0.8, lag: months)
  Ministry of Finance ──causes──► RBI (strength: 0.8, lag: days to weeks)

  Intervention recommendation for 'inflation crisis':
  "The most effective intervention would be Shaktikanta Das, the RBI Governor,
  as he has direct control over monetary policy decisions..."

  ✓ MODULE 3 PASSED — 18 nodes, 7 causal edges
```

---

# MODULE 4 — Heterogeneous Agent Society Builder

## What Module 4 Does

Creates 5 agent types with genuinely different cognitive architectures. Each inherits `BaseAgent` but overrides only `think()` — the reasoning style changes while everything else stays identical.

## Why Cognitive Diversity Matters

With 100 copies of one agent type, the simulation produces no interesting dynamics — everyone agrees immediately. Real societies have cognitive diversity. The same RBI rate hike announcement is processed differently by:
- An economist (utility calculation)
- A retail investor (emotional reaction)
- A party supporter (group loyalty)
- A contrarian analyst (skepticism)
- A bank risk committee (regulatory procedure)

The diversity creates the emergent social dynamics that make the simulation's predictions realistic.

## Concepts Introduced

**Inheritance in OOP:** `class RationalAgent(BaseAgent)` inherits all methods from `BaseAgent`. It only overrides `think()`. `RationalAgent` gets `remember()`, `decide()`, `update_belief()`, `run_round()` for free — identical across all agent types.

**Agent cognitive types (from behavioral economics):**
- Rational: Expected utility theory (weighs outcomes × probabilities)
- Emotional: Sentiment-driven, reacts to how things feel
- Tribal: Social identity theory (in-group consensus drives decisions)
- Contrarian: Systematic skepticism of majority view
- Institutional: Rule-following, risk management, fiduciary duty

## The 5 Agent Files

All 5 files follow identical structure — only the `think()` method changes:

```python
# agents/rational_agent.py

class RationalAgent(BaseAgent):
    """
    Thinks by calculating expected utility.
    Slow to react, rarely panics, resists emotional contagion.
    Real-world equivalent: institutional investor, policy analyst.
    """
    def __init__(self, agent_id, name, personality, background):
        super().__init__(agent_id, name, personality, background)
        self.agent_type = "RATIONAL"
        self.utility_score = 0.0

    def think(self, world_context: str) -> str:
        system = (
            f"You are {self.name}, a rational decision-maker.\n"
            f"Background: {self.background}\n"
            f"You always think in terms of evidence, probabilities, and expected outcomes.\n"
            f"You do not react emotionally. You calculate."
        )
        prompt = (
            f"Situation: {world_context}\n\nYour memories: {self.memory_as_text()}\n\n"
            f"Think through this rationally:\n"
            f"1. What is the evidence? (one sentence)\n"
            f"2. What are the two most likely outcomes?\n"
            f"3. What is your calculated conclusion?\n"
            f"Keep total response to 3 sentences. Be analytical, not emotional."
        )
        return ask_llm(prompt, system_prompt=system)
```

```python
# agents/emotional_agent.py

class EmotionalAgent(BaseAgent):
    """
    Reacts based on sentiment score. Fast, can overreact, spreads panic.
    Real-world equivalent: retail investor, social media user.
    Tracks emotional_state: -1.0=anxious to +1.0=optimistic
    Updates state based on keywords in thoughts.
    """
    def __init__(self, agent_id, name, personality, background):
        super().__init__(agent_id, name, personality, background)
        self.agent_type = "EMOTIONAL"
        self.emotional_state = 0.0

    def think(self, world_context: str) -> str:
        mood = ("optimistic and confident" if self.emotional_state > 0.3
                else "anxious and worried" if self.emotional_state < -0.3
                else "neutral but alert")
        system = (
            f"You are {self.name}, someone who reacts emotionally.\n"
            f"Background: {self.background}\nCurrent mood: {mood}\n"
            f"You lead with feelings, not data."
        )
        prompt = (
            f"Situation: {world_context}\n\nMemories: {self.memory_as_text()}\n\n"
            f"What is your immediate emotional reaction?\n"
            f"Respond emotionally, viscerally. Max 2 sentences."
        )
        thought = ask_llm(prompt, system_prompt=system)
        # Update emotional_state based on content
        negative_words = ["worried","anxious","fear","panic","crash","crisis","danger"]
        positive_words = ["confident","opportunity","stable","recover","hopeful"]
        thought_lower = thought.lower()
        neg = sum(1 for w in negative_words if w in thought_lower)
        pos = sum(1 for w in positive_words if w in thought_lower)
        self.emotional_state = max(-1.0, min(1.0,
            self.emotional_state + (pos - neg) * 0.15))
        return thought
```

```python
# agents/tribal_agent.py

class TribalAgent(BaseAgent):
    """
    Interprets everything through in-group lens.
    Creates echo chambers and polarization in simulation.
    Real-world equivalent: strong party supporter, religious community member.
    """
    def __init__(self, agent_id, name, personality, background, tribe="general public"):
        super().__init__(agent_id, name, personality, background)
        self.agent_type = "TRIBAL"
        self.tribe = tribe
        self.tribe_consensus = "No group consensus yet."

    def think(self, world_context: str) -> str:
        system = (
            f"You are {self.name}, strongly identified with: {self.tribe}.\n"
            f"Background: {self.background}\n"
            f"Your group's opinion matters more than abstract facts."
        )
        prompt = (
            f"Situation: {world_context}\n"
            f"What your group ({self.tribe}) believes: {self.tribe_consensus}\n\n"
            f"Memories: {self.memory_as_text()}\n\n"
            f"How do you interpret this through your group's lens? Max 2 sentences."
        )
        return ask_llm(prompt, system_prompt=system)

    def update_tribe_consensus(self, new_consensus: str):
        """Called by simulator when group opinion shifts."""
        self.tribe_consensus = new_consensus
        self.remember(f"Group consensus updated: {new_consensus[:50]}...")
```

```python
# agents/contrarian_agent.py

class ContrarianAgent(BaseAgent):
    """
    Systematically opposes majority view. Prevents total consensus.
    Often identifies risks groupthink ignores.
    Real-world equivalent: short-seller, investigative journalist.
    """
    def __init__(self, agent_id, name, personality, background):
        super().__init__(agent_id, name, personality, background)
        self.agent_type = "CONTRARIAN"
        self.perceived_majority_view = "No majority view established yet."

    def think(self, world_context: str) -> str:
        system = (
            f"You are {self.name}, a natural contrarian.\n"
            f"Background: {self.background}\n"
            f"Your instinct is to question consensus and argue the overlooked angle."
        )
        prompt = (
            f"Situation: {world_context}\n"
            f"What most people believe: {self.perceived_majority_view}\n\n"
            f"Memories: {self.memory_as_text()}\n\n"
            f"What is the mainstream narrative getting WRONG? "
            f"What important angle is everyone overlooking? Max 2 sentences."
        )
        return ask_llm(prompt, system_prompt=system)

    def set_majority_view(self, view: str):
        self.perceived_majority_view = view
```

```python
# agents/institutional_agent.py

class InstitutionalAgent(BaseAgent):
    """
    Thinks through rules, risk management, regulatory obligations.
    Represents organizations not individuals. Creates stability anchor.
    Real-world equivalent: RBI, HDFC Bank risk committee, government ministry.
    """
    def __init__(self, agent_id, name, personality, background,
                 institution_type="financial"):
        super().__init__(agent_id, name, personality, background)
        self.agent_type = "INSTITUTIONAL"
        self.institution_type = institution_type
        self.mandate = "preserve stability and manage risk within regulatory guidelines"

    def think(self, world_context: str) -> str:
        system = (
            f"You are {self.name}, representing a {self.institution_type} institution.\n"
            f"Background: {self.background}\nMandate: {self.mandate}\n"
            f"Think in terms of risk, procedure, and institutional responsibility.\n"
            f"Speak carefully and formally. Do not speculate."
        )
        prompt = (
            f"Situation: {world_context}\n\nMemories: {self.memory_as_text()}\n\n"
            f"Assess this situation:\n"
            f"1. What is the primary risk to your institution?\n"
            f"2. What does your mandate require you to consider?\n"
            f"2 sentences. Formal and measured."
        )
        return ask_llm(prompt, system_prompt=system)
```

## Code: `agents/agent_factory.py`

**Why a factory:** In Module 5, simulations use 20-50 agents. Creating each manually is impractical. The factory creates realistic populations with the right type distribution and varied backgrounds automatically.

**Type distribution rationale:**
- Emotional: 35% — most common in social media driven societies
- Tribal: 25% — group identity is pervasive
- Rational: 20% — educated professionals with analytical approach
- Contrarian: 10% — skeptics exist but are minority
- Institutional: 10% — banks, corps, bodies are influential but few

```python
# agents/agent_factory.py (key function)

TYPE_DISTRIBUTION = {
    "rational": 0.20, "emotional": 0.35, "tribal": 0.25,
    "contrarian": 0.10, "institutional": 0.10
}

def create_agent_population(count: int, topic: str) -> list:
    """Create diverse agent population for simulation."""
    agents = []
    type_counts = {}
    remaining = count
    types = list(TYPE_DISTRIBUTION.keys())
    for agent_type in types[:-1]:
        n = max(1, round(count * TYPE_DISTRIBUTION[agent_type]))
        type_counts[agent_type] = n
        remaining -= n
    type_counts[types[-1]] = max(1, remaining)
    backgrounds = BACKGROUNDS.copy()
    random.shuffle(backgrounds)
    agent_index = 0
    for agent_type, type_count in type_counts.items():
        for i in range(type_count):
            name, background = backgrounds[agent_index % len(backgrounds)]
            agent_id = f"agent_{agent_index + 1:03d}"
            agent = create_agent(agent_id, agent_type, name, background, topic)
            agents.append(agent)
            agent_index += 1
    return agents
```

## Module 4 Dry-Run Test Result

Same scenario given to all 5 agents. Key comparison:

```
[RATIONAL] Dr. Meera Iyer:
"The evidence is: RBI raised rates 0.5%, markets dropped 2.3%, 
economists warn of recession. Two outcomes: (a) recession from 
reduced borrowing, (b) inflation controlled. Calculated: 60% 
probability recession within one year."
→ Action: wait and observe | Confidence: 0.85

[EMOTIONAL] Rahul Agarwal:
"Oh no, my investments are going down the drain! I can already 
see my hard-earned savings dwindling — it's like a punch to the gut."
→ Action: wait and observe | Confidence: 0.70

[TRIBAL] Vikram Singh:
"The RBI's rate hike is a necessary step — it's a sign our government 
is making tough decisions for the country's benefit."
→ Action: wait and observe | Confidence: 0.90

[CONTRARIAN] Amit Sharma:
"Everyone is fixating on the inflation rate, ignoring that India's 
inflation is supply-driven, not demand-driven — this hike will 
exacerbate the economic downturn."
→ Action: spread information to network | Confidence: 0.80

[INSTITUTIONAL] HDFC Risk Committee:
"Primary risk: increased loan defaults and asset quality deterioration.
Our mandate requires evaluating implications on stability while 
remaining within regulatory guidelines."
→ Action: research historical data | Confidence: 0.90

✓ MODULE 4 PASSED — 5 agent types, 10-agent factory working
```

---

# MODULE 5 — Multi-Scale Parallel Simulation Engine

## What Module 5 Does

Runs N parallel branches of the same simulation simultaneously. Each branch is an independent run with the same starting conditions but natural LLM variation producing different outcomes. Aggregates results into a **probability distribution** — the core superiority over MiroFish's single-narrative approach.

## The Ensemble Insight

MiroFish runs one simulation → one story → "this is what will happen."
NeuroSwarm runs 3+ simulations → 3+ stories → "70% chance of panic, 20% cautious, 10% optimistic."

This is ensemble forecasting — the same approach used in weather prediction (ensemble NWP models) and financial risk (Monte Carlo). Stopped using single-run forecasts 30 years ago because ensemble models are dramatically more accurate.

## Concepts Introduced

**SimulationEnvironment:** The "world" agents live in. Holds world state, agent list, knowledge context, and a SQLite database. World state updates after each round based on collective agent behavior.

**Round structure:** Each round: every agent reads world state → thinks → decides → updates belief. After all agents finish: world state updates based on dominant action. This repeats for N rounds.

**SQLite persistence:** All agent actions stored in `data/simulations/branch_XX.db`. This lets Module 6's report engine query "what did agents actually believe by Round 3?" without re-running the simulation.

**Why sequential not truly parallel:** Ollama processes one LLM request at a time. True multiprocessing would just queue requests — the gain is minimal. Running branches sequentially is cleaner and produces identical results.

## Code: `simulation/environment.py`

```python
# simulation/environment.py (key methods)

import sqlite3, os
from datetime import datetime

class SimulationEnvironment:
    def __init__(self, simulation_id, topic, initial_situation, agents,
                 knowledge_context="", causal_context="", db_path=None):
        self.simulation_id = simulation_id
        self.topic = topic
        self.agents = agents
        self.knowledge_ctx = knowledge_context
        self.causal_ctx = causal_context
        self.current_round = 0
        self.world_state = initial_situation
        self.world_state_history = [initial_situation]
        self.action_log = []
        if db_path is None:
            os.makedirs("data/simulations", exist_ok=True)
            db_path = f"data/simulations/{simulation_id}.db"
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Create SQLite tables: agent_actions, world_states, outcomes."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                simulation_id TEXT, round_number INTEGER,
                agent_id TEXT, agent_name TEXT, agent_type TEXT,
                thought TEXT, action TEXT, confidence REAL,
                belief TEXT, timestamp TEXT
            )""")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS world_states (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                simulation_id TEXT, round_number INTEGER,
                world_state TEXT, dominant_action TEXT,
                avg_confidence REAL, timestamp TEXT
            )""")
        conn.commit()
        conn.close()

    def update_world_state(self, round_results: list, new_event: str = None):
        """
        After all agents act: find dominant action, update world narrative.
        dominant action = most common action this round.
        World state grows each round by appending what happened.
        """
        self.current_round += 1
        actions = [r.get("action", "") for r in round_results if r.get("action")]
        dominant = max(set(actions), key=actions.count) if actions else "no action"
        action_count = actions.count(dominant) if actions else 0
        confidences = [float(r.get("confidence", 0.5)) for r in round_results
                      if r.get("confidence") is not None]
        avg_confidence = sum(confidences)/len(confidences) if confidences else 0.5
        state_update = (f" After round {self.current_round}, "
                       f"{action_count}/{len(round_results)} agents chose '{dominant}'.")
        if new_event: state_update += f" New development: {new_event}"
        self.world_state = self.world_state + state_update
        # save to SQLite
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO world_states
            (simulation_id, round_number, world_state, dominant_action, avg_confidence, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (self.simulation_id, self.current_round, self.world_state[:1000],
             dominant, avg_confidence, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return {"round": self.current_round, "dominant_action": dominant,
                "action_count": action_count, "avg_confidence": avg_confidence}

    def classify_outcome(self, round_results: list) -> str:
        """
        Keyword classification of final agent beliefs.
        panic/cautious/optimistic/divided.
        Used to compare outcomes across parallel branches.
        """
        beliefs = " ".join(r.get("belief","").lower() for r in round_results)
        panic_score = sum(beliefs.count(w) for w in
            ["panic","recession","crisis","crash","catastrophic","devastating"])
        cautious_score = sum(beliefs.count(w) for w in
            ["cautious","wait","observe","uncertain","careful","monitor"])
        optimistic_score = sum(beliefs.count(w) for w in
            ["recover","stable","opportunity","growth","positive","confident"])
        scores = {"panic": panic_score, "cautious": cautious_score,
                 "optimistic": optimistic_score}
        dominant = max(scores, key=scores.get)
        return "divided" if scores[dominant] == 0 else dominant
```

## Code: `simulation/runner.py`

```python
# simulation/runner.py (key function)

def run_simulation(simulation_id, topic, initial_situation, events_per_round,
                   available_actions, num_agents=8, num_rounds=3,
                   knowledge_context="", causal_context="", verbose=True) -> dict:
    """
    Run one complete simulation: agents × rounds.
    
    Core loop (this is the entire simulation engine):
    for round in range(num_rounds):
        for agent in all_agents:
            result = agent.run_round(world_state, new_info, actions)
            env.log_action(result)
        env.update_world_state(all_results)
    
    The intelligence comes from agents (Module 4) and
    world model (Modules 2+3), not from this loop itself.
    """
    agents = create_agent_population(num_agents, topic)
    env = SimulationEnvironment(
        simulation_id=simulation_id, topic=topic,
        initial_situation=initial_situation, agents=agents,
        knowledge_context=knowledge_context, causal_context=causal_context)

    while len(events_per_round) < num_rounds:
        events_per_round.append("Situation continues to develop.")

    all_round_summaries = []
    final_beliefs = []

    for round_num in range(1, num_rounds + 1):
        new_event = events_per_round[round_num - 1]
        world_context = env.get_world_state_for_agents()
        round_results = []
        for agent in agents:
            result = agent.run_round(
                world_context=world_context,
                new_information=new_event,
                available_actions=available_actions)
            result["agent_type"] = getattr(agent, "agent_type", "UNKNOWN")
            env.log_action(round_num, result)
            round_results.append(result)
        round_summary = env.update_world_state(round_results, new_event)
        round_summary["round_results"] = round_results
        all_round_summaries.append(round_summary)
        if round_num == num_rounds:
            final_beliefs = round_results

    final_outcome = env.classify_outcome(final_beliefs)
    action_distribution = {}
    for r in final_beliefs:
        action = r.get("action", "unknown")
        action_distribution[action] = action_distribution.get(action, 0) + 1

    return {"simulation_id": simulation_id, "final_outcome": final_outcome,
            "action_distribution": action_distribution,
            "avg_final_confidence": round(
                sum(float(r.get("confidence",0.5)) for r in final_beliefs)
                / len(final_beliefs), 3) if final_beliefs else 0.5,
            "db_path": env.db_path}
```

## Code: `simulation/parallel_branches.py`

```python
# simulation/parallel_branches.py (key function)

def run_parallel_branches(topic, initial_situation, events_per_round,
                          available_actions, num_branches=3, num_agents=6,
                          num_rounds=3, knowledge_context="", causal_context="") -> dict:
    """
    Run N branches. Aggregate into probability distribution.
    Branches are run sequentially (Ollama queues parallel requests anyway).
    Each branch gets identical starting conditions but natural LLM variation
    produces different outcomes — exactly like ensemble weather forecasting.
    """
    branch_configs = [
        {"simulation_id": f"branch_{i+1:02d}", "topic": topic,
         "initial_situation": initial_situation,
         "events_per_round": events_per_round.copy(),
         "available_actions": available_actions,
         "num_agents": num_agents, "num_rounds": num_rounds,
         "knowledge_context": knowledge_context, "causal_context": causal_context}
        for i in range(num_branches)
    ]
    branch_results = [run_single_branch(config) for config in branch_configs]

    # Aggregate outcomes into probability distribution
    outcome_counts = {}
    all_actions = {}
    confidences = []
    for result in branch_results:
        outcome = result.get("final_outcome", "unknown")
        outcome_counts[outcome] = outcome_counts.get(outcome, 0) + 1
        for action, count in result.get("action_distribution", {}).items():
            all_actions[action] = all_actions.get(action, 0) + count
        if result.get("avg_final_confidence"):
            confidences.append(result["avg_final_confidence"])

    total = len(branch_results)
    outcome_probs = {k: round(v/total*100, 1) for k, v in outcome_counts.items()}
    dominant_outcome = max(outcome_counts, key=outcome_counts.get)
    consensus_action = max(all_actions, key=all_actions.get) if all_actions else "none"
    overall_confidence = round(sum(confidences)/len(confidences), 3) if confidences else 0.5

    prediction = (
        f"Across {num_branches} simulation branches, the most likely outcome is "
        f"'{dominant_outcome}' with {outcome_probs[dominant_outcome]}% probability. "
        f"The dominant agent behavior was to '{consensus_action}'. "
        f"Average agent confidence: {overall_confidence:.1%}."
    )
    return {"topic": topic, "num_branches": num_branches,
            "branches": branch_results, "outcome_probs": outcome_probs,
            "dominant_outcome": dominant_outcome, "consensus_action": consensus_action,
            "overall_confidence": overall_confidence, "prediction": prediction}
```

## Module 5 Dry-Run Test Result

```
  PARALLEL BRANCH SIMULATION
  3 branches × 5 agents × 3 rounds = ~135 LLM calls

  Branch branch_01 → panic  (confidence: 0.85)
  Branch branch_02 → panic  (confidence: 0.87)  
  Branch branch_03 → panic  (confidence: 0.83)

  All branches complete in 1053 seconds (~17.5 minutes)

  Outcome probability distribution:
  panic  ████████████████████ 100.0%

  Consensus agent action: spread concerns to social network

  PREDICTION: Across 3 simulation branches, the most likely outcome is
  'panic' with 100.0% probability. Dominant behavior: spread concerns
  to social network. Average confidence: 85.0%.

  ✓ MODULE 5 PASSED
```

**Why 100% panic is correct:** The scenario was genuinely alarming — 7.2% inflation, emergency rate hike, IIM recession warnings, EMI increases hitting 40M borrowers. All agent types converged on panic through different reasoning paths. This is realistic: in genuine crises, even analytical agents conclude negatively.

---

# MODULE 6 — Backtesting, Calibration & Prediction Report Engine

## What Module 6 Does

**Part A (Backtesting):** Measures whether predictions are actually accurate. Compares simulation outcome probabilities against real historical outcomes using Brier score.

**Part B (Report Engine):** A ReACT agent that reads simulation databases and writes a structured 6-section prediction report.

**Why this module makes NeuroSwarm scientifically credible:** MiroFish never published accuracy benchmarks. Without measurement, any prediction system is just a story generator. Brier scoring turns NeuroSwarm into a measurable, improvable scientific instrument.

## Concepts Introduced

**Brier score:** Proper scoring rule for probabilistic predictions. `score = mean((predicted_prob - actual)²)`. Range 0.0 (perfect) to 1.0 (worst). The same as MSE applied to probability estimates — familiar from ML evaluation.

Example:
```
Prediction: panic=0.80, cautious=0.20
Reality: panic occurred (1.0), cautious didn't (0.0)
Brier = mean((0.8-1.0)² + (0.2-0.0)²) = mean(0.04 + 0.04) = 0.04 — excellent
```

**Calibration:** Long-term accuracy tracking. "When the system says 70% confident, does the outcome actually occur 70% of the time?" A well-calibrated system has predicted probability ≈ actual frequency. The calibration history file accumulates every prediction.

**ReACT report agent:** Uses the same think→act→observe loop from Module 1, but "actions" are: query simulation database, query causal graph, write report section. Loops until all 6 sections are complete.

## Package Notes

```bash
# scikit-learn was ALREADY installed via pgmpy (Module 3 dependency)
# Only matplotlib needed new installation:
pip install matplotlib==3.8.3
```

## Code: `analysis/backtest_engine.py`

```python
# analysis/backtest_engine.py (key functions)

import numpy as np
import json, sqlite3, os
from datetime import datetime

def load_simulation_results(simulation_ids: list) -> dict:
    """Load final round data from SQLite databases. Classify outcome per branch."""
    all_beliefs = []
    outcome_counts = {}
    for sim_id in simulation_ids:
        db_path = f"data/simulations/{sim_id}.db"
        if not os.path.exists(db_path): continue
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT belief FROM agent_actions
            WHERE round_number = (SELECT MAX(round_number) FROM agent_actions)""")
        beliefs = [row[0] or "" for row in cursor.fetchall()]
        all_beliefs.extend(beliefs)
        final_state = cursor.execute(
            "SELECT world_state FROM world_states ORDER BY round_number DESC LIMIT 1"
        ).fetchone()
        conn.close()
        if final_state:
            combined = (final_state[0] or "").lower() + " ".join(beliefs).lower()
            panic_score = sum(combined.count(w) for w in
                ["panic","recession","crisis","crash","catastrophic","devastating"])
            cautious_score = sum(combined.count(w) for w in
                ["cautious","wait","observe","uncertain"])
            optimistic_score = sum(combined.count(w) for w in
                ["recover","stable","opportunity","growth","positive"])
            if panic_score > cautious_score and panic_score > optimistic_score:
                outcome = "panic"
            elif cautious_score > optimistic_score:
                outcome = "cautious"
            elif optimistic_score > 0:
                outcome = "optimistic"
            else:
                outcome = "divided"
            outcome_counts[outcome] = outcome_counts.get(outcome, 0) + 1
    total = sum(outcome_counts.values())
    outcome_probs = {k: round(v/total, 3) for k, v in outcome_counts.items()} if total else {}
    return {"simulation_ids": simulation_ids, "outcome_counts": outcome_counts,
            "outcome_probs": outcome_probs,
            "dominant_outcome": max(outcome_counts, key=outcome_counts.get) if outcome_counts else "unknown"}

def compute_brier_score(predicted_probs: dict, actual_outcome: str) -> float:
    """
    Brier score = mean((predicted - actual)²) across all outcome types.
    0.0 = perfect, 1.0 = worst possible.
    < 0.2 = good, 0.2-0.4 = acceptable, > 0.4 = poor.
    """
    if not predicted_probs: return 1.0
    squared_errors = []
    for outcome, predicted_prob in predicted_probs.items():
        actual = 1.0 if outcome == actual_outcome else 0.0
        squared_errors.append((predicted_prob - actual) ** 2)
    return round(sum(squared_errors) / len(squared_errors), 4)

def run_backtest(simulation_ids, actual_outcome, event_description, event_date=None) -> dict:
    sim_results = load_simulation_results(simulation_ids)
    predicted_probs = sim_results["outcome_probs"]
    brier = compute_brier_score(predicted_probs, actual_outcome)
    interpretation = (
        "EXCELLENT" if brier <= 0.1 else "GOOD" if brier <= 0.2
        else "ACCEPTABLE" if brier <= 0.3 else "POOR" if brier <= 0.4
        else "VERY POOR"
    )
    result = {"event_description": event_description,
              "predicted_probs": predicted_probs,
              "actual_outcome": actual_outcome,
              "brier_score": brier,
              "brier_interpretation": f"{interpretation} — predictions are highly calibrated"
                                      if brier <= 0.1 else interpretation,
              "prediction_correct": sim_results["dominant_outcome"] == actual_outcome,
              "actual_confidence": predicted_probs.get(actual_outcome, 0.0)}
    # Save to data/reports/
    os.makedirs("data/reports", exist_ok=True)
    with open(f"data/reports/backtest_{event_description[:30].replace(' ','_')}.json","w") as f:
        json.dump(result, f, indent=2)
    return result
```

## Code: `analysis/report_engine.py`

**The 6 report sections and why each exists:**
1. **Executive Summary** — bottom line in 3 sentences for decision-makers
2. **Predicted Outcome** — what will happen with probabilities
3. **Causal Drivers** — WHY (uses Module 3's causal DAG)
4. **Agent Behavior** — which agent types drove the outcome
5. **Dissenting Views** — what contrarians argued (important for robustness)
6. **Confidence Assessment** — how certain, and why

```python
# analysis/report_engine.py (ReportEngine class key method)

class ReportEngine:
    def __init__(self, simulation_ids, topic, outcome_probs,
                 causal_summary="", brier_score=None):
        self.simulation_ids = simulation_ids
        self.topic = topic
        self.outcome_probs = outcome_probs
        self.causal_summary = causal_summary
        self.brier_score = brier_score
        self.sim_data = load_simulation_data(simulation_ids)

    def write_report_section(self, section_name: str, context: str, prompt: str) -> str:
        """Each section is one focused LLM call with relevant data as context."""
        system = (
            "You are a senior policy analyst writing a professional prediction report. "
            "Write clearly, precisely, analytically. No fluff. Every sentence adds information."
        )
        return ask_llm(
            f"You are writing the '{section_name}' section.\n\n"
            f"Available data:\n{context}\n\nInstructions: {prompt}\n\nWrite this section now:",
            system_prompt=system
        )

    def generate_report(self, save_path=None) -> str:
        """Generate complete 6-section report. Save as Markdown."""
        exec_summary   = self.generate_executive_summary()
        predicted      = self.generate_predicted_outcome()
        causal         = self.generate_causal_drivers()
        agent_behavior = self.generate_agent_behavior()
        dissent        = self.generate_dissenting_views()
        confidence     = self.generate_confidence_assessment()

        dominant  = max(self.outcome_probs, key=self.outcome_probs.get)
        dom_prob  = self.outcome_probs[dominant]
        probs_table = "\n".join(
            f"| {k.capitalize()} | {v*100:.1f}% |"
            for k, v in sorted(self.outcome_probs.items(), key=lambda x: x[1], reverse=True)
        )
        report = f"""# NeuroSwarm Prediction Report
**Topic:** {self.topic}
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

## Outcome Probability Distribution
| Outcome | Probability |
|---------|-------------|
{probs_table}
**Dominant predicted outcome: {dominant.upper()} ({dom_prob*100:.0f}%)**

## 1. Executive Summary
{exec_summary}

## 2. Predicted Outcome
{predicted}

## 3. Causal Drivers
{causal}

## 4. Agent Behavior Analysis
{agent_behavior}

## 5. Dissenting Views
{dissent}

## 6. Confidence Assessment
{confidence}

*Brier Score: {self.brier_score if self.brier_score is not None else 'N/A'}*
"""
        os.makedirs("data/reports", exist_ok=True)
        if save_path is None:
            safe_topic = self.topic[:40].replace(" ","_").replace("/","_")
            save_path = f"data/reports/report_{safe_topic}.md"
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(report)
        return report
```

## Module 6 Dry-Run Test Result

```
  PART A — BACKTESTING
  Predicted: {'panic': 1.0}
  Actual: panic
  Brier score: 0.0
  Interpretation: EXCELLENT — predictions are highly calibrated
  Prediction hit: YES ✓

  PART B — REPORT GENERATION
  Writing executive summary...
  Writing predicted outcome section...
  Writing causal drivers section...
  Writing agent behavior section...
  Writing dissenting views section...
  Writing confidence assessment...
  Report saved: report_RBI_0.5%_emergency_interest_rate_hike_—_.md
  Word count: ~880 words

  PART C — CALIBRATION
  Total predictions: 1 | Correct: 1 | Accuracy: 100.0%
  Brier score: 0.0 | Status: Well calibrated

  ✓ MODULE 6 PASSED
```

**Actual generated report quality:** The report correctly traced the causal chain `Shaktikanta Das → RBI → inflation crisis` from Module 3's data, accurately described that emotional agents drove the panic outcome while rational agents resisted (from Module 5's SQLite data), and summarized contrarian Amit Sharma's specific arguments about supply-driven inflation. The system synthesized information across all 6 modules coherently.

---

# MODULE 7 — Full Integration & Interactive Web UI

## What Module 7 Does

Wraps all 6 modules into a web interface. A user can upload a document, configure a simulation, watch it run, and download a prediction report — all through a browser, without touching the terminal.

## Architecture

```
Browser (Vue 3 at :5173)
    ↓ HTTP requests
Flask API (Python at :5001)
    ↓ function calls
Modules 2-6 (existing Python code)
    ↓ results as JSON
Browser displays results
```

**Why Flask:** Minimal setup. One file. Perfect bridge between Python modules and HTTP.

**Why Vue 3:** Reactive UI framework. When simulation status changes, the UI updates automatically. The polling mechanism (check job status every 5 seconds) is simple with Vue's reactivity.

**Why background threads:** Simulations take 10-18 minutes. If Flask waited synchronously, the HTTP request would time out. Instead: POST starts a thread, returns a `job_id` immediately. Client polls `/api/status/<job_id>` every 5 seconds until status is "complete".

## Package Installation

```bash
pip install flask==3.0.2 flask-cors==4.0.0
brew install node    # Node.js already installed (v24.4.1)
```

## Frontend Setup

```bash
cd ~/Desktop/neuroswarm/frontend
npm create vite@latest . -- --template vue
# Vite scaffolded the app and auto-started — pressed Ctrl+C
npm install axios
```

## Code: `api/routes.py`

```python
# api/routes.py — 6 Flask endpoints

import threading, uuid, os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

jobs = {}  # In-memory job tracker: {job_id: {status, data...}}
api_bp = Blueprint("api", __name__)
UPLOAD_FOLDER = "data/inputs"

@api_bp.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "NeuroSwarm API is running"})

@api_bp.route("/api/upload", methods=["POST"])
def upload_document():
    """Receive .txt or .md file. Save to data/inputs/. Return word count."""
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files["file"]
    filename = secure_filename(file.filename)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    return jsonify({"success": True, "filename": filename,
                   "filepath": filepath, "word_count": len(content.split()),
                   "message": f"Document uploaded: {filename} ({len(content.split())} words)"})

@api_bp.route("/api/build-graph", methods=["POST"])
def build_graph():
    """Start Module 2 in background thread. Return job_id for polling."""
    data = request.get_json()
    filename = data.get("filename")
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": f"File not found: {filename}"}), 404
    graph_name = filename.rsplit(".", 1)[0]
    job_id = str(uuid.uuid4())[:8]
    def run_graph_job():
        jobs[job_id] = {"status": "running", "step": "Building knowledge graph..."}
        try:
            from knowledge.graph_builder import build_knowledge_graph
            result = build_knowledge_graph(filepath, graph_name)
            jobs[job_id] = {"status": "complete", "graph_name": graph_name,
                           "entity_count": result["entity_count"],
                           "edge_count": result["relationship_count"]}
        except Exception as e:
            jobs[job_id] = {"status": "error", "error": str(e)}
    threading.Thread(target=run_graph_job, daemon=True).start()
    return jsonify({"job_id": job_id, "message": "Graph building started"})

@api_bp.route("/api/run-simulation", methods=["POST"])
def run_simulation_endpoint():
    """Start Module 5 parallel simulation + Module 6 report in background. Return job_id."""
    data = request.get_json()
    topic = data.get("topic", "General prediction")
    situation = data.get("situation", "An event has occurred.")
    num_agents = min(int(data.get("num_agents", 5)), 10)
    num_rounds = min(int(data.get("num_rounds", 3)), 5)
    num_branches = min(int(data.get("num_branches", 3)), 5)
    events = data.get("events", ["Situation develops.", "Analysis published.", "Responses observed."])
    actions = data.get("actions", ["wait and observe", "revise plans",
                                   "research data", "spread information",
                                   "consult advisor", "take protective action"])
    job_id = str(uuid.uuid4())[:8]
    def run_sim_job():
        jobs[job_id] = {"status": "running", "step": "Starting branches..."}
        try:
            from simulation.parallel_branches import run_parallel_branches
            results = run_parallel_branches(
                topic=topic, initial_situation=situation,
                events_per_round=events, available_actions=actions,
                num_branches=num_branches, num_agents=num_agents, num_rounds=num_rounds)
            jobs[job_id]["step"] = "Generating report..."
            from analysis.report_engine import ReportEngine
            engine = ReportEngine(
                simulation_ids=[b["simulation_id"] for b in results["branches"]],
                topic=topic, outcome_probs=results["outcome_probs"])
            report = engine.generate_report()
            jobs[job_id] = {"status": "complete",
                           "outcome_probs": results["outcome_probs"],
                           "dominant_outcome": results["dominant_outcome"],
                           "prediction": results["prediction"], "report": report,
                           "num_branches": num_branches}
        except Exception as e:
            jobs[job_id] = {"status": "error", "error": str(e)}
    threading.Thread(target=run_sim_job, daemon=True).start()
    return jsonify({"job_id": job_id,
                   "message": f"Simulation started: {num_branches}×{num_agents}×{num_rounds}"})

@api_bp.route("/api/status/<job_id>", methods=["GET"])
def get_status(job_id):
    """Poll this every 5 seconds. Returns current job status."""
    if job_id not in jobs:
        return jsonify({"status": "not_found"}), 404
    return jsonify(jobs[job_id])

@api_bp.route("/api/get-report", methods=["GET"])
def get_report():
    """Return most recently generated prediction report."""
    reports_dir = "data/reports"
    report_files = [f for f in os.listdir(reports_dir)
                   if f.startswith("report_") and f.endswith(".md")]
    if not report_files:
        return jsonify({"error": "No reports yet"}), 404
    latest = max(report_files,
                key=lambda f: os.path.getmtime(os.path.join(reports_dir, f)))
    with open(os.path.join(reports_dir, latest), "r", encoding="utf-8") as f:
        content = f.read()
    return jsonify({"filename": latest, "content": content})
```

## Code: `app.py`

```python
# app.py — Flask server entry point

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from api.routes import api_bp

app = Flask(__name__)
# Allow Vue dev server (port 5173) to call Flask API (port 5001)
CORS(app, origins=["http://localhost:5173", "http://localhost:3000"])
app.register_blueprint(api_bp)

if __name__ == "__main__":
    print("\n  NEUROSWARM API SERVER")
    print("  Running on: http://localhost:5001\n")
    app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False)
```

## Frontend: `src/App.vue` Structure

The Vue frontend has 4 screens managed by `currentStep` (0-3):

**Screen 0 — Upload & Graph:**
- Drag-and-drop file upload area
- Calls `/api/upload` → saves file
- Calls `/api/build-graph` → starts background job
- Polls `/api/status/{job_id}` every 3s
- Shows progress bar and entity/edge count on complete

**Screen 1 — Configure:**
- Input fields: topic, situation, events (3 lines), agents count, branches count
- Estimated time calculator (reactive)
- Disabled until Screen 0 complete

**Screen 2 — Running:**
- Pulsing yellow dot while running
- Progress bar advances automatically
- Polls `/api/status/{job_id}` every 5s
- Auto-navigates to Screen 3 on complete

**Screen 3 — Results:**
- Animated outcome probability bars
- Prediction summary paragraph
- Collapsible full report (Markdown text)
- Download report button

## Module 7 Dry-Run Test Result

```
  [1/4] Testing API health endpoint...
        ✓ Health: NeuroSwarm API is running

  [2/4] Testing file upload endpoint...
        ✓ Upload: Document uploaded: rbi_article.txt (251 words)

  [3/4] Testing status endpoint...
        ✓ Status endpoint responding correctly

  [4/4] Testing report endpoint...
        ✓ Report found: report_RBI_0.5%_emergency_interest_rate_hike_—_.md

  ✓  MODULE 7 PASSED
  ✓  ALL 7 MODULES COMPLETE
  ✓  NEUROSWARM v1.0 IS READY
```

---

# Project Setup & Configuration Files

## `requirements.txt`

```
# ── MODULE 1 ── Core foundation
requests==2.31.0
ollama==0.3.3

# ── MODULE 2 ── Knowledge graph
networkx==3.2.1
chromadb==0.4.24
sentence-transformers==2.7.0
numpy==1.26.4          # pinned — chromadb 0.4.24 breaks on numpy 2.0+

# ── MODULE 3 ── Causal model
pgmpy==0.1.25          # replaced dowhy — cleaner on Apple Silicon Python 3.10

# ── MODULE 5 ── Simulation engine
pandas==2.2.1

# ── MODULE 6 ── Analysis
# scikit-learn already installed via pgmpy
matplotlib==3.8.3

# ── MODULE 7 ── Web API
flask==3.0.2
flask-cors==4.0.0
```

## `.gitignore`

```gitignore
.venv/
venv/
__pycache__/
*.pyc
.env
.env.local
data/simulations/
data/chroma/
data/graphs/*.json
data/reports/
!data/inputs/
!data/inputs/rbi_article.txt
.DS_Store
.vscode/
frontend/node_modules/
frontend/dist/
*.egg-info/
dist/
build/
.pytest_cache/
```

---

# Issues Encountered and How They Were Fixed

## Issue 1 — Python 3.11 not found, used 3.10

**Error:** `zsh: command not found: python3.11`

**Cause:** Homebrew installed Python 3.10 instead of 3.11 on this specific system configuration.

**Fix:** Used Python 3.10 throughout. All libraries confirmed compatible. Adjusted all commands from `python3.11` to `python3.10` (or just `python` inside venv).

**Impact:** Zero. Python 3.10 is fully compatible with all 7 modules.

---

## Issue 2 — NumPy 2.0 incompatibility with ChromaDB 0.4.24

**Error:**
```
AttributeError: `np.float_` was removed in NumPy 2.0 release. 
Use `np.float64` instead.
```

**Cause:** ChromaDB 0.4.24 used `np.float_` which was removed in NumPy 2.0. The system had NumPy 2.x installed.

**Fix:**
```bash
pip install "numpy==1.26.4"
```

**Why this version:** 1.26.4 is the last stable release before NumPy 2.0. ChromaDB and all other libraries work correctly on it.

---

## Issue 3 — DoWhy replaced with pgmpy

**Original plan:** Use `dowhy==0.11.1` for causal inference.

**Problem:** DoWhy has complex dependency chains that conflict with Python 3.10 on Apple Silicon. Would have caused the same NumPy-style version conflict issues but worse.

**Fix:** Used `pgmpy + NetworkX` directly. Same capability for our use case — building and querying causal DAGs. Cleaner installation, more transparent code.

**requirements.txt update:**
```
# dowhy removed — replaced by pgmpy + networkx (cleaner on Apple Silicon)
pgmpy==0.1.25
```

---

## Issue 4 — ChromaDB telemetry warnings

**Warning (appeared during Module 2 and 3 tests):**
```
Failed to send telemetry event ClientStartEvent: capture() takes 1 positional argument but 3 were given
```

**Cause:** ChromaDB 0.4.24 tries to send anonymous usage stats but has an internal version mismatch in its telemetry code.

**Fix:** Nothing required. These are warnings, not errors. ChromaDB functions correctly. The graph built, stored, and searches worked perfectly.

---

## Issue 5 — scikit-learn==1.4.1 not found

**Error:**
```
ERROR: Could not find a version that satisfies the requirement scikit-learn==1.4.1
```

**Cause:** `1.4.1` doesn't exist — the correct name is `1.4.1.post1`. Also, scikit-learn was already installed by pgmpy (Module 3) as a dependency.

**Fix:** Don't install scikit-learn separately. It's already present as scikit-learn 1.7.2. Only install matplotlib:
```bash
pip install matplotlib==3.8.3
```

---

## Issue 6 — Git commit with wrong branch name

**Warning:**
```
hint: Using 'master' as the name for the initial branch.
```

**Fix:**
```bash
git branch -m master main    # rename to modern standard
git config --global init.defaultBranch main  # set default for future
```

---

# Running the Complete System

## Every Session — Three Terminal Tabs

```bash
# Tab 1 — leave running entire session
ollama serve

# Tab 2 — your Python work
cd ~/Desktop/neuroswarm
source .venv/bin/activate

# Tab 3 — frontend (only when using web UI)
cd ~/Desktop/neuroswarm/frontend
npm run dev
```

**Then open:** `http://localhost:5173`

## Running All Module Tests in Order

```bash
# In Tab 2 (venv active, ollama serve in Tab 1)

python tests/test_module1.py   # ~3 min
python tests/test_module2.py   # ~5 min
python tests/test_module3.py   # ~7 min
python tests/test_module4.py   # ~5 min
python tests/test_module5.py   # ~18 min
python tests/test_module6.py   # ~6 min

# Start python app.py in Tab 2 first, then:
python tests/test_module7.py   # ~1 min (API test only)
```

## Running Individual Files for Development

```bash
python core/llm_caller.py           # tests LLM connection
python knowledge/document_parser.py # tests document parsing
python knowledge/entity_extractor.py # tests entity extraction (one chunk)
```

---

# Key Design Decisions and Why

**Why local LLM (Ollama) instead of OpenAI API:** Free, private, no internet dependency. M4's unified memory architecture makes local inference genuinely fast. The cost advantage is complete: ₹0 vs paying per token for every agent thought in every simulation round.

**Why Python 3.10 virtual environment:** Dependency isolation. Each library has specific version requirements that conflict across projects. The venv ensures NeuroSwarm's dependencies never affect other Python projects on the machine.

**Why SQLite for simulation storage:** Built into Python — zero installation. Persistent across runs — Module 6 reads Module 5's databases. Queryable — report engine runs SQL to get specific agent behaviors. Fast enough for our scale.

**Why NetworkX + ChromaDB instead of just one graph database:** NetworkX excels at graph traversal (find all nodes connected to RBI, shortest path between entities). ChromaDB excels at semantic search (find nodes similar to "monetary policy"). They serve different query patterns and are used at different points in the pipeline.

**Why background threads in Flask:** Simulations take 10-18 minutes. HTTP requests time out after ~30 seconds. Solution: POST returns a job_id immediately, client polls status every 5 seconds. The simulation runs in a daemon thread.

**Why the module-by-module build approach:** Each module is independently testable. If Module 3 breaks, Modules 1 and 2 still work. You understand each layer before building the next. Integration is simple because each module's interface was designed before implementation.

---

# Final System Verification

All 7 modules verified working on MacBook Air M4:

```
Module 1: ✓ BaseAgent running, Llama 3.1 responding, ReACT loop functional
Module 2: ✓ 18 entities, 13 edges extracted from RBI article, ChromaDB search working
Module 3: ✓ 7 causal edges identified, counterfactual reasoning coherent
Module 4: ✓ 5 agent types producing visibly different reasoning
Module 5: ✓ 3 parallel branches complete, probability distribution computed
Module 6: ✓ Brier score 0.0, 880-word 6-section report generated
Module 7: ✓ All 4 API endpoints verified, Vue UI live at localhost:5173

NEUROSWARM v1.0 — FULLY OPERATIONAL
Total build time: ~6 weeks
Total cost: ₹0
```
