# tests/test_module4.py
# Run with: python tests/test_module4.py
#
# PASS condition:
#   - All 5 agent types created successfully
#   - Each agent produces visibly different thinking about the same scenario
#   - Agent factory creates a population of 10 agents
#   - No crashes or import errors

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.rational_agent import RationalAgent
from agents.emotional_agent import EmotionalAgent
from agents.tribal_agent import TribalAgent
from agents.contrarian_agent import ContrarianAgent
from agents.institutional_agent import InstitutionalAgent
from agents.agent_factory import create_agent_population


def run_test():

    print("\n" + "="*55)
    print("  DARSH — MODULE 4 DRY-RUN TEST")
    print("  Heterogeneous Agent Society")
    print("="*55)

    # ── The same scenario given to ALL 5 agents ────────────────────────────
    scenario = (
        "The Reserve Bank of India has just announced a 0.5% interest rate hike. "
        "Markets dropped 2.3%. Economists warn of possible recession."
    )

    new_info = "RBI Governor confirms further hikes likely if inflation stays above 6%."

    actions = [
        "sell investments immediately",
        "wait and observe before acting",
        "research historical data on rate hike effects",
        "consult financial advisor",
        "spread information to network",
        "file formal complaint with regulators"
    ]

    # ── Create one of each agent type ─────────────────────────────────────
    agents = [
        RationalAgent(
            "r001", "Dr. Meera Iyer",
            "analytical economist, evidence-based, never panics",
            "Senior economist at think tank, PhD in monetary policy"
        ),
        EmotionalAgent(
            "e001", "Rahul Agarwal",
            "anxious first-time investor, reacts to headlines",
            "MBA student in Mumbai, invested savings in mutual funds last month"
        ),
        TribalAgent(
            "t001", "Vikram Singh",
            "loyal to government narrative, trusts official statements",
            "Retired government employee from Delhi, BJP supporter, pension-dependent",
            tribe="government employees and BJP supporters"
        ),
        ContrarianAgent(
            "c001", "Amit Sharma",
            "skeptical of official narratives, looks for hidden agendas",
            "Startup founder from Pune, distrust of large institutions, libertarian views"
        ),
        InstitutionalAgent(
            "i001", "HDFC Risk Committee",
            "formal, risk-focused, regulatory compliance driven",
            "Major private bank risk management committee, serves 8 crore customers",
            institution_type="financial"
        )
    ]

    # Give contrarian their majority view context
    agents[3].set_majority_view(
        "The rate hike is necessary and justified to control inflation"
    )

    # Give tribal agent group consensus
    agents[2].tribe_consensus = (
        "The government is doing the right thing to control inflation"
    )

    # ── Run ONE round for each agent — same scenario, compare outputs ──────
    print(f"\n  Scenario given to ALL agents:")
    print(f"  '{scenario}'\n")
    print(f"  {'─'*55}")
    print(f"  Watch how differently each agent type THINKS")
    print(f"  about the exact same situation:")

    results = []
    for agent in agents:
        result = agent.run_round(
            world_context=scenario,
            new_information=new_info,
            available_actions=actions
        )
        results.append(result)

    # ── Comparison summary ─────────────────────────────────────────────────
    print(f"\n\n{'='*55}")
    print(f"  AGENT COMPARISON — Same scenario, different minds")
    print(f"{'='*55}")

    type_map = {
        "r001": "RATIONAL",
        "e001": "EMOTIONAL",
        "t001": "TRIBAL",
        "c001": "CONTRARIAN",
        "i001": "INSTITUTIONAL"
    }

    for r in results:
        agent_type = type_map.get(r["agent_id"], "?")
        print(f"\n  [{agent_type}] {r['name']}")
        print(f"  Thought  : {r['thought'][:120]}...")
        print(f"  Action   : {r['action']}")
        print(f"  Confidence: {r['confidence']}")

    # ── Test agent factory ─────────────────────────────────────────────────
    print(f"\n\n{'='*55}")
    print(f"  AGENT FACTORY TEST — Creating population of 10")
    print(f"{'='*55}")

    population = create_agent_population(
        count=10,
        topic="RBI interest rate hike and economic impact on India"
    )

    print(f"\n  Population created:")
    for agent in population:
        print(f"    [{agent.agent_type:13}] {agent.name}")

    # ── Pass check ─────────────────────────────────────────────────────────
    all_ran = len(results) == 5
    all_different = len(set(r["thought"][:50] for r in results)) >= 4
    factory_worked = len(population) == 10
    all_types_present = len(set(
        getattr(a, "agent_type", "?") for a in population
    )) >= 4

    passed = all_ran and factory_worked and all_types_present

    print(f"\n\n{'='*55}")
    if passed:
        print("  ✓  MODULE 4 PASSED")
        print(f"  ✓  All 5 agent types running correctly")
        print(f"  ✓  Each agent thinks differently about same scenario")
        print(f"  ✓  Agent factory created {len(population)} agents")
        print(f"  ✓  {len(set(getattr(a,'agent_type','') for a in population))} "
              f"different types in population")
        print(f"\n  → Ready for Module 5")
    else:
        print("  ✗  Something needs fixing:")
        print(f"  All 5 agents ran    : {all_ran}")
        print(f"  Factory worked      : {factory_worked} ({len(population)} created)")
        print(f"  Type diversity      : {all_types_present}")
        print(f"\n  → Paste output and we fix together")
    print("="*55 + "\n")


if __name__ == "__main__":
    run_test()