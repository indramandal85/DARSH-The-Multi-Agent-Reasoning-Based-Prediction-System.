# api/routes.py
#
# THE FLASK API — bridges the Vue frontend to all 6 Python modules.
#
# 5 endpoints:
#   POST /api/upload          — receive a document file
#   POST /api/build-graph     — run Module 2 knowledge graph builder
#   POST /api/run-simulation  — run Module 5 parallel simulation
#   GET  /api/get-report      — return the generated report
#   GET  /api/status/<job_id> — check if a long job is done

import sys
import os
import json
import uuid
import time
import threading
from io import BytesIO
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, request, jsonify, send_file
from api.document_utils import ALLOWED_EXTENSIONS, allowed_file, normalize_uploaded_file

# Job tracking — stores status of long-running tasks
# In production this would be Redis; for our project a dict is fine
jobs = {}

api_bp = Blueprint("api", __name__)

UPLOAD_FOLDER = "data/inputs"


# ── ENDPOINT 1: Upload document ───────────────────────────────────────────────

@api_bp.route("/api/upload", methods=["POST"])
def upload_document():
    """
    Receive a text document from the frontend.
    Save it to data/inputs/.
    Return the filename for subsequent steps.
    """

    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    if not allowed_file(file.filename):
        extensions = ", ".join(sorted(f".{ext}" for ext in ALLOWED_EXTENSIONS))
        return jsonify({"error": f"Supported file types: {extensions}"}), 400

    try:
        normalized = normalize_uploaded_file(file, UPLOAD_FOLDER)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({
        "success"          : True,
        "filename"         : normalized["filename"],
        "display_filename" : normalized["display_filename"],
        "filepath"         : normalized["filepath"],
        "source_filepath"  : normalized["source_filepath"],
        "source_format"    : normalized["source_format"],
        "word_count"       : normalized["word_count"],
        "message"          : (
            f"Document uploaded: {normalized['display_filename']} "
            f"→ normalized to {normalized['filename']} "
            f"({normalized['word_count']} words)"
        )
    })


@api_bp.route("/api/fetch-news", methods=["POST"])
def fetch_news():
    """
    MODE A — Live news ingestion.

    Fetches real RSS news matching topics, saves as input document.
    Returns filepath ready for /api/build-graph.

    Body: { "topics": ["RBI", "interest rate", "India inflation"] }
    """
    data   = request.get_json()
    topics = data.get("topics", [])

    if not topics:
        return jsonify({"error": "topics list is required"}), 400

    # Clean and validate topics
    topics = [t.strip() for t in topics if t.strip()]
    if not topics:
        return jsonify({"error": "topics list is empty after cleaning"}), 400

    job_id = str(uuid.uuid4())[:8]

    def run_news_fetch():
        jobs[job_id] = {"status": "running", "step": "Fetching RSS feeds..."}
        try:
            from knowledge.news_ingestor import fetch_live_news

            result = fetch_live_news(topics=topics, save=True)

            if result["article_count"] == 0:
                jobs[job_id] = {
                    "status"       : "complete",
                    "warning"      : "No articles found — using fallback document",
                    "filepath"     : result["filepath"],
                    "filename"     : os.path.basename(result["filepath"]),
                    "article_count": 0,
                    "word_count"   : result["word_count"],
                    "sources"      : [],
                    "topics"       : topics,
                    "mode"         : "live"
                }
            else:
                jobs[job_id] = {
                    "status"       : "complete",
                    "filepath"     : result["filepath"],
                    "filename"     : os.path.basename(result["filepath"]),
                    "article_count": result["article_count"],
                    "word_count"   : result["word_count"],
                    "sources"      : result["sources"],
                    "topics"       : topics,
                    "mode"         : "live",
                    "message"      : (
                        f"Fetched {result['article_count']} articles "
                        f"from {len(result['sources'])} sources — "
                        f"{result['word_count']} words"
                    )
                }

        except ImportError as e:
            jobs[job_id] = {
                "status": "error",
                "error" : "feedparser not installed. Run: pip install feedparser==6.0.11"
            }
        except Exception as e:
            jobs[job_id] = {"status": "error", "error": str(e)}

    threading.Thread(target=run_news_fetch, daemon=True).start()
    return jsonify({
        "job_id" : job_id,
        "message": f"Fetching news for: {', '.join(topics)}"
    })


