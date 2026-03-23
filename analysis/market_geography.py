import json
import os
from copy import deepcopy


DEFAULT_GEOGRAPHY = "global"


def _role(population_count: int, unit_label: str, capital_influence: float, velocity_influence: float) -> dict:
    return {
        "population_count": int(population_count),
        "unit_label": unit_label,
        "capital_influence": float(capital_influence),
        "velocity_influence": float(velocity_influence),
    }


GLOBAL_ROLE_BASELINE = {
    "RETAIL_TRADER": _role(28_000_000, "active retail accounts", 0.40, 0.85),
    "DOMESTIC_MUTUAL_FUND": _role(18_000_000, "fund and ETF investor accounts", 0.82, 0.38),
    "FII_ANALYST": _role(9_000, "cross-border institutional desks", 0.95, 0.65),
    "HEDGE_FUND_PM": _role(2_500, "hedge fund strategy desks", 1.00, 0.88),
    "PRIVATE_BANK_TREASURY": _role(900, "private bank treasury desks", 0.80, 0.48),
    "PSU_BANK_DESK": _role(300, "policy-sensitive bank desks", 0.76, 0.42),
    "BROKER_RESEARCH_DESK": _role(6_000, "broker research desks", 0.36, 0.92),
    "FINANCIAL_MEDIA_EDITOR": _role(2_200, "financial media desks", 0.12, 0.98),
    "REGULATOR_POLICY_DESK": _role(120, "regulator policy teams", 0.62, 0.25),
    "MINISTRY_POLICY_TEAM": _role(80, "economic policy teams", 0.58, 0.22),
    "CORPORATE_TREASURY": _role(30_000, "corporate treasury teams", 0.55, 0.55),
    "SECTOR_OPERATING_FIRM": _role(400_000, "sector operating firms", 0.30, 0.60),
}


INDIA_ROLE_WEIGHTS = {
    "RETAIL_TRADER": _role(40_000_000, "active retail trading accounts", 0.55, 1.00),
    "DOMESTIC_MUTUAL_FUND": _role(47_000_000, "mutual fund folios", 0.90, 0.45),
    "FII_ANALYST": _role(12_000, "foreign institutional desks", 1.00, 0.70),
    "HEDGE_FUND_PM": _role(450, "hedge fund strategy desks", 0.95, 0.85),
    "PRIVATE_BANK_TREASURY": _role(320, "private bank treasury desks", 0.82, 0.50),
    "PSU_BANK_DESK": _role(180, "PSU banking desks", 0.78, 0.44),
    "BROKER_RESEARCH_DESK": _role(3_500, "broker research desks", 0.42, 0.90),
    "FINANCIAL_MEDIA_EDITOR": _role(1_200, "financial media desks", 0.18, 0.98),
    "REGULATOR_POLICY_DESK": _role(75, "regulator policy teams", 0.70, 0.28),
    "MINISTRY_POLICY_TEAM": _role(60, "ministry policy teams", 0.65, 0.25),
    "CORPORATE_TREASURY": _role(8_000, "corporate treasury teams", 0.58, 0.52),
    "SECTOR_OPERATING_FIRM": _role(250_000, "listed / large operating firms", 0.36, 0.62),
}


def _merged_role_weights(base: dict, overrides: dict) -> dict:
    merged = deepcopy(base)
    for role_key, fields in (overrides or {}).items():
        merged.setdefault(role_key, {})
        merged[role_key].update(fields)
    return merged


