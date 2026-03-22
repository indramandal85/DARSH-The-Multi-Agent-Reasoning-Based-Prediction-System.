# simulation/simulation_chat.py
#
# Phase 6 partial interactive analysis helpers.

import json
import os
import re
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import networkx as nx
from core.llm_caller import ask_llm
from causal.counterfactual import CounterfactualEngine


def _format_label(value: str) -> str:
    acronyms = {
        "nbfc": "NBFC",
        "rbi": "RBI",
        "fii": "FII",
        "psu": "PSU",
        "fmcg": "FMCG",
        "it": "IT",
        "fx": "FX",
    }
    parts = (value or "").replace("_", " ").split()
    formatted = []
    for part in parts:
        formatted.append(acronyms.get(part.lower(), part.title()))
    return " ".join(formatted)


def _tighten_answer(text: str, max_sentences: int = 2, max_words: int = 60) -> str:
    cleaned = " ".join((text or "").strip().split())
    if not cleaned:
        return ""
    sentences = re.split(r"(?<=[.!?])\s+", cleaned)
    clipped = " ".join(sentences[:max_sentences]).strip()
    words = clipped.split()
    if len(words) > max_words:
        clipped = " ".join(words[:max_words]).rstrip(",;:") + "..."
    return clipped


def _fallback_sector_answer(sector_key: str, sector_data: dict, market_impact: dict, topic: str) -> dict:
    direction = _format_label(sector_data.get("direction", "neutral"))
    confidence = round(float(sector_data.get("confidence", 0.0)) * 100)
    monitoring = market_impact.get("monitoring_signals", [])[:2]
    strengthening = market_impact.get("triggers_that_strengthen", [])[:2]

    supporting_points = [
        sector_data.get("reasoning", ""),
        f"Current direction bias: {direction} with {confidence}% confidence.",
        f"Watchlist names: {', '.join(sector_data.get('representative_stocks', [])[:3]) or 'No watchlist names mapped yet.'}",
    ]
    supporting_points = [point for point in supporting_points if point]

    answer = (
        f"{_format_label(sector_key)} is currently mapped as {direction.lower()} "
        f"because the simulation sees {topic.lower()} transmitting into this sector through "
        f"the current {market_impact.get('market_regime', 'market').replace('_', ' ')} regime. "
        f"The clearest confirmation signals are {', '.join(monitoring) if monitoring else 'the next pre-market cues'}, "
        f"while the strongest reinforcers are {', '.join(strengthening) if strengthening else 'follow-through from institutional commentary'}."
    )

    return {
        "mode": "ask_sector",
        "title": f"{_format_label(sector_key)} Sector View",
        "answer": _tighten_answer(answer),
        "supporting_points": supporting_points,
        "sector": sector_key,
        "direction": sector_data.get("direction", "neutral"),
        "confidence": sector_data.get("confidence", 0.0),
    }


def _fallback_change_answer(market_impact: dict, topic: str) -> dict:
    strengthens = market_impact.get("triggers_that_strengthen", [])[:3]
    weakens = market_impact.get("triggers_that_weaken", [])[:3]
    monitoring = market_impact.get("monitoring_signals", [])[:3]

    answer = (
        f"This forecast changes most if the next market signals stop supporting the current "
        f"{market_impact.get('market_regime', 'base').replace('_', ' ')} regime. "
        f"What strengthens it: {', '.join(strengthens) if strengthens else 'aligned pre-open cues and broker follow-through'}. "
        f"What weakens it: {', '.join(weakens) if weakens else 'policy clarification or contradictory market signals'}."
    )

    return {
        "mode": "what_would_change",
        "title": "What Would Change This Forecast",
        "answer": _tighten_answer(answer),
        "supporting_points": monitoring,
        "strengthens": strengthens,
        "weakens": weakens,
    }


def _fallback_cohort_answer(cohort_key: str, cohort_rows: list, market_impact: dict, topic: str) -> dict:
    sample_actions = [row["action"] for row in cohort_rows if row.get("action")][:3]
    sample_thoughts = [row["thought"] for row in cohort_rows if row.get("thought")][:2]
    answer = (
        f"{_format_label(cohort_key)} is reacting to {topic.lower()} through the current "
        f"{market_impact.get('market_regime', 'market').replace('_', ' ')} lens. "
        f"The cohort is mostly clustering around actions like {', '.join(sample_actions) if sample_actions else 'observe and reassess'}, "
        f"which suggests they are focused on confirmation signals before committing harder."
    )

    supporting_points = []
    for row in cohort_rows[:3]:
        supporting_points.append(
            f"{row.get('agent_name', 'Agent')} ({row.get('agent_type', 'UNKNOWN')}): "
            f"{(row.get('thought') or '').strip()[:140]}"
        )
    if not supporting_points and sample_thoughts:
        supporting_points = sample_thoughts

    return {
        "mode": "ask_cohort",
        "title": f"{_format_label(cohort_key)} Cohort View",
        "answer": _tighten_answer(answer),
        "supporting_points": supporting_points,
        "cohort": cohort_key,
        "sample_size": len(cohort_rows),
    }


