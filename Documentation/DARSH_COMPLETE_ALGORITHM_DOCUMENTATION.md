# DARSH — Complete Algorithm and Python Implementation Documentation

**Project:** DARSH  
**Codebase audit basis:** live repository code as of 2026-03-22  
**Primary runtime:** Python 3.10 + Flask + Ollama + Vue frontend  
**Primary deployment mode:** local-first, locally runnable, zero paid inference API cost when paired with local models through Ollama

---

## 1. What DARSH Is, In One Technical Sentence

DARSH is a local-first behavioral intelligence system that converts raw scenario text, live news, or historical event dossiers into a graph-grounded world model, simulates heterogeneous agents over structured rounds and branches, aggregates belief distributions into forecast probabilities, and renders the result as a reportable, inspectable decision workbench.

---

## 2. Design Principles Behind The Algorithm

1. **Local-first by default**  
   The LLM bridge points to Ollama, graph memory uses ChromaDB locally, simulations log to local SQLite files, and reports are written to the repo.

2. **Zero paid API cost at runtime**  
   The main app is designed to run with local models. No cloud inference API is required for the normal DARSH path.

3. **Graph memory before agent reasoning**  
   DARSH does not ask agents to reason from raw text alone. It first extracts entities, relations, and optionally causal structure.

4. **Probability distributions instead of single answers**  
   Belief is represented as a distribution over `panic`, `cautious`, `optimistic`, and `divided`, not a single hard label.

5. **Branching instead of one “future”**  
   Multiple branches are run and aggregated, so DARSH produces a forecast surface, not a single narrative.

6. **Explanation as a first-class output**  
   The system preserves graph structure, round logs, thought traces, market overlays, track record data, and report sections.

---

## 3. End-to-End Algorithm

```text
Input Source
  ├─ Upload (.txt / .md / .pdf)
  ├─ Live RSS topic fetch
  └─ Historical backtest dossier
          ↓
Normalization + parsing + chunking
          ↓
Chunk-level entity / relation extraction with local LLM
          ↓
Validation + deduplication + contextual edge augmentation
          ↓
Directed knowledge graph + local semantic graph memory
          ↓
Optional causal DAG and counterfactual surface
          ↓
Market-role-aware heterogeneous agent population
          ↓
Round loop:
  think → decide → update belief → remember
          ↓
Social network propagation + world-state logging
          ↓
Parallel branches across rounds
          ↓
Branch aggregation → forecast distribution
          ↓
Market impact model + population-weighted cohort model
          ↓
6-section report + PDF export + track record + interactive follow-up
```

### Step-by-step algorithm

1. **Input ingestion**  
   Documents arrive through upload, RSS ingestion, or historical document loading.

2. **Normalization**  
   Markdown is stripped, PDFs are converted to text, filenames are sanitized, and a normalized `.txt` is created under `data/inputs/`.

3. **Chunking**  
   The text is split into overlapping chunks so entities and relations near boundaries are not lost.

4. **Structured extraction**  
   Each chunk is sent to the local model with a JSON-only prompt requesting entities and relationships.

5. **Validation**  
   Hallucinated entities, substring bugs, bad types, fuzzy duplicates, and broken relationship endpoints are filtered.

6. **Graph build**  
   Validated entities become nodes and validated relationships become directed edges in NetworkX. The graph is saved as JSON and also indexed in ChromaDB for semantic retrieval.

7. **Optional causal upgrade**  
   Knowledge-graph edges are reinterpreted as causal candidates. The model scores direction, strength, and lag, producing a causal DAG.

8. **Agent population creation**  
   DARSH composes cognition style and market role to create a heterogeneous population with distinct backgrounds, speeds, constraints, and sources.

9. **Simulation rounds**  
   For each round, every agent sees current world context, reads social feed, thinks in character, chooses an action, updates belief with Bayesian math, and stores memory.

10. **World update**  
    The environment aggregates agent behavior into a new world-state narrative and logs all actions and world states to SQLite.

11. **Branch aggregation**  
    Multiple branches are run with the same initial conditions but natural LLM divergence. Outcome frequencies and smoothed belief distributions are aggregated.

12. **Post-processing**  
    DARSH maps outcomes into market regime, sector impacts, population-weighted cohort views, backtest scores, track records, and grounded reports.

---

## 4. Folder Map

| Folder | Responsibility |
| --- | --- |
| `api/` | Flask endpoints, file normalization, background-job orchestration |
| `core/` | LLM bridge and shared agent loop |
| `knowledge/` | Parsing, extraction, validation, graph build, graph merge, news ingestion |
| `causal/` | Causal DAG construction and counterfactual reasoning |
| `agents/` | Agent subclasses, belief math, semantic memory, market-role overlays |
| `simulation/` | Environment, round engine, social graph, branch aggregation, simulation chat |
| `analysis/` | Reporting, backtesting, calibration, market mapping, population weighting, PDF export |
| `market/` | Market ontology and preset template rendering |
| `tests/` | Regression tests, module dry-runs, v2/v3 phase tests |

