# agents/tribal_agent.py
#
# THE TRIBAL AGENT
#
# Reasoning style: in-group conformity.
# A tribal agent's primary question is not "what do I think?"
# but "what does MY GROUP think?"
#
# Tribal agents:
#   - Look for social consensus before forming opinions
#   - Are highly influenced by trusted group members
#   - Resist information from out-groups even if factually correct
#   - Create echo chambers and information bubbles
#
# In simulations, tribal agents cluster into factions.
# They're responsible for polarization dynamics — two groups
# can hold completely opposite beliefs about the same facts.
#
# Real-world equivalent: strong party supporter, religious community
# member, sports fan — anyone whose group identity shapes their beliefs.

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.base_agent import BaseAgent


class TribalAgent(BaseAgent):
    """
    Thinks through in-group lens and social consensus.
    Overrides only think().
    """

    def __init__(self, agent_id, name, personality, background,
                 tribe="general public", chroma_client=None, simulation_id="default"):
        super().__init__(agent_id, name, personality, background,
                        chroma_client=chroma_client, simulation_id=simulation_id)
        self.agent_type = "TRIBAL"
        self.temperature = 0.5
        # Which group this agent identifies with most strongly
        self.tribe = tribe
        # What the tribe currently believes (updated externally by simulator)
        self.tribe_consensus = "No group consensus yet."

    def think(self, world_context: str, social_feed: str = "") -> str:
        social_section = f"\n{social_feed}\n" if social_feed else ""

        system = (
            f"You are {self.name}, strongly identified with: {self.tribe}.\n"
            f"Background: {self.background}\n"
            f"Your group's opinion matters more than abstract facts."
        )
        prompt = (
            f"Situation: {world_context}\n"
            f"{social_section}"
            f"\nWhat your group ({self.tribe}) believes: {self.tribe_consensus}\n\n"
            f"Memories: {self.memory_as_text(query=world_context)}\n\n"
            f"How do you interpret this through your group's lens? Max 2 sentences."
        )
        return self._ask_thought_llm(prompt, system)

    def update_tribe_consensus(self, new_consensus: str):
        """Called by the simulator when group opinion shifts."""
        self.tribe_consensus = new_consensus
        self.remember(f"Group consensus updated: {new_consensus[:50]}...")
