import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis.market_geography import DEFAULT_GEOGRAPHY, resolve_market_geography
from core.llm_caller import ask_llm_json
from analysis.market_output_schema import INDIA_SECTORS


SECTOR_MATRIX_PATH = "data/market/sector_sensitivity_matrix.json"

SECTOR_REPRESENTATIVE_STOCKS = {
    "banking_private": ["HDFC Bank", "ICICI Bank", "Axis Bank", "Kotak Mahindra"],
    "banking_psu": ["SBI", "Bank of Baroda", "PNB", "Canara Bank"],
    "nbfc": ["Bajaj Finance", "Muthoot Finance", "Cholamandalam"],
    "insurance": ["HDFC Life", "SBI Life", "ICICI Prudential Life"],
    "real_estate": ["DLF", "Godrej Properties", "Prestige Estates"],
    "it_services": ["TCS", "Infosys", "HCL Tech", "Wipro"],
    "fmcg": ["HUL", "ITC", "Nestle India", "Britannia"],
    "pharma": ["Sun Pharma", "Dr Reddy's", "Cipla", "Divis Labs"],
    "auto": ["Maruti Suzuki", "Tata Motors", "M&M", "Bajaj Auto"],
    "energy_oil_gas": ["ONGC", "Reliance Industries", "BPCL", "IOC"],
    "metals_mining": ["Tata Steel", "JSW Steel", "Hindalco", "SAIL"],
    "infrastructure": ["L&T", "Adani Ports", "IRB Infra"],
    "telecom": ["Bharti Airtel", "Vodafone Idea", "Tata Communications"],
    "defence": ["HAL", "BEL", "Bharat Dynamics", "Mazagon Dock"],
    "fintech": ["Paytm", "PB Fintech", "MobiKwik", "Policybazaar"],
    "chemicals": ["Asian Paints", "Pidilite", "SRF", "Navin Fluorine"],
    "consumption": ["DMart", "Titan", "Trent", "V-Mart"],
    "capital_goods": ["L&T", "Siemens India", "ABB India", "Cummins India"],
    "aviation": ["InterGlobe Aviation", "SpiceJet", "Air India"],
}

US_SECTOR_REPRESENTATIVE_STOCKS = {
    "banks": ["JPMorgan", "Bank of America", "Wells Fargo", "Citigroup"],
    "regional_banks": ["PNC Financial", "Regions Financial", "Truist", "KeyCorp"],
    "fintech": ["PayPal", "Block", "Fiserv", "SoFi"],
    "insurance": ["Berkshire Hathaway", "AIG", "MetLife", "Travelers"],
    "real_estate": ["Prologis", "Equinix", "Simon Property", "AvalonBay"],
    "software": ["Microsoft", "Oracle", "Salesforce", "Adobe"],
    "consumer_staples": ["Walmart", "Costco", "Coca-Cola", "Procter & Gamble"],
    "pharma_biotech": ["Eli Lilly", "Johnson & Johnson", "Pfizer", "Amgen"],
    "autos": ["Tesla", "Ford", "General Motors", "Rivian"],
    "energy": ["Exxon Mobil", "Chevron", "ConocoPhillips", "Schlumberger"],
    "materials": ["Freeport-McMoRan", "Nucor", "Dow", "DuPont"],
    "industrials": ["Caterpillar", "Honeywell", "GE Aerospace", "Deere"],
    "telecom": ["AT&T", "Verizon", "T-Mobile US", "Comcast"],
    "aerospace_defense": ["Lockheed Martin", "RTX", "Northrop Grumman", "Boeing"],
    "airlines": ["Delta", "United Airlines", "American Airlines", "Southwest"],
}

EUROPE_SECTOR_REPRESENTATIVE_STOCKS = {
    "banks": ["HSBC", "BNP Paribas", "Santander", "Deutsche Bank"],
    "insurers": ["Allianz", "AXA", "Zurich Insurance", "Prudential"],
    "real_estate": ["Vonovia", "LEG Immobilien", "Unibail-Rodamco-Westfield", "Klepierre"],
    "industrials": ["Siemens", "Schneider Electric", "ABB", "Safran"],
    "construction": ["Vinci", "Bouygues", "Hochtief", "Skanska"],
    "consumer_staples": ["Nestle", "Unilever", "Danone", "Carrefour"],
    "luxury_consumption": ["LVMH", "Hermes", "Kering", "Richemont"],
    "pharma": ["Novo Nordisk", "Roche", "Sanofi", "AstraZeneca"],
    "autos": ["Volkswagen", "BMW", "Mercedes-Benz", "Stellantis"],
    "energy": ["Shell", "TotalEnergies", "BP", "Eni"],
    "telecom": ["Deutsche Telekom", "Orange", "Vodafone", "Telefonica"],
    "defence": ["BAE Systems", "Rheinmetall", "Thales", "Leonardo"],
    "airlines": ["Lufthansa", "Ryanair", "IAG", "Air France-KLM"],
}