---

## 5. Root Entrypoints

### `app.py`

**What**  
The main Flask entrypoint for the original DARSH app.

**Why**  
It exposes the live API and serves the real frontend build.

**How**  
It registers the `api_bp` blueprint, enables CORS for the Vue dev server, and serves `frontend/dist/index.html` in production mode.

**Key snippet**

```python
app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "http://localhost:3000"])
app.register_blueprint(api_bp)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    dist_dir = os.path.join(os.path.dirname(__file__), "frontend", "dist")
    if path and os.path.exists(os.path.join(dist_dir, path)):
        return send_from_directory(dist_dir, path)
    return send_from_directory(dist_dir, "index.html")
```

### `app_demo.py`

**What**  
Static demo server entrypoint.

**Why**  
It gives a presentation-ready walkthrough without booting the real graph/simulation backend.

**How**  
It serves `frontend/dist/demo.html` and returns a helpful `503` if the frontend build is missing.

---

## 6. `api/` Folder

### File-by-file map

| File | What | Why | How / Key Anchors |
| --- | --- | --- | --- |
| `api/__init__.py` | Package marker | Makes `api` importable | Empty initializer |
| `api/document_utils.py` | Upload normalization utilities | Ensures all sources become clean `.txt` inputs | `allowed_file`, `normalize_uploaded_file`, `_extract_pdf_text`, `_strip_markdown` |
| `api/routes.py` | Flask API surface | Connects frontend actions to graph build, simulation, report, history, merge, and chat | `upload_document`, `fetch_news`, `load_historical`, `build_graph`, `run_simulation_endpoint`, `get_status`, `get_graph`, `merge_graphs_endpoint` |

### Deep note — `api/document_utils.py`

**What**  
Converts uploaded `.txt`, `.md`, or `.pdf` files into a normalized text artifact.

**Why**  
The downstream graph builder assumes a stable text input. This module removes document-format variability before any extraction begins.

**How**

1. Save the original uploaded file into `data/inputs/originals/`.
2. Decode or extract text depending on extension.
3. Strip markdown syntax when needed.
4. Normalize whitespace and line breaks.
5. Write a clean `.txt` version back into `data/inputs/`.

**Representative snippet**

```python
def normalize_uploaded_file(file_storage, upload_folder: str) -> dict:
    os.makedirs(upload_folder, exist_ok=True)
    original_name = file_storage.filename or "uploaded_document.txt"
    source_ext = (original_name.rsplit(".", 1)[1].lower() if "." in original_name else "txt")
    source_path = _write_source_file(file_storage, upload_folder, original_name)

    if source_ext == "pdf":
        text_content = _extract_pdf_text(source_path)
    else:
        with open(source_path, "rb") as handle:
            raw = handle.read()
        text_content = _decode_text(raw)

    normalized_text = _normalize_content(text_content, source_ext)
```

### Deep note — `api/routes.py`

**What**  
The orchestration layer for the original app.

**Why**  
The frontend needs one stable contract to trigger long-running jobs and retrieve results incrementally.

**How**

- Uses a process-local `jobs` dictionary to track background work.
- Starts graph-building and simulation tasks in daemon threads so HTTP requests return immediately.
- Updates job status progressively for the frontend polling loop.
- Exposes graph history, replay, merge, PDF export, scoring, and interactive simulation chat.

**Representative snippet**

```python
jobs[job_id] = {
    "status": "running",
    "step": f"Starting {num_branches} simulation branches...",
    "live_focus": {...}
}

results = run_parallel_branches(
    topic=topic,
    initial_situation=situation,
    events_per_round=events,
    available_actions=actions,
    num_branches=num_branches,
    num_agents=num_agents,
    num_rounds=num_rounds,
    event_type=event_type,
    causal_dag_path=inferred_causal_dag_path or None,
    status_callback=update_live_focus
)
```

**Core API families**

- **Input:** upload, fetch live news, load historical documents
- **Graph:** build graph, fetch graph JSON, list graphs, merge graphs
- **Simulation:** run simulation, poll status, get simulation history, get round detail
- **Analysis:** get report, export PDF, score prediction, track record
- **Interaction:** simulation chat, event templates, health check

---

## 7. `core/` Folder

### File-by-file map

| File | What | Why | How / Key Anchors |
| --- | --- | --- | --- |
| `core/__init__.py` | Package marker | Makes `core` importable | Empty initializer |
| `core/llm_caller.py` | Local LLM bridge | Centralizes every Ollama call and hardens JSON parsing | `_coerce_json_object`, `ask_llm`, `ask_llm_json` |
| `core/base_agent.py` | Shared agent loop | Encodes the simulation’s canonical `think → decide → update_belief → remember` pattern | `think`, `decide`, `update_belief`, `run_round` |

### Deep note — `core/llm_caller.py`

