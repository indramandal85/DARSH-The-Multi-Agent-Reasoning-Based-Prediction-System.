# RUNNING.md — DARSH Complete Run Instructions

Every command you need, in order, with expected output.

DARSH is designed to run locally. For the original app, the recommended path is local-first inference through Ollama, which means no paid cloud inference API is required for normal use.

---

## Prerequisites

```bash
# Verify Python 3.10
python3.10 --version           # Python 3.10.x

# Verify Node.js
node --version                 # v18+ or v24.x

# Verify Homebrew (macOS)
brew --version
```

---

## ONE-TIME SETUP

### Step 1 — Clone and create virtual environment

```bash
cd ~/Desktop
git clone https://github.com/YOUR_USERNAME/neuroswarm.git
cd neuroswarm
python3.10 -m venv .venv
source .venv/bin/activate
# You should see (.venv) in your terminal prompt
```

### Step 2 — Install Python dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install feedparser==6.0.11    # Live news ingestion
```

**If NumPy version error appears:**
```bash
pip install "numpy==1.26.4"
```

### Step 3 — Install frontend dependencies

```bash
cd frontend
npm install
cd ..
```

### Step 4 — Install and configure Ollama

This is what enables the zero-paid-API local run path for the original app.

```bash
brew install ollama
brew services start ollama
ollama pull llama3.1              # Downloads 4.7GB — one time only
```

**Verify Ollama works:**
```bash
ollama run llama3.1
# Type: "Hello" — should get a response
# Type: /bye to exit
```

### Step 5 — Create required data directories

```bash
mkdir -p data/inputs data/graphs data/simulations data/reports
mkdir -p data/agent_memories data/chroma
mkdir -p data/historical_events/docs
```

### Step 6 — Verify historical events exist

```bash
ls data/historical_events/docs/
# Should show:
# corporate_tax_cut_2019.txt
# covid_lockdown_2020.txt
# demonetization_2016.txt
# election_result_2024.txt
# rbi_rate_hike_2022.txt
# gdp_recovery_2021.txt
# ukraine_oil_crisis_2022.txt
# paytm_rbi_2024.txt
```

---

## EVERY SESSION — Three Terminal Tabs

Open three separate terminal windows/tabs. Run these in order:

### Tab 1 — LLM Server (leave running entire session)

```bash
ollama serve
# Expected output:
# Listening on 127.0.0.1:11434
```

### Tab 2 — Flask API Server

```bash
cd ~/Desktop/neuroswarm
source .venv/bin/activate
python app.py
# Expected output:
# DARSH API SERVER
# Running on: http://localhost:5001
```

### Tab 3 — Frontend Development Server

```bash
cd ~/Desktop/neuroswarm/frontend
npm run dev
# Expected output:
# Local: http://localhost:5173/
```

### Open in Browser

```
http://localhost:5173
```

This is the full original DARSH app with local graph building, simulation, and reporting.

### Optional — Run the Demo App Instead

The demo app is useful when you want a presentation-ready walkthrough without running live inference.

```bash
cd ~/Desktop/neuroswarm/frontend
npm run build
cd ..
source .venv/bin/activate
python app_demo.py
```

Open:

```text
http://localhost:5002
```

---

## USING THE WEB UI

### Home Screen
The home screen shows the DARSH title with animated background. Click **"Start Exploring"** to enter the app.

### Screen 0 — Input Source (three modes)

**Mode A: Manual Upload**
- Click the drop zone or drag a `.txt` file
- File uploads to `data/inputs/`
- Click **"Build Knowledge Graph →"**
- Wait 3-5 minutes for graph building
- Automatically advances to Screen 1

**Mode B: Live News**
- Type comma-separated topics: `RBI, interest rate, India inflation, 2025`
- Click **"Fetch Live News"**
- Fetches from BBC, Reuters, Economic Times, Moneycontrol
- Then build knowledge graph as normal

**Mode C: Historical Backtest**
- Select an event from the dropdown
- Click **"Load Historical Document"**
- Actual outcome is hidden during simulation
- After simulation, click **"Reveal Actual Outcome & Score"** for Brier score

### Screen 1 — Configure Simulation

Fill in:
- **Topic:** One sentence prediction question (e.g., `RBI rate hike — social and market reaction`)
- **Initial Situation:** 3-4 sentences describing world state at T=0 with specific numbers
- **Events per round:** One line per round (3 lines recommended)
- **Agents:** 5 for standard, 3 for fast testing
- **Branches:** 3 for standard, 2 for fast testing
- **Rounds:** 3 for standard, 2 for fast testing

**Fast test configuration (12-15 minutes total):**
- Agents: 3, Branches: 2, Rounds: 2

**Standard configuration (35-45 minutes total):**
- Agents: 5, Branches: 3, Rounds: 3

Click **"Run Simulation →"**

### Screen 2 — Running

The page polls every 5 seconds. Do NOT refresh. Status updates show:
- `Starting simulation branches...`
- `Agents reasoning...`
- `Generating report (1/6) — executive summary...` through `(6/6)`

### Screen 3 — Results

- Animated probability bars show outcome distribution
- Dominant outcome badge with percentage
- For historical backtest: click "Reveal Actual Outcome & Score" for Brier score
- "Show full 6-section report" to read the complete analysis
- "Download Report (.md)" to save

### Advanced Graph Tools (appear after graph is built)

After building a knowledge graph, three buttons appear in the toolbar:

- **🕸 Knowledge Graph** — Interactive force-directed graph. Click nodes for details. Toggle between Knowledge Graph and Causal DAG view. Drag to pan, scroll to zoom.
- **📋 History** — List of all past simulations. Click any to see round-by-round replay with timeline scrubber.
- **🔗 Merge Graphs** — Select 2+ graphs and merge into one combined world model.

---

## RUNNING TESTS

Run all tests in order (each takes 3-20 minutes):

```bash
cd ~/Desktop/neuroswarm
source .venv/bin/activate

