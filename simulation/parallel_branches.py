# simulation/parallel_branches.py
#
# PARALLEL BRANCH MANAGER — THE KEY SUPERIORITY OVER MIROFISH
#
# MiroFish runs one simulation → gets one story → reports it as "the future"
#
# We run N branches simultaneously → get N different stories →
# calculate probability of each outcome type.
#
# Why do branches differ even with same starting conditions?
# Because agents use an LLM with temperature > 0, meaning responses
# have natural variation. Small differences compound across rounds
# to produce meaningfully different outcomes — just like reality.
#
# This is ensemble simulation — the same approach used in:
#   - Weather forecasting (ensemble NWP models)
#   - Financial risk modeling (Monte Carlo)
#   - Military planning (war-gaming multiple scenarios)

import sys
import os
import json
import time
from multiprocessing import Pool, cpu_count
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation.market_timeline import get_branch_narratives
from simulation.runner import run_simulation


def run_single_branch(branch_config: dict, status_callback=None) -> dict:
    """
    Run one simulation branch. Called by multiprocessing.Pool.

    branch_config : dict containing all parameters for run_simulation()
    Returns       : result dict from run_simulation()
    """

    branch_id = branch_config["simulation_id"]
    print(f"\n  [Branch {branch_id}] Starting...")

    try:
        if status_callback:
            status_callback({
                "kind": "branch_start",
                "step": f"Starting {branch_id}...",
                "branch_id": branch_id,
                "round_number": 0,
                "round_label": "",
                "market_role": "",
                "agent_name": "",
                "focus_terms": [
                    branch_config.get("topic", ""),
                    branch_config.get("event_type", "general"),
                    branch_config.get("branch_narrative", {}).get("label", ""),
                ],
            })

        result = run_simulation(
            simulation_id      = branch_config["simulation_id"],
            topic              = branch_config["topic"],
            initial_situation  = branch_config["initial_situation"],
            events_per_round   = branch_config["events_per_round"],
            available_actions  = branch_config["available_actions"],
            num_agents         = branch_config["num_agents"],
            num_rounds         = branch_config["num_rounds"],
            event_type         = branch_config.get("event_type", "general"),
            knowledge_context  = branch_config.get("knowledge_context", ""),
            causal_context     = branch_config.get("causal_context", ""),
            causal_dag_path    = branch_config.get("causal_dag_path", None),  # NEW
            branch_narrative   = branch_config.get("branch_narrative"),
            status_callback    = status_callback,
            verbose            = False
        )
        result["branch_narrative"] = branch_config.get("branch_narrative")
        print(f"  [Branch {branch_id}] Complete → outcome: {result['final_outcome']}")

        if status_callback:
            status_callback({
                "kind": "branch_complete",
                "step": f"{branch_id} complete — outcome {result['final_outcome']}.",
                "branch_id": branch_id,
                "round_number": branch_config["num_rounds"],
                "round_label": "complete",
                "market_role": "",
                "agent_name": "",
                "focus_terms": [
                    branch_config.get("topic", ""),
                    result.get("final_outcome", ""),
                    result.get("dominant_action", ""),
                ],
            })
        return result

    except Exception as e:
        print(f"  [Branch {branch_id}] Error: {e}")
        return {
            "simulation_id": branch_id,
            "final_outcome": "error",
            "error": str(e),
            "action_distribution": {},
            "avg_final_confidence": 0.0
        }


