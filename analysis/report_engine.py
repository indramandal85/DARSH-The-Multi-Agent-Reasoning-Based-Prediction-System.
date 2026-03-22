# analysis/report_engine.py
#
# 6-SECTION PREDICTION REPORT ENGINE
#
# v2 upgrades from Phase 1:
#   - _fetch_verified_facts(): pulls real numbers from SQLite before writing
#   - generate_executive_summary(): grounded in verified facts
#   - generate_agent_behavior(): grounded in verified action counts
#   - _assemble_report(): assembles pre-generated sections (used by routes.py)
#
# Every section generator calls write_report_section() which is the
# base LLM call wrapper. This must exist for any section to work.

import os
import sqlite3
from datetime import datetime

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.llm_caller import ask_llm


def load_simulation_data(simulation_ids: list) -> dict:
    """
    Load agent action data from SQLite databases for all branches.
    Returns dict with all agent actions, thoughts, beliefs, and world states.
    """
    all_data = {
        "agent_actions": [],
        "world_states" : [],
        "simulation_ids": simulation_ids
    }

    for sim_id in simulation_ids:
        db_path = f"data/simulations/{sim_id}.db"
        if not os.path.exists(db_path):
            continue

        conn   = sqlite3.connect(db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT agent_id, agent_name, agent_type, round_number,
                       action, confidence, thought, belief
                FROM agent_actions
                ORDER BY round_number, agent_id
            """)
            for row in cursor.fetchall():
                all_data["agent_actions"].append({
                    "agent_id"   : row[0],
                    "agent_name" : row[1],
                    "agent_type" : row[2],
                    "round"      : row[3],
                    "action"     : row[4],
                    "confidence" : row[5],
                    "thought"    : row[6],
                    "belief"     : row[7]
                })

            cursor.execute("""
                SELECT round_number, world_state, dominant_action, avg_confidence
                FROM world_states
                ORDER BY round_number
            """)
            for row in cursor.fetchall():
                all_data["world_states"].append({
                    "round"           : row[0],
                    "world_state"     : row[1],
                    "dominant_action" : row[2],
                    "avg_confidence"  : row[3]
                })

        except Exception as e:
            print(f"    Warning: could not load {db_path}: {e}")
        finally:
            conn.close()

    return all_data


class ReportEngine:
    """
    Generates a structured 6-section prediction report.

    Sections:
        1. Executive Summary      — bottom line in 3 sentences
        2. Predicted Outcome      — what will happen with probabilities
        3. Causal Drivers         — WHY (uses causal summary if available)
        4. Agent Behavior         — which agent types drove the outcome
        5. Dissenting Views       — what contrarians argued
        6. Confidence Assessment  — how certain, and why

    v2: sections 1 and 4 are grounded with verified SQLite facts.
    All sections use write_report_section() as the LLM call base.
    """

    def __init__(
        self,
        simulation_ids : list,
        topic          : str,
        outcome_probs  : dict,
        causal_summary : str  = "",
        brier_score    : float = None
    ):
        self.simulation_ids = simulation_ids
        self.topic          = topic
        self.outcome_probs  = outcome_probs
        self.causal_summary = causal_summary
        self.brier_score    = brier_score

        print(f"  Loading simulation data...")
        self.sim_data = load_simulation_data(simulation_ids)


    # ── CORE LLM CALL WRAPPER ──────────────────────────────────────────────

    def write_report_section(
        self,
        section_name : str,
        context      : str,
        prompt       : str
    ) -> str:
        """
        Base method for all section generators.
        Every generate_*() method calls this.

        Sends one focused LLM call with the section name, relevant data,
        and writing instructions. Returns the generated section text.
        """
        system = (
            "You are a senior policy analyst writing a professional prediction report. "
            "Write clearly, precisely, analytically. No fluff. "
            "Every sentence must add information. "
            "Never start with 'I' or 'In conclusion'. "
            "Write in third person analytical voice."
        )

        full_prompt = (
            f"You are writing the '{section_name}' section of a prediction report.\n\n"
            f"Available data:\n{context}\n\n"
            f"Instructions: {prompt}\n\n"
            f"Write this section now:"
        )

        return ask_llm(full_prompt, system_prompt=system)


    # ── VERIFIED FACTS EXTRACTOR ───────────────────────────────────────────

    def _fetch_verified_facts(self) -> dict:
        """
        Pull exact verified facts from SQLite databases before writing.

        These numbers are injected directly into section prompts.
        The LLM writes prose AROUND these numbers — it cannot invent others.

        Returns dict with:
          total_agents           : int
          total_rounds           : int
          action_counts          : {action: count} sorted by frequency
          dominant_action        : str
          agent_type_actions     : {agent_type: {action: count}}
          avg_confidence_by_round: {round_num: avg_confidence}
          overall_avg_confidence : float
          sample_thoughts        : list of (name, type, thought) verbatim
          sample_beliefs         : list of (name, belief_text) verbatim
        """
        action_counts       = {}
        agent_type_actions  = {}
        confidence_by_round = {}
        sample_thoughts     = []
        sample_beliefs      = []
        total_agents_seen   = set()
        max_round           = 0

        for action_row in self.sim_data.get("agent_actions", []):
            name   = action_row.get("agent_name", "")
            atype  = action_row.get("agent_type", "")
            rnd    = action_row.get("round", 0)
            action = action_row.get("action", "")
            conf   = action_row.get("confidence")
            thought = action_row.get("thought", "")
            belief  = action_row.get("belief", "")

            total_agents_seen.add(name)
            if rnd > max_round:
                max_round = rnd

            if action:
                action_counts[action] = action_counts.get(action, 0) + 1

            if atype:
                if atype not in agent_type_actions:
                    agent_type_actions[atype] = {}
                if action:
                    agent_type_actions[atype][action] = (
                        agent_type_actions[atype].get(action, 0) + 1
                    )

            if conf is not None and rnd is not None:
                if rnd not in confidence_by_round:
                    confidence_by_round[rnd] = []
                confidence_by_round[rnd].append(float(conf))

            if thought and rnd == max_round and len(sample_thoughts) < 5:
                sample_thoughts.append((name, atype or "UNKNOWN", thought[:200]))

            if belief and rnd == max_round and len(sample_beliefs) < 5:
                sample_beliefs.append((name, belief[:150]))

        avg_conf_by_round = {
            rnd: round(sum(confs) / len(confs), 3)
            for rnd, confs in sorted(confidence_by_round.items())
        }
        all_confs   = [c for confs in confidence_by_round.values() for c in confs]
        overall_avg = round(sum(all_confs) / len(all_confs), 3) if all_confs else 0.5

        dominant_action = (
            max(action_counts, key=action_counts.get)
            if action_counts else "none"
        )

        return {
            "total_agents"           : len(total_agents_seen),
            "total_rounds"           : max_round,
            "action_counts"          : dict(sorted(
                action_counts.items(), key=lambda x: x[1], reverse=True
            )),
            "dominant_action"        : dominant_action,
            "agent_type_actions"     : agent_type_actions,
            "avg_confidence_by_round": avg_conf_by_round,
            "overall_avg_confidence" : overall_avg,
            "sample_thoughts"        : sample_thoughts,
            "sample_beliefs"         : sample_beliefs
        }


    # ── SECTION 1: EXECUTIVE SUMMARY (grounded) ───────────────────────────

    def generate_executive_summary(self) -> str:
        """Section 1: Grounded executive summary using verified facts only."""
        print("  Writing executive summary (grounded)...")

        facts    = self._fetch_verified_facts()
        dominant = max(self.outcome_probs, key=self.outcome_probs.get)
        dom_prob = self.outcome_probs[dominant]

        top_actions = list(facts["action_counts"].items())[:3]
        action_summary = "; ".join(
            f"'{a}' ({c} times)" for a, c in top_actions
        )

        context = (
            f"Topic: {self.topic}\n"
            f"Total agents simulated: {facts['total_agents']} "
            f"across {len(self.simulation_ids)} parallel branches\n"
            f"Simulation rounds per branch: {facts['total_rounds']}\n"
            f"Dominant predicted outcome: {dominant} ({dom_prob:.0f}% of branches)\n"
            f"Top agent actions taken: {action_summary}\n"
            f"Average agent confidence: {facts['overall_avg_confidence']:.1%}"
        )

        prompt = (
            f"Write a 3-sentence executive summary using ONLY these verified facts.\n"
            f"Sentence 1: What was simulated and at what scale.\n"
            f"Sentence 2: Primary predicted outcome and probability.\n"
            f"Sentence 3: What agent behavior drove this outcome.\n"
            f"Do not add any information not listed in the data above."
        )

        return self.write_report_section("Executive Summary", context, prompt)


    # ── SECTION 2: PREDICTED OUTCOME ──────────────────────────────────────

    def generate_predicted_outcome(self) -> str:
        """Section 2: Predicted outcome with probability distribution."""
        print("  Writing predicted outcome section...")

        dominant = max(self.outcome_probs, key=self.outcome_probs.get)
        probs_text = "\n".join(
            f"  {k}: {v:.1f}%"
            for k, v in sorted(
                self.outcome_probs.items(),
                key=lambda x: x[1], reverse=True
            )
        )

        context = (
            f"Outcome probability distribution:\n{probs_text}\n\n"
            f"Dominant outcome: {dominant} "
            f"({self.outcome_probs[dominant]:.0f}% of branches)\n"
            f"Number of simulation branches: {len(self.simulation_ids)}"
        )

        prompt = (
            f"Explain what '{dominant}' means as a predicted social outcome "
            f"for this topic. Describe what this outcome looks like in practice. "
            f"Explain why the probability distribution shows this pattern. "
            f"Write 3-4 sentences."
        )

        return self.write_report_section("Predicted Outcome", context, prompt)


    # ── SECTION 3: CAUSAL DRIVERS ─────────────────────────────────────────

    def generate_causal_drivers(self) -> str:
        """Section 3: Causal chain analysis using causal DAG data."""
        print("  Writing causal drivers section...")

        world_states = self.sim_data.get("world_states", [])
        final_state  = world_states[-1]["world_state"] if world_states else "Unknown"

        context = (
            f"Topic: {self.topic}\n\n"
            f"Causal model summary: {self.causal_summary or 'Not available'}\n\n"
            f"Final world state after simulation:\n{final_state[:400]}"
        )

        prompt = (
            f"Identify the 2-3 primary causal drivers that led to the predicted outcome. "
            f"For each driver, explain: (1) what it is, (2) how it caused the outcome, "
            f"(3) its causal strength. "
            f"Use the causal model data if available. "
            f"Write 4-5 sentences."
        )

        return self.write_report_section("Causal Drivers", context, prompt)


    # ── SECTION 4: AGENT BEHAVIOR (grounded) ──────────────────────────────

    def generate_agent_behavior(self) -> str:
        """Section 4: Agent behavior analysis grounded in verified action counts."""
        print("  Writing agent behavior section (grounded)...")

        facts = self._fetch_verified_facts()

        type_summaries = []
        for atype, actions in facts["agent_type_actions"].items():
            if actions:
                top   = max(actions, key=actions.get)
                count = actions[top]
                type_summaries.append(
                    f"  {atype}: primarily '{top}' ({count} times)"
                )

        thought_samples = "\n".join(
            f"  [{atype}] {name}: \"{thought}\""
            for name, atype, thought in facts["sample_thoughts"][:4]
        ) or "  No samples available."

        context = (
            f"VERIFIED action counts by agent type:\n"
            f"{chr(10).join(type_summaries)}\n\n"
            f"VERBATIM thought samples from simulation database:\n"
            f"{thought_samples}\n\n"
            f"Overall average confidence: {facts['overall_avg_confidence']:.1%}"
        )

        prompt = (
            f"Describe how the different agent types responded, using ONLY the "
            f"verified counts and verbatim quotes above. "
            f"Do not invent statistics. "
            f"Note which agent types drove the dominant outcome and which resisted. "
            f"Write 4-5 sentences."
        )

        return self.write_report_section("Agent Behavior Analysis", context, prompt)


    # ── SECTION 5: DISSENTING VIEWS ───────────────────────────────────────

    def generate_dissenting_views(self) -> str:
        """Section 5: Contrarian and minority viewpoints from the simulation."""
        print("  Writing dissenting views section...")

        contrarian_thoughts = [
            row for row in self.sim_data.get("agent_actions", [])
            if row.get("agent_type") == "CONTRARIAN"
            and row.get("thought")
        ]

        if contrarian_thoughts:
            dissent_text = "\n".join(
                f"  Round {r['round']}: \"{r['thought'][:180]}\""
                for r in contrarian_thoughts[:3]
            )
        else:
            dissent_text = "  No contrarian agents found in simulation data."

        context = (
            f"Contrarian agent thoughts (verbatim):\n{dissent_text}\n\n"
            f"Dominant outcome: {max(self.outcome_probs, key=self.outcome_probs.get)}"
        )

        prompt = (
            f"Summarize the dissenting views and alternative analyses from the simulation. "
            f"What did contrarian agents identify that others missed? "
            f"How strong was the dissent relative to the dominant outcome? "
            f"Why does this matter for confidence in the prediction? "
            f"Write 3-4 sentences."
        )

        return self.write_report_section("Dissenting Views", context, prompt)


    # ── SECTION 6: CONFIDENCE ASSESSMENT ─────────────────────────────────

    def generate_confidence_assessment(self) -> str:
        """Section 6: Overall confidence and reliability assessment."""
        print("  Writing confidence assessment section...")

        facts    = self._fetch_verified_facts()
        dominant = max(self.outcome_probs, key=self.outcome_probs.get)
        dom_prob = self.outcome_probs[dominant]

        context = (
            f"Dominant outcome: {dominant} ({dom_prob:.0f}% of branches)\n"
            f"Number of branches: {len(self.simulation_ids)}\n"
            f"Average agent confidence: {facts['overall_avg_confidence']:.1%}\n"
            f"Brier score (if available): {self.brier_score}\n"
            f"Agent type consensus: {len(facts['agent_type_actions'])} types simulated"
        )

        prompt = (
            f"Assess the overall confidence in this prediction. "
            f"Explain: (1) what the branch consensus tells us, "
            f"(2) what the agent confidence scores mean, "
            f"(3) what would change the prediction, "
            f"(4) the key uncertainty factors. "
            f"Write 4 sentences."
        )

        return self.write_report_section("Confidence Assessment", context, prompt)


    # ── ASSEMBLER ─────────────────────────────────────────────────────────

    def _assemble_report(
        self,
        exec_summary   : str,
        predicted      : str,
        causal         : str,
        agent_behavior : str,
        dissent        : str,
        confidence     : str,
        market_impact  : dict | None = None,
        population_model: dict | None = None,
    ) -> str:
        """
        Assemble a complete report from pre-generated sections.

        Used by api/routes.py when sections are generated one at a time
        with live status updates (so the UI shows progress per section).

        Saves to disk and returns full report text.
        """
        dominant = max(self.outcome_probs, key=self.outcome_probs.get)
        dom_prob = self.outcome_probs[dominant]
        market_impact = market_impact or {}
        population_model = population_model or {}

        probs_table = "\n".join(
            f"| {k.capitalize()} | {v:.1f}% |"
            for k, v in sorted(
                self.outcome_probs.items(),
                key=lambda x: x[1], reverse=True
            )
        )

        trigger_map = market_impact.get("confidence_triggers") or {}
        strengthen = trigger_map.get("strengthens") or market_impact.get("triggers_that_strengthen") or []
        weaken = trigger_map.get("weakens") or market_impact.get("triggers_that_weaken") or []

        top_beneficiaries = market_impact.get("likely_beneficiaries") or []
        top_laggards = market_impact.get("likely_laggards") or []
        monitoring = market_impact.get("monitoring_signals") or []
        sector_impacts = market_impact.get("sector_impacts") or {}
        top_sector_lines = []
        for sector in sorted(sector_impacts.values(), key=lambda item: item.get("confidence", 0), reverse=True)[:4]:
            top_sector_lines.append(
                f"- {str(sector.get('sector', 'unknown')).replace('_', ' ').title()}: "
                f"{str(sector.get('direction', 'neutral')).replace('_', ' ')} "
                f"({round(float(sector.get('confidence', 0)) * 100):.0f}%)"
            )

        snapshot_lines = [
            f"- Dominant outcome: **{dominant.upper()}** ({dom_prob:.1f}%)",
            f"- Parallel branches: **{len(self.simulation_ids)}**",
            f"- Market regime: **{str(market_impact.get('market_regime', 'n/a')).replace('_', ' ')}**",
            f"- Volatility expectation: **{str(market_impact.get('volatility_expectation', 'n/a')).replace('_', ' ')}**",
            f"- Price discovery window: **{market_impact.get('expected_price_discovery_hours', 'n/a')}h**",
        ]
        if population_model:
            snapshot_lines.append(
                f"- Population-weighted read: **{str(population_model.get('dominant_population_outcome', 'n/a')).replace('_', ' ')}**"
            )

        beneficiary_lines = "\n".join(
            f"- {item.get('sector', 'Unknown')} ({round(float(item.get('confidence', 0)) * 100):.0f}%)"
            for item in top_beneficiaries[:3]
        ) or "- No clear beneficiaries generated."
        laggard_lines = "\n".join(
            f"- {item.get('sector', 'Unknown')} ({round(float(item.get('confidence', 0)) * 100):.0f}%)"
            for item in top_laggards[:3]
        ) or "- No clear laggards generated."
        monitoring_lines = "\n".join(f"- {item}" for item in monitoring[:4]) or "- Monitoring signals not generated."
        strengthen_lines = "\n".join(f"- {item}" for item in strengthen[:4]) or "- No explicit strengthening triggers generated."
        weaken_lines = "\n".join(f"- {item}" for item in weaken[:4]) or "- No explicit weakening triggers generated."

        population_lines = []
        if population_model:
            population_lines = [
                f"- Sampled cohorts: **{population_model.get('sampled_cohort_count', 'n/a')}**",
                f"- Sampled agents: **{population_model.get('sampled_agent_count', 'n/a')}**",
                f"- Represented population: **{population_model.get('represented_population', 'n/a')}**",
                f"- Coverage ratio: **{round(float(population_model.get('coverage_ratio', 0)) * 100):.0f}%**",
            ]
            for cohort in (population_model.get("cohort_breakdown") or [])[:4]:
                population_lines.append(
                    f"- {cohort.get('label', cohort.get('role_key', 'Cohort'))}: "
                    f"{str(cohort.get('dominant_outcome', 'n/a')).replace('_', ' ')} | "
                    f"{cohort.get('sampled_agents', 'n/a')} sampled agents"
                )
        else:
            population_lines = ["- Population model was not available for this run."]

        report = f"""# DARSH Prediction Report
**Topic:** {self.topic}
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}
**Branches:** {len(self.simulation_ids)} parallel simulations

