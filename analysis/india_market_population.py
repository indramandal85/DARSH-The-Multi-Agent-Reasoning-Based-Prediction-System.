import re
from statistics import mean

from agents.belief_state import OUTCOMES
from agents.market_roles import MARKET_ROLES
from analysis.market_geography import (
    DEFAULT_GEOGRAPHY,
    get_market_config,
    resolve_market_geography,
)
from analysis.market_impact_mapper import classify_market_regime, normalize_behavioral_distribution

BLEND_WEIGHTS = {
    "participation": 0.30,
    "capital": 0.45,
    "velocity": 0.25,
}


def _parse_distribution_from_text(belief_text: str) -> dict:
    matches = re.findall(r"(\w+):\s*(\d+(?:\.\d+)?)%", belief_text or "")
    if not matches:
        return {}
    parsed = {outcome: float(value) for outcome, value in matches}
    return normalize_behavioral_distribution(parsed)


def _extract_distribution(agent_result: dict) -> dict:
    direct = agent_result.get("belief_distribution")
    if isinstance(direct, dict) and direct:
        return normalize_behavioral_distribution(direct)

    parsed = _parse_distribution_from_text(agent_result.get("belief", ""))
    if parsed:
        return parsed

    fallback = {"cautious": 1.0}
    return normalize_behavioral_distribution(fallback)


def _extract_final_round_agents(branch_results: list) -> list:
    final_agents = []
    for branch in branch_results or []:
        round_summaries = branch.get("round_summaries") or []
        if not round_summaries:
            continue
        latest_round = round_summaries[-1]
        for result in latest_round.get("round_results", []) or []:
            enriched = dict(result)
            enriched["simulation_id"] = branch.get("simulation_id")
            final_agents.append(enriched)
    return final_agents


def _average_distribution(agent_results: list) -> dict:
    if not agent_results:
        return normalize_behavioral_distribution({})

    outcome_means = {}
    for outcome in OUTCOMES:
        outcome_means[outcome] = mean(
            _extract_distribution(result).get(outcome, 0.0)
            for result in agent_results
        )
    return normalize_behavioral_distribution(outcome_means)


def _confidence_margin(distribution: dict) -> float:
    sorted_values = sorted(distribution.values(), reverse=True)
    if len(sorted_values) < 2:
        return round(sorted_values[0] if sorted_values else 0.0, 3)
    return round(sorted_values[0] - sorted_values[1], 3)


def _top_cohorts(entries: list, weight_key: str, limit: int = 4) -> list:
    total_weight = sum(entry.get(weight_key, 0.0) for entry in entries) or 1.0
    top_entries = sorted(entries, key=lambda item: item.get(weight_key, 0.0), reverse=True)[:limit]
    formatted = []
    for entry in top_entries:
        formatted.append({
            "role_key": entry["role_key"],
            "label": entry["label"],
            "represented_population": entry["represented_population"],
            "dominant_outcome": entry["dominant_outcome"],
            "share": round(entry.get(weight_key, 0.0) / total_weight, 3),
        })
    return formatted


def _combine_lens(entries: list, weight_key: str) -> dict:
    if not entries:
        distribution = normalize_behavioral_distribution({})
    else:
        totals = {outcome: 0.0 for outcome in OUTCOMES}
        total_weight = sum(entry.get(weight_key, 0.0) for entry in entries) or 1.0
        for entry in entries:
            distribution = entry["belief_distribution"]
            weight = entry.get(weight_key, 0.0)
            for outcome in OUTCOMES:
                totals[outcome] += distribution.get(outcome, 0.0) * weight
        distribution = normalize_behavioral_distribution({
            outcome: totals[outcome] / total_weight
            for outcome in OUTCOMES
        })

    regime, regime_confidence = classify_market_regime(distribution)
    dominant_outcome = max(distribution, key=distribution.get)
    return {
        "distribution": distribution,
        "dominant_outcome": dominant_outcome,
        "market_regime": regime,
        "regime_confidence": regime_confidence,
    }


def _blend_lenses(lenses: dict) -> dict:
    blended = {outcome: 0.0 for outcome in OUTCOMES}
    for lens_name, lens_weight in BLEND_WEIGHTS.items():
        distribution = lenses.get(lens_name, {}).get("distribution", {})
        for outcome in OUTCOMES:
            blended[outcome] += distribution.get(outcome, 0.0) * lens_weight
    return normalize_behavioral_distribution(blended)


def _build_summary_takeaways(
    topic: str,
    blended_regime: str,
    top_capital_cohorts: list,
    top_velocity_cohorts: list,
    blended_distribution: dict,
) -> list:
    takeaways = []
    if top_capital_cohorts:
        capital_labels = ", ".join(item["label"] for item in top_capital_cohorts[:2])
        takeaways.append(
            f"Capital-sensitive positioning is being driven most by {capital_labels} in this {blended_regime.replace('_', ' ')} setup."
        )
    if top_velocity_cohorts:
        velocity_labels = ", ".join(item["label"] for item in top_velocity_cohorts[:2])
        takeaways.append(
            f"Headline and narrative velocity should be watched through {velocity_labels}, because they can accelerate how {topic.lower()} is priced."
        )
    dominant = max(blended_distribution, key=blended_distribution.get)
    takeaways.append(
        f"The blended cohort model leans {dominant} rather than relying only on equal-weight sample agents, which gives a more market-shaped view of the event."
    )
    return takeaways[:3]


