# agents/rational_agent.py
#
# THE RATIONAL AGENT
#
# Reasoning style: expected utility calculation.
# Before reacting to anything, a rational agent:
#   1. Lists what they know (evidence)
#   2. Considers possible outcomes
#   3. Weighs probability × impact for each outcome
#   4. Chooses the action with highest expected value
#
# This agent is slow to react and rarely panics.
# In simulations, rational agents tend to stabilize group behavior
# because they resist emotional contagion.
#
# Real-world equivalent: institutional investor, policy analyst,
# trained economist.

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.base_agent import BaseAgent
from core.llm_caller import ask_llm


class RationalAgent(BaseAgent):
    """
    Thinks by calculating expected utility.
    Overrides only think() — all other methods from BaseAgent.
    """

    def __init__(self, agent_id, name, personality, background,
                 chroma_client=None, simulation_id="default"):
        super().__init__(agent_id, name, personality, background,
                        chroma_client=chroma_client, simulation_id=simulation_id)
        self.agent_type = "RATIONAL"
        # Rational agents track an explicit utility score
        self.utility_score = 0.0

    def think(self, world_context: str, social_feed: str = "") -> str:
        social_section = f"\n{social_feed}\n" if social_feed else ""

        system = (
            f"You are {self.name}, a rational decision-maker.\n"
            f"Background: {self.background}\n"
            f"You always think in terms of evidence, probabilities, and expected outcomes.\n"
            f"You do not react emotionally. You calculate."
        )
        prompt = (
            f"Situation: {world_context}\n"
            f"{social_section}"
            f"\nYour memories: {self.memory_as_text(query=world_context)}\n\n"
            f"Think through this rationally:\n"
            f"1. What is the evidence? (one sentence)\n"
            f"2. What are the two most likely outcomes?\n"
            f"3. What is your calculated conclusion?\n"
            f"Keep total response to 3 sentences. Be analytical, not emotional."
        )
        return ask_llm(prompt, system_prompt=system)