MARKET_CONFIGS = {
    "india": {
        "description": "Indian equity market (NSE/BSE oriented structure)",
        "population_data_year": 2024,
        "role_weights": INDIA_ROLE_WEIGHTS,
    },
    "us": {
        "description": "US equity market (NYSE/NASDAQ oriented structure)",
        "population_data_year": 2024,
        "role_weights": _merged_role_weights(GLOBAL_ROLE_BASELINE, {
            "RETAIL_TRADER": _role(32_000_000, "active retail brokerage accounts", 0.28, 0.82),
            "DOMESTIC_MUTUAL_FUND": _role(24_000_000, "fund and ETF allocator accounts", 0.85, 0.35),
            "FII_ANALYST": _role(18_000, "global macro and foreign institutional desks", 0.95, 0.72),
            "HEDGE_FUND_PM": _role(3_200, "hedge fund and fast-money desks", 1.00, 0.90),
            "PRIVATE_BANK_TREASURY": _role(1_400, "bank treasury desks", 0.85, 0.52),
            "PSU_BANK_DESK": _role(220, "policy-sensitive bank desks", 0.74, 0.36),
            "BROKER_RESEARCH_DESK": _role(9_000, "sell-side research desks", 0.38, 0.94),
            "FINANCIAL_MEDIA_EDITOR": _role(2_600, "financial media desks", 0.12, 0.98),
            "REGULATOR_POLICY_DESK": _role(140, "market and policy regulator teams", 0.66, 0.24),
            "MINISTRY_POLICY_TEAM": _role(90, "economic policy teams", 0.60, 0.20),
            "CORPORATE_TREASURY": _role(42_000, "corporate treasury teams", 0.60, 0.58),
            "SECTOR_OPERATING_FIRM": _role(520_000, "listed / large operating firms", 0.32, 0.60),
        }),
    },
    "europe": {
        "description": "European market (ECB and regional exchange structure)",
        "population_data_year": 2024,
        "role_weights": _merged_role_weights(GLOBAL_ROLE_BASELINE, {
            "RETAIL_TRADER": _role(14_000_000, "active retail investor accounts", 0.20, 0.55),
            "DOMESTIC_MUTUAL_FUND": _role(16_000_000, "fund and pension allocator accounts", 0.78, 0.32),
            "FII_ANALYST": _role(10_000, "cross-border institutional desks", 0.82, 0.60),
            "HEDGE_FUND_PM": _role(1_800, "hedge fund strategy desks", 0.88, 0.78),
            "PRIVATE_BANK_TREASURY": _role(1_200, "bank treasury desks", 0.84, 0.45),
            "PSU_BANK_DESK": _role(600, "public and policy-sensitive bank desks", 0.90, 0.36),
            "BROKER_RESEARCH_DESK": _role(5_000, "broker and strategist desks", 0.34, 0.85),
            "FINANCIAL_MEDIA_EDITOR": _role(1_600, "financial media desks", 0.10, 0.92),
            "REGULATOR_POLICY_DESK": _role(180, "market and central-bank policy teams", 0.70, 0.22),
            "MINISTRY_POLICY_TEAM": _role(140, "finance ministry teams", 0.66, 0.20),
            "CORPORATE_TREASURY": _role(28_000, "corporate treasury teams", 0.52, 0.50),
            "SECTOR_OPERATING_FIRM": _role(350_000, "listed / large operating firms", 0.28, 0.56),
        }),
    },
    "china": {
        "description": "Chinese market (A-share and policy-guided structure)",
        "population_data_year": 2024,
        "role_weights": _merged_role_weights(GLOBAL_ROLE_BASELINE, {
            "RETAIL_TRADER": _role(58_000_000, "active retail trading accounts", 0.48, 0.88),
            "DOMESTIC_MUTUAL_FUND": _role(22_000_000, "fund investor accounts", 0.72, 0.38),
            "FII_ANALYST": _role(4_000, "foreign and cross-border desks", 0.55, 0.48),
            "HEDGE_FUND_PM": _role(1_200, "fast-money and hedge-fund desks", 0.75, 0.72),
            "PRIVATE_BANK_TREASURY": _role(700, "commercial bank treasury desks", 0.68, 0.42),
            "PSU_BANK_DESK": _role(950, "state-influenced bank desks", 0.96, 0.30),
            "BROKER_RESEARCH_DESK": _role(4_500, "broker research desks", 0.30, 0.82),
            "FINANCIAL_MEDIA_EDITOR": _role(1_500, "financial media desks", 0.14, 0.95),
            "REGULATOR_POLICY_DESK": _role(220, "market and policy regulator teams", 0.78, 0.24),
            "MINISTRY_POLICY_TEAM": _role(160, "economic policy teams", 0.76, 0.22),
            "CORPORATE_TREASURY": _role(34_000, "corporate treasury teams", 0.56, 0.50),
            "SECTOR_OPERATING_FIRM": _role(480_000, "listed / large operating firms", 0.34, 0.58),
        }),
    },
    "global": {
        "description": "Global cross-market scenario (balanced default)",
        "population_data_year": 2024,
        "role_weights": deepcopy(GLOBAL_ROLE_BASELINE),
    },
}


