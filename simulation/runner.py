# simulation/runner.py
#
# THE SIMULATION RUNNER
#
# Runs one complete simulation: agents × rounds.
# This is the core loop of the entire DARSH system.
#
# Structure:
#   for round in range(total_rounds):
#       for agent in all_agents:
#           result = agent.run_round(world_state, new_info, actions)
#           environment.log_action(result)
#       environment.update_world_state(all_results)
#
# That's the entire simulation engine. The intelligence comes
# from the agents (Module 4), the world model (Modules 2+3),
# and the parallel branching (parallel_branches.py).

import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation.environment import SimulationEnvironment
from simulation.market_timeline import build_market_timeline
from agents.agent_factory import create_agent_population
from simulation.social_network import SocialNetwork

def _get_causal_insight(causal_dag_data: dict, world_context: str) -> str:
    """
    Given the current world context and causal DAG data,
    find the most relevant causal relationships to surface.

    Searches causal edges for entities mentioned in the world context.
    Returns a concise description of predicted downstream effects.
    Example output: "Rate Hike causes Market Drop (strength 0.8, immediate);
                     Rate Hike causes EMI Increase (strength 0.95, days)"
    """
    if not causal_dag_data:
        return ""

    edges = causal_dag_data.get("causal_edges", [])
    if not edges:
        return ""

    context_lower = world_context.lower()
    relevant_effects = []

    for edge in edges[:20]:  # check first 20 edges for performance
        cause = edge.get("cause", "")
        effect = edge.get("effect", "")
        strength = edge.get("strength", 0)
        time_lag = edge.get("time_lag", "unknown")

        # Only include if the cause is mentioned in current world context
        if cause.lower() in context_lower and strength >= 0.5:
            relevant_effects.append(
                f"{cause} → {effect} (strength {strength}, {time_lag})"
            )

    if not relevant_effects:
        return ""

    return "; ".join(relevant_effects[:3])  # limit to 3 most relevant