**What**  
DARSH’s only direct bridge to the model runtime.

**Why**  
Without a single gateway, JSON parsing, timeouts, and system-prompt behavior would drift across modules.

**How**

- `ask_llm()` handles plain-text generations.
- `ask_llm_json()` forces JSON mode and tries multiple recovery strategies when model output drifts.
- The helper stack strips markdown fences, `<think>` blocks, trailing commas, and extracts balanced JSON objects.

**Representative snippet**

```python
payload = {
    "model": MODEL_NAME,
    "prompt": prompt,
    "stream": False,
    "format": "json",
    "system": full_system,
    "options": {
        "temperature": 0.0,
        "num_predict": 768
    }
}

raw = response.json()["response"].strip()
parsed = _coerce_json_object(raw)
```

### Deep note — `core/base_agent.py`

**What**  
The canonical DARSH agent.

**Why**  
A single LLM call is not a behavior model. DARSH agents persist memory, belief, and round-to-round evolution.

**How**

1. `think()` builds a role/personality prompt around world context, relevant memory, and optional social feed.
2. `decide()` requests a structured JSON action choice.
3. `update_belief()` asks the model for likelihoods and then applies Bayesian math.
4. `run_round()` ties everything together and returns a structured result payload.

**Representative snippet**

```python
thought = self.think(world_context, social_feed=social_feed)
decision = self.decide(thought, available_actions)
self.update_belief(
    new_information,
    thought=thought,
    decision=decision,
    world_context=world_context
)
```

---

## 8. `knowledge/` Folder

### File-by-file map

| File | What | Why | How / Key Anchors |
| --- | --- | --- | --- |
| `knowledge/__init__.py` | Package marker | Makes `knowledge` importable | Empty initializer |
| `knowledge/document_parser.py` | Text loader and chunker | Keeps long documents within prompt limits while preserving boundary context | `load_document`, `chunk_document`, `parse_document` |
| `knowledge/entity_extractor.py` | Chunk-level structured extraction | Turns raw text into entities and typed relationships | `extract_entities_from_chunk`, `extract_from_document`, `augment_contextual_relationships` |
| `knowledge/entity_validator.py` | Entity and edge cleanup | Stops hallucinations, substring bugs, alias duplication, and unresolved edges | `validate_entities`, `validate_relationships`, `_is_present_in_text`, `_find_canonical_name` |
| `knowledge/graph_builder.py` | Graph and graph-memory builder | Converts validated extraction into NetworkX + ChromaDB artifacts | `build_graph`, `save_graph`, `store_in_chromadb`, `build_knowledge_graph` |
| `knowledge/graph_densifier.py` | Post-build visual densifier | Adds grounded contextual edges for richer graph visualization | `densify_saved_graph` |
| `knowledge/graph_merger.py` | Multi-graph fusion | Combines several graph JSONs into one merged world model | `load_graph_json`, `_find_canonical`, `merge_graphs` |
| `knowledge/news_ingestor.py` | Live RSS and historical doc ingestion | Creates clean input documents without changing downstream graph logic | `fetch_live_news`, `load_historical_document`, `list_historical_events`, `fetch_news_document` |

### Deep note — `knowledge/document_parser.py`

**What**  
Loads a text file and chunk-splits it with overlap.

**Why**  
Entity relations often cross sentence boundaries. Simple hard splits lose those cross-boundary links.

**Representative snippet**

```python
while start < len(text):
    end = start + chunk_size
    if end < len(text):
        last_period = text.rfind(".", start, end)
        if last_period > start + (chunk_size // 2):
            end = last_period + 1
    chunk = text[start:end].strip()
    start = end - overlap
```

### Deep note — `knowledge/entity_extractor.py`

**What**  
Runs JSON extraction per chunk, merges entities, and augments the graph with grounded context-proximity edges.

**Why**  
The LLM alone produces sparse or inconsistent edges for dense event documents. The contextual augmentation stage adds grounded density without inventing unsupported facts.

**How**

- Prompts for exact-name entities and explicit relations.
- Safely returns empty lists on parse failure instead of crashing the pipeline.
- Merges chunk outputs into one document-level extraction result.
- Adds `CONTEXT_NEAR` edges between entities that repeatedly occur near one another in the source text.

**Representative snippet**

```python
augmented.append({
    "source": source_name,
    "target": target_name,
    "relation": CONTEXT_EDGE_RELATION,
    "inferred": True,
    "weight": min(1.0, 0.35 + count * 0.15),
})
```

### Deep note — `knowledge/entity_validator.py`

**What**  
The extraction cleanup layer.

**Why**  
Without this file, graph quality collapses from substring hallucinations, alias duplication, bad types, and relationships that point to nodes that should not exist.

**How**

- Uses word-boundary matching for single-token entities.
- Uses stronger containment rules for multi-token alias cases.
- Preserves numeric distinctions such as `56 Mountain Brigade` vs `79 Mountain Brigade`.
- Canonicalizes relationship endpoints after validation.

