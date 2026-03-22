# NeuroSwarm v2
### A Superior Multi-Agent AI Prediction System

NeuroSwarm is an open-source AI prediction engine that simulates heterogeneous agents — rational, emotional, tribal, contrarian, and institutional — to forecast how societies, markets, and groups respond to real-world events.

Unlike single-model prediction tools, NeuroSwarm uses **ensemble simulation**: running N parallel branches of the same scenario simultaneously to produce a **probability distribution** over possible futures — not just one story.

**Total API cost: ₹0 | Total cloud cost: ₹0 | Runs entirely on MacBook Air M4**

---

## What Makes It Superior

| Feature | MiroFish | NeuroSwarm v2 |
|---|---|---|
| Agent diversity | Uniform LLM agents | 5 cognitive architectures |
| World model | Knowledge graph only | Causal DAG + counterfactuals |
| Output | Single narrative | Probability distribution |
| Belief updating | Verbal rewrite | Bayesian math (Bayes' rule) |
| Agent memory | None | Per-agent semantic ChromaDB |
| Social influence | None | Full follower graph |
| Accuracy measurement | None published | Brier score + calibration |
| Outcome classification | Keyword counting | Median Bayesian aggregation |
| Cost | Paid API required | 100% free, fully local |
| Explainability | Narrative only | Causal attribution chains |
| Input sources | Manual upload only | Upload + Live RSS + Historical |

---

## System Architecture

```
Document / Live News / Historical Event
           ↓
    Module 2: Knowledge Graph
    (entities + relationships + ChromaDB)
           ↓
    Module 3: Causal DAG
    (cause → effect + counterfactuals)
           ↓
    Module 4: Agent Society
    (5 cognitive types, Bayesian beliefs, semantic memory)
           ↓
    Module 5: Parallel Simulation
    (N branches × agents × rounds, social network layer)
           ↓
    Module 6: Analysis
    (Brier scoring, grounded 6-section report)
           ↓
    Module 7: Web UI
    (Flask API + Vue 3, home screen, Phase 4 features)
```

---

## Technology Stack

| Component | Technology |
|---|---|
| LLM | Llama 3.1 8B via Ollama (local, free) |
| Backend | Python 3.10, Flask 3.0.2 |
| Knowledge Graph | NetworkX 3.2.1 + ChromaDB 0.4.24 |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Causal AI | pgmpy 0.1.25 |
| Simulation DB | SQLite (built-in Python) |
| Analysis | scikit-learn, matplotlib |
| Frontend | Vue 3 + Vite + axios |
| Platform | MacBook Air M4 (Apple Silicon) |

---

## Quick Start

**Prerequisites:** macOS, Homebrew, Python 3.10+, Node.js 18+, Ollama

```bash
# 1. Clone and setup
git clone https://github.com/YOUR_USERNAME/neuroswarm.git
cd neuroswarm
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install feedparser==6.0.11

# 2. Frontend
cd frontend && npm install && cd ..

# 3. Download LLM (one time, 4.7GB)
ollama pull llama3.1
```

**Every session — three terminal tabs:**

```bash
# Tab 1
ollama serve

# Tab 2
cd ~/Desktop/neuroswarm && source .venv/bin/activate && python app.py

# Tab 3
cd ~/Desktop/neuroswarm/frontend && npm run dev
```

Open `http://localhost:5173`

---

## Three Input Modes

### 1. Manual Upload
Upload any `.txt` document. The system builds a knowledge graph, causal DAG, and runs multi-agent simulation.

### 2. Live News (Forward Prediction)
Type topics like `"RBI, interest rate, India inflation"`. The system fetches today's real news from BBC, Reuters, Economic Times, and Moneycontrol. Use this to predict what will happen next.

### 3. Historical Backtest
Load a pre-written historical event document. The system predicts the outcome without seeing it, then reveals the actual outcome and scores with a Brier score.

---

## Example Output

**Input:** RBI emergency off-cycle rate hike of 40 basis points

```
Outcome probability distribution:
  panic      ████████████████████ 80%
  cautious   ████                 15%
  optimistic █                     3%
  divided    █                     2%

Dominant prediction: PANIC (80%)
Brier Score: 0.0 — EXCELLENT — near-perfect calibration
```

**Full 6-section report includes:**
1. Executive Summary (grounded in verified SQLite facts)
2. Predicted Outcome (with probability reasoning)
3. Causal Drivers (traced from causal DAG)
4. Agent Behavior Analysis (verbatim thoughts from simulation)
5. Dissenting Views (contrarian perspectives)
6. Confidence Assessment (Brier score interpretation)

---

## Historical Backtesting Results

| Event | Predicted | Actual | Brier Score |
|---|---|---|---|
| RBI Rate Hike 2022 | panic | panic | 0.0 — EXCELLENT |
| India Demonetization 2016 | cautious | cautious | ~0.17 — GOOD |
| GDP Recovery Q1 FY22 | cautious | cautious | ~0.17 — GOOD |
| Ukraine Oil Crisis 2022 | cautious | cautious | TBD |
| Paytm RBI Crisis 2024 | cautious | cautious | TBD |

---

## Project Structure

```
neuroswarm/
├── core/
│   ├── llm_caller.py           # Bridge to Ollama
│   └── base_agent.py           # BaseAgent: think→decide→update + Bayesian belief
├── knowledge/
│   ├── document_parser.py      # Reads + chunks documents
│   ├── entity_extractor.py     # LLM extracts entities + validation
│   ├── graph_builder.py        # NetworkX + ChromaDB
│   ├── news_ingestor.py        # Live RSS + historical document loader
│   └── graph_merger.py         # Multi-document graph fusion
├── causal/
│   ├── causal_extractor.py     # Builds causal DAG
│   └── counterfactual.py       # "What if X had not happened?"
├── agents/
│   ├── belief_state.py         # Bayesian belief updating
│   ├── semantic_memory.py      # Per-agent ChromaDB memory
│   ├── agent_factory.py        # Population creation
│   ├── rational_agent.py
│   ├── emotional_agent.py
│   ├── tribal_agent.py
│   ├── contrarian_agent.py
│   └── institutional_agent.py
├── simulation/
│   ├── environment.py          # World state + SQLite + median outcome classifier
│   ├── runner.py               # Single simulation loop
│   ├── parallel_branches.py    # N branches → probability distribution
│   └── social_network.py       # Agent-to-agent follower graph
├── analysis/
│   ├── backtest_engine.py      # Brier score computation
│   ├── batch_backtest.py       # Run all historical events suite
│   ├── report_engine.py        # 6-section grounded report writer
│   └── calibration.py          # Long-term accuracy tracking
├── api/
│   └── routes.py               # Flask API: 12 endpoints
├── frontend/
│   └── src/
│       ├── App.vue             # Complete UI: home screen + 4 screens + Phase 4
│       ├── GraphViewer.vue     # Interactive knowledge graph + causal DAG
│       ├── main.js
│       └── style.css
├── data/
│   ├── inputs/                 # Uploaded + fetched documents
│   ├── graphs/                 # Saved knowledge graphs
│   ├── simulations/            # SQLite simulation databases
│   ├── reports/                # Generated prediction reports
│   ├── agent_memories/         # ChromaDB agent memory store
│   └── historical_events/      # Historical backtest suite
│       ├── index.json          # 5 events with actual outcomes
│       └── docs/               # Pre-written historical documents
├── tests/
│   ├── test_module1.py through test_module7.py
│   ├── test_v2_phase1.py
│   ├── test_v2_phase2.py
│   ├── test_v2_phase3.py
│   └── test_v2_phase4.py
├── app.py                      # Flask entry point
├── requirements.txt
├── README.md
├── RUNNING.md
└── .gitignore
```

---

## v2 Phase Upgrades

### Phase 1 — Foundation Fixes
- Entity extraction validation (word-boundary regex deduplication)
- Bayesian belief state (real Bayes' rule, not verbal rewriting)
- Grounded report generation (verified SQLite facts injected)

### Phase 2 — Intelligence Upgrades
- Per-agent ChromaDB semantic memory (relevance-ranked, not recency-ranked)
- Social network layer (follower graph, posts between agents each round)
- Causal DAG active during simulation (causal insights injected into world context)

### Phase 3 — Credibility Upgrades
- Historical backtesting suite (5 events, Brier scoring)
- Confidence intervals (±std% across branches)
- Live news ingestion (RSS feeds, forward prediction mode)

### Phase 4 — UI Upgrades
- Home screen with animated grid and orbital nodes
- Interactive knowledge graph + causal DAG viewer (force-directed layout, pan/zoom)
- Simulation history + timeline scrubber (round-by-round replay)
- Multi-document graph fusion (fuzzy entity matching across documents)

---

## License

MIT License — use freely, credit appreciated.

**Built by:** Indra Mandal  
**Device:** MacBook Air M4 | **Python:** 3.10 | **LLM:** Llama 3.1 8B  
**Total cost:** ₹0