def _fallback_counterfactual_answer(question: str, market_impact: dict, topic: str) -> dict:
    weakens = market_impact.get("triggers_that_weaken", [])[:2]
    second_order = market_impact.get("second_order_effects", [])[:2]
    answer = (
        f"In the counterfactual where {question.lower().rstrip('?')}, the current "
        f"{market_impact.get('market_regime', 'market').replace('_', ' ')} regime would likely soften first. "
        f"The most sensitive pieces of the forecast are {', '.join(weakens) if weakens else 'the key invalidation signals already highlighted'}, "
        f"and the second-order effects most likely to change are {', '.join(second_order) if second_order else 'the current follow-through effects'}."
    )
    return {
        "mode": "counterfactual",
        "title": "Counterfactual Scenario",
        "answer": _tighten_answer(answer),
        "supporting_points": second_order,
        "used_causal_dag": False,
    }


def _load_latest_cohort_rows(simulation_ids: list, cohort_key: str) -> list:
    rows = []
    for sim_id in simulation_ids or []:
        db_path = os.path.join("data", "simulations", f"{sim_id}.db")
        if not os.path.exists(db_path):
            continue

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(agent_actions)")
        columns = {row[1] for row in cursor.fetchall()}
        if "market_role" not in columns:
            conn.close()
            continue

        cursor.execute("""
            SELECT agent_name, agent_type, market_role, action, confidence, thought, belief
            FROM agent_actions
            WHERE market_role = ?
              AND round_number = (SELECT MAX(round_number) FROM agent_actions)
            ORDER BY agent_type, agent_name
        """, (cohort_key,))

        for row in cursor.fetchall():
            rows.append({
                "agent_name": row[0],
                "agent_type": row[1],
                "market_role": row[2],
                "action": row[3],
                "confidence": row[4],
                "thought": row[5],
                "belief": row[6],
            })
        conn.close()

    return rows