**Representative snippet**

```python
if len(words) == 1:
    pattern = r'\b' + re.escape(name_lower) + r'\b'
    return bool(re.search(pattern, text_lower))
```

### Deep note — `knowledge/graph_builder.py`

**What**  
Builds the persistent graph layer.

**Why**  
DARSH needs both symbolic structure and semantic retrieval. NetworkX handles traversable structure; ChromaDB handles semantic search over nodes.

**How**

- Creates a directed graph from validated entities and relations.
- Skips unresolved edge endpoints instead of inventing `UNKNOWN` nodes.
- Saves graph JSON to `data/graphs/`.
- Stores node descriptions in a graph-specific ChromaDB collection.

**Representative snippet**

```python
G.add_node(
    name,
    type=entity.get("type", "UNKNOWN"),
    description=entity.get("description", "")
)

G.add_edge(
    source,
    target,
    relation=relation,
    inferred=bool(rel.get("inferred", False)),
    weight=float(rel.get("weight", 1.0)),
)
```

### Deep note — `knowledge/news_ingestor.py`

**What**  
Provides two document-generation modes: live RSS ingestion and historical backtest loading.

**Why**  
DARSH treats “uploaded document,” “live topic digest,” and “historical dossier” as interchangeable downstream graph inputs.

**How**

- RSS feeds are filtered by topic keywords and rendered into a normalized digest document.
- Historical events come from an indexed repository of curated documents that intentionally stop before the actual outcome to avoid data leakage.

---

## 9. `causal/` Folder

### File-by-file map

| File | What | Why | How / Key Anchors |
| --- | --- | --- | --- |
| `causal/__init__.py` | Package marker | Makes `causal` importable | Empty initializer |
| `causal/causal_extractor.py` | Knowledge graph → causal DAG upgrade | Separates correlation from directional influence | `determine_causal_direction`, `build_causal_dag`, `save_causal_dag`, `get_root_causes`, `get_downstream_effects` |
| `causal/counterfactual.py` | Counterfactual reasoning engine | Answers “what if X had been removed or changed?” | `CounterfactualEngine.what_if_removed`, `what_if_changed`, `find_intervention_points` |

### Deep note — `causal/causal_extractor.py`

**What**  
Reinterprets graph relationships as causal candidates.

**Why**  
The graph knows relatedness; the DAG knows direction, strength, and lag.

**How**

For each graph edge, DARSH asks:

1. Does A cause B?
2. Does B cause A?
3. Is causation bidirectional or absent?
4. If causal, how strong and how delayed is the effect?

**Representative snippet**

```python
causal_info = determine_causal_direction(source, target, relation, context)

if direction == "A_CAUSES_B" and strength > 0.1:
    causal_dag.add_edge(source, target, strength=strength, time_lag=time_lag)
elif direction == "B_CAUSES_A" and strength > 0.1:
    causal_dag.add_edge(target, source, strength=strength, time_lag=time_lag)
```

### Deep note — `causal/counterfactual.py`

**What**  
Runs alternate-world reasoning over the causal DAG.

**Why**  
Prediction becomes more useful when DARSH can also say what intervention or missing cause would have changed the path.

**How**

- Trace downstream effects from a cause node.
- Feed the causal trace to the model.
- Ask for a concise natural-language alternate-world explanation.

---

## 10. `agents/` Folder

### File-by-file map

| File | What | Why | How / Key Anchors |
| --- | --- | --- | --- |
| `agents/__init__.py` | Package marker | Makes `agents` importable | Empty initializer |
| `agents/agent_factory.py` | Population constructor | Builds agent sets with cognition mix and optional market-role overlay | `create_agent`, `_calculate_type_counts`, `create_market_agent_population`, `create_agent_population` |
| `agents/belief_state.py` | Bayesian belief engine | Replaces string-based belief drift with explicit probability math | `BeliefState`, `get_likelihoods_from_llm`, `_calibrate_likelihoods_from_evidence`, `aggregate_beliefs` |
| `agents/rational_agent.py` | Rational agent specialization | Models evidence-first reasoning | `RationalAgent.think` |
| `agents/emotional_agent.py` | Emotional agent specialization | Models sentiment-first reactions and internal mood drift | `EmotionalAgent.think` |
| `agents/tribal_agent.py` | Tribal agent specialization | Models in-group consensus and echo-chamber behavior | `TribalAgent.think`, `update_tribe_consensus` |
| `agents/contrarian_agent.py` | Contrarian agent specialization | Preserves dissent and anti-consensus hypotheses | `ContrarianAgent.think`, `set_majority_view` |
| `agents/institutional_agent.py` | Institutional agent specialization | Models procedural, risk-managed institutional reasoning | `InstitutionalAgent.think` |
| `agents/market_roles.py` | Role registry and assignment helpers | Adds market-participant overlays on top of cognition types | `MARKET_ROLES`, `EVENT_ROLE_WEIGHTS`, `assign_roles_to_agent_types`, `build_market_role_background` |
| `agents/semantic_memory.py` | Chroma-backed per-agent memory | Gives agents semantic retrieval instead of short recency-only memory | `_get_embedding_fn`, `create_shared_chroma_client`, `SemanticMemory` |

