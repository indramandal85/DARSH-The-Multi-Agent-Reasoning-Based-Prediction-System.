import json
import os
from copy import deepcopy


MARKET_DATA_DIR = "data/market"
TEMPLATES_DIR = os.path.join(MARKET_DATA_DIR, "event_templates")
ONTOLOGY_PATH = os.path.join(MARKET_DATA_DIR, "india_market_ontology.json")


def load_market_ontology() -> dict:
    if not os.path.exists(ONTOLOGY_PATH):
        return {}
    with open(ONTOLOGY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def list_event_templates() -> list:
    if not os.path.exists(TEMPLATES_DIR):
        return []

    templates = []
    for filename in sorted(os.listdir(TEMPLATES_DIR)):
        if not filename.endswith(".json"):
            continue
        template = load_event_template(filename[:-5])
        templates.append({
            "template_id": template["template_id"],
            "display_name": template["display_name"],
            "category": template["category"],
            "description": template.get("description", ""),
            "required_inputs": template.get("required_inputs", [])
        })
    return templates


def load_event_template(template_id: str) -> dict:
    path = os.path.join(TEMPLATES_DIR, f"{template_id}.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Template not found: {template_id}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _parse_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes", "y", "on"}
    return False


def _parse_float(value, default=0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float(default)


def derive_template_fields(template_id: str, raw_inputs: dict) -> dict:
    derived = deepcopy(raw_inputs)

    if template_id == "rbi_rate_hike":
        current_rate = _parse_float(raw_inputs.get("current_repo_rate_percent"), 6.0)
        hike_bps = _parse_float(raw_inputs.get("hike_magnitude_bps"), 25.0)
        inflation = _parse_float(raw_inputs.get("current_inflation_percent"), 6.0)
        sensex_move = _parse_float(raw_inputs.get("sensex_immediate_move"), -400.0)
        off_cycle = _parse_bool(raw_inputs.get("was_off_cycle"))
        expected = _parse_bool(raw_inputs.get("market_consensus_expected"))

        derived["new_rate"] = round(current_rate + (hike_bps / 100.0), 2)
        derived["off_cycle_text"] = "in an emergency off-cycle move, " if off_cycle else ""
        derived["surprise_text"] = (
            "The move surprised the street and repriced rate-sensitive sectors immediately. "
            if not expected else
            "The move broadly matched expectations, but traders are reassessing the policy path. "
        )
        derived["rupee_direction"] = (
            "is holding firmer on tighter-rate expectations" if off_cycle or inflation > 6.0
            else "is relatively stable as markets reassess the policy path"
        )
        derived["bond_yield_estimate"] = int(max(8, round(hike_bps * 0.75)))
        derived["inflation_band_comment"] = (
            "well above RBI's 6% upper tolerance band" if inflation > 6.0
            else "near the upper end of RBI's tolerance band"
        )
        derived["market_shock_label"] = "sharp selloff" if sensex_move <= -800 else "measured decline"

    elif template_id == "union_budget_expansion":
        fiscal_push = _parse_float(raw_inputs.get("capex_growth_percent"), 15.0)
        deficit = _parse_float(raw_inputs.get("fiscal_deficit_percent"), 5.3)
        market_move = _parse_float(raw_inputs.get("gift_nifty_move_percent"), 0.8)
        defence_boost = _parse_bool(raw_inputs.get("defence_allocation_boost"))
        subsidy_relief = _parse_bool(raw_inputs.get("consumption_relief_measures"))

        derived["budget_tone"] = "growth-oriented and expansionary"
        derived["market_reaction_text"] = (
            "Gift Nifty indicates an upbeat pre-open response" if market_move >= 0
            else "Gift Nifty suggests investors are cautious despite the spending push"
        )
        derived["defence_text"] = (
            "Defence-linked names are expected to draw immediate attention. "
            if defence_boost else ""
        )
        derived["consumption_text"] = (
            "Consumption and rural-demand counters may also react positively to relief measures. "
            if subsidy_relief else ""
        )
        derived["fiscal_balance_text"] = (
            "The market is balancing capex optimism against the higher fiscal deficit path."
            if deficit >= 5.5 else
            "The fiscal math still looks manageable relative to the growth impulse."
        )
        derived["capex_growth_bucket"] = "aggressive" if fiscal_push >= 20 else "supportive"

    elif template_id == "oil_price_spike":
        oil_price = _parse_float(raw_inputs.get("brent_price_usd"), 95.0)
        oil_jump = _parse_float(raw_inputs.get("one_day_spike_percent"), 6.0)
        rupee = _parse_float(raw_inputs.get("usd_inr_level"), 83.0)
        shipping = _parse_bool(raw_inputs.get("shipping_disruption"))
        opec = _parse_bool(raw_inputs.get("opec_supply_signal"))

        derived["shock_text"] = "a major supply-side shock" if oil_jump >= 8 else "a sharp energy-price repricing"
        derived["rupee_text"] = (
            "The rupee is under pressure from imported inflation concerns." if rupee >= 83
            else "The rupee is stable for now, but energy sensitivity remains high."
        )
        derived["shipping_text"] = (
            "Shipping and logistics risks are amplifying the crude move. " if shipping else ""
        )
        derived["opec_text"] = (
            "OPEC commentary is reinforcing fears of a tighter supply outlook. " if opec else ""
        )
        derived["inflation_risk_text"] = (
            "The market is repricing inflation-sensitive sectors and fuel-linked margins."
        )

    return derived


def _normalize_render_inputs(required_inputs: list, raw_inputs: dict) -> dict:
    normalized = {}
    for field in required_inputs:
        key = field["key"]
        value = raw_inputs.get(key)
        field_type = field.get("type", "text")

        if field_type == "boolean":
            normalized[key] = _parse_bool(value)
        elif field_type == "number":
            normalized[key] = _parse_float(value, field.get("default", 0.0))
        else:
            normalized[key] = "" if value is None else str(value)
    return normalized


def render_event_template(template_id: str, raw_inputs: dict) -> dict:
    template = load_event_template(template_id)
    normalized_inputs = _normalize_render_inputs(template.get("required_inputs", []), raw_inputs)
    merged_inputs = derive_template_fields(template_id, normalized_inputs)

    try:
        situation = template["situation_template"].format(**merged_inputs)
        round_events = [
            event.format(**merged_inputs)
            for event in template.get("round_events", [])
        ]
    except KeyError as e:
        missing = e.args[0]
        raise ValueError(f"Missing template variable during render: {missing}")

    return {
        "template_id": template["template_id"],
        "display_name": template["display_name"],
        "category": template.get("category", "general"),
        "topic": f"{template['display_name']} — Market and Sector Impact",
        "situation": situation,
        "round_events": round_events,
        "default_actions": template.get("default_actions", []),
        "event_type": template.get("event_type_key", "general"),
        "inputs": normalized_inputs,
        "derived_inputs": merged_inputs
    }
