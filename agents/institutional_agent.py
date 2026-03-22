# agents/institutional_agent.py
#
# THE INSTITUTIONAL AGENT
#
# Reasoning style: rules, procedures, and risk management.
# An institutional agent represents organizations — banks,
# government bodies, corporations — not individuals.
#
# Institutional agents:
#   - Follow established procedures before acting
#   - Are highly risk-averse — protecting the institution is priority
#   - Communicate formally and carefully
#   - Slow to change position even with new evidence
#   - Have fiduciary or regulatory obligations
#
# In simulations, institutional agents represent stability anchors.
# They slow down trend propagation and add realistic institutional
# inertia to the system.
#
# Real-world equivalent: RBI itself, HDFC Bank risk committee,
# government ministry, large corporate treasury.

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.base_agent import BaseAgent
from core.llm_caller import ask_llm


class InstitutionalAgent(BaseAgent):
    """
    Thinks through institutional risk management and procedure.
    Overrides only think().
    """

    def __init__(self, agent_id, name, personality, background,
                 institution_type="financial", chroma_client=None, simulation_id="default"):
        super().__init__(agent_id, name, personality, background,
                        chroma_client=chroma_client, simulation_id=simulation_id)
        self.agent_type = "INSTITUTIONAL"
        # What kind of institution this represents
        self.institution_type = institution_type
        # Institutions have mandates — what they are required to do
        self.mandate = "preserve stability and manage risk within regulatory guidelines"

    def think(self, world_context: str, social_feed: str = "") -> str:
        social_section = f"\n{social_feed}\n" if social_feed else ""

        system = (
            f"You are {self.name}, representing a {self.institution_type} institution.\n"
            f"Background: {self.background}\nMandate: {self.mandate}\n"
            f"Think in terms of risk, procedure, and institutional responsibility.\n"
            f"Speak carefully and formally. Do not speculate."
        )
        prompt = (
            f"Situation: {world_context}\n"
            f"{social_section}"
            f"\nMemories: {self.memory_as_text(query=world_context)}\n\n"
            f"Assess this situation:\n"
            f"1. What is the primary risk to your institution?\n"
            f"2. What does your mandate require you to consider?\n"
            f"2 sentences. Formal and measured."
        )
        return ask_llm(prompt, system_prompt=system)