def compute_population_weighted_sentiment(
    branch_results: list,
    topic: str,
    event_type: str = "general",
    geography: str = None,
    graph_path: str = None,
) -> dict:
    resolved_geography = resolve_market_geography(
        geography=geography,
        graph_path=graph_path,
        topic=topic,
        event_type=event_type,
    )
    market_config = get_market_config(resolved_geography)
    role_weights = market_config.get("role_weights", {})

    print(
        "  [market_population] Using "
        f"'{resolved_geography}' market structure "
        f"({market_config.get('description', 'unknown scope')})"
    )

    final_agents = _extract_final_round_agents(branch_results)
    total_known_population = sum(
        meta["population_count"] for meta in role_weights.values()
    ) or 1

    grouped = {}
    for result in final_agents:
        role_key = result.get("market_role", "RETAIL_TRADER")
        grouped.setdefault(role_key, []).append(result)

    cohort_entries = []
    for role_key, rows in grouped.items():
        role_meta = role_weights.get(role_key)
        if not role_meta and resolved_geography != DEFAULT_GEOGRAPHY:
            role_meta = get_market_config(DEFAULT_GEOGRAPHY).get("role_weights", {}).get(role_key)
        if not role_meta:
            continue

        belief_distribution = _average_distribution(rows)
        represented_population = int(role_meta["population_count"])
        participation_weight = float(represented_population)
        capital_weight = represented_population * float(role_meta["capital_influence"])
        velocity_weight = represented_population * float(role_meta["velocity_influence"])
        avg_confidence = mean(float(row.get("confidence", 0.5) or 0.5) for row in rows)
        dominant_outcome = max(belief_distribution, key=belief_distribution.get)

        cohort_entries.append({
            "role_key": role_key,
            "label": MARKET_ROLES.get(role_key, {}).get("label", role_key.replace("_", " ").title()),
            "sampled_agents": len(rows),
            "represented_population": represented_population,
            "population_unit": role_meta["unit_label"],
            "dominant_outcome": dominant_outcome,
            "belief_distribution": belief_distribution,
            "outcome_confidence": _confidence_margin(belief_distribution),
            "avg_decision_confidence": round(avg_confidence, 3),
            "participation_weight": participation_weight,
            "capital_weight": capital_weight,
            "velocity_weight": velocity_weight,
            "capital_influence": role_meta["capital_influence"],
            "velocity_influence": role_meta["velocity_influence"],
        })

    participation_lens = _combine_lens(cohort_entries, "participation_weight")
    capital_lens = _combine_lens(cohort_entries, "capital_weight")
    velocity_lens = _combine_lens(cohort_entries, "velocity_weight")

    lens_views = {
        "participation": participation_lens,
        "capital": capital_lens,
        "velocity": velocity_lens,
    }
    blended_distribution = _blend_lenses(lens_views)
    blended_regime, blended_regime_confidence = classify_market_regime(blended_distribution, event_type)
    dominant_population_outcome = max(blended_distribution, key=blended_distribution.get)

    represented_population = sum(entry["represented_population"] for entry in cohort_entries)
    coverage_ratio = round(represented_population / total_known_population, 3)

    for entry in cohort_entries:
        entry["participation_share"] = round(
            entry["represented_population"] / represented_population, 3
        ) if represented_population else 0.0

    top_capital_cohorts = _top_cohorts(cohort_entries, "capital_weight")
    top_velocity_cohorts = _top_cohorts(cohort_entries, "velocity_weight")

    return {
        "event_type": event_type,
        "market_geography": resolved_geography,
        "market_scope_description": market_config.get("description", ""),
        "population_data_year": market_config.get("population_data_year", 2024),
        "population_method": "population_weighted_market_cohort_model",
        "sampled_agent_count": len(final_agents),
        "sampled_cohort_count": len(cohort_entries),
        "represented_population": represented_population,
        "coverage_ratio": coverage_ratio,
        "dominant_population_outcome": dominant_population_outcome,
        "blended_distribution": blended_distribution,
        "blended_market_regime": blended_regime,
        "blended_regime_confidence": blended_regime_confidence,
        "lens_views": lens_views,
        "top_capital_cohorts": top_capital_cohorts,
        "top_velocity_cohorts": top_velocity_cohorts,
        "cohort_breakdown": sorted(
            cohort_entries,
            key=lambda item: item.get("capital_weight", 0.0),
            reverse=True
        ),
        "summary_takeaways": _build_summary_takeaways(
            topic=topic,
            blended_regime=blended_regime,
            top_capital_cohorts=top_capital_cohorts,
            top_velocity_cohorts=top_velocity_cohorts,
            blended_distribution=blended_distribution,
        ),
        "data_note": (
            f"Geography-aware weighting resolved this run to '{resolved_geography}'. "
            "Cohorts use DARSH's shared market-role taxonomy, then apply geography-specific "
            "participation, capital, and velocity anchors so non-India scenarios are not silently "
            "weighted with India-only assumptions."
        ),
    }
