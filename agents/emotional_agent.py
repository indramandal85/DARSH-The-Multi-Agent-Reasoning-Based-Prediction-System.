# agents/emotional_agent.py
#
# THE EMOTIONAL AGENT
#
# Reasoning style: sentiment-driven reaction.
# An emotional agent processes information through how it FEELS
# rather than what the data objectively says.
#
# Emotional agents:
#   - React faster than rational agents
#   - Are more susceptible to alarming news
#   - Can spread panic or enthusiasm through social networks
#   - Update beliefs more dramatically on new information
#
# In simulations, emotional agents create volatility and
# amplify trends — they're why markets overshoot in both directions.
#
# Real-world equivalent: retail investor, social media user,
# person reading headlines without context.

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.base_agent import BaseAgent
from core.llm_caller import ask_llm


class EmotionalAgent(BaseAgent):
    """
    Thinks through emotional response and sentiment.
    Overrides only think().
    """

    def __init__(self, agent_id, name, personality, background,
                 chroma_client=None, simulation_id="default"):
        super().__init__(agent_id, name, personality, background,
                        chroma_client=chroma_client, simulation_id=simulation_id)
        self.agent_type = "EMOTIONAL"
        # Emotional state: -1.0 = very anxious, 0 = neutral, +1.0 = optimistic
        self.emotional_state = 0.0

    def think(self, world_context: str, social_feed: str = "") -> str:
        social_section = f"\n{social_feed}\n" if social_feed else ""

        mood = ("optimistic and confident" if self.emotional_state > 0.3
                else "anxious and worried" if self.emotional_state < -0.3
                else "neutral but alert")
        system = (
            f"You are {self.name}, someone who reacts emotionally.\n"
            f"Background: {self.background}\nCurrent mood: {mood}\n"
            f"You lead with feelings, not data."
        )
        prompt = (
            f"Situation: {world_context}\n"
            f"{social_section}"
            f"\nMemories: {self.memory_as_text(query=world_context)}\n\n"
            f"What is your immediate emotional reaction?\n"
            f"Respond emotionally, viscerally. Max 2 sentences."
        )
        thought = ask_llm(prompt, system_prompt=system)

        negative_words = ["worried","anxious","fear","panic","crash","crisis","danger"]
        positive_words = ["confident","opportunity","stable","recover","hopeful"]
        thought_lower = thought.lower()
        neg = sum(1 for w in negative_words if w in thought_lower)
        pos = sum(1 for w in positive_words if w in thought_lower)
        self.emotional_state = max(-1.0, min(1.0,
            self.emotional_state + (pos - neg) * 0.15))
        return thought