# core/base_agent.py
#
# THE BASE AGENT — foundation of the entire DARSH simulation.
#
# Key idea: a single LLM call is NOT an agent.
# An agent is a LOOP:
#
#   Round 1: Think about situation → Decide action → Update memory
#   Round 2: Think again (now WITH Round 1 memory) → Decide → Update
#   Round 3: Think again (with Rounds 1+2 memory) → Decide → Update
#
# Each round the agent knows more. This is what creates
# intelligent, evolving behaviour across simulation time.

from core.llm_caller import ask_llm, ask_llm_json
from agents.belief_state import BeliefState, get_likelihoods_from_llm, OUTCOMES     # NEW in Phase 2
from agents.semantic_memory import SemanticMemory   # NEW in Phase 2


class BaseAgent:
    """
    One intelligent agent in the DARSH simulation.

    Has identity, memory, belief, and a think→decide→update loop.
    All other agent types in Module 4 inherit from this class.
    """

    def __init__(
        self,
        agent_id: str,
        name: str,
        personality: str,
        background: str,
        chroma_client=None,       # NEW: shared ChromaDB client for semantic memory
        simulation_id: str = "default"  # NEW: ties memory to a specific simulation
    ):
        self.agent_id    = agent_id
        self.name        = name
        self.personality = personality
        self.background  = background

        # Memory: list of strings. Upgraded to ChromaDB in Module 4.
        #self.memory = []

        # v2: semantic memory via ChromaDB if client provided,
        # otherwise fall back to simple list (for tests that don't need it)
        if chroma_client is not None:
            self.memory = SemanticMemory(agent_id, chroma_client, simulation_id)
            self._use_semantic_memory = True
        else:
            self.memory = []
            self._use_semantic_memory = False

        # v2: belief_state replaces the verbal belief string
        # It's a proper probability distribution updated by Bayes' rule
        self.belief_state = BeliefState(outcomes=OUTCOMES)

        # Keep this for backward compatibility with Module 6 report engine
        # It gets updated each round to a human-readable summary
        self.belief      = self.belief_state.as_text()
        self.confidence  = self.belief_state.confidence()

        # Round counter
        self.round = 0


    # ── MEMORY ────────────────────────────────────────────────────────────────

    def remember(self, item: str, category: str = "observation"):
        """
        Store something in memory.
        v2: routes to SemanticMemory.store() or list.append() depending on setup.
        """
        if self._use_semantic_memory:
            self.memory.store(item, round_num=self.round, category=category)
        else:
            # Fallback: original list-based memory
            self.memory.append(f"[Round {self.round}] {item}")
            if len(self.memory) > 8:
                self.memory = self.memory[-8:]

    def memory_as_text(self, query: str = None) -> str:
        """
        Return relevant memories as formatted text for LLM prompts.
        v2: uses semantic search if ChromaDB memory is active.
        v1 fallback: returns last 8 items from list.
        """
        if self._use_semantic_memory:
            # Use the current world context as the query if none provided
            search_query = query or "recent important events and observations"
            return self.memory.retrieve(search_query, n_results=3)
        else:
            # Fallback: original list behavior
            if not self.memory:
                return "  No memories yet."
            return "\n".join(f"  {m}" for m in self.memory)


    # ── PHASE 1: THINK ────────────────────────────────────────────────────────

    def think(self, world_context: str, social_feed: str = "") -> str:
        """
        PHASE 1: Read the world, read social feed, produce a thought.

        v2 upgrade: social_feed parameter adds posts from followed agents.
        This creates real social influence — emotional agents see panic posts
        and become more fearful; rational agents filter social noise.
        """

        # Build social context section
        social_section = ""
        if social_feed:
            social_section = f"\n{social_feed}\n"

        system = (
            f"You are {self.name}.\n"
            f"Background: {self.background}\n"
            f"Personality: {self.personality}\n"
            f"Always respond in character."
        )

        prompt = (
            f"Current situation:\n{world_context}\n"
            f"{social_section}"
            f"\nYour most relevant memories:\n"
            f"{self.memory_as_text(query=world_context)}\n\n"
            f"What is your honest reaction to this situation?\n"
            f"First person. In character. Maximum 2 sentences."
        )

        return ask_llm(prompt, system_prompt=system)


    # ── PHASE 2: DECIDE ───────────────────────────────────────────────────────

    def decide(self, thought: str, available_actions: list) -> dict:
        """
        Given the thought, pick one action to take.
        Returns dict with 'action', 'reason', 'confidence'.
        """

        actions_text = "\n".join(f"  - {a}" for a in available_actions)

        system = (
            f"You are {self.name}. "
            f"Personality: {self.personality}. "
            f"Stay in character when deciding."
        )

        prompt = (
            f"Your thought: {thought}\n\n"
            f"Available actions:\n{actions_text}\n\n"
            f"Choose ONE action from the list.\n"
            f"Return JSON with exactly these keys:\n"
            f'  "action": the exact action string you chose\n'
            f'  "reason": one sentence why, as {self.name}\n'
            f'  "confidence": decimal 0.0 to 1.0'
        )

        result = ask_llm_json(prompt, system_prompt=system)

        # Safe fallback if JSON parsing failed
        if result.get("parse_error"):
            return {
                "action": available_actions[0],
                "reason": "Fallback — JSON parsing failed.",
                "confidence": 0.3
            }

        return result


    # ── PHASE 3: UPDATE BELIEF ────────────────────────────────────────────────

    def update_belief(
        self,
        new_information: str,
        thought: str = "",
        decision: dict = None,
        world_context: str = ""
    ):
        """
        PHASE 3: Receive new info. Update belief using Bayesian inference.

        v2 upgrade: replaces the verbal LLM rewrite with proper Bayes update.

        Step 1: Ask LLM to score how consistent this evidence is with each outcome
                (likelihoods — this is where LLM judgment is used)
        Step 2: Apply Bayes' rule to update the probability distribution
                (posterior — this is where math takes over from LLM)
        Step 3: Update self.belief (text) and self.confidence (float)
                for backward compatibility with report engine
        """

        evidence_packet = [f"New development: {new_information}"]
        if world_context:
            evidence_packet.append(f"Scenario context: {world_context[:320]}")
        if thought:
            evidence_packet.append(f"Agent interpretation: {thought}")
        chosen_action = (decision or {}).get("action", "")
        if chosen_action:
            evidence_packet.append(f"Chosen action: {chosen_action}")

        # Step 1: get likelihood scores from LLM
        likelihoods = get_likelihoods_from_llm(
            evidence="\n".join(evidence_packet),
            outcomes=OUTCOMES,
            agent_name=self.name,
            agent_personality=self.personality
        )

        # Step 2: Bayesian update
        self.belief_state.bayesian_update(likelihoods)

        # Step 3: update the text/float fields for backward compat
        self.belief = self.belief_state.as_text()
        self.confidence = self.belief_state.confidence()

        # Store in memory
        dominant = self.belief_state.dominant_outcome()
        self.remember(f"Info received: {new_information[:60]}...")
        self.remember(f"Belief: {dominant} most likely "
                     f"({self.belief_state.distribution[dominant]*100:.0f}%)")


    # ── FULL ROUND ────────────────────────────────────────────────────────────

    def run_round(
        self,
        world_context: str,
        new_information: str,
        available_actions: list,
        social_feed: str = ""       # NEW: feed from followed agents
    ) -> dict:
        """
        One complete Think → Decide → Update cycle.
        v2: social_feed injected into think() for social influence.
        """

        self.round += 1

        print(f"\n{'─'*52}")
        print(f"  {self.name}  |  Round {self.round}")
        print(f"{'─'*52}")

        # Phase 1 — Think (now with social feed)
        print("\n  [THINKING]")
        if social_feed:
            print(f"  (reading {social_feed.count('•')} social posts)")
        thought = self.think(world_context, social_feed=social_feed)
        print(f"  → {thought}")

        # Phase 2 — Decide (unchanged)
        print("\n  [DECIDING]")
        decision = self.decide(thought, available_actions)
        print(f"  → Action     : {decision.get('action')}")
        print(f"  → Reason     : {decision.get('reason')}")
        print(f"  → Confidence : {decision.get('confidence')}")

        # Phase 3 — Update belief (Bayesian, from Phase 1 fix)
        print("\n  [UPDATING BELIEF]")
        self.update_belief(
            new_information,
            thought=thought,
            decision=decision,
            world_context=world_context
        )
        print(f"  → {self.belief[:120]}")

        return {
            "agent_id"           : self.agent_id,
            "name"               : self.name,
            "thought"            : thought,
            "action"             : decision.get("action", "observe"),
            "reason"             : decision.get("reason", ""),
            "confidence"         : decision.get("confidence", 0.5),
            "belief"             : self.belief,
            # v2: include the actual probability dict so classify_outcome
            # can use Bayesian aggregation instead of keyword counting.
            # Without this, belief_distribution is always missing from
            # round_results and classify_outcome falls back to broken
            # keyword counting.
            "belief_distribution": (
                dict(self.belief_state.distribution)
                if hasattr(self, 'belief_state') and self.belief_state
                else {}
            ),
        }