# v1 module tests (no ollama needed for 1-2, need ollama for 3-7)
python tests/test_module1.py    # ~3 min — BaseAgent + Ollama connection
python tests/test_module2.py    # ~5 min — Knowledge graph
python tests/test_module3.py    # ~7 min — Causal DAG
python tests/test_module4.py    # ~5 min — 5 agent types
python tests/test_module5.py    # ~18 min — Parallel simulation

# Start python app.py first for Module 7
python tests/test_module6.py    # ~6 min — Backtesting + report
python tests/test_module7.py    # ~1 min — API endpoints (needs app.py running)

# phase-level integration tests
python tests/test_v2_phase1.py  # ~2 min — Validation, Bayesian, grounded report
python tests/test_v2_phase2.py  # ~8 min — Semantic memory, social network, causal
python tests/test_v2_phase3.py  # ~15 min — Historical backtest, confidence, live news
python tests/test_v2_phase4.py  # ~1 min — Graph API, history, merger

# newer v3 suites
python tests/test_v3_phase1.py
python tests/test_v3_phase2.py
python tests/test_v3_phase3.py
python tests/test_v3_phase4.py
python tests/test_v3_phase5.py
python tests/test_v3_phase6_partial.py
python tests/test_v3_phase6_full.py
python tests/test_v3_phase7.py
```

**Run the legacy v2 phase set at once:**
```bash
python tests/test_v2_phase1.py && \
python tests/test_v2_phase2.py && \
python tests/test_v2_phase3.py && \
python tests/test_v2_phase4.py
```

---

## RUNNING INDIVIDUAL MODULES

```bash
# Test Ollama connection
python core/llm_caller.py

# Test document parsing
python knowledge/document_parser.py

# Test entity extraction
python knowledge/entity_extractor.py

# Run batch historical backtest (all 5 events, ~40 min)
python analysis/batch_backtest.py
```

---

## API ENDPOINTS

The Flask API runs at `http://localhost:5001`. All endpoints:

| Endpoint | Method | Description |
|---|---|---|
| `/api/health` | GET | Check API is running |
| `/api/upload` | POST | Upload a .txt document |
| `/api/build-graph` | POST | Start knowledge graph build job |
| `/api/run-simulation` | POST | Start parallel simulation job |
| `/api/status/<job_id>` | GET | Poll job status |
| `/api/get-report` | GET | Get most recent report |
| `/api/fetch-news` | POST | Fetch live RSS news |
| `/api/historical-events` | GET | List backtest events |
| `/api/load-historical` | POST | Load historical document |
| `/api/score-prediction` | POST | Compute Brier score |
| `/api/graph/<name>` | GET | Get graph for visualization |
| `/api/graphs` | GET | List all saved graphs |
| `/api/merge-graphs` | POST | Merge multiple graphs |
| `/api/simulations/history` | GET | List all past simulations |
| `/api/simulations/<id>/round/<n>` | GET | Get round detail for replay |

**Quick health check:**
```bash
curl http://localhost:5001/api/health
# {"message":"DARSH API is running","status":"ok"}
```

**List historical events:**
```bash
curl http://localhost:5001/api/historical-events
```

**Load and score a historical event:**
```bash
# Load
curl -X POST http://localhost:5001/api/load-historical \
  -H "Content-Type: application/json" \
  -d '{"event_id": "rbi_rate_hike_2022"}'

# Score after simulation
curl -X POST http://localhost:5001/api/score-prediction \
  -H "Content-Type: application/json" \
  -d '{"predicted_probs": {"panic": 80, "cautious": 15, "optimistic": 5}, "actual_outcome": "panic", "event_id": "rbi_rate_hike_2022"}'
```

---

## HISTORICAL BACKTEST CONFIGURATIONS

Use these exact configurations for all 5 historical events:

### Event 1 — India Demonetization 2016

```
Historical Event: india_demonetization_2016
Topic: India demonetization shock — immediate public and market reaction
Situation: PM Narendra Modi has announced at 8pm that Rs 500 and Rs 1000 notes are 
no longer legal tender from midnight tonight. These notes represent 86% of all 
currency in circulation. Citizens have until December 30 to exchange old notes at 
banks. ATMs will be closed tomorrow.

Round 1: Banks report unprecedented queues beginning at 6am. RBI announces daily 
withdrawal limit of Rs 2000. Hospitals and petrol stations report turning away cash 
customers.
Round 2: Sensex drops 1689 points. ATMs run dry within hours. Farmers unable to 
purchase seeds and fertilizers for rabi crop.
Round 3: Opposition parties call for Parliament session. World Bank warns of 
short-term GDP contraction.

Agents: 5 | Branches: 3 | Rounds: 3
Expected: cautious
```

### Event 2 — RBI Rate Hike 2022

```
Historical Event: rbi_rate_hike_2022
Topic: RBI emergency rate hike — market and social reaction
Situation: The Reserve Bank of India has called an emergency unscheduled Monetary 
Policy Committee meeting and raised the benchmark repo rate by 40 basis points 
to 4.4%. The hike was completely unexpected — all 40 economists polled by Reuters 
expected no change. Governor Shaktikanta Das cited rising inflation above the 6% 
tolerance ceiling.

Round 1: Sensex drops 1400 points in immediate reaction. Bond yields spike. 
All major banks announce EMI increases within 24 hours.
Round 2: Finance Ministry issues statement backing RBI decision. IMF warns India 
growth may slow. Small business associations raise concerns about loan costs.
Round 3: RBI Governor signals more hikes possible if inflation persists. 
World Bank revises India growth forecast downward.

Agents: 5 | Branches: 3 | Rounds: 3
Expected: panic
```

### Event 3 — GDP Recovery Q1 FY22

```
Historical Event: india_gdp_recovery_2021
Topic: India Q1 FY22 GDP recovery — social confidence and investment sentiment
Situation: India has posted 20.1% GDP growth in Q1 FY22, the strongest quarterly 
growth since records began. The surge is partly driven by a favorable base effect 
from the COVID lockdown contraction. The Finance Minister has called this a turning 
point. BSE Sensex opens up 1.2%.

Round 1: RBI maintains accommodative monetary policy, signals continued support for 
growth.
Round 2: Foreign institutional investors add $2.1 billion to Indian equities 
following the GDP data.
Round 3: IMF raises India FY22 growth forecast to 9.5%, among fastest globally.

Agents: 5 | Branches: 3 | Rounds: 3
Expected: cautious
```

### Event 4 — Ukraine Oil Crisis 2022