def run_parallel_branches(
    topic: str,
    initial_situation: str,
    events_per_round: list,
    available_actions: list,
    num_branches: int = 3,
    num_agents: int = 6,
    num_rounds: int = 3,
    event_type: str = "general",
    knowledge_context: str = "",
    causal_context: str = "",
    causal_dag_path: str = None,      # NEW
    status_callback = None
) -> dict:
    """
    Run N simulation branches in parallel and aggregate results.

    num_branches : how many independent simulations to run
                   3 is good for testing, 5-10 for real predictions
    num_agents   : agents per branch (keep low for speed during testing)
    num_rounds   : rounds per branch

    Returns dict with:
      branches         : list of individual branch results
      outcome_probs    : probability of each outcome type
      consensus_action : most common action across all branches
      prediction       : plain English prediction summary
    """

    # Clean up old agent memories to prevent cross-simulation contamination
    try:
        from agents.semantic_memory import clear_old_agent_memories
        clear_old_agent_memories(keep_recent_n=3)
    except Exception:
        pass   # non-fatal

    print(f"\n{'='*55}")
    print(f"  PARALLEL BRANCH SIMULATION")
    print(f"  Topic    : {topic}")
    print(f"  Branches : {num_branches}")
    print(f"  Agents   : {num_agents} per branch")
    print(f"  Rounds   : {num_rounds} per branch")
    print(f"  Total LLM calls ≈ {num_branches * num_agents * num_rounds * 3}")
    print(f"{'='*55}")

    # Build config for each branch
    # Each branch gets a unique ID but identical starting conditions
    branch_configs = []
    branch_narratives = get_branch_narratives(num_branches)
    for i in range(num_branches):
        import time as _t
        run_stamp = str(int(_t.time()))[-6:]   # last 6 digits of timestamp
        branch_configs.append({
            "simulation_id"    : f"branch_{run_stamp}_{i+1:02d}",
            "topic"            : topic,
            "initial_situation": initial_situation,
            "events_per_round" : events_per_round.copy(),
            "available_actions": available_actions,
            "num_agents"       : num_agents,
            "num_rounds"       : num_rounds,
            "event_type"       : event_type,
            "branch_narrative" : branch_narratives[i],
            "knowledge_context": knowledge_context,
            "causal_context"   : causal_context,
            "causal_dag_path"  : causal_dag_path   # NEW
        })

    # ── RUN BRANCHES ──────────────────────────────────────────────────────
    # Use max 3 parallel processes to avoid overwhelming Ollama
    # Ollama handles one request at a time — parallelism helps with
    # the Python overhead but actual LLM calls are still sequential
    max_workers = min(num_branches, 3)

    start_time = time.time()
    branch_results = []

    # Note: running sequentially for Ollama compatibility
    # (Ollama queues parallel requests anyway)
    print(f"\n  Running {num_branches} branches sequentially")
    print(f"  (Ollama processes requests one at a time)")

    for config in branch_configs:
        result = run_single_branch(config, status_callback=status_callback)
        branch_results.append(result)

    elapsed = time.time() - start_time
    print(f"\n  All branches complete in {elapsed:.0f} seconds")

    # ── v2: Aggregate using proper mathematical methods ───────────────────
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

    total_branches = len(branch_results)

    # Convert counts to percentages for display
    outcome_probs = {
        k: round(v / total_branches * 100, 1)
        for k, v in outcome_counts.items()
    }

    # v2: also compute standard deviation across branches for confidence intervals
    from statistics import stdev as _stdev
    outcome_std = {}
    for outcome in outcome_probs:
        branch_probs = [
            1.0 if b.get("final_outcome") == outcome else 0.0
            for b in branch_results
        ]
        if len(branch_probs) > 1:
            outcome_std[outcome] = round(_stdev(branch_probs) * 100, 1)
        else:
            outcome_std[outcome] = 0.0

    dominant_outcome = max(outcome_counts, key=outcome_counts.get)
    consensus_action = max(all_actions, key=all_actions.get) if all_actions else "none"
    overall_confidence = round(
        sum(confidences) / len(confidences), 3
    ) if confidences else 0.5
    dominant_prob = outcome_probs[dominant_outcome]
    dominant_std  = outcome_std.get(dominant_outcome, 0.0)

    prediction = (
        f"Across {total_branches} simulation branches, the most likely outcome is "
        f"'{dominant_outcome}' with {dominant_prob}% probability "
        f"(±{dominant_std}% across branches). "
        f"The dominant agent behavior was to '{consensus_action}'. "
        f"Average agent confidence: {overall_confidence:.1%}."
    )

    population_model = None
    try:
        from analysis.india_market_population import compute_population_weighted_sentiment

        population_model = compute_population_weighted_sentiment(
            branch_results=branch_results,
            topic=topic,
            event_type=event_type
        )
    except Exception as e:
        print(f"  Warning: population-weighted cohort model failed: {e}")

    return {
        "topic"             : topic,
        "num_branches"      : total_branches,
        "event_type"        : event_type,
        "branch_narratives" : branch_narratives,
        "branches"          : branch_results,
        "outcome_probs"     : outcome_probs,
        "outcome_std"       : outcome_std,
        "outcome_counts"    : outcome_counts,
        "dominant_outcome"  : dominant_outcome,
        "consensus_action"  : consensus_action,
        "overall_confidence": overall_confidence,
        "prediction"        : prediction,
        "population_model"  : population_model,
        "elapsed_seconds"   : round(elapsed, 1)
    }


def print_results(results: dict):
    """Pretty-print the parallel branch results."""

    print(f"\n\n{'='*55}")
    print(f"  PREDICTION RESULTS")
    print(f"  Topic: {results['topic']}")
    print(f"{'='*55}")

    print(f"\n  Outcome probability distribution:")
    for outcome, prob in sorted(
        results["outcome_probs"].items(), key=lambda x: x[1], reverse=True
    ):
        bar = "█" * int(prob / 5)
        print(f"  {outcome:12} {bar} {prob}%")

    print(f"\n  Individual branch outcomes:")
    for branch in results["branches"]:
        bid = branch.get("simulation_id", "?")
        outcome = branch.get("final_outcome", "?")
        conf = branch.get("avg_final_confidence", 0)
        print(f"  Branch {bid} → {outcome:12} (confidence: {conf:.2f})")

    print(f"\n  Consensus agent action : {results['consensus_action']}")
    print(f"  Overall confidence     : {results['overall_confidence']:.1%}")
    print(f"  Time taken             : {results['elapsed_seconds']}s")

    print(f"\n  PREDICTION SUMMARY:")
    print(f"  {results['prediction']}")