GEOGRAPHY_KEYWORDS = {
    "india": [
        "india", "indian", "rbi", "reserve bank of india", "sebi",
        "nse", "bse", "sensex", "nifty", "rupee", "inr", "mumbai",
    ],
    "us": [
        "united states", "u.s.", "usa", "american", "federal reserve",
        "fed", "nyse", "nasdaq", "s&p 500", "dow jones", "treasury",
        "usd", "dollar", "sec",
    ],
    "europe": [
        "europe", "european", "ecb", "european central bank", "bank of england",
        "boe", "euro", "eur", "dax", "ftse", "cac 40", "stoxx",
    ],
    "china": [
        "china", "chinese", "pboc", "people's bank of china", "peoples bank of china",
        "shanghai", "shenzhen", "yuan", "renminbi", "cny", "a-share", "csrc",
    ],
}


GEOGRAPHY_ALIASES = {
    "usa": "us",
    "u.s.": "us",
    "united_states": "us",
    "eu": "europe",
    "european_union": "europe",
    "uk": "europe",
    "united_kingdom": "europe",
    "prc": "china",
    "world": "global",
}


def normalize_geography_key(geography: str | None) -> str | None:
    if geography is None:
        return None
    cleaned = str(geography).strip().lower().replace("-", "_").replace(" ", "_")
    if not cleaned:
        return None
    return GEOGRAPHY_ALIASES.get(cleaned, cleaned)


def _detect_geography_from_text(text: str) -> str:
    haystack = (text or "").lower()
    if not haystack.strip():
        return DEFAULT_GEOGRAPHY

    scores = {geo: 0 for geo in GEOGRAPHY_KEYWORDS}
    for geo, keywords in GEOGRAPHY_KEYWORDS.items():
        for keyword in keywords:
            scores[geo] += haystack.count(keyword.lower())

    best_geo = max(scores, key=scores.get)
    best_score = scores[best_geo]
    if best_score == 0:
        return DEFAULT_GEOGRAPHY

    ordered_scores = sorted(scores.values(), reverse=True)
    if len(ordered_scores) > 1 and best_score == ordered_scores[1]:
        return DEFAULT_GEOGRAPHY

    return best_geo


def detect_geography_from_graph(graph_path: str | None) -> str:
    """
    Read the saved graph JSON and infer a geography from node IDs/descriptions.
    """
    if not graph_path or not os.path.exists(graph_path):
        return DEFAULT_GEOGRAPHY

    try:
        with open(graph_path, "r", encoding="utf-8") as handle:
            graph_data = json.load(handle)
    except Exception:
        return DEFAULT_GEOGRAPHY

    nodes = graph_data.get("nodes", []) or []
    searchable = " ".join(
        f"{node.get('id', '')} {node.get('description', '')}"
        for node in nodes
    )
    return _detect_geography_from_text(searchable)


def resolve_market_geography(
    geography: str | None = None,
    graph_path: str | None = None,
    topic: str = "",
    event_type: str = "general",
) -> str:
    """
    Resolve the market geography from explicit override, graph signals, or topic text.
    """
    normalized = normalize_geography_key(geography)
    if normalized in MARKET_CONFIGS:
        return normalized

    graph_geo = detect_geography_from_graph(graph_path)
    if graph_geo != DEFAULT_GEOGRAPHY:
        return graph_geo

    combined_text = " ".join([
        topic or "",
        event_type or "",
        os.path.basename(graph_path or ""),
    ])
    return _detect_geography_from_text(combined_text)


def get_market_config(geography: str | None) -> dict:
    normalized = normalize_geography_key(geography)
    return MARKET_CONFIGS.get(normalized, MARKET_CONFIGS[DEFAULT_GEOGRAPHY])