```
Historical Event: india_ukraine_oil_2022
Topic: India-Russia Ukraine war stance — diplomatic and economic sentiment
Situation: Russia has invaded Ukraine. Global oil prices have crossed 100 dollars 
per barrel for the first time since 2014. Western allies are pressuring India to 
condemn Russia. India abstained from the UN Security Council vote. India imports 
85% of its oil needs and 60% of its defense equipment from Russia.

Round 1: External Affairs Minister Jaishankar states India will protect its national 
interest. Rupee weakens to 76 against dollar.
Round 2: India begins negotiating rupee-ruble payment mechanism to bypass SWIFT 
sanctions. Sensex falls 1100 points on global uncertainty but recovers half by close.
Round 3: MEA issues statement: India will judge every proposal on its merits. 
IMF warns of global growth slowdown.

Agents: 5 | Branches: 3 | Rounds: 3
Expected: cautious
```

### Event 5 — Paytm RBI Crisis 2024

```
Historical Event: paytm_rbi_2024
Topic: Paytm RBI regulatory action — fintech sector confidence and investor sentiment
Situation: The Reserve Bank of India has ordered Paytm Payments Bank to stop 
accepting new deposits from February 29, 2024. Paytm has 330 million registered 
users and processes 1.4 billion transactions per month. Paytm stock has halted 
trading on NSE.

Round 1: Paytm stock reopens down 20% hitting lower circuit. RBI clarifies 
existing balances are safe. Competitor fintech companies report UPI volumes unaffected.
Round 2: Paytm CEO meets RBI Governor. Company announces partnerships with Axis 
Bank and Yes Bank. SEBI puts analyst reports under watch.
Round 3: RBI Governor reaffirms action was company-specific not sector-wide. 
Digital payments overall volume grows 2% despite Paytm disruption.

Agents: 5 | Branches: 3 | Rounds: 3
Expected: cautious
```

---

## TIMING GUIDE

| Configuration | Total Time |
|---|---|
| 2 agents, 2 branches, 2 rounds | ~12 min |
| 3 agents, 2 branches, 2 rounds | ~15 min |
| 5 agents, 2 branches, 3 rounds | ~25 min |
| 5 agents, 3 branches, 3 rounds | ~40 min |
| All 5 historical events (sequential) | ~3-4 hours |

Report generation adds 12-18 minutes after simulation completes (6 LLM calls).

---

## TROUBLESHOOTING

### Ollama not responding
```bash
brew services restart ollama
# Wait 30 seconds, then retry
```

### ChromaDB telemetry warnings
You should not normally see these in the current build. If you do, they are usually harmless legacy warnings:
```
Failed to send telemetry event ClientStartEvent: capture() takes 1 positional argument
```
Ignore them. ChromaDB works correctly.

### "File not found" when building graph for historical event
This means `load-historical` didn't copy the file to `data/inputs/`. Restart Flask and try again.

### Simulation stuck on report generation
Normal — each of 6 report sections takes 2-3 minutes with Llama 3.1. Total report time is 12-18 minutes. The status bar updates per section. Do not refresh.

### Panic bias in predictions
If all predictions show panic regardless of input:
1. Check `agents/belief_state.py` has the new `get_likelihoods_from_llm` with the behavioural framing prompt
2. Check `simulation/environment.py` uses median aggregation (not mean)
3. Check `core/base_agent.py` returns `belief_distribution` in `run_round`

### Memory bleed between simulations
If agents reason about the wrong topic (e.g., RBI rate hike memories in a GDP simulation):
1. Check `simulation/runner.py` creates `memory_sim_id = f"{simulation_id}_{int(_time.time())}"`
2. Check `simulation/parallel_branches.py` uses `run_stamp` in branch IDs
3. Delete `data/agent_memories/` and restart Flask

### NumPy compatibility error
```bash
pip install "numpy==1.26.4"
```

---

## GIT SETUP

```bash
cd ~/Desktop/neuroswarm
git init
git branch -m master main
git add .
git commit -m "DARSH initial local-first release"
```

`.gitignore` excludes: `.venv/`, `data/simulations/`, `data/chroma/`, `data/agent_memories/`, `data/graphs/*.json`, `data/reports/`, `frontend/node_modules/`