### Deep note — `agents/agent_factory.py`

**What**  
Builds the actual population that the simulation loop uses.

**Why**  
The algorithm needs both **cognitive diversity** and **market-role diversity**. `agent_factory.py` is where those two axes are combined.

**How**

- First, compute target counts for cognition types.
- Then, assign market roles based on event-specific role weights.
- Finally, create agents with both personality and market-role overlays.

**Representative snippet**

```python
role_assignments = assign_roles_to_agent_types(type_counts, event_type)

agent = create_agent(
    agent_id=f"agent_{index + 1:03d}",
    agent_type=agent_type,
    name=name,
    background=f"{background}. {role_overlay}",
    topic=topic,
    chroma_client=chroma_client,
    simulation_id=simulation_id,
)
```

### Deep note — `agents/belief_state.py`

**What**  
The mathematical heart of DARSH’s forecast logic.

**Why**  
This file is what turns “agent vibe” into updateable probability mass.

**How**

- The model scores likelihood of evidence under each outcome.
- DARSH applies Bayes’ rule.
- An entropy-style regularization mix prevents pathological overconfidence.
- A rule-based calibration layer tilts the raw model scores using cue detection and slight personality bias.

**Representative snippet**

```python
for outcome in self.outcomes:
    prior_prob = prior.get(outcome, 0.0)
    likelihood = likelihoods.get(outcome, 0.5)
    unnormalized[outcome] = prior_prob * likelihood

raw_posterior = {o: round(v / total, 4) for o, v in unnormalized.items()}
epsilon = 0.08
self.distribution = {
    o: round((1 - epsilon) * raw_posterior.get(o, 0) + epsilon * (1.0 / n), 4)
    for o in self.outcomes
}
```

### Deep note — `agents/semantic_memory.py`

**What**  
Per-agent semantic memory storage and retrieval.

**Why**  
List-based memory makes agents see only the most recent messages. Semantic memory lets them retrieve the most relevant old memory instead.

**How**

- Each agent gets its own Chroma collection.
- Memories are stored with metadata (`round`, `category`, `agent_id`).
- Retrieval is semantic, not recency-based.

**Implementation note**  
`simulation/parallel_branches.py` attempts a best-effort old-memory cleanup before runs. The simulation is still protected from memory bleed primarily by timestamped simulation namespaces in `runner.py`.

### Specialized agent subclasses

| File | Behavioral specialization | Core algorithmic difference |
| --- | --- | --- |
| `rational_agent.py` | Evidence-weighted reasoning | Prompts for evidence and likely outcomes before conclusion |
| `emotional_agent.py` | Fast sentiment propagation | Tracks internal `emotional_state` and reacts viscerally |
| `tribal_agent.py` | Group-identity filtering | Injects `tribe_consensus` into interpretation |
| `contrarian_agent.py` | Anti-consensus hypothesis generation | Injects `perceived_majority_view` and asks what is being missed |
| `institutional_agent.py` | Rule- and mandate-based analysis | Prompts around risk, mandate, and procedural responsibility |

---

## 11. `simulation/` Folder

### File-by-file map

| File | What | Why | How / Key Anchors |
| --- | --- | --- | --- |
| `simulation/__init__.py` | Package marker | Makes `simulation` importable | Empty initializer |
| `simulation/environment.py` | Shared world and SQLite logger | Persists all round-level state for replay and analysis | `SimulationEnvironment`, `log_action`, `update_world_state`, `classify_outcome` |
| `simulation/market_timeline.py` | Round-stage templates | Gives rounds semantic market phases instead of generic loop numbers | `MARKET_TIMELINE_STAGES`, `build_market_timeline`, `get_branch_narratives` |
| `simulation/parallel_branches.py` | Branch orchestrator and aggregator | Produces forecast distributions instead of one single story | `run_single_branch`, `run_parallel_branches`, `print_results` |
| `simulation/runner.py` | One-branch core loop | Executes agents × rounds with context, social feed, and world updates | `_get_causal_insight`, `run_simulation` |
| `simulation/simulation_chat.py` | Post-run interactive Q&A helpers | Turns the result surface into an interactive analysis layer | `answer_sector_question`, `answer_what_would_change`, `answer_cohort_question`, `answer_counterfactual_question`, `run_simulation_chat` |
| `simulation/social_network.py` | Follower graph and round-post system | Creates true agent-to-agent information cascades | `SocialNetwork.build`, `post`, `get_feed`, `clear_round_posts` |

### Deep note — `simulation/environment.py`

**What**  
The persistent world-state container and logger.

