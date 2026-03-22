# simulation/environment.py
#
# THE SIMULATION ENVIRONMENT
#
# Think of this as the "world" that agents live in.
# It holds:
#   - The current state of the world (what has happened so far)
#   - The list of all agents participating
#   - The knowledge graph context (from Module 2)
#   - The causal model context (from Module 3)
#   - A log of everything that has happened each round
#
# Every round, the environment:
#   1. Tells each agent the current world state
#   2. Collects all agent actions
#   3. Updates the world state based on collective behavior
#   4. Logs everything to SQLite for later analysis

import sys
import os
import json
import sqlite3
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class SimulationEnvironment:
    """
    The world in which agents operate.

    Tracks world state evolution across rounds.
    Logs all agent actions to SQLite database.
    """

    def __init__(
        self,
        simulation_id: str,
        topic: str,
        initial_situation: str,
        agents: list,
        knowledge_context: str = "",
        causal_context: str = "",
        db_path: str = None
    ):
        """
        simulation_id     : unique ID for this run e.g. "sim_001"
        topic             : what this simulation is about
        initial_situation : the starting world state description
        agents            : list of agent objects from Module 4
        knowledge_context : summary of knowledge graph (from Module 2)
        causal_context    : summary of causal DAG (from Module 3)
        db_path           : where to save SQLite database
        """

        self.simulation_id   = simulation_id
        self.topic           = topic
        self.agents          = agents
        self.knowledge_ctx   = knowledge_context
        self.causal_ctx      = causal_context
        self.current_round   = 0

        # World state starts at initial situation and evolves each round
        self.world_state = initial_situation
        self.world_state_history = [initial_situation]

        # Action log — what every agent did every round
        self.action_log = []

        # Outcome tracking — what the simulation concludes
        self.outcomes = []

        # Database setup
        if db_path is None:
            os.makedirs("data/simulations", exist_ok=True)
            db_path = f"data/simulations/{simulation_id}.db"

        self.db_path = db_path
        self._init_database()

        print(f"  Environment ready: {simulation_id}")
        print(f"  Topic    : {topic}")
        print(f"  Agents   : {len(agents)}")
        print(f"  Database : {db_path}")


    def _init_database(self):
        """Create SQLite tables for storing simulation results."""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Table for individual agent actions each round
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_actions (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                simulation_id   TEXT,
                round_number    INTEGER,
                agent_id        TEXT,
                agent_name      TEXT,
                agent_type      TEXT,
                market_role     TEXT,
                thought         TEXT,
                action          TEXT,
                confidence      REAL,
                belief          TEXT,
                timestamp       TEXT
            )
        """)

        # Table for world state at each round
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS world_states (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                simulation_id   TEXT,
                round_number    INTEGER,
                round_label     TEXT,
                time_window     TEXT,
                world_state     TEXT,
                dominant_action TEXT,
                avg_confidence  REAL,
                timestamp       TEXT
            )
        """)

        # Table for final simulation outcomes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS outcomes (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                simulation_id   TEXT,
                outcome_type    TEXT,
                description     TEXT,
                confidence      REAL,
                supporting_agents INTEGER,
                timestamp       TEXT
            )
        """)

        # Safe schema migration for older simulation databases.
        cursor.execute("PRAGMA table_info(agent_actions)")
        existing_columns = {row[1] for row in cursor.fetchall()}
        if "market_role" not in existing_columns:
            cursor.execute(
                "ALTER TABLE agent_actions "
                "ADD COLUMN market_role TEXT DEFAULT 'RETAIL_TRADER'"
            )

        cursor.execute("PRAGMA table_info(world_states)")
        world_state_columns = {row[1] for row in cursor.fetchall()}
        if "round_label" not in world_state_columns:
            cursor.execute(
                "ALTER TABLE world_states "
                "ADD COLUMN round_label TEXT DEFAULT ''"
            )
        if "time_window" not in world_state_columns:
            cursor.execute(
                "ALTER TABLE world_states "
                "ADD COLUMN time_window TEXT DEFAULT ''"
            )

        conn.commit()
        conn.close()


    def get_world_state_for_agents(self, round_context: dict = None, branch_narrative: dict = None) -> str:
        """
        Build the full context string that gets passed to each agent's think().
        Includes current situation + knowledge context + causal context.
        """

        context = f"Current situation: {self.world_state}"

        if round_context:
            context += (
                f"\n\nCurrent market stage: {round_context.get('label', '')} "
                f"({round_context.get('time_window', '')})."
                f"\nStage focus: {round_context.get('focus', '')}"
            )

        if branch_narrative:
            context += (
                f"\n\nScenario lens for this branch: "
                f"{branch_narrative.get('label', '')} — "
                f"{branch_narrative.get('summary', '')}"
            )

        if self.knowledge_ctx:
            context += f"\n\nBackground knowledge: {self.knowledge_ctx[:300]}"

        if self.causal_ctx:
            context += f"\n\nKnown causal factors: {self.causal_ctx[:200]}"

        return context


    def log_action(self, round_num: int, agent_result: dict):
        """Save one agent's round result to the database and action log.

        NOTE: belief_distribution is kept in memory only (not saved to SQLite).
        It is used by classify_outcome() at end of simulation via runner.py's
        final_beliefs list, which holds the original result dicts including
        belief_distribution. Do not strip it here.
        """
        # Keep the full dict in memory (including belief_distribution)
        self.action_log.append(agent_result)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO agent_actions
            (simulation_id, round_number, agent_id, agent_name, agent_type,
             market_role, thought, action, confidence, belief, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            self.simulation_id,
            round_num,
            agent_result.get("agent_id", ""),
            agent_result.get("name", ""),
            agent_result.get("agent_type", ""),
            agent_result.get("market_role", "RETAIL_TRADER"),
            agent_result.get("thought", "")[:500],
            agent_result.get("action", ""),
            float(agent_result.get("confidence", 0.5)),
            agent_result.get("belief", "")[:500],
            datetime.now().isoformat()
        ))

        conn.commit()
        conn.close()


    def update_world_state(self, round_results: list, new_event: str = None, round_context: dict = None):
        """
        After all agents act in a round, update the world state.

        Finds the most common action (dominant behavior) and
        adds it to the world state narrative.
        Also logs the world state to database.

        round_results : list of agent result dicts from this round
        new_event     : optional external event injected this round
        """

        self.current_round += 1

        # Find dominant action this round
        actions = [r.get("action", "") for r in round_results if r.get("action")]
        if actions:
            dominant = max(set(actions), key=actions.count)
            action_count = actions.count(dominant)
        else:
            dominant = "no action"
            action_count = 0

        # Calculate average confidence
        confidences = [
            float(r.get("confidence", 0.5))
            for r in round_results
            if r.get("confidence") is not None
        ]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.5

        # Update world state narrative
        round_label = (round_context or {}).get("label", f"Round {self.current_round}")
        time_window = (round_context or {}).get("time_window", "")
        state_update = (
            f" During {round_label}"
            f"{f' ({time_window})' if time_window else ''}, "
            f"{action_count}/{len(round_results)} agents chose to '{dominant}'."
        )

        if new_event:
            state_update += f" New development: {new_event}"

        self.world_state = self.world_state + state_update
        self.world_state_history.append(self.world_state)

        # Save world state to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO world_states
            (simulation_id, round_number, round_label, time_window, world_state,
             dominant_action, avg_confidence, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            self.simulation_id,
            self.current_round,
            round_label,
            time_window,
            self.world_state[:1000],
            dominant,
            avg_confidence,
            datetime.now().isoformat()
        ))
        conn.commit()
        conn.close()

        print(f"\n  [World updated — Round {self.current_round}]")
        print(f"  Dominant action : '{dominant}' ({action_count}/{len(actions)} agents)")
        print(f"  Avg confidence  : {avg_confidence:.2f}")

        return {
            "round": self.current_round,
            "round_label": round_label,
            "time_window": time_window,
            "timeline_focus": (round_context or {}).get("focus", ""),
            "dominant_action": dominant,
            "action_count": action_count,
            "total_agents": len(round_results),
            "avg_confidence": avg_confidence,
            "world_state": self.world_state
        }


    def classify_outcome(self, round_results: list) -> str:
        """
        Classify the final simulation outcome from agent results.

        v2 UPGRADE: Uses actual Bayesian probability distributions when available.
        The v1 keyword counting was broken for v2 Bayesian belief text because:
        - "panic" IS in the keyword list → counted from "panic: 45%" labels
        - "optimistic" is NOT in the keyword list → NOT counted from "optimistic: 15%"
        - Result: panic always wins regardless of actual agent beliefs

        v2 fix: average the belief_distribution dicts directly.
        Keyword counting kept as fallback for old databases without distributions.
        """

        # ── v2 PATH: use actual Bayesian probability distributions ────────────
        # belief_distribution is set by run_round() from BeliefState.distribution
        distributions = [
            r.get("belief_distribution")
            for r in round_results
            if r.get("belief_distribution")
        ]

        if distributions:
            # Median-based aggregation — outlier resistant.
            #
            # Why median not mean:
            # Mean is skewed by extreme agents. One contrarian at panic=0.94
            # pulls the mean past optimistic even when 4/5 agents lean optimistic.
            # Sorted panic values: [0.37, 0.37, 0.43, 0.44, 0.94] → mean=0.51
            # Sorted panic values: [0.37, 0.37, 0.43, 0.44, 0.94] → median=0.43
            # Sorted optimistic:   [0.00, 0.44, 0.47, 0.47, 0.54] → median=0.47
            # Median correctly identifies optimistic as dominant.
            #
            # This is standard robust statistics — median is preferred over mean
            # when the distribution may contain outliers.

            import statistics

            all_outcomes = set()
            for d in distributions:
                all_outcomes.update(d.keys())

            medians = {}
            for outcome in all_outcomes:
                values = [d.get(outcome, 0.0) for d in distributions]
                medians[outcome] = statistics.median(values)

            # Find dominant outcome from medians
            dominant = max(medians, key=medians.get)
            dominant_prob = medians[dominant]

            # Classify as "divided" only if top two medians are very close (within 5%)
            sorted_probs = sorted(medians.values(), reverse=True)
            if (len(sorted_probs) >= 2 and
                    sorted_probs[0] - sorted_probs[1] < 0.05):
                return "divided"

            return dominant

        # ── v1 FALLBACK: keyword counting for old simulation data ─────────────
        # Fixed to include "optimistic" and "divided" as direct keywords
        # so Bayesian belief text labels are caught correctly
        beliefs = " ".join(r.get("belief", "").lower() for r in round_results)

        panic_score = sum(beliefs.count(w) for w in [
            "panic", "recession", "crisis", "crash", "catastrophic", "devastating"
        ])
        cautious_score = sum(beliefs.count(w) for w in [
            "cautious", "wait", "observe", "uncertain", "careful", "monitor"
        ])
        optimistic_score = sum(beliefs.count(w) for w in [
            "recover", "stable", "opportunity", "growth", "positive",
            "confident", "optimistic"   # ← "optimistic" added
        ])
        divided_score = sum(beliefs.count(w) for w in [
            "divided", "split", "mixed", "varied"
        ])

        scores = {
            "panic"    : panic_score,
            "cautious" : cautious_score,
            "optimistic": optimistic_score,
            "divided"  : divided_score
        }

        dominant = max(scores, key=scores.get)
        return "divided" if scores[dominant] == 0 else dominant
