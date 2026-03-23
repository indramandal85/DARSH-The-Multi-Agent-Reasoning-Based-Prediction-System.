# tests/test_agent_temperatures.py
#
# Focused checks for per-agent thinking temperature behavior.
#
# Run with:
#   .venv/bin/python tests/test_agent_temperatures.py

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_agent_temperature_assignments():
    print("\n" + "=" * 55)
    print("  TEST 1 — Agent Temperature Assignments")
    print("=" * 55)

    from agents.rational_agent import RationalAgent
    from agents.emotional_agent import EmotionalAgent
    from agents.tribal_agent import TribalAgent
    from agents.contrarian_agent import ContrarianAgent
    from agents.institutional_agent import InstitutionalAgent

    agents = [
        RationalAgent("r1", "Rational", "analytical", "evidence-based"),
        EmotionalAgent("e1", "Emotional", "reactive", "headline-driven"),
        TribalAgent("t1", "Tribal", "group-first", "community lens"),
        ContrarianAgent("c1", "Contrarian", "skeptical", "looks for the hidden angle"),
        InstitutionalAgent("i1", "Institutional", "formal", "risk managed"),
    ]

    expected = {
        "RATIONAL": 0.1,
        "EMOTIONAL": 0.7,
        "TRIBAL": 0.5,
        "CONTRARIAN": 0.4,
        "INSTITUTIONAL": 0.1,
    }

    all_ok = True
    for agent in agents:
        actual = getattr(agent, "temperature", None)
        ok = actual == expected.get(agent.agent_type)
        all_ok = all_ok and ok
        print(f"  {agent.agent_type:14} : {actual} {'✓' if ok else '✗'}")

    print(f"\n  {'✓ TEST 1 PASSED' if all_ok else '✗ TEST 1 FAILED'}")
    return all_ok


def test_think_routes_agent_temperature():
    print("\n" + "=" * 55)
    print("  TEST 2 — Think Uses Agent Temperature")
    print("=" * 55)

    import core.base_agent as base_agent_module
    from agents.rational_agent import RationalAgent
    from agents.emotional_agent import EmotionalAgent
    from agents.tribal_agent import TribalAgent
    from agents.contrarian_agent import ContrarianAgent
    from agents.institutional_agent import InstitutionalAgent

    original_helper = base_agent_module.BaseAgent._ask_thought_llm
    captured = []

    def fake_helper(self, prompt, system_prompt):
        captured.append((self.agent_type, self.temperature))
        return f"{self.agent_type} mock thought"

    base_agent_module.BaseAgent._ask_thought_llm = fake_helper

    try:
        agents = [
            RationalAgent("r1", "Rational", "analytical", "evidence-based"),
            EmotionalAgent("e1", "Emotional", "reactive", "headline-driven"),
            TribalAgent("t1", "Tribal", "group-first", "community lens"),
            ContrarianAgent("c1", "Contrarian", "skeptical", "looks for the hidden angle"),
            InstitutionalAgent("i1", "Institutional", "formal", "risk managed"),
        ]

        for agent in agents:
            thought = agent.think("A market shock just happened.")
            print(f"  {agent.agent_type:14} -> {thought}")
    finally:
        base_agent_module.BaseAgent._ask_thought_llm = original_helper

    expected = {
        "RATIONAL": 0.1,
        "EMOTIONAL": 0.7,
        "TRIBAL": 0.5,
        "CONTRARIAN": 0.4,
        "INSTITUTIONAL": 0.1,
    }
    observed = {agent_type: temp for agent_type, temp in captured}
    passed = observed == expected

    print(f"\n  Captured temperatures: {observed}")
    print(f"\n  {'✓ TEST 2 PASSED' if passed else '✗ TEST 2 FAILED'}")
    return passed


def test_decide_keeps_json_deterministic():
    print("\n" + "=" * 55)
    print("  TEST 3 — Decide Keeps JSON Temperature At Default")
    print("=" * 55)

    import core.base_agent as base_agent_module
    from agents.rational_agent import RationalAgent

    original_json = base_agent_module.ask_llm_json
    captured = {}

    def fake_json(prompt, system_prompt=None, temperature=0.0):
        captured["temperature"] = temperature
        return {
            "action": "wait and observe",
            "reason": "Structured output remains deterministic.",
            "confidence": 0.62,
        }

    base_agent_module.ask_llm_json = fake_json

    try:
        agent = RationalAgent("r1", "Rational", "analytical", "evidence-based")
        result = agent.decide("I should stay calm and review the facts.", ["wait and observe"])
    finally:
        base_agent_module.ask_llm_json = original_json

    temp_ok = captured.get("temperature") == 0.0
    action_ok = result.get("action") == "wait and observe"

    print(f"  Captured JSON temperature : {captured.get('temperature')}")
    print(f"  Returned action           : {result.get('action')}")

    passed = temp_ok and action_ok
    print(f"\n  {'✓ TEST 3 PASSED' if passed else '✗ TEST 3 FAILED'}")
    return passed


def run_all_tests():
    print("\n" + "=" * 55)
    print("  DARSH — AGENT TEMPERATURE TESTS")
    print("=" * 55)

    results = {}
    for name, func in [
        ("1_assignments", test_agent_temperature_assignments),
        ("2_think_routing", test_think_routes_agent_temperature),
        ("3_json_stability", test_decide_keeps_json_deterministic),
    ]:
        try:
            results[name] = func()
        except Exception as e:
            print(f"\n  ✗ {name} ERROR: {e}")
            import traceback
            traceback.print_exc()
            results[name] = False

    print("\n\n" + "=" * 55)
    print("  AGENT TEMPERATURE SUMMARY")
    print("=" * 55)

    all_passed = True
    for name, ok in results.items():
        print(f"  {'✓' if ok else '✗'}  {name}")
        if not ok:
            all_passed = False

    print("\n" + "=" * 55)
    if all_passed:
        print("  ✓  ALL AGENT TEMPERATURE TESTS PASSED")
    else:
        print("  ✗  Some agent temperature tests failed")
    print("=" * 55)


if __name__ == "__main__":
    run_all_tests()