def _load_causal_dag_from_json(causal_path: str):
    if not causal_path or not os.path.exists(causal_path):
        return None

    with open(causal_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    dag = nx.DiGraph()
    for node in data.get("nodes", []):
        dag.add_node(
            node.get("id", ""),
            type=node.get("type", "UNKNOWN"),
            description=node.get("description", "")
        )

    for edge in data.get("causal_edges", []):
        cause = edge.get("cause")
        effect = edge.get("effect")
        if not cause or not effect:
            continue
        dag.add_edge(
            cause,
            effect,
            strength=edge.get("strength", 0.0),
            time_lag=edge.get("time_lag", "unknown"),
            explanation=edge.get("explanation", ""),
            causal_type=edge.get("causal_type", "")
        )
    return dag


def answer_sector_question(question: str, sector_key: str, market_impact: dict, topic: str) -> dict:
    sector_impacts = market_impact.get("sector_impacts", {})
    if sector_key not in sector_impacts:
        return {
            "error": f"Sector not found: {sector_key}",
            "available_sectors": sorted(sector_impacts.keys())[:10]
        }

    sector_data = sector_impacts[sector_key]
    fallback = _fallback_sector_answer(sector_key, sector_data, market_impact, topic)

    prompt = (
        f"Event topic: {topic}\n"
        f"Question: {question or f'Why is {_format_label(sector_key)} moving this way?'}\n"
        f"Market regime: {market_impact.get('market_regime')}\n"
        f"Sector direction: {sector_data.get('direction')}\n"
        f"Sector confidence: {sector_data.get('confidence')}\n"
        f"Sector reasoning: {sector_data.get('reasoning')}\n"
        f"Representative stocks: {sector_data.get('representative_stocks', [])[:4]}\n"
        f"Monitoring signals: {market_impact.get('monitoring_signals', [])[:3]}\n\n"
        f"Answer in 2 short executive sentences, under 60 words total. "
        f"Sentence 1: state the sector bias and strongest driver. "
        f"Sentence 2: state the main confirmation or invalidation signal before the open. "
        f"No preamble, no bullets."
    )

    try:
        response = ask_llm(prompt)
        if not response.strip():
            return fallback
        fallback["answer"] = _tighten_answer(response.strip())
        return fallback
    except Exception:
        return fallback


def answer_what_would_change(question: str, market_impact: dict, topic: str) -> dict:
    fallback = _fallback_change_answer(market_impact, topic)

    prompt = (
        f"Event topic: {topic}\n"
        f"Question: {question or 'What would change this forecast before the market open?'}\n"
        f"Market regime: {market_impact.get('market_regime')}\n"
        f"Volatility expectation: {market_impact.get('volatility_expectation')}\n"
        f"Strengthens: {market_impact.get('triggers_that_strengthen', [])[:3]}\n"
        f"Weakens: {market_impact.get('triggers_that_weaken', [])[:3]}\n"
        f"Monitoring signals: {market_impact.get('monitoring_signals', [])[:3]}\n"
        f"Second-order effects: {market_impact.get('second_order_effects', [])[:3]}\n\n"
        f"Answer in 2 short executive sentences, under 65 words total. "
        f"Sentence 1: what strengthens the current forecast. "
        f"Sentence 2: what weakens it and which signal matters most next. "
        f"No preamble, no bullets."
    )

    try:
        response = ask_llm(prompt)
        if not response.strip():
            return fallback
        fallback["answer"] = _tighten_answer(response.strip())
        return fallback
    except Exception:
        return fallback


def answer_cohort_question(question: str, cohort_key: str, simulation_ids: list, market_impact: dict, topic: str) -> dict:
    cohort_rows = _load_latest_cohort_rows(simulation_ids, cohort_key)
    if not cohort_rows:
        return {
            "error": f"No cohort data found for {cohort_key}",
            "available_simulations": simulation_ids or []
        }

    fallback = _fallback_cohort_answer(cohort_key, cohort_rows, market_impact, topic)
    sample_text = "\n".join(
        f"- {row['agent_name']} ({row['agent_type']}): action={row['action']}; thought={row['thought'][:140]}"
        for row in cohort_rows[:4]
    )
    prompt = (
        f"Event topic: {topic}\n"
        f"Cohort: {cohort_key}\n"
        f"Question: {question or f'How is {_format_label(cohort_key)} reacting?'}\n"
        f"Market regime: {market_impact.get('market_regime')}\n"
        f"Sample cohort evidence:\n{sample_text}\n\n"
        f"Answer in 2 short executive sentences, under 65 words total. "
        f"Sentence 1: summarize the cohort's current stance. "
        f"Sentence 2: say what they are focused on and what could change their stance. "
        f"No preamble, no bullets."
    )

    try:
        response = ask_llm(prompt)
        if response.strip():
            fallback["answer"] = _tighten_answer(response.strip())
        return fallback
    except Exception:
        return fallback


def answer_counterfactual_question(
    question: str,
    market_impact: dict,
    topic: str,
    causal_dag_path: str = "",
    counterfactual_target: str = ""
) -> dict:
    fallback = _fallback_counterfactual_answer(question or counterfactual_target or "the key driver changed", market_impact, topic)
    if causal_dag_path:
        try:
            dag = _load_causal_dag_from_json(causal_dag_path)
            if dag and counterfactual_target and counterfactual_target in dag:
                engine = CounterfactualEngine(dag, domain_context=topic)
                cf = engine.what_if_removed(counterfactual_target)
                if not cf.get("error"):
                    return {
                        "mode": "counterfactual",
                        "title": f"Counterfactual — {_format_label(counterfactual_target)} Removed",
                        "answer": _tighten_answer(cf.get("counterfactual", "")),
                        "supporting_points": [
                            f"Direct effects: {len(cf.get('direct_effects', []))}",
                            f"Indirect effects: {len(cf.get('indirect_effects', []))}",
                            f"Confidence: {round(float(cf.get('confidence', 0.0)) * 100)}%",
                        ],
                        "used_causal_dag": True,
                        "counterfactual_target": counterfactual_target,
                    }
        except Exception:
            pass

    prompt = (
        f"Event topic: {topic}\n"
        f"Counterfactual question: {question or counterfactual_target}\n"
        f"Market regime: {market_impact.get('market_regime')}\n"
        f"Weakening triggers: {market_impact.get('triggers_that_weaken', [])[:3]}\n"
        f"Second-order effects: {market_impact.get('second_order_effects', [])[:3]}\n\n"
        f"Answer in 2 short executive sentences, under 65 words total. "
        f"Sentence 1: what changes first in this alternate scenario. "
        f"Sentence 2: which sector or market effects become smaller or larger. "
        f"No preamble, no bullets."
    )

    try:
        response = ask_llm(prompt)
        if response.strip():
            fallback["answer"] = _tighten_answer(response.strip())
        return fallback
    except Exception:
        return fallback


def run_simulation_chat(
    mode: str,
    question: str,
    market_impact: dict,
    topic: str,
    sector_key: str = "",
    cohort_key: str = "",
    simulation_ids: list = None,
    causal_dag_path: str = "",
    counterfactual_target: str = ""
) -> dict:
    if not market_impact:
        return {"error": "market_impact is required for interactive analysis"}

    if mode == "ask_sector":
        return answer_sector_question(question, sector_key, market_impact, topic)

    if mode == "what_would_change":
        return answer_what_would_change(question, market_impact, topic)

    if mode == "ask_cohort":
        return answer_cohort_question(question, cohort_key, simulation_ids or [], market_impact, topic)

    if mode == "counterfactual":
        return answer_counterfactual_question(
            question=question,
            market_impact=market_impact,
            topic=topic,
            causal_dag_path=causal_dag_path,
            counterfactual_target=counterfactual_target
        )

    return {"error": f"Unsupported mode: {mode}"}
