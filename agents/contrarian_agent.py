# agents/contrarian_agent.py
#
# THE CONTRARIAN AGENT
#
# Reasoning style: systematic opposition to majority view.
# A contrarian agent's default is skepticism of consensus.
# They look for what everyone else is missing.
#
# Contrarian agents:
#   - Push back against dominant narratives
#   - Often identify real risks that groupthink ignores
#   - Can also be wrong — opposing consensus isn't always right
#   - Create healthy debate in simulations
#
# In simulations, contrarian agents prevent total consensus
# and introduce alternative hypotheses. Without them, simulations
# converge too quickly to one opinion.
#
# Real-world equivalent: short-seller, investigative journalist,
# opposition analyst, academic critic.

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.base_agent import BaseAgent


class ContrarianAgent(BaseAgent):
    """
    Thinks by challenging the dominant view.
    Overrides only think().
    """

    def __init__(self, agent_id, name, personality, background,
                 chroma_client=None, simulation_id="default"):
        super().__init__(agent_id, name, personality, background,
                        chroma_client=chroma_client, simulation_id=simulation_id)
        self.agent_type = "CONTRARIAN"
        self.temperature = 0.4
        # What the contrarian perceives as the current majority view
        self.perceived_majority_view = "No majority view established yet."

    def think(self, world_context: str, social_feed: str = "") -> str:
        social_section = f"\n{social_feed}\n" if social_feed else ""

        system = (
            f"You are {self.name}, a natural contrarian.\n"
            f"Background: {self.background}\n"
            f"Your instinct is to question consensus and argue the overlooked angle."
        )
        prompt = (
            f"Situation: {world_context}\n"
            f"{social_section}"
            f"\nWhat most people believe: {self.perceived_majority_view}\n\n"
            f"Memories: {self.memory_as_text(query=world_context)}\n\n"
            f"What is the mainstream narrative getting WRONG? "
            f"What important angle is everyone overlooking? Max 2 sentences."
        )
        return self._ask_thought_llm(prompt, system)

    def set_majority_view(self, view: str):
        """Called by simulator to tell this agent what the majority thinks."""
        self.perceived_majority_view = view