## Prediction Snapshot
{chr(10).join(snapshot_lines)}

## Outcome Probability Distribution
| Outcome | Probability |
|---------|-------------|
{probs_table}
**Dominant predicted outcome: {dominant.upper()} ({dom_prob:.0f}%)**

## Market Intelligence
### Top Sector Read
{chr(10).join(top_sector_lines) or "- Sector impacts were not generated."}

### Likely Beneficiaries
{beneficiary_lines}

### Likely Laggards
{laggard_lines}

### Monitoring Signals
{monitoring_lines}

## Population Model
{chr(10).join(population_lines)}

## Market Triggers
### Strengthens
{strengthen_lines}

### Weakens
{weaken_lines}

## 1. Executive Summary
{exec_summary}

## 2. Predicted Outcome
{predicted}

## 3. Causal Drivers
{causal}

## 4. Agent Behavior Analysis
{agent_behavior}

## 5. Dissenting Views
{dissent}

## 6. Confidence Assessment
{confidence}

---
*Brier Score: {self.brier_score if self.brier_score is not None else 'N/A — forward prediction'}*
*Generated by DARSH — Multi-Agent Behavioral Intelligence System*
"""

        os.makedirs("data/reports", exist_ok=True)
        safe_topic = self.topic[:40].replace(" ", "_").replace("/", "_")
        save_path  = f"data/reports/report_{safe_topic}.md"

        with open(save_path, "w", encoding="utf-8") as f:
            f.write(report)

        print(f"  Report saved: {save_path}")
        print(f"  Word count  : ~{len(report.split())} words")
        return report


    # ── FULL REPORT (generates all sections in sequence) ──────────────────

    def generate_report(self, save_path: str = None) -> str:
        """
        Generate the complete 6-section report in one call.

        Used by command-line tests and batch_backtest.
        For web API, use the section-by-section approach in routes.py
        which provides live status updates to the frontend.
        """
        exec_summary   = self.generate_executive_summary()
        predicted      = self.generate_predicted_outcome()
        causal         = self.generate_causal_drivers()
        agent_behavior = self.generate_agent_behavior()
        dissent        = self.generate_dissenting_views()
        confidence     = self.generate_confidence_assessment()

        return self._assemble_report(
            exec_summary, predicted, causal,
            agent_behavior, dissent, confidence
        )