CHINA_SECTOR_REPRESENTATIVE_STOCKS = {
    "banks": ["ICBC", "China Construction Bank", "Bank of China", "Agricultural Bank of China"],
    "state_enterprises": ["China State Construction", "PetroChina", "Sinopec", "China Railway"],
    "real_estate": ["China Resources Land", "Longfor", "Poly Developments", "Vanke"],
    "internet_platforms": ["Tencent", "Alibaba", "Meituan", "JD.com"],
    "consumer_staples": ["Kweichow Moutai", "Yili", "Wuliangye", "Tingyi"],
    "pharma": ["Mindray", "WuXi AppTec", "Jiangsu Hengrui", "Sinopharm"],
    "autos_ev": ["BYD", "Geely", "Li Auto", "NIO"],
    "energy": ["CNOOC", "China Shenhua", "LONGi", "CATL"],
    "industrials": ["Sany", "CRRC", "Midea", "Zoomlion"],
    "telecom": ["China Mobile", "China Telecom", "China Unicom", "ZTE"],
    "defence": ["AVIC", "Aerospace CH UAV", "Norinco proxies", "CSSC"],
    "airlines": ["Air China", "China Southern", "China Eastern", "Spring Airlines"],
}

GLOBAL_SECTOR_REPRESENTATIVE_STOCKS = {
    "private_banks": ["JPMorgan", "HDFC Bank", "HSBC", "ICICI Bank"],
    "public_banks": ["SBI", "Bank of China", "BNP Paribas", "Wells Fargo"],
    "real_estate": ["Prologis", "DLF", "Vonovia", "China Resources Land"],
    "technology": ["Microsoft", "Infosys", "Tencent", "SAP"],
    "consumer_staples": ["Nestle", "Walmart", "HUL", "Kweichow Moutai"],
    "pharma": ["Novo Nordisk", "Sun Pharma", "Eli Lilly", "Roche"],
    "autos": ["Tesla", "BYD", "Maruti Suzuki", "Volkswagen"],
    "energy": ["Exxon Mobil", "Reliance Industries", "Shell", "CNOOC"],
    "materials": ["Tata Steel", "Nucor", "Rio Tinto", "Sinopec"],
    "infrastructure": ["L&T", "Vinci", "China State Construction", "Caterpillar"],
    "telecom": ["Bharti Airtel", "AT&T", "Deutsche Telekom", "China Mobile"],
    "defence": ["HAL", "Lockheed Martin", "BAE Systems", "AVIC"],
    "fintech": ["PayPal", "Paytm", "Block", "Adyen"],
    "airlines": ["Delta", "IndiGo", "Lufthansa", "Air China"],
}