def run_simulation(
    simulation_id: str,
    topic: str,
    initial_situation: str,
    events_per_round: list,
    available_actions: list,
    num_agents: int = 8,
    num_rounds: int = 3,
    event_type: str = "general",
    knowledge_context: str = "",
    causal_context: str = "",
    causal_dag_path: str = None,    # NEW: path to causal DAG JSON
    branch_narrative: dict = None,
    status_callback = None,
    verbose: bool = True
) -> dict:
    """
    Run one complete simulation and return results.

    simulation_id      : unique ID e.g. "sim_branch_001"
    topic              : simulation topic
    initial_situation  : starting world state
    events_per_round   : list of new events, one per round
                         e.g. ["Markets drop 2%", "RBI confirms more hikes"]
    available_actions  : actions agents can choose from
    num_agents         : how many agents to create
    num_rounds         : how many rounds to simulate
    knowledge_context  : summary from Module 2 graph
    causal_context     : summary from Module 3 causal DAG
    verbose            : whether to print detailed output

    Returns dict with all results and outcome classification.
    """

    if verbose:
        print(f"\n{'='*50}")
        print(f"  SIMULATION: {simulation_id}")
        print(f"  Topic: {topic}")
        print(f"  Agents: {num_agents}  |  Rounds: {num_rounds}")
        print(f"{'='*50}")

    import time as _time
    # Unique simulation namespace prevents memory bleed between runs
    # Without this, branch_01 agents from RBI simulation contaminate
    # branch_01 agents from GDP simulation via shared ChromaDB collections
    memory_sim_id = f"{simulation_id}_{int(_time.time())}"
    agents = create_agent_population(
        num_agents,
        topic,
        event_type=event_type,
        use_semantic_memory=True,
        simulation_id=memory_sim_id
    )

    # Create environment
    env = SimulationEnvironment(
        simulation_id=simulation_id,
        topic=topic,
        initial_situation=initial_situation,
        agents=agents,
        knowledge_context=knowledge_context,
        causal_context=causal_context
    )

    # v2: build social network for agent-to-agent influence
    social_network = SocialNetwork()
    social_network.build(agents)

    # v2: load causal DAG for agent-aware causal reasoning
    causal_dag_data = None
    if causal_dag_path and os.path.exists(causal_dag_path):
        try:
            with open(causal_dag_path, "r") as f:
                causal_dag_data = json.load(f)
            print(f"  Causal DAG loaded: "
                  f"{len(causal_dag_data.get('causal_edges', []))} edges")
        except Exception as e:
            print(f"  Warning: could not load causal DAG: {e}")

    # Ensure events list covers all rounds
    while len(events_per_round) < num_rounds:
        events_per_round.append("Situation continues to develop.")

    market_timeline = build_market_timeline(
        num_rounds=num_rounds,
        events_per_round=events_per_round,
        topic=topic,
        event_type=event_type
    )

    # ── MAIN SIMULATION LOOP ──────────────────────────────────────────────
    all_round_summaries = []
    final_beliefs = []

    for round_num in range(1, num_rounds + 1):
        round_context = market_timeline[round_num - 1]

        if verbose:
            print(f"\n\n{'─'*50}")
            print(
                f"  ROUND {round_num} of {num_rounds} — "
                f"{round_context['label']} ({round_context['time_window']})"
            )
            print(f"  World: {env.world_state[:100]}...")
            print(f"{'─'*50}")

        # Get new event for this round
        new_event = round_context["event"]
        world_context = env.get_world_state_for_agents(
            round_context=round_context,
            branch_narrative=branch_narrative
        )

        if status_callback:
            status_callback({
                "kind": "round_start",
                "step": (
                    f"Round {round_num}/{num_rounds} — "
                    f"{round_context['label']} is unfolding..."
                ),
                "branch_id": simulation_id,
                "round_number": round_num,
                "round_label": round_context["label"],
                "market_role": "",
                "agent_name": "",
                "focus_terms": [
                    topic,
                    new_event,
                    round_context["label"],
                    round_context["time_window"],
                ],
            })

        # v2: enrich context with causal predictions if DAG available
        if causal_dag_data:
            causal_insight = _get_causal_insight(causal_dag_data, world_context)
            if causal_insight:
                world_context = world_context + f"\n\nCausal model predicts: {causal_insight}"

        round_results = []

        # v2: Each agent gets social feed BEFORE thinking,
        # then posts their thought for others to read
        for agent in agents:
            # Get this agent's social feed (posts from agents they follow)
            social_feed = social_network.get_feed(agent.agent_id)
            market_role = getattr(agent, "market_role", "RETAIL_TRADER")

            if status_callback:
                status_callback({
                    "kind": "agent_thinking",
                    "step": (
                        f"Round {round_num}/{num_rounds} — "
                        f"{agent.name} ({market_role}) is thinking..."
                    ),
                    "branch_id": simulation_id,
                    "round_number": round_num,
                    "round_label": round_context["label"],
                    "market_role": market_role,
                    "agent_name": agent.name,
                    "focus_terms": [
                        topic,
                        new_event,
                        round_context["label"],
                        round_context["time_window"],
                        market_role,
                        agent.name,
                    ],
                })

            result = agent.run_round(
                world_context=world_context,
                new_information=new_event,
                available_actions=available_actions,
                social_feed=social_feed          # NEW
            )

            # After thinking, post this agent's thought to the network
            social_network.post(
                agent_id   = agent.agent_id,
                agent_name = agent.name,
                agent_type = getattr(agent, "agent_type", "UNKNOWN"),
                content    = result.get("thought", "")
            )

            if status_callback:
                status_callback({
                    "kind": "agent_update",
                    "step": (
                        f"Round {round_num}/{num_rounds} — "
                        f"{agent.name} updated belief and action."
                    ),
                    "branch_id": simulation_id,
                    "round_number": round_num,
                    "round_label": round_context["label"],
                    "market_role": market_role,
                    "agent_name": agent.name,
                    "focus_terms": [
                        topic,
                        new_event,
                        round_context["label"],
                        result.get("thought", "")[:220],
                        result.get("action", ""),
                        market_role,
                        agent.name,
                    ],
                })

            # Add agent type to result for analysis
            result["agent_type"] = getattr(agent, "agent_type", "UNKNOWN")
            result["market_role"] = market_role

            # Log to database
            env.log_action(round_num, result)
            round_results.append(result)

        # Clear posts at end of round — each round starts fresh
        social_network.clear_round_posts()
        # Update world state based on collective agent behavior
        round_summary = env.update_world_state(
            round_results,
            new_event,
            round_context=round_context
        )

        if status_callback:
            status_callback({
                "kind": "round_complete",
                "step": (
                    f"Round {round_num}/{num_rounds} complete — "
                    f"{round_summary.get('dominant_action', 'agents repositioned')}."
                ),
                "branch_id": simulation_id,
                "round_number": round_num,
                "round_label": round_context["label"],
                "market_role": "",
                "agent_name": "",
                "focus_terms": [
                    topic,
                    new_event,
                    round_context["label"],
                    round_summary.get("dominant_action", ""),
                ],
            })

        round_summary["round_results"] = round_results
        all_round_summaries.append(round_summary)

        # Collect final beliefs for outcome classification
        if round_num == num_rounds:
            final_beliefs = round_results

    # ── CLASSIFY FINAL OUTCOME ─────────────────────────────────────────────
    final_outcome = env.classify_outcome(final_beliefs)

    # Count how many agents hold each position
    action_distribution = {}
    if final_beliefs:
        for r in final_beliefs:
            action = r.get("action", "unknown")
            action_distribution[action] = action_distribution.get(action, 0) + 1

    # Average final confidence
    final_confidences = [
        float(r.get("confidence", 0.5))
        for r in final_beliefs
        if r.get("confidence") is not None
    ]
    avg_final_confidence = (
        sum(final_confidences) / len(final_confidences)
        if final_confidences else 0.5
    )

    result_summary = {
        "simulation_id"       : simulation_id,
        "topic"               : topic,
        "num_agents"          : num_agents,
        "num_rounds"          : num_rounds,
        "event_type"          : event_type,
        "branch_narrative"    : branch_narrative,
        "final_outcome"       : final_outcome,
        "action_distribution" : action_distribution,
        "avg_final_confidence": round(avg_final_confidence, 3),
        "market_timeline"     : market_timeline,
        "round_summaries"     : all_round_summaries,
        "db_path"             : env.db_path
    }

    if verbose:
        print(f"\n\n{'='*50}")
        print(f"  SIMULATION COMPLETE: {simulation_id}")
        print(f"  Final outcome    : {final_outcome.upper()}")
        print(f"  Avg confidence   : {avg_final_confidence:.2f}")
        print(f"  Action breakdown :")
        for action, count in sorted(
            action_distribution.items(), key=lambda x: x[1], reverse=True
        ):
            print(f"    {count} agents → {action}")
        print(f"{'='*50}")

    return result_summary