**Why**  
DARSH needs one authoritative place for evolving situation text, round summaries, agent actions, and replay data.

**How**

- Initializes SQLite tables for `agent_actions`, `world_states`, and `outcomes`.
- Logs every agent result per round.
- Updates the world narrative based on the dominant action.
- Classifies final outcome using median aggregation over belief distributions when available.

**Representative snippet**

```python
distributions = [
    r.get("belief_distribution")
    for r in round_results
    if r.get("belief_distribution")
]

for outcome in all_outcomes:
    values = [d.get(outcome, 0.0) for d in distributions]
    medians[outcome] = statistics.median(values)
```

### Deep note — `simulation/runner.py`

**What**  
Executes one complete branch.

**Why**  
This is the engine that actually turns graph context, causal hints, market timeline, and agent society into a branch trajectory.

**How**

1. Create agent population.
2. Create environment and social network.
3. Load causal DAG if available.
4. Build structured round timeline.
5. For each round: gather world context, run each agent, post to social network, log actions, update world state.
6. Classify final branch outcome and return a branch summary.

**Representative snippet**

```python
for round_num in range(1, num_rounds + 1):
    round_context = market_timeline[round_num - 1]
    world_context = env.get_world_state_for_agents(
        round_context=round_context,
        branch_narrative=branch_narrative
    )

    for agent in agents:
        social_feed = social_network.get_feed(agent.agent_id)
        result = agent.run_round(
            world_context=world_context,
            new_information=new_event,
            available_actions=available_actions,
            social_feed=social_feed
        )
```

### Deep note — `simulation/parallel_branches.py`

**What**  
Aggregates multiple branch runs into a final probability surface.

**Why**  
DARSH is deliberately an ensemble system. This file is what turns branch divergence into forecast percentages.

**How**

- Creates branch configs with deterministic narrative labels.
- Runs branches sequentially for Ollama compatibility.
- Aggregates branch outcomes, action distributions, and average confidence.
- Computes branch-level outcome standard deviation.
- Calls the population model after branch completion.

**Representative snippet**

```python
outcome_probs = {
    k: round(v / total_branches * 100, 1)
    for k, v in outcome_counts.items()
}
```

### Deep note — `simulation/social_network.py`

**What**  
Creates actual information flow between agents.

**Why**  
Without this file, agents would only read the same global context. Social influence would be fake.

**How**

- Builds a follow graph per simulation.
- Varies follow density by agent type.
- Creates tribal echo chambers and contrarian diversity.
- Provides per-agent feeds before thinking.

---

## 12. `analysis/` Folder

### File-by-file map

| File | What | Why | How / Key Anchors |
| --- | --- | --- | --- |
| `analysis/__init__.py` | Package marker | Makes `analysis` importable | Empty initializer |
| `analysis/backtest_engine.py` | Historical scoring engine | Measures DARSH forecast quality with Brier score | `load_simulation_results`, `compute_brier_score`, `interpret_brier_score`, `run_backtest` |
| `analysis/batch_backtest.py` | Multi-event historical suite | Runs DARSH over several historical events and summarizes accuracy | `load_historical_events`, `run_single_historical_event`, `run_historical_suite` |
| `analysis/calibration.py` | Calibration tracker | Measures whether predicted confidence matches realized frequency over time | `save_prediction`, `compute_calibration_summary`, `print_calibration_report` |
| `analysis/india_market_population.py` | Population-weighted cohort model | Reweights sampled agent outputs to better match real market structure | `compute_population_weighted_sentiment`, `_combine_lens`, `_blend_lenses` |
| `analysis/market_impact_mapper.py` | Market regime and sector mapper | Converts behavioral distribution into sector impacts, triggers, and narratives | `classify_market_regime`, `compute_sector_impacts`, `generate_full_market_impact` |
| `analysis/market_output_schema.py` | Output schema constants and dataclasses | Defines the typed shape of market-impact output | `SectorImpact`, `MarketImpactOutput`, `INDIA_SECTORS` |
| `analysis/pdf_export.py` | Pure-Python PDF renderer | Produces a lightweight downloadable PDF without external PDF dependencies | `build_report_pdf_bytes`, `_build_lines`, `_render_pdf` |
| `analysis/prediction_logger.py` | Persistent prediction log and track record | Stores scored predictions and computes long-run summary metrics | `log_prediction`, `build_track_record_table`, `compute_track_record_summary` |
| `analysis/report_engine.py` | 6-section grounded report generator | Converts simulation traces into analyst-style prose and result markdown | `load_simulation_data`, `ReportEngine`, `_fetch_verified_facts`, `_assemble_report`, `generate_report` |

### Deep note — `analysis/backtest_engine.py`

**What**  
Scores historical forecasts.

**Why**  
DARSH is not only a visualization system; it is intended to be measurable.

**Representative snippet**