MARKET_SECTOR_SCHEMAS = {
    "india": {
        "description": "Indian sector and watchlist schema",
        "sectors": INDIA_SECTORS,
        "representative_stocks": SECTOR_REPRESENTATIVE_STOCKS,
        "matrix_aliases": {sector: sector for sector in INDIA_SECTORS},
        "monitor_signals": [
            "Gift Nifty / SGX Nifty direction",
            "USD/INR and bond yield movement",
            "First domestic institutional commentary before the open",
        ],
    },
    "us": {
        "description": "US sector and watchlist schema",
        "sectors": [
            "banks", "regional_banks", "fintech", "insurance", "real_estate",
            "software", "consumer_staples", "pharma_biotech", "autos", "energy",
            "materials", "industrials", "telecom", "aerospace_defense", "airlines",
        ],
        "representative_stocks": US_SECTOR_REPRESENTATIVE_STOCKS,
        "matrix_aliases": {
            "banks": "banking_private",
            "regional_banks": "banking_psu",
            "fintech": "fintech",
            "insurance": "insurance",
            "real_estate": "real_estate",
            "software": "it_services",
            "consumer_staples": "fmcg",
            "pharma_biotech": "pharma",
            "autos": "auto",
            "energy": "energy_oil_gas",
            "materials": "metals_mining",
            "industrials": "capital_goods",
            "telecom": "telecom",
            "aerospace_defense": "defence",
            "airlines": "aviation",
        },
        "monitor_signals": [
            "Nasdaq and S&P futures direction",
            "US 2Y yield and DXY movement",
            "Pre-market bank, broker, and Fed-watch commentary",
        ],
    },
    "europe": {
        "description": "European sector and watchlist schema",
        "sectors": [
            "banks", "insurers", "real_estate", "industrials", "construction",
            "consumer_staples", "luxury_consumption", "pharma", "autos", "energy",
            "telecom", "defence", "airlines",
        ],
        "representative_stocks": EUROPE_SECTOR_REPRESENTATIVE_STOCKS,
        "matrix_aliases": {
            "banks": "banking_private",
            "insurers": "insurance",
            "real_estate": "real_estate",
            "industrials": "capital_goods",
            "construction": "infrastructure",
            "consumer_staples": "fmcg",
            "luxury_consumption": "consumption",
            "pharma": "pharma",
            "autos": "auto",
            "energy": "energy_oil_gas",
            "telecom": "telecom",
            "defence": "defence",
            "airlines": "aviation",
        },
        "monitor_signals": [
            "Euro Stoxx / DAX futures direction",
            "Bund yields and EUR/USD movement",
            "ECB, BOE, and large-bank commentary before the open",
        ],
    },
    "china": {
        "description": "China sector and watchlist schema",
        "sectors": [
            "banks", "state_enterprises", "real_estate", "internet_platforms",
            "consumer_staples", "pharma", "autos_ev", "energy", "industrials",
            "telecom", "defence", "airlines",
        ],
        "representative_stocks": CHINA_SECTOR_REPRESENTATIVE_STOCKS,
        "matrix_aliases": {
            "banks": "banking_private",
            "state_enterprises": "banking_psu",
            "real_estate": "real_estate",
            "internet_platforms": "it_services",
            "consumer_staples": "fmcg",
            "pharma": "pharma",
            "autos_ev": "auto",
            "energy": "energy_oil_gas",
            "industrials": "capital_goods",
            "telecom": "telecom",
            "defence": "defence",
            "airlines": "aviation",
        },
        "monitor_signals": [
            "CSI 300 / Hong Kong futures direction",
            "CNY fixing and local bond movement",
            "PBOC, regulator, and state-media policy tone",
        ],
    },
    "global": {
        "description": "Global cross-market sector and watchlist schema",
        "sectors": [
            "private_banks", "public_banks", "real_estate", "technology",
            "consumer_staples", "pharma", "autos", "energy", "materials",
            "infrastructure", "telecom", "defence", "fintech", "airlines",
        ],
        "representative_stocks": GLOBAL_SECTOR_REPRESENTATIVE_STOCKS,
        "matrix_aliases": {
            "private_banks": "banking_private",
            "public_banks": "banking_psu",
            "real_estate": "real_estate",
            "technology": "it_services",
            "consumer_staples": "fmcg",
            "pharma": "pharma",
            "autos": "auto",
            "energy": "energy_oil_gas",
            "materials": "metals_mining",
            "infrastructure": "infrastructure",
            "telecom": "telecom",
            "defence": "defence",
            "fintech": "fintech",
            "airlines": "aviation",
        },
        "monitor_signals": [
            "Cross-market index futures and volatility tone",
            "Dollar, yields, and commodity direction",
            "Large-bank and macro-desk commentary before cash open",
        ],
    },
}


def _get_market_sector_schema(geography: str) -> dict:
    return MARKET_SECTOR_SCHEMAS.get(geography, MARKET_SECTOR_SCHEMAS[DEFAULT_GEOGRAPHY])