@api_bp.route("/api/historical-events", methods=["GET"])
def list_historical_events():
    """
    Returns the list of available historical events for backtesting.
    Used by the UI to populate the historical event dropdown.
    """
    try:
        from knowledge.news_ingestor import list_historical_events as _list
        events = _list()
        return jsonify({"events": events, "count": len(events)})
    except Exception as e:
        return jsonify({"events": [], "error": str(e)}), 200


@api_bp.route("/api/load-historical", methods=["POST"])
def load_historical():
    """
    MODE B — Load a historical document for backtesting.

    Loads pre-written historical document (outcome not in text).
    Copies it to data/inputs/ so /api/build-graph can find it.
    Returns filepath ready for /api/build-graph.
    Also returns actual_outcome — used after simulation to compute Brier score.

    Body: { "event_id": "rbi_rate_hike_2022" }

    ROOT CAUSE FIX:
    load_historical_document() returns a path inside data/historical_events/docs/
    but build_knowledge_graph() always looks in data/inputs/
    Solution: copy the file to data/inputs/ before returning the filename.
    """
    import shutil

    data     = request.get_json()
    event_id = data.get("event_id", "").strip()

    if not event_id:
        return jsonify({"error": "event_id is required"}), 400

    try:
        from knowledge.news_ingestor import load_historical_document

        # Load metadata and original file path from historical_events/docs/
        result = load_historical_document(event_id=event_id)

        original_path = result["filepath"]   # data/historical_events/docs/xxx.txt
        doc_filename  = os.path.basename(original_path)

        # Copy to data/inputs/ — this is where build_knowledge_graph looks
        inputs_dir   = "data/inputs"
        os.makedirs(inputs_dir, exist_ok=True)
        dest_path = os.path.join(inputs_dir, doc_filename)

        shutil.copy2(original_path, dest_path)
        print(f"  Copied historical doc to: {dest_path}")

        return jsonify({
            "status"        : "complete",
            "filepath"      : dest_path,
            "filename"      : doc_filename,
            "event_id"      : event_id,
            "actual_outcome": result["actual_outcome"],
            "date"          : result["date"],
            "description"   : result["description"],
            "domain"        : result.get("domain", "unknown"),
            "word_count"    : result["word_count"],
            "mode"          : "historical",
            "message"       : (
                f"Loaded: {result['description'][:60]}... "
                f"({result['word_count']} words)"
            )
        })

    except (FileNotFoundError, ValueError) as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/api/event-templates", methods=["GET"])
def list_event_templates_endpoint():
    """Return the available market event templates."""
    try:
        from market.template_renderer import list_event_templates
        templates = list_event_templates()
        return jsonify({"templates": templates, "count": len(templates)})
    except Exception as e:
        return jsonify({"templates": [], "error": str(e)}), 200