```python
for outcome, predicted_prob in predicted_probs.items():
    actual = 1.0 if outcome == actual_outcome else 0.0
    squared_errors.append((predicted_prob - actual) ** 2)

brier = sum(squared_errors) / len(squared_errors)
```

### Deep note — `analysis/india_market_population.py`

**What**  
Builds a more market-shaped view of the simulation result.

**Why**  
Equal-weight agent samples are useful for dynamics, but not for estimating how retail, mutual funds, FIIs, media, and institutional desks reshape the final market picture.

**How**

- Groups final-round agents by market role.
- Computes role-level belief distributions.
- Builds three weighted lenses: participation, capital, and velocity.
- Blends those lenses into a final population-weighted distribution.

**Representative snippet**

```python
lens_views = {
    "participation": participation_lens,
    "capital": capital_lens,
    "velocity": velocity_lens,
}
blended_distribution = _blend_lenses(lens_views)
```

### Deep note — `analysis/market_impact_mapper.py`

**What**  
Maps behavioral outcomes into a market regime and sector-level consequences.

**Why**  
Forecast probabilities alone are too abstract for decision support. This file converts them into market interpretation.

**How**

- Normalize outcome distribution.
- Classify regime (`risk_on`, `policy_shock`, `sector_rotation`, etc.).
- Apply sector sensitivity matrix with behavior-dependent multipliers.
- Generate sector explanations, watchlists, triggers, and narrative expectations.

### Deep note — `analysis/report_engine.py`

**What**  
Generates DARSH’s report layer.

**Why**  
The system needs a human-readable end product that stays grounded in recorded simulation facts.

**How**

- Reads SQLite logs from all branch databases.
- Extracts verified counts, confidence profiles, verbatim thoughts, and world-state summaries.
- Writes six sections:
  1. Executive Summary
  2. Predicted Outcome
  3. Causal Drivers
  4. Agent Behavior Analysis
  5. Dissenting Views
  6. Confidence Assessment
- Assembles the full report and writes markdown to `data/reports/`.

**Representative snippet**

```python
report = f"""# DARSH Prediction Report
**Topic:** {self.topic}
...
## 1. Executive Summary
{exec_summary}
...
## 6. Confidence Assessment
{confidence}
"""
```

### Deep note — `analysis/pdf_export.py`

**What**  
Builds a simple PDF directly from markdown and summary data.

**Why**  
This keeps export self-contained and avoids heavier PDF dependencies.

**How**  
It tokenizes report content into typed lines, paginates them, and writes raw PDF objects manually.

### Deep note — `analysis/prediction_logger.py`

**What**  
Stores long-run forecast outcomes and builds track-record summaries.

**Why**  
DARSH needs more than one-off backtest scores. This file accumulates evidence across many resolved events.

---

## 13. `market/` Folder

### File-by-file map

| File | What | Why | How / Key Anchors |
| --- | --- | --- | --- |
| `market/__init__.py` | Package marker | Makes `market` importable | Empty initializer |
| `market/template_renderer.py` | Event-template system | Lets DARSH render scenario presets from structured market inputs | `load_market_ontology`, `list_event_templates`, `derive_template_fields`, `render_event_template` |

### Deep note — `market/template_renderer.py`

**What**  
Renders preset market-event scenarios into a ready topic, situation, and round-event pack.

**Why**  
This gives DARSH repeatable structured scenarios for faster setup and consistent market framing.

**How**

- Loads ontology and template JSON.
- Normalizes raw inputs to text/number/boolean.
- Computes derived values such as new rate, market shock label, or fiscal framing.
- Renders the final scenario text with `.format(**merged_inputs)`.

**Representative snippet**

```python
return {
    "template_id": template["template_id"],
    "display_name": template["display_name"],
    "topic": f"{template['display_name']} — Market and Sector Impact",
    "situation": situation,
    "round_events": round_events,
    "event_type": template.get("event_type_key", "general"),
}
```

---

## 14. `tests/` Folder

### Testing philosophy

The `tests/` folder mixes:

- **regression tests** for specific algorithm fixes,
- **module dry-runs** for foundational system layers,
- **phase tests** that mirror the system’s historical development.

Because these files validate the algorithm rather than implement it, they are documented more compactly below.

### File-by-file test map