def load_sector_matrix() -> dict:
    if not os.path.exists(SECTOR_MATRIX_PATH):
        return {}
    with open(SECTOR_MATRIX_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_behavioral_distribution(behavioral_distribution: dict) -> dict:
    if not behavioral_distribution:
        return {
            "panic": 0.25,
            "cautious": 0.25,
            "optimistic": 0.25,
            "divided": 0.25,
        }

    cleaned = {}
    for key, value in behavioral_distribution.items():
        try:
            cleaned[key] = float(value)
        except (TypeError, ValueError):
            cleaned[key] = 0.0

    if any(v > 1.0 for v in cleaned.values()):
        total = sum(cleaned.values()) or 1.0
        return {k: round(v / total, 4) for k, v in cleaned.items()}

    total = sum(cleaned.values()) or 1.0
    return {k: round(v / total, 4) for k, v in cleaned.items()}


def classify_market_regime(behavioral_distribution: dict, event_type: str = "general") -> tuple:
    behavioral_distribution = normalize_behavioral_distribution(behavioral_distribution)
    dominant = max(behavioral_distribution, key=behavioral_distribution.get)
    dominant_prob = behavioral_distribution[dominant]

    if dominant == "panic":
        regime = "policy_shock" if dominant_prob >= 0.70 else "risk_off"
    elif dominant == "cautious":
        regime = "uncertainty_hold" if dominant_prob >= 0.70 else "risk_off"
    elif dominant == "optimistic":
        regime = "relief_rally" if dominant_prob >= 0.70 else "risk_on"
    elif dominant == "divided":
        regime = "sector_rotation"
    else:
        regime = "uncertainty_hold"

    sorted_probs = sorted(behavioral_distribution.values(), reverse=True)
    lead = sorted_probs[0] - (sorted_probs[1] if len(sorted_probs) > 1 else 0.0)
    return regime, round(lead, 3)


def compute_sector_impacts(
    behavioral_distribution: dict,
    event_type: str,
    topic: str,
    geography: str = DEFAULT_GEOGRAPHY,
) -> dict:
    behavioral_distribution = normalize_behavioral_distribution(behavioral_distribution)
    matrix = load_sector_matrix()
    event_sensitivities = matrix.get("event_type_mappings", {}).get(event_type, {})
    market_schema = _get_market_sector_schema(geography)

    dominant = max(behavioral_distribution, key=behavioral_distribution.get)
    dominant_prob = behavioral_distribution[dominant]

    behavioral_multipliers = {
        "panic": {"negative": 1.30, "positive": 0.70, "neutral": 1.00},
        "cautious": {"negative": 0.90, "positive": 0.85, "neutral": 1.00},
        "optimistic": {"negative": 0.65, "positive": 1.25, "neutral": 1.00},
        "divided": {"negative": 0.80, "positive": 0.80, "neutral": 1.00},
    }
    multipliers = behavioral_multipliers.get(dominant, behavioral_multipliers["cautious"])

    sector_impacts = {}
    for sector in market_schema["sectors"]:
        source_sector = market_schema.get("matrix_aliases", {}).get(sector, sector)
        base = event_sensitivities.get(source_sector, {"direction": "neutral", "magnitude": 0.15})
        base_direction = base.get("direction", "neutral")
        base_magnitude = float(base.get("magnitude", 0.15))

        if "negative" in base_direction:
            direction_type = "negative"
        elif "positive" in base_direction:
            direction_type = "positive"
        else:
            direction_type = "neutral"

        adjusted_magnitude = base_magnitude * multipliers[direction_type]
        adjusted_confidence = min(0.95, adjusted_magnitude * dominant_prob + 0.1)

        sector_impacts[sector] = {
            "sector": sector,
            "direction": base_direction,
            "confidence": round(adjusted_confidence, 3),
            "reasoning": "",
            "base_sensitivity": round(base_magnitude, 3),
            "behavioral_adjustment": round(multipliers[direction_type], 3),
            "representative_stocks": market_schema["representative_stocks"].get(sector, [])[:4],
        }

    return sector_impacts


def _default_sector_reasoning(sector: str, impact: dict, topic: str, regime: str) -> str:
    direction = impact.get("direction", "neutral").replace("_", " ")
    sector_name = sector.replace("_", " ").title()
    if "negative" in impact.get("direction", ""):
        return f"{sector_name} faces pressure under the {regime.replace('_', ' ')} setup because {topic.lower()} raises earnings uncertainty and weakens short-term positioning."
    if "positive" in impact.get("direction", ""):
        return f"{sector_name} is positioned to benefit under the {regime.replace('_', ' ')} setup because {topic.lower()} improves relative demand, policy support, or defensive allocation."
    return f"{sector_name} is likely to remain comparatively stable because the simulated market response suggests only limited direct transmission from {topic.lower()}."


def generate_sector_reasonings(
    sector_impacts: dict,
    behavioral_distribution: dict,
    topic: str,
    market_regime: str
) -> dict:
    high_impact = [
        (sector, data) for sector, data in sector_impacts.items()
        if data.get("confidence", 0.0) >= 0.60
    ][:6]

    if not high_impact:
        return {}

    payload = []
    for sector, data in high_impact:
        payload.append({
            "sector": sector,
            "direction": data.get("direction"),
            "stocks": data.get("representative_stocks", [])[:3]
        })

    prompt = (
        f"Event: {topic}\n"
        f"Market regime: {market_regime}\n"
        f"Behavioral distribution: {behavioral_distribution}\n\n"
        f"For each sector below, write one sentence of market-specific causal reasoning.\n"
        f"Return JSON object mapping sector key -> reasoning sentence only.\n"
        f"Sectors: {json.dumps(payload)}"
    )

    result = ask_llm_json(prompt)
    if result.get("parse_error"):
        return {
            sector: _default_sector_reasoning(sector, data, topic, market_regime)
            for sector, data in high_impact
        }

    reasonings = {}
    for sector, data in high_impact:
        reasoning = result.get(sector, "")
        reasonings[sector] = reasoning.strip() if isinstance(reasoning, str) and reasoning.strip() else _default_sector_reasoning(sector, data, topic, market_regime)
    return reasonings


def build_watchlists(sector_impacts: dict) -> dict:
    laggards = []
    resilient = []
    beneficiaries = []

    for sector, impact in sector_impacts.items():
        item = {
            "sector": sector.replace("_", " ").title(),
            "confidence": impact["confidence"],
            "stocks": impact["representative_stocks"][:3]
        }
        direction = impact["direction"]
        confidence = impact["confidence"]

        if "negative" in direction and confidence > 0.55:
            laggards.append(item)
        elif "positive" in direction and confidence > 0.55:
            beneficiaries.append(item)
        elif direction == "neutral" and confidence > 0.50:
            resilient.append(item)

    laggards.sort(key=lambda x: x["confidence"], reverse=True)
    resilient.sort(key=lambda x: x["confidence"], reverse=True)
    beneficiaries.sort(key=lambda x: x["confidence"], reverse=True)

    return {
        "likely_laggards": laggards[:5],
        "likely_resilient": resilient[:4],
        "likely_beneficiaries": beneficiaries[:4]
    }


def generate_narrative_expectations(
    topic: str,
    dominant_outcome: str,
    market_regime: str,
    geography: str = DEFAULT_GEOGRAPHY,
) -> dict:
    prompt = (
        f"Event: {topic}\n"
        f"Market geography: {geography}\n"
        f"Market regime predicted: {market_regime}\n"
        f"Dominant behavioral response: {dominant_outcome}\n\n"
        f"Return JSON with keys retail_narrative, institutional_narrative, media_narrative. "
        f"Each should be one concise sentence describing likely framing."
    )
    result = ask_llm_json(prompt)
    if result.get("parse_error"):
        return {
            "retail_narrative": "Retail participants are likely to focus on immediate gain or loss and react to the strongest headline framing.",
            "institutional_narrative": "Institutional desks are likely to frame the event through positioning, policy transmission, and sector allocation changes.",
            "media_narrative": "Financial media is likely to frame the event around market winners, losers, and whether the move signals a broader regime shift."
        }
    return {
        "retail_narrative": result.get("retail_narrative", ""),
        "institutional_narrative": result.get("institutional_narrative", ""),
        "media_narrative": result.get("media_narrative", "")
    }


def generate_confidence_triggers(
    topic: str,
    market_regime: str,
    geography: str = DEFAULT_GEOGRAPHY,
) -> dict:
    market_schema = _get_market_sector_schema(geography)
    prompt = (
        f"Event: {topic}\n"
        f"Market geography: {geography}\n"
        f"Predicted market regime: {market_regime}\n\n"
        f"Return JSON with three lists: strengthens, weakens, monitor_signals. "
        f"Each list should contain exactly three short pre-market signals."
    )
    result = ask_llm_json(prompt)
    if result.get("parse_error"):
        return {
            "strengthens": [
                "Global cues move in the same direction as the forecast",
                "Early brokerage notes reinforce the same sector narrative",
                "Pre-open index signals confirm the initial risk tone"
            ],
            "weakens": [
                "A policy clarification softens the event shock",
                "Global cues reverse sharply before the open",
                "Key management or regulator commentary contradicts the dominant narrative"
            ],
            "monitor_signals": market_schema.get("monitor_signals", [])[:3]
        }
    return {
        "strengthens": result.get("strengthens", []),
        "weakens": result.get("weakens", []),
        "monitor_signals": result.get("monitor_signals", [])
    }


def _estimate_volatility(behavioral_distribution: dict) -> tuple:
    panic_weight = behavioral_distribution.get("panic", 0.0)
    cautious_weight = behavioral_distribution.get("cautious", 0.0)

    if panic_weight > 0.60:
        return "extreme", "rising"
    if panic_weight > 0.40:
        return "high", "rising"
    if cautious_weight > 0.55:
        return "moderate", "stable"
    return "low", "falling"


def _expected_price_discovery_hours(market_regime: str) -> int:
    mapping = {
        "policy_shock": 24,
        "risk_off": 18,
        "risk_on": 18,
        "relief_rally": 12,
        "uncertainty_hold": 36,
        "sector_rotation": 30,
    }
    return mapping.get(market_regime, 24)


def _second_order_effects(event_type: str, market_regime: str) -> list:
    defaults = {
        "rbi_rate_hike": [
            "Borrowing-sensitive sectors may see weaker earnings expectations over the next two sessions.",
            "Defensive allocation could increase if policy communication stays hawkish.",
            "Loan growth and funding-cost narratives may dominate broker notes."
        ],
        "oil_price_spike": [
            "Input-cost pressure may widen beyond transport into chemicals and consumption.",
            "Energy beneficiaries may outperform if crude remains elevated.",
            "Inflation-linked policy concerns may become a second-order market driver."
        ],
        "general": [
            "Sector leadership may become clearer after institutional commentary matures.",
            "Analyst notes and media framing may shift the second-day narrative.",
            "Policy clarification could either stabilize or intensify the initial move."
        ]
    }
    return defaults.get(event_type, defaults["general"])


def generate_full_market_impact(
    behavioral_distribution: dict,
    event_type: str,
    topic: str,
    branch_count: int = 3,
    geography: str = None,
    graph_path: str = None,
) -> dict:
    resolved_geography = resolve_market_geography(
        geography=geography,
        graph_path=graph_path,
        topic=topic,
        event_type=event_type,
    )
    market_schema = _get_market_sector_schema(resolved_geography)

    print(
        "\n  Generating market impact analysis for "
        f"{resolved_geography} ({market_schema['description']})..."
    )

    normalized = normalize_behavioral_distribution(behavioral_distribution)
    regime, regime_confidence = classify_market_regime(normalized, event_type)
    sector_impacts = compute_sector_impacts(
        normalized,
        event_type,
        topic,
        geography=resolved_geography,
    )

    reasonings = generate_sector_reasonings(
        sector_impacts=sector_impacts,
        behavioral_distribution=normalized,
        topic=topic,
        market_regime=regime
    )
    for sector, reasoning in reasonings.items():
        sector_impacts[sector]["reasoning"] = reasoning

    for sector, impact in sector_impacts.items():
        if not impact.get("reasoning"):
            impact["reasoning"] = _default_sector_reasoning(sector, impact, topic, regime)

    watchlists = build_watchlists(sector_impacts)
    dominant_outcome = max(normalized, key=normalized.get)
    narratives = generate_narrative_expectations(
        topic,
        dominant_outcome,
        regime,
        geography=resolved_geography,
    )
    triggers = generate_confidence_triggers(
        topic,
        regime,
        geography=resolved_geography,
    )
    volatility_expectation, vix_direction = _estimate_volatility(normalized)
    simulation_confidence = round(max(normalized.values()), 3)

    print("  Market impact analysis complete.")

    return {
        "market_geography": resolved_geography,
        "market_scope_description": market_schema["description"],
        "market_regime": regime,
        "regime_confidence": regime_confidence,
        "sector_impacts": sector_impacts,
        "volatility_expectation": volatility_expectation,
        "vix_direction": vix_direction,
        "likely_laggards": watchlists["likely_laggards"],
        "likely_resilient": watchlists["likely_resilient"],
        "likely_beneficiaries": watchlists["likely_beneficiaries"],
        "triggers_that_strengthen": triggers.get("strengthens", []),
        "triggers_that_weaken": triggers.get("weakens", []),
        "monitoring_signals": triggers.get("monitor_signals", []),
        "retail_narrative": narratives.get("retail_narrative", ""),
        "institutional_narrative": narratives.get("institutional_narrative", ""),
        "media_narrative": narratives.get("media_narrative", ""),
        "expected_price_discovery_hours": _expected_price_discovery_hours(regime),
        "second_order_effects": _second_order_effects(event_type, regime),
        "behavioral_distribution": normalized,
        "branch_count": branch_count,
        "simulation_confidence": simulation_confidence,
        "dominant_outcome": dominant_outcome,
        "event_type": event_type,
    }