@api_bp.route("/api/event-templates/<template_id>", methods=["GET"])
def get_event_template_endpoint(template_id):
    """Return the full template definition for one market event template."""
    try:
        from market.template_renderer import load_event_template
        template = load_event_template(template_id)
        return jsonify(template)
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/api/event-templates/render", methods=["POST"])
def render_event_template_endpoint():
    """Fill a market template with user values and return a ready scenario."""
    data = request.get_json()
    template_id = (data or {}).get("template_id", "").strip()
    user_inputs = (data or {}).get("inputs", {})

    if not template_id:
        return jsonify({"error": "template_id is required"}), 400

    try:
        from market.template_renderer import render_event_template
        rendered = render_event_template(template_id, user_inputs)
        return jsonify(rendered)
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/api/simulation-chat", methods=["POST"])
def simulation_chat_endpoint():
    """Interactive post-simulation analysis for sector and forecast-change questions."""
    data = request.get_json() or {}
    mode = data.get("mode", "").strip()
    question = data.get("question", "").strip()
    topic = data.get("topic", "").strip() or "Current market scenario"
    sector_key = data.get("sector", "").strip()
    cohort_key = data.get("cohort", "").strip()
    counterfactual_target = data.get("counterfactual_target", "").strip()
    simulation_ids = data.get("simulation_ids", [])
    market_impact = data.get("market_impact", {})
    causal_dag_path = data.get("causal_dag_path", "").strip()

    if not mode:
        return jsonify({"error": "mode is required"}), 400
    if not market_impact:
        return jsonify({"error": "market_impact is required"}), 400

    try:
        from simulation.simulation_chat import run_simulation_chat
        result = run_simulation_chat(
            mode=mode,
            question=question,
            market_impact=market_impact,
            topic=topic,
            sector_key=sector_key,
            cohort_key=cohort_key,
            simulation_ids=simulation_ids,
            causal_dag_path=causal_dag_path,
            counterfactual_target=counterfactual_target
        )
        if result.get("error"):
            return jsonify(result), 400
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route("/api/score-prediction", methods=["POST"])
def score_prediction():
    """
    Score a completed historical backtest against the actual outcome.
    Call this after /api/run-simulation completes for a historical event.

    Body: {
      "predicted_probs": {"panic": 80, "cautious": 15, "optimistic": 5},
      "actual_outcome" : "panic",
      "event_id"       : "rbi_rate_hike_2022"
    }

    Returns: { brier_score, interpretation, correct, predicted_probs, actual_outcome }
    """
    data            = request.get_json()
    predicted_probs = data.get("predicted_probs", {})
    actual_outcome  = data.get("actual_outcome", "")
    event_id        = data.get("event_id", "unknown")
    topic           = data.get("topic", event_id)
    event_type      = data.get("event_type", "general")
    event_date      = data.get("event_date", "")
    domain          = data.get("domain", "")
    model_version   = data.get("model_version", "v3")
    phase_config    = data.get("phase_config", [])
    branch_count    = int(data.get("branch_count", 0) or 0)
    agent_count     = int(data.get("agent_count", 0) or 0)
    used_market_roles = bool(data.get("used_market_roles", True))
    market_impact   = data.get("market_impact", {})
    actual_sector_moves = data.get("actual_sector_moves", {})

    if not predicted_probs or not actual_outcome:
        return jsonify({"error": "predicted_probs and actual_outcome required"}), 400

    try:
        from analysis.backtest_engine import (
            compute_brier_score,
            interpret_brier_score
        )
        from analysis.prediction_logger import (
            compute_track_record_summary,
            log_prediction
        )

        # Convert percentage to 0-1 scale
        probs_01 = {k: v / 100.0 for k, v in predicted_probs.items()}

        brier  = compute_brier_score(probs_01, actual_outcome)
        interp = interpret_brier_score(brier)

        dominant_predicted = max(predicted_probs, key=predicted_probs.get)
        correct = dominant_predicted == actual_outcome
        logged_entry = log_prediction(
            event_id=event_id,
            topic=topic,
            predicted_probs=probs_01,
            actual_outcome=actual_outcome,
            dominant_predicted=dominant_predicted,
            brier_score=brier,
            interpretation=interp,
            correct=correct,
            event_type=event_type,
            event_date=event_date,
            domain=domain,
            model_version=model_version,
            phase_config=phase_config,
            branch_count=branch_count,
            agent_count=agent_count,
            used_market_roles=used_market_roles,
            market_impact=market_impact,
            actual_sector_moves=actual_sector_moves
        )
        track_record = compute_track_record_summary()

        return jsonify({
            "event_id"          : event_id,
            "brier_score"       : brier,
            "interpretation"    : interp,
            "correct"           : correct,
            "dominant_predicted": dominant_predicted,
            "actual_outcome"    : actual_outcome,
            "predicted_probs"   : predicted_probs,
            "logged_prediction" : logged_entry,
            "track_record_summary": track_record
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/api/prediction-track-record", methods=["GET"])
def prediction_track_record():
    """Return aggregate prediction log summary and markdown table."""
    try:
        from analysis.prediction_logger import compute_track_record_summary
        return jsonify(compute_track_record_summary())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── ENDPOINT 2: Build knowledge graph ─────────────────────────────────────────

@api_bp.route("/api/build-graph", methods=["POST"])
def build_graph():
    """
    Run Module 2 on the uploaded document.
    Returns job_id — client polls /api/status/<job_id> for completion.
    """

    data = request.get_json()
    filename = data.get("filename")

    if not filename:
        return jsonify({"error": "filename required"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": f"File not found: {filename}"}), 404

    graph_name = filename.rsplit(".", 1)[0]   # remove extension
    job_id = str(uuid.uuid4())[:8]

    # Start background thread so API returns immediately
    def run_graph_job():
        jobs[job_id] = {"status": "running", "step": "Building knowledge graph..."}
        try:
            from knowledge.graph_builder import build_knowledge_graph
            result = build_knowledge_graph(filepath, graph_name)
            jobs[job_id] = {
                "status"      : "complete",
                "graph_name"  : graph_name,
                "entity_count": result["entity_count"],
                "edge_count"  : result["relationship_count"],
                "message"     : f"Graph built: {result['entity_count']} entities, "
                                f"{result['relationship_count']} relationships"
            }
        except Exception as e:
            jobs[job_id] = {"status": "error", "error": str(e)}

    thread = threading.Thread(target=run_graph_job)
    thread.daemon = True
    thread.start()

    return jsonify({"job_id": job_id, "message": "Graph building started"})


# ── ENDPOINT 3: Run simulation ─────────────────────────────────────────────────

@api_bp.route("/api/run-simulation", methods=["POST"])
def run_simulation_endpoint():
    """
    Run Module 5 parallel simulation.
    Accepts configuration from frontend.
    Returns job_id for polling.
    """

    data = request.get_json()

    topic       = data.get("topic", "General social and economic prediction")
    situation   = data.get("situation", "A significant event has occurred.")
    event_type  = data.get("event_type", "general")
    graph_name  = data.get("graph_name", "").strip()
    num_agents  = min(int(data.get("num_agents", 5)), 10)   # cap at 10 for speed
    num_rounds  = min(int(data.get("num_rounds", 3)), 5)    # cap at 5
    num_branches = min(int(data.get("num_branches", 3)), 5)

    events = data.get("events", [
        "Situation continues to develop with new information emerging.",
        "Experts publish analysis of the unfolding events.",
        "Public response and institutional reactions are observed."
    ])

    actions = data.get("actions", [
        "wait and observe before acting",
        "immediately revise plans",
        "research historical data before deciding",
        "spread information to network",
        "consult an expert or advisor",
        "take immediate protective action"
    ])

    job_id = str(uuid.uuid4())[:8]
    inferred_causal_dag_path = ""
    if graph_name:
        candidate = os.path.join("data", "graphs", f"{graph_name}_causal.json")
        if os.path.exists(candidate):
            inferred_causal_dag_path = candidate

    def run_sim_job():
        jobs[job_id] = {
            "status": "running",
            "step"  : f"Starting {num_branches} simulation branches...",
            "live_focus": {
                "branch_id": "",
                "round_number": 0,
                "round_label": "",
                "market_role": "",
                "agent_name": "",
                "focus_terms": [],
                "pulse": int(time.time() * 1000),
            }
        }
        try:
            from simulation.parallel_branches import run_parallel_branches

            def update_live_focus(payload):
                current = jobs.get(job_id)
                if not isinstance(current, dict) or current.get("status") != "running":
                    return

                current["step"] = payload.get("step", current.get("step", "Running simulation..."))
                current["live_focus"] = {
                    "kind": payload.get("kind", ""),
                    "branch_id": payload.get("branch_id", ""),
                    "round_number": payload.get("round_number", 0),
                    "round_label": payload.get("round_label", ""),
                    "market_role": payload.get("market_role", ""),
                    "agent_name": payload.get("agent_name", ""),
                    "focus_terms": payload.get("focus_terms", [])[:8],
                    "pulse": int(time.time() * 1000),
                }

            jobs[job_id]["step"] = "Running agents across rounds..."
            results = run_parallel_branches(
                topic             = topic,
                initial_situation = situation,
                events_per_round  = events,
                available_actions = actions,
                num_branches      = num_branches,
                num_agents        = num_agents,
                num_rounds        = num_rounds,
                event_type        = event_type,
                causal_dag_path   = inferred_causal_dag_path or None,
                status_callback   = update_live_focus
            )

            jobs[job_id]["step"] = "Generating report (1/6) — executive summary..."
            from analysis.report_engine import ReportEngine
            engine = ReportEngine(
                simulation_ids=[b["simulation_id"] for b in results["branches"]],
                topic=topic, outcome_probs=results["outcome_probs"])

            # Generate each section with live status updates
            # so the frontend shows progress instead of appearing frozen
            exec_summary = engine.generate_executive_summary()
            jobs[job_id]["step"] = "Generating report (2/6) — predicted outcome..."

            predicted = engine.generate_predicted_outcome()
            jobs[job_id]["step"] = "Generating report (3/6) — causal drivers..."

            causal = engine.generate_causal_drivers()
            jobs[job_id]["step"] = "Generating report (4/6) — agent behavior..."

            agent_beh = engine.generate_agent_behavior()
            jobs[job_id]["step"] = "Generating report (5/6) — dissenting views..."

            dissent = engine.generate_dissenting_views()
            jobs[job_id]["step"] = "Generating report (6/6) — confidence assessment..."

            confidence_sec = engine.generate_confidence_assessment()

            # Compute smooth outcome_probs from aggregated agent belief
            # distributions rather than binary branch classification counts.
            # Binary counts: cautious=100%, optimistic=0% → Brier=1.0
            # Agent averages: cautious=60%, optimistic=30% → Brier=0.49
            # Agent averages are scientifically more honest and give
            # fairer Brier scores for near-correct predictions.

            smooth_probs = results.get("outcome_probs", {})

            # Try to get agent-level distributions from branch results
            all_dists = []
            for branch in results.get("branches", []):
                db_path = branch.get("db_path") or (
                    f"data/simulations/{branch.get('simulation_id','')}.db"
                )
                if os.path.exists(db_path):
                    try:
                        import sqlite3, json as _json
                        conn   = sqlite3.connect(db_path)
                        cursor = conn.cursor()
                        cursor.execute("""
                            SELECT belief FROM agent_actions
                            WHERE round_number = (SELECT MAX(round_number) FROM agent_actions)
                        """)
                        for (belief_text,) in cursor.fetchall():
                            if belief_text:
                                # Parse "cautious: 53%, optimistic: 30%, ..."
                                import re
                                matches = re.findall(
                                    r'(\w+):\s*(\d+(?:\.\d+)?)%', belief_text)
                                if matches:
                                    dist = {m[0]: float(m[1])/100 for m in matches}
                                    total = sum(dist.values())
                                    if total > 0:
                                        all_dists.append(
                                            {k: v/total for k,v in dist.items()})
                        conn.close()
                    except Exception:
                        pass

            if all_dists:
                import statistics as _stats
                all_outcomes = set()
                for d in all_dists:
                    all_outcomes.update(d.keys())
                smooth_probs = {
                    o: round(_stats.mean(
                        d.get(o, 0.0) for d in all_dists) * 100, 1)
                    for o in all_outcomes
                }

            jobs[job_id]["step"] = "Generating market impact analysis..."
            market_impact = None
            try:
                from analysis.market_impact_mapper import generate_full_market_impact

                market_impact = generate_full_market_impact(
                    behavioral_distribution=smooth_probs,
                    event_type=event_type,
                    topic=topic,
                    branch_count=num_branches
                )
            except Exception as e:
                print(f"  Warning: market impact generation failed: {e}")

            # Assemble the full report from pre-generated sections
            report = engine._assemble_report(
                exec_summary,
                predicted,
                causal,
                agent_beh,
                dissent,
                confidence_sec,
                market_impact=market_impact,
                population_model=results.get("population_model"),
            )

            jobs[job_id] = {"status": "complete",
                           "topic"            : topic,
                           "graph_name"       : graph_name,
                           "simulation_ids"   : [b["simulation_id"] for b in results["branches"]],
                           "causal_dag_path"  : inferred_causal_dag_path,
                           "outcome_probs"    : smooth_probs,
                           "dominant_outcome" : results["dominant_outcome"],
                           "prediction"       : results["prediction"],
                           "report"           : report,
                           "market_impact"    : market_impact,
                           "population_model" : results.get("population_model"),
                           "event_type"       : event_type,
                           "num_agents"       : num_agents,
                           "num_branches"     : num_branches}

        except Exception as e:
            jobs[job_id] = {"status": "error", "error": str(e)}

    thread = threading.Thread(target=run_sim_job)
    thread.daemon = True
    thread.start()

    return jsonify({
        "job_id" : job_id,
        "message": f"Simulation started: {num_branches} branches × {num_agents} agents × {num_rounds} rounds",
        "estimated_minutes": round(num_branches * num_agents * num_rounds * 3 / 60 * 0.25, 1)
    })


# ── ENDPOINT 4: Get status of any job ─────────────────────────────────────────

@api_bp.route("/api/status/<job_id>", methods=["GET"])
def get_status(job_id):
    """
    Poll this endpoint to check if a background job is done.
    Frontend polls every 5 seconds.
    """

    if job_id not in jobs:
        return jsonify({"status": "not_found"}), 404

    return jsonify(jobs[job_id])


# ── ENDPOINT 5: Get existing report ───────────────────────────────────────────

@api_bp.route("/api/get-report", methods=["GET"])
def get_report():
    """
    Return the most recently generated prediction report.
    """

    reports_dir = "data/reports"
    if not os.path.exists(reports_dir):
        return jsonify({"error": "No reports found"}), 404

    report_files = [
        f for f in os.listdir(reports_dir)
        if f.startswith("report_") and f.endswith(".md")
    ]

    if not report_files:
        return jsonify({"error": "No reports generated yet"}), 404

    # Get most recent
    latest = max(
        report_files,
        key=lambda f: os.path.getmtime(os.path.join(reports_dir, f))
    )

    with open(os.path.join(reports_dir, latest), "r", encoding="utf-8") as f:
        content = f.read()

    return jsonify({
        "filename": latest,
        "content" : content
    })


@api_bp.route("/api/export-report-pdf", methods=["POST"])
def export_report_pdf():
    """Render the current report into a lightweight PDF and return it as a download."""
    data = request.get_json() or {}
    topic = data.get("topic", "DARSH Prediction")
    report = data.get("report", "")
    outcome_probs = data.get("outcome_probs", {}) or {}
    market_impact = data.get("market_impact", {}) or {}
    population_model = data.get("population_model", {}) or {}

    if not report.strip():
        return jsonify({"error": "report is required"}), 400

    try:
        from analysis.pdf_export import build_report_pdf_bytes

        pdf_bytes = build_report_pdf_bytes(
            topic=topic,
            report_markdown=report,
            outcome_probs=outcome_probs,
            market_impact=market_impact,
            population_model=population_model,
        )
        safe_topic = "".join(ch if ch.isalnum() or ch in {"_", "-"} else "_" for ch in topic.strip().replace(" ", "_")) or "report"
        return send_file(
            BytesIO(pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"darsh_report_{safe_topic}.pdf",
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── ENDPOINT 6: Health check ───────────────────────────────────────────────────

@api_bp.route("/api/health", methods=["GET"])
def health():
    """Simple health check — confirms API is running."""
    return jsonify({"status": "ok", "message": "DARSH API is running"})


@api_bp.route("/api/graph/<graph_name>", methods=["GET"])
def get_graph(graph_name):
    """
    Return knowledge graph JSON ready for D3 visualization.
    graph_name: the base filename without extension, e.g. 'rbi_article'

    Returns D3-compatible format:
    {
      "nodes": [{"id": "RBI", "type": "ORGANIZATION", "description": "..."}],
      "links": [{"source": "RBI", "target": "Sensex", "relation": "CAUSED"}],
      "causal_nodes": [...],
      "causal_links": [...]   <- includes strength and time_lag
    }
    """
    import json

    graph_path  = f"data/graphs/{graph_name}.json"
    causal_path = f"data/graphs/{graph_name}_causal.json"

    if not os.path.exists(graph_path):
        # Try partial match
        graphs_dir = "data/graphs"
        matches = [f for f in os.listdir(graphs_dir)
                  if f.endswith(".json") and "_causal" not in f
                  and graph_name.lower() in f.lower()]
        if matches:
            graph_path = os.path.join(graphs_dir, matches[0])
        else:
            return jsonify({"error": f"Graph not found: {graph_name}"}), 404

    with open(graph_path) as f:
        graph_data = json.load(f)

    # Convert to D3 format
    nodes = []
    for node in graph_data.get("nodes", []):
        nodes.append({
            "id"         : node.get("id", ""),
            "type"       : node.get("type", "UNKNOWN"),
            "description": node.get("description", "")
        })

    links = []
    for edge in graph_data.get("edges", []):
        links.append({
            "source"  : edge.get("source", ""),
            "target"  : edge.get("target", ""),
            "relation": edge.get("relation", ""),
            "inferred": edge.get("inferred", False),
            "weight"  : edge.get("weight", 1.0),
        })

    # Load causal DAG if exists
    causal_links = []
    if os.path.exists(causal_path):
        with open(causal_path) as f:
            causal_data = json.load(f)
        for edge in causal_data.get("causal_edges", []):
            causal_links.append({
                "source"  : edge.get("cause", ""),
                "target"  : edge.get("effect", ""),
                "strength": edge.get("strength", 0.5),
                "time_lag": edge.get("time_lag", "unknown"),
                "causal"  : True
            })

    return jsonify({
        "graph_name"  : graph_name,
        "nodes"       : nodes,
        "links"       : links,
        "causal_links": causal_links,
        "node_count"  : len(nodes),
        "link_count"  : len(links)
    })


@api_bp.route("/api/graphs", methods=["GET"])
def list_graphs():
    """List all available knowledge graphs."""
    graphs_dir = "data/graphs"
    if not os.path.exists(graphs_dir):
        return jsonify({"graphs": []})

    graphs = []
    for f in os.listdir(graphs_dir):
        if f.endswith(".json") and "_causal" not in f:
            name = f.replace(".json", "")
            has_causal = os.path.exists(
                os.path.join(graphs_dir, f"{name}_causal.json"))
            graphs.append({
                "name"      : name,
                "filename"  : f,
                "has_causal": has_causal
            })

    return jsonify({"graphs": graphs})



@api_bp.route("/api/simulations/history", methods=["GET"])
def simulation_history():
    """
    Return list of all past simulations from SQLite databases.
    Used by the History screen to populate the timeline.
    """
    import sqlite3, json

    sims_dir = "data/simulations"
    if not os.path.exists(sims_dir):
        return jsonify({"simulations": []})

    history = []
    db_files = sorted(
        [f for f in os.listdir(sims_dir) if f.endswith(".db")],
        key=lambda f: os.path.getmtime(os.path.join(sims_dir, f)),
        reverse=True
    )[:20]  # last 20 simulations

    for db_file in db_files:
        db_path = os.path.join(sims_dir, db_file)
        sim_id  = db_file.replace(".db", "")
        try:
            conn   = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Get basic stats
            cursor.execute("SELECT COUNT(DISTINCT agent_name) FROM agent_actions")
            agent_count = cursor.fetchone()[0]

            cursor.execute("SELECT MAX(round_number) FROM agent_actions")
            max_round = cursor.fetchone()[0] or 0

            # Get dominant action
            cursor.execute("""
                SELECT action, COUNT(*) as cnt FROM agent_actions
                WHERE action IS NOT NULL
                GROUP BY action ORDER BY cnt DESC LIMIT 1
            """)
            dom_row = cursor.fetchone()
            dominant_action = dom_row[0] if dom_row else "unknown"

            # Get world state progression
            cursor.execute("""
                PRAGMA table_info(world_states)
            """)
            world_state_columns = {row[1] for row in cursor.fetchall()}

            if {"round_label", "time_window"}.issubset(world_state_columns):
                cursor.execute("""
                    SELECT round_number, round_label, time_window,
                           dominant_action, avg_confidence
                    FROM world_states ORDER BY round_number
                """)
                rounds = [
                    {
                        "round": r[0],
                        "round_label": r[1],
                        "time_window": r[2],
                        "dominant": r[3],
                        "confidence": r[4]
                    }
                    for r in cursor.fetchall()
                ]
            else:
                cursor.execute("""
                    SELECT round_number, dominant_action, avg_confidence
                    FROM world_states ORDER BY round_number
                """)
                rounds = [
                    {"round": r[0], "dominant": r[1], "confidence": r[2]}
                    for r in cursor.fetchall()
                ]

            conn.close()

            history.append({
                "simulation_id"  : sim_id,
                "db_file"        : db_file,
                "agent_count"    : agent_count,
                "round_count"    : max_round,
                "dominant_action": dominant_action,
                "rounds"         : rounds,
                "modified"       : os.path.getmtime(db_path)
            })

        except Exception as e:
            continue

    return jsonify({"simulations": history, "count": len(history)})


@api_bp.route("/api/simulations/<sim_id>/round/<int:round_num>", methods=["GET"])
def get_round_detail(sim_id, round_num):
    """
    Return all agent actions and thoughts for a specific round.
    Used by the timeline scrubber to show what happened each round.
    """
    import sqlite3

    db_path = f"data/simulations/{sim_id}.db"
    if not os.path.exists(db_path):
        return jsonify({"error": f"Simulation {sim_id} not found"}), 404

    conn   = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(agent_actions)")
    agent_action_columns = {row[1] for row in cursor.fetchall()}

    if "market_role" in agent_action_columns:
        cursor.execute("""
            SELECT agent_name, agent_type, market_role, action, confidence, thought, belief
            FROM agent_actions
            WHERE round_number = ?
            ORDER BY agent_type, agent_name
        """, (round_num,))
    else:
        cursor.execute("""
            SELECT agent_name, agent_type, action, confidence, thought, belief
            FROM agent_actions
            WHERE round_number = ?
            ORDER BY agent_type, agent_name
        """, (round_num,))

    agents = []
    for row in cursor.fetchall():
        if "market_role" in agent_action_columns:
            agents.append({
                "name"      : row[0],
                "type"      : row[1],
                "market_role": row[2],
                "action"    : row[3],
                "confidence": row[4],
                "thought"   : row[5],
                "belief"    : row[6]
            })
        else:
            agents.append({
                "name"      : row[0],
                "type"      : row[1],
                "market_role": "RETAIL_TRADER",
                "action"    : row[2],
                "confidence": row[3],
                "thought"   : row[4],
                "belief"    : row[5]
            })

    cursor.execute("PRAGMA table_info(world_states)")
    world_state_columns = {row[1] for row in cursor.fetchall()}

    if {"round_label", "time_window"}.issubset(world_state_columns):
        cursor.execute("""
            SELECT round_label, time_window, world_state, dominant_action, avg_confidence
            FROM world_states WHERE round_number = ?
        """, (round_num,))
        ws_row = cursor.fetchone()
        world_state = {
            "round_label": ws_row[0] if ws_row else "",
            "time_window": ws_row[1] if ws_row else "",
            "text"      : ws_row[2] if ws_row else "",
            "dominant"  : ws_row[3] if ws_row else "",
            "confidence": ws_row[4] if ws_row else 0
        }
    else:
        cursor.execute("""
            SELECT world_state, dominant_action, avg_confidence
            FROM world_states WHERE round_number = ?
        """, (round_num,))
        ws_row = cursor.fetchone()
        world_state = {
            "round_label": "",
            "time_window": "",
            "text"      : ws_row[0] if ws_row else "",
            "dominant"  : ws_row[1] if ws_row else "",
            "confidence": ws_row[2] if ws_row else 0
        }

    conn.close()

    return jsonify({
        "simulation_id": sim_id,
        "round"        : round_num,
        "agents"       : agents,
        "world_state"  : world_state
    })

@api_bp.route("/api/merge-graphs", methods=["POST"])
def merge_graphs_endpoint():
    """
    Merge multiple knowledge graphs into one combined world model.

    Body: {
      "graph_names": ["rbi_article", "live_rbi_20260319"],
      "merged_name": "rbi_combined"   (optional)
    }
    """
    data         = request.get_json()
    graph_names  = data.get("graph_names", [])
    merged_name  = data.get("merged_name", None)

    if len(graph_names) < 2:
        return jsonify({"error": "Need at least 2 graph names"}), 400

    try:
        from knowledge.graph_merger import merge_graphs
        result = merge_graphs(graph_names, merged_name)
        return jsonify({
            "success"    : True,
            "merged_name": result["merged_name"],
            "node_count" : len(result["merged"]["nodes"]),
            "edge_count" : len(result["merged"]["edges"]),
            "message"    : (
                f"Merged {len(graph_names)} graphs → "
                f"{len(result['merged']['nodes'])} nodes, "
                f"{len(result['merged']['edges'])} edges"
            )
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
