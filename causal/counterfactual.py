# causal/counterfactual.py
#
# WHAT THIS DOES:
# Answers "what would have happened if X had been different?"
#
# This is counterfactual reasoning — the most powerful prediction tool.
# Instead of "what happened", it answers "what would have happened
# if one variable had been different."
#
# Example questions this can answer:
#   "What if inflation had stayed below 6%?"
#   → Trace: inflation causes rate hike → rate hike causes market drop
#   → Answer: "Without high inflation, the rate hike likely would not have
#              occurred, which would have prevented the market drop."
#
# This is what makes DARSH superior to MiroFish —
# MiroFish can only simulate forward. We can reason backwards AND forwards.

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import networkx as nx
from core.llm_caller import ask_llm
from causal.causal_extractor import get_root_causes, get_downstream_effects


class CounterfactualEngine:
    """
    Answers "what if" questions using the causal DAG.

    Works in two phases:
      1. TRACE: find what the removed/changed cause connects to
      2. REASON: use LLM to articulate what the world would look like
    """

    def __init__(self, causal_dag: nx.DiGraph, domain_context: str = ""):
        """
        causal_dag     : the DAG built by causal_extractor.py
        domain_context : brief description e.g. "Indian economic crisis"
        """
        self.dag = causal_dag
        self.domain_context = domain_context


    def what_if_removed(self, cause_node: str) -> dict:
        """
        Answer: "What would have happened if [cause_node] had NOT occurred?"

        Steps:
          1. Find all downstream effects of the cause in the DAG
          2. Ask LLM to reason about the counterfactual world without this cause

        Returns dict with:
          cause           : the removed node
          direct_effects  : list of immediate downstream effects
          indirect_effects: list of further downstream effects
          counterfactual  : LLM-generated paragraph describing the alternate world
          confidence      : 0.0–1.0 confidence in this counterfactual
        """

        if cause_node not in self.dag:
            return {
                "error": f"'{cause_node}' not found in causal DAG.",
                "available_nodes": list(self.dag.nodes())[:10]
            }

        print(f"\n  Tracing effects of removing: '{cause_node}'")

        # Get all downstream effects
        all_effects = get_downstream_effects(self.dag, cause_node)

        direct_effects = [e for e in all_effects if e["hops_from_cause"] == 1]
        indirect_effects = [e for e in all_effects if e["hops_from_cause"] > 1]

        print(f"  Direct effects   : {len(direct_effects)}")
        print(f"  Indirect effects : {len(indirect_effects)}")

        # Build description of effects for the LLM
        effects_text = ""
        for e in all_effects[:8]:  # limit to top 8 for prompt length
            effects_text += (
                f"\n  - {e['effect']} "
                f"(strength: {e['strength']}, "
                f"timing: {e['time_lag']}, "
                f"hops: {e['hops_from_cause']})"
            )

        if not effects_text:
            effects_text = "  No significant downstream effects found."

        # Ask LLM to reason about the counterfactual
        print(f"\n  Generating counterfactual reasoning...")

        prompt = f"""
You are analyzing a causal model about: {self.domain_context}

The causal analysis shows that "{cause_node}" causes these downstream effects:
{effects_text}

Answer this counterfactual question:
"What would have happened if '{cause_node}' had NOT occurred?"

Instructions:
- Reason through the causal chain step by step
- Explain which effects would NOT have happened
- Explain which effects might still have happened through other causes
- Be specific about the domain: {self.domain_context}
- Write 3-4 clear sentences
- End with a confidence assessment: HIGH, MEDIUM, or LOW
  (HIGH = clear causal chain, LOW = many other possible causes)
"""

        reasoning = ask_llm(prompt)

        # Extract confidence from response
        confidence = 0.5
        if "HIGH" in reasoning.upper():
            confidence = 0.8
        elif "LOW" in reasoning.upper():
            confidence = 0.3

        return {
            "cause_removed"   : cause_node,
            "direct_effects"  : direct_effects,
            "indirect_effects": indirect_effects,
            "all_effects_count": len(all_effects),
            "counterfactual"  : reasoning,
            "confidence"      : confidence
        }


    def what_if_changed(self, cause_node: str, change_description: str) -> dict:
        """
        Answer: "What would have happened if [cause_node] had been [different]?"

        More nuanced than what_if_removed — handles partial changes
        like "what if inflation had been 4% instead of 7.2%?"

        change_description: plain English description of the change
          e.g. "inflation had stayed below 6% instead of reaching 7.2%"
        """

        if cause_node not in self.dag:
            return {"error": f"'{cause_node}' not found in causal DAG."}

        all_effects = get_downstream_effects(self.dag, cause_node)

        effects_text = "\n".join(
            f"  - {e['effect']} (strength: {e['strength']}, timing: {e['time_lag']})"
            for e in all_effects[:8]
        )

        prompt = f"""
You are analyzing a causal model about: {self.domain_context}

Current causal chain starting from "{cause_node}":
{effects_text}

Counterfactual scenario: "What if {change_description}?"

Analyze:
1. Which downstream effects would be PREVENTED or REDUCED?
2. Which effects might still occur through other causal pathways?
3. What new outcomes might emerge in this alternate scenario?
4. What is the overall probability that the final outcomes change significantly?

Write a clear 4-5 sentence analysis. Be specific to: {self.domain_context}
End with: "Overall confidence in this counterfactual: HIGH / MEDIUM / LOW"
"""

        reasoning = ask_llm(prompt)

        confidence = 0.5
        if "HIGH" in reasoning.upper():
            confidence = 0.8
        elif "LOW" in reasoning.upper():
            confidence = 0.3

        return {
            "cause_node"        : cause_node,
            "change_description": change_description,
            "effects_analyzed"  : all_effects,
            "counterfactual"    : reasoning,
            "confidence"        : confidence
        }


    def find_intervention_points(self, target_outcome: str) -> dict:
        """
        Given an outcome you want to PREVENT, find where to intervene.

        This is the most practically useful function —
        "we don't want a recession, what should we have done differently?"

        Returns the root causes of the target outcome, ranked by
        how much intervening there would change things.
        """

        if target_outcome not in self.dag:
            return {"error": f"'{target_outcome}' not found in causal DAG."}

        root_causes = get_root_causes(self.dag, target_outcome)

        if not root_causes:
            return {
                "target_outcome": target_outcome,
                "message": "No root causes found — this may itself be a root cause.",
                "intervention_points": []
            }

        # Ask LLM which intervention would be most effective
        causes_text = "\n".join(
            f"  - {r['root_cause']} "
            f"(causal strength: {r['accumulated_strength']}, "
            f"path: {' → '.join(r['path'][::-1])})"
            for r in root_causes[:5]
        )

        prompt = f"""
You are advising policymakers about: {self.domain_context}

The outcome to prevent: "{target_outcome}"

Root causes found (ranked by causal strength):
{causes_text}

Question: Which intervention point would be MOST effective at preventing 
"{target_outcome}", and why?

Instructions:
- Recommend the single best intervention point
- Explain the causal chain from that intervention to the outcome
- Explain WHY this intervention is more effective than the others
- Note any practical constraints on this intervention
- Be specific to: {self.domain_context}
- Write 3-4 clear sentences
"""

        recommendation = ask_llm(prompt)

        return {
            "target_outcome"      : target_outcome,
            "root_causes_found"   : len(root_causes),
            "root_causes"         : root_causes,
            "best_intervention"   : recommendation
        }