| File | What it validates |
| --- | --- |
| `tests/test_belief_signal_calibration.py` | Positive and negative evidence calibration in `belief_state.py` |
| `tests/test_graph_density_fixes.py` | Numeric-entity distinctness, relationship canonicalization, and contextual edge densification |
| `tests/test_historical_event_coverage.py` | Historical-event index quality and outcome coverage |
| `tests/test_llm_caller_json_mode.py` | JSON-mode robustness for fenced JSON, `<think>` blocks, and Python-style dict drift |
| `tests/test_module1.py` | BaseAgent dry run |
| `tests/test_module2.py` | Document → graph → Chroma pipeline |
| `tests/test_module3.py` | Causal DAG build and counterfactual engine |
| `tests/test_module4.py` | Heterogeneous agent society behavior |
| `tests/test_module5.py` | Parallel branch simulation |
| `tests/test_module6.py` | Backtesting and report generation |
| `tests/test_module7.py` | API endpoint health and integration |
| `tests/test_v2_phase1.py` | Validation, Bayesian beliefs, grounded report primitives |
| `tests/test_v2_phase2.py` | Semantic memory, social network, causal integration |
| `tests/test_v2_phase3.py` | Historical backtest, confidence, live-news integration |
| `tests/test_v2_phase4.py` | Graph API, history, merger workflows |
| `tests/test_v3_phase1.py` | Early v3 feature integration |
| `tests/test_v3_phase2.py` | v3 feature and regression coverage |
| `tests/test_v3_phase3.py` | Market-role population and related phase logic |
| `tests/test_v3_phase4.py` | Structured market timeline and round metadata |
| `tests/test_v3_phase5.py` | Population-weighted market cohort model |
| `tests/test_v3_phase6_partial.py` | Partial interactive-analysis helpers |
| `tests/test_v3_phase6_full.py` | Cohort chat and counterfactual interaction paths |
| `tests/test_v3_phase7.py` | Prediction logger and track-record summary |

---

## 15. Data Artifacts The Algorithm Produces

| Path | Produced by | Meaning |
| --- | --- | --- |
| `data/inputs/` | `document_utils.py`, `news_ingestor.py`, `load_historical()` | normalized input documents |
| `data/graphs/*.json` | `graph_builder.py`, `graph_merger.py`, `graph_densifier.py` | knowledge graph artifacts |
| `data/graphs/*_causal.json` | `causal_extractor.py` | causal DAG artifacts |
| `data/chroma/` | `graph_builder.py` | graph semantic memory |
| `data/agent_memories/` | `semantic_memory.py` | per-agent semantic memories |
| `data/simulations/*.db` | `environment.py` | per-branch SQLite logs |
| `data/reports/*.md` | `report_engine.py` | assembled markdown reports |
| `data/reports/*.pdf` | `pdf_export.py` via API | exported PDFs |
| `data/reports/prediction_log.json` | `prediction_logger.py` | scored prediction history |
| `data/reports/track_record_table.md` | `prediction_logger.py` | markdown track record table |
| `data/reports/calibration_history.json` | `calibration.py` | calibration history |

---

## 16. The Core DARSH Algorithm In “What / Why / How” Form

### What DARSH computes

DARSH computes:

- a **structured world model** from text,
- an **agent society** with differentiated cognition and market roles,
- a **belief distribution** over forecast outcomes,
- a **market interpretation layer**,
- a **population-weighted cohort interpretation**,
- and a **report-ready explanation surface**.

### Why the pieces are arranged this way

- **Graph first** keeps the world model inspectable.
- **Agent society second** keeps the reasoning plural rather than singular.
- **Bayesian belief tracking** keeps the forecast mathematical rather than purely rhetorical.
- **Branching** keeps the result probabilistic rather than falsely certain.
- **Backtesting and track record** keep the system measurable rather than theatrical.

### How the pieces interact

1. Input creates the scenario.
2. Knowledge extraction creates the symbolic memory surface.
3. Optional causal modeling adds directional reasoning.
4. Agent factory populates the world with heterogeneous participants.
5. Runner executes round-by-round cognition plus social influence.
6. Parallel branches aggregate multiple possible evolutions.
7. Analysis modules translate raw output into decision-ready interpretation.

---

## 17. Practical Reading Order For New Developers

If someone is onboarding to DARSH, the most useful read order is:

1. `app.py`
2. `api/routes.py`
3. `core/llm_caller.py`
4. `knowledge/document_parser.py`
5. `knowledge/entity_extractor.py`
6. `knowledge/entity_validator.py`
7. `knowledge/graph_builder.py`
8. `core/base_agent.py`
9. `agents/belief_state.py`
10. `agents/agent_factory.py`
11. `simulation/runner.py`
12. `simulation/environment.py`
13. `simulation/parallel_branches.py`
14. `analysis/report_engine.py`
15. `analysis/market_impact_mapper.py`
16. `analysis/india_market_population.py`

That order follows the actual control flow of the product.

---

## 18. Closing Summary

DARSH is not one model, one prompt, or one simulation loop.

It is a layered algorithm:

1. **Normalize input**
2. **Extract symbolic structure**
3. **Validate and densify**
4. **Build graph memory**
5. **Optionally infer causal structure**
6. **Create a heterogeneous market-aware agent population**
7. **Run socially connected Bayesian agents over structured rounds**
8. **Branch the simulation**
9. **Aggregate outcomes**
10. **Map the result into market, population, and report layers**
11. **Score itself against history**

That architecture is what makes DARSH simultaneously:

- local-first,
- zero-paid-API-cost in its intended runtime mode,
- visually inspectable,
- behaviorally plural,
- and scientifically more defensible than a single opaque answer system.

