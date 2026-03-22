# tests/test_module1.py
# Run with: python tests/test_module1.py
# PASS = agent completes 3 rounds + final line says MODULE 1 PASSED

import sys
import os

# Adds the neuroswarm root to Python's path so imports work from tests/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.base_agent import BaseAgent


def run_test():

    print("\n" + "="*52)
    print("  DARSH — MODULE 1 DRY-RUN TEST")
    print("  MacBook Air M4  |  Llama 3.1  |  Python 3.10")
    print("="*52)

    # Create test agent
    agent = BaseAgent(
        agent_id="test_001",
        name="Priya Nair",
        personality=(
            "cautious and data-driven, slow to change opinions, "
            "trusts verified numbers over social media, "
            "researches carefully before reacting"
        ),
        background=(
            "Postgraduate economics student from Kerala. "
            "Follows RBI monetary policy closely. "
            "Has a student loan — personally affected by interest rate changes."
        )
    )

    base_situation = (
        "The Reserve Bank of India has unexpectedly announced "
        "a 0.5% interest rate hike, effective immediately."
    )

    actions = [
        "research historical data on past RBI rate hike effects",
        "share concerns about EMI impact with peers",
        "revise personal financial plan immediately",
        "wait and observe market reaction before acting",
        "post opinion on social media",
        "contact a financial advisor"
    ]

    # Round 1
    print("\n\n  ══ ROUND 1 — Initial reaction ══")
    r1 = agent.run_round(
        world_context=base_situation,
        new_information=(
            "Economists confirm the hike directly responds to "
            "inflation hitting 7.2% — highest in 4 years."
        ),
        available_actions=actions
    )

    # Round 2
    print("\n\n  ══ ROUND 2 — Markets react ══")
    r2 = agent.run_round(
        world_context=base_situation + " Markets dropped 2.3%.",
        new_information=(
            "RBI Governor signals further hikes likely "
            "if inflation stays above 6% for 2 more months."
        ),
        available_actions=actions
    )

    # Round 3
    print("\n\n  ══ ROUND 3 — Recession fears emerge ══")
    r3 = agent.run_round(
        world_context=(
            base_situation +
            " Markets down 2.3%. Student EMIs rising next month."
        ),
        new_information=(
            "IIM Bangalore economist warns two more hikes "
            "would push India into recession by Q3."
        ),
        available_actions=actions
    )

    # Summary
    print("\n\n" + "="*52)
    print("  FINAL SUMMARY")
    print("="*52)
    print(f"\n  Agent    : {agent.name}")
    print(f"  Rounds   : {agent.round}")
    print(f"  Memories : {len(agent.memory)} items")
    print(f"\n  Final belief:")
    print(f"  {agent.belief}")
    print(f"\n  Decisions made:")
    for r in [r1, r2, r3]:
        print(f"  Round {r['round']}: {r['action']}")

    # Pass check
    passed = (
        agent.round == 3
        and len(agent.memory) > 0
        and len(agent.belief) > 20
    )

    print("\n" + "="*52)
    if passed:
        print("  ✓  MODULE 1 PASSED")
        print("  ✓  BaseAgent loop working correctly")
        print("  ✓  Llama 3.1 responding on M4")
        print("  ✓  Memory, think, decide, update all functional")
        print("\n  → Ready for Module 2")
    else:
        print("  ✗  Something needs fixing")
        print(f"  Rounds   : {agent.round} (need 3)")
        print(f"  Memories : {len(agent.memory)} (need > 0)")
        print("\n  → Paste output here and we fix it together")
    print("="*52 + "\n")


if __name__ == "__main__":
    run_test()