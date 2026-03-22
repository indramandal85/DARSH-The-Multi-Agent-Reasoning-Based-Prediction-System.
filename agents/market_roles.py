# agents/market_roles.py
#
# Phase 3 market participant role registry and assignment helpers.

import random


MARKET_ROLES = {
    "RETAIL_TRADER": {
        "label": "Retail Trader",
        "category": "individual",
        "reaction_speed": "very_fast",
        "constraints": [
            "Limited access to privileged information",
            "React strongly to headlines and price moves",
            "Must balance conviction with personal capital risk",
        ],
        "information_sources": [
            "broker app alerts",
            "financial influencers and social feeds",
            "headline news and price charts",
        ],
        "background_template": (
            "Acts as a retail market participant focused on near-term market moves. "
            "Relies on broker dashboards, headline sentiment, and price action."
        ),
    },
    "DOMESTIC_MUTUAL_FUND": {
        "label": "Domestic Mutual Fund Manager",
        "category": "institutional_human",
        "reaction_speed": "medium",
        "constraints": [
            "Must justify allocation shifts to investment committee",
            "Cannot overtrade on thin information",
            "Balances benchmark risk with long-only discipline",
        ],
        "information_sources": [
            "internal sector notes",
            "company management commentary",
            "macro and liquidity dashboards",
        ],
        "background_template": (
            "Acts as a domestic mutual fund participant weighing sector rotation, flows, "
            "and benchmark-relative positioning."
        ),
    },
    "FII_ANALYST": {
        "label": "Foreign Institutional Analyst",
        "category": "institutional_human",
        "reaction_speed": "medium",
        "constraints": [
            "Frames India within global risk appetite",
            "Compares local events with USD, rates, and EM positioning",
            "Needs clean macro narrative before increasing risk",
        ],
        "information_sources": [
            "global macro desk updates",
            "currency and bond market moves",
            "cross-market relative-value notes",
        ],
        "background_template": (
            "Acts as a foreign institutional participant comparing India-specific events "
            "against global flows, rates, and currency risk."
        ),
    },
    "HEDGE_FUND_PM": {
        "label": "Hedge Fund PM",
        "category": "institutional_human",
        "reaction_speed": "fast",
        "constraints": [
            "Seeks asymmetric upside and downside trades",
            "Can move quickly but demands an edge versus consensus",
            "Looks for narrative dislocations and crowded positioning",
        ],
        "information_sources": [
            "fast macro commentary",
            "positioning and flow chatter",
            "cross-asset volatility signals",
        ],
        "background_template": (
            "Acts as a hedge fund portfolio manager hunting for asymmetric trades and "
            "mispriced second-order effects."
        ),
    },
    "PRIVATE_BANK_TREASURY": {
        "label": "Private Bank Treasury",
        "category": "institution",
        "reaction_speed": "medium",
        "constraints": [
            "Must manage liquidity, duration, and treasury risk prudently",
            "Cannot respond impulsively to noise",
            "Tracks impact on funding costs and client books",
        ],
        "information_sources": [
            "bond market and swap curves",
            "treasury desk signals",
            "internal ALM commentary",
        ],
        "background_template": (
            "Acts as a private bank treasury desk focused on rates, liquidity, and client risk transmission."
        ),
    },
    "PSU_BANK_DESK": {
        "label": "PSU Bank Desk",
        "category": "institution",
        "reaction_speed": "medium",
        "constraints": [
            "Balances commercial logic with public policy sensitivity",
            "Must consider transmission to broad customer base",
            "Cannot ignore government and regulatory tone",
        ],
        "information_sources": [
            "public sector banking channels",
            "policy and regulator commentary",
            "loan and deposit transmission data",
        ],
        "background_template": (
            "Acts as a PSU bank desk evaluating policy transmission, credit conditions, "
            "and public-sector balance-sheet implications."
        ),
    },
    "BROKER_RESEARCH_DESK": {
        "label": "Broker Research Desk",
        "category": "institutional_human",
        "reaction_speed": "fast",
        "constraints": [
            "Needs to publish coherent sector calls quickly",
            "Balances conviction with reputational risk",
            "Translates macro events into stock and sector notes",
        ],
        "information_sources": [
            "sell-side channel checks",
            "management commentary",
            "macro and valuation models",
        ],
        "background_template": (
            "Acts as a broker research desk converting market-moving events into sector "
            "notes, downgrades, and actionable watchlists."
        ),
    },
    "FINANCIAL_MEDIA_EDITOR": {
        "label": "Financial Media Editor",
        "category": "institutional_human",
        "reaction_speed": "very_fast",
        "constraints": [
            "Prioritizes the angle audiences will notice first",
            "Can amplify emotion or calm depending on framing",
            "Needs crisp narrative more than full certainty",
        ],
        "information_sources": [
            "live headlines",
            "broker and strategist quotes",
            "social narrative velocity",
        ],
        "background_template": (
            "Acts as a financial media editor shaping the narrative that reaches traders, "
            "retail investors, and business audiences."
        ),
    },
    "REGULATOR_POLICY_DESK": {
        "label": "Regulator Policy Desk",
        "category": "institution",
        "reaction_speed": "slow",
        "constraints": [
            "Must preserve market functioning and credibility",
            "Avoids reactive statements without policy basis",
            "Prioritizes stability over speculative upside",
        ],
        "information_sources": [
            "official data releases",
            "policy memos",
            "systemic risk dashboards",
        ],
        "background_template": (
            "Acts as a regulator-side policy desk watching market stability, transmission, "
            "and the need for communication or intervention."
        ),
    },
    "MINISTRY_POLICY_TEAM": {
        "label": "Ministry Policy Team",
        "category": "institution",
        "reaction_speed": "slow",
        "constraints": [
            "Frames the event through political and economic trade-offs",
            "Needs to assess public and sector spillovers",
            "Communicates cautiously but watches narrative drift closely",
        ],
        "information_sources": [
            "inter-ministry feedback",
            "headline economic indicators",
            "sector and public-impact briefings",
        ],
        "background_template": (
            "Acts as a ministry policy team balancing growth, inflation, public sentiment, "
            "and political-economic consequences."
        ),
    },
    "CORPORATE_TREASURY": {
        "label": "Corporate Treasury",
        "category": "institution",
        "reaction_speed": "medium",
        "constraints": [
            "Evaluates funding cost, FX exposure, and working-capital stress",
            "Looks at operational rather than purely trading impact",
            "Prefers scenario planning to speculative action",
        ],
        "information_sources": [
            "funding and FX dashboards",
            "input-cost assumptions",
            "management risk reports",
        ],
        "background_template": (
            "Acts as a corporate treasury function translating market events into funding, "
            "margin, and operating-risk decisions."
        ),
    },
    "SECTOR_OPERATING_FIRM": {
        "label": "Sector Operating Firm",
        "category": "institution",
        "reaction_speed": "medium",
        "constraints": [
            "Evaluates how the event affects sector demand, costs, and execution",
            "Focuses on real-business transmission rather than only prices",
            "Interprets policy through sector-specific operating pressure",
        ],
        "information_sources": [
            "supplier and customer signals",
            "industry body commentary",
            "sector-specific margin and demand indicators",
        ],
        "background_template": (
            "Acts as an operating firm inside the affected sector, assessing how the event "
            "changes demand, margins, financing conditions, or execution risk."
        ),
    },
}


ROLE_COGNITION_WEIGHTS = {
    "RETAIL_TRADER": {"emotional": 0.45, "tribal": 0.25, "rational": 0.20, "contrarian": 0.05, "institutional": 0.05},
    "DOMESTIC_MUTUAL_FUND": {"rational": 0.45, "institutional": 0.35, "contrarian": 0.10, "emotional": 0.05, "tribal": 0.05},
    "FII_ANALYST": {"rational": 0.50, "contrarian": 0.20, "institutional": 0.20, "emotional": 0.05, "tribal": 0.05},
    "HEDGE_FUND_PM": {"contrarian": 0.40, "rational": 0.30, "institutional": 0.15, "emotional": 0.10, "tribal": 0.05},
    "PRIVATE_BANK_TREASURY": {"institutional": 0.55, "rational": 0.30, "contrarian": 0.05, "emotional": 0.05, "tribal": 0.05},
    "PSU_BANK_DESK": {"institutional": 0.50, "rational": 0.25, "tribal": 0.10, "contrarian": 0.10, "emotional": 0.05},
    "BROKER_RESEARCH_DESK": {"rational": 0.40, "contrarian": 0.25, "institutional": 0.20, "emotional": 0.10, "tribal": 0.05},
    "FINANCIAL_MEDIA_EDITOR": {"emotional": 0.30, "tribal": 0.20, "contrarian": 0.20, "rational": 0.15, "institutional": 0.15},
    "REGULATOR_POLICY_DESK": {"institutional": 0.60, "rational": 0.25, "contrarian": 0.05, "tribal": 0.05, "emotional": 0.05},
    "MINISTRY_POLICY_TEAM": {"institutional": 0.45, "rational": 0.20, "tribal": 0.15, "contrarian": 0.10, "emotional": 0.10},
    "CORPORATE_TREASURY": {"institutional": 0.35, "rational": 0.35, "contrarian": 0.15, "emotional": 0.10, "tribal": 0.05},
    "SECTOR_OPERATING_FIRM": {"rational": 0.25, "institutional": 0.25, "tribal": 0.20, "emotional": 0.15, "contrarian": 0.15},
}


EVENT_ROLE_WEIGHTS = {
    "general": {
        "RETAIL_TRADER": 0.18,
        "DOMESTIC_MUTUAL_FUND": 0.10,
        "FII_ANALYST": 0.09,
        "HEDGE_FUND_PM": 0.06,
        "PRIVATE_BANK_TREASURY": 0.08,
        "PSU_BANK_DESK": 0.08,
        "BROKER_RESEARCH_DESK": 0.10,
        "FINANCIAL_MEDIA_EDITOR": 0.08,
        "REGULATOR_POLICY_DESK": 0.06,
        "MINISTRY_POLICY_TEAM": 0.05,
        "CORPORATE_TREASURY": 0.06,
        "SECTOR_OPERATING_FIRM": 0.06,
    },
    "rbi_rate_hike": {
        "RETAIL_TRADER": 0.14,
        "DOMESTIC_MUTUAL_FUND": 0.10,
        "FII_ANALYST": 0.10,
        "HEDGE_FUND_PM": 0.06,
        "PRIVATE_BANK_TREASURY": 0.11,
        "PSU_BANK_DESK": 0.11,
        "BROKER_RESEARCH_DESK": 0.09,
        "FINANCIAL_MEDIA_EDITOR": 0.07,
        "REGULATOR_POLICY_DESK": 0.09,
        "MINISTRY_POLICY_TEAM": 0.05,
        "CORPORATE_TREASURY": 0.04,
        "SECTOR_OPERATING_FIRM": 0.04,
    },
    "budget_fiscal_expansion": {
        "RETAIL_TRADER": 0.12,
        "DOMESTIC_MUTUAL_FUND": 0.11,
        "FII_ANALYST": 0.09,
        "HEDGE_FUND_PM": 0.07,
        "PRIVATE_BANK_TREASURY": 0.06,
        "PSU_BANK_DESK": 0.07,
        "BROKER_RESEARCH_DESK": 0.11,
        "FINANCIAL_MEDIA_EDITOR": 0.09,
        "REGULATOR_POLICY_DESK": 0.04,
        "MINISTRY_POLICY_TEAM": 0.11,
        "CORPORATE_TREASURY": 0.06,
        "SECTOR_OPERATING_FIRM": 0.07,
    },
    "oil_price_spike": {
        "RETAIL_TRADER": 0.12,
        "DOMESTIC_MUTUAL_FUND": 0.08,
        "FII_ANALYST": 0.10,
        "HEDGE_FUND_PM": 0.09,
        "PRIVATE_BANK_TREASURY": 0.06,
        "PSU_BANK_DESK": 0.06,
        "BROKER_RESEARCH_DESK": 0.10,
        "FINANCIAL_MEDIA_EDITOR": 0.10,
        "REGULATOR_POLICY_DESK": 0.05,
        "MINISTRY_POLICY_TEAM": 0.05,
        "CORPORATE_TREASURY": 0.09,
        "SECTOR_OPERATING_FIRM": 0.10,
    },
}


def get_market_role_definition(role_key: str) -> dict:
    return MARKET_ROLES[role_key]


def get_event_role_weights(event_type: str) -> dict:
    return EVENT_ROLE_WEIGHTS.get(event_type, EVENT_ROLE_WEIGHTS["general"])


def allocate_counts_from_weights(total_count: int, weights: dict) -> dict:
    items = list(weights.items())
    counts = {}
    remainders = []
    assigned = 0

    for key, weight in items:
        exact = total_count * weight
        count = int(exact)
        counts[key] = count
        assigned += count
        remainders.append((exact - count, key))

    remaining = total_count - assigned
    for _, key in sorted(remainders, reverse=True)[:remaining]:
        counts[key] += 1

    return {key: value for key, value in counts.items() if value > 0}


def build_market_role_background(role_key: str, event_type: str, topic: str) -> str:
    role = get_market_role_definition(role_key)
    constraints = "; ".join(role["constraints"])
    sources = ", ".join(role["information_sources"])
    return (
        f"Market role: {role['label']}.\n"
        f"Role context: {role['background_template']}\n"
        f"Reaction speed: {role['reaction_speed']}.\n"
        f"Key information sources: {sources}.\n"
        f"Operating constraints: {constraints}.\n"
        f"Current event frame: {event_type.replace('_', ' ')} related to {topic}."
    )


def assign_roles_to_agent_types(type_counts: dict, event_type: str) -> list:
    """
    Pair market roles with cognition types while preserving the overall
    cognitive distribution already used by the project.
    """
    role_counts = allocate_counts_from_weights(sum(type_counts.values()), get_event_role_weights(event_type))
    role_sequence = []
    for role_key, count in role_counts.items():
        role_sequence.extend([role_key] * count)
    random.shuffle(role_sequence)

    remaining_type_counts = dict(type_counts)
    assignments = []

    for role_key in role_sequence:
        compatible_weights = ROLE_COGNITION_WEIGHTS.get(role_key, {})
        candidate_types = []
        candidate_weights = []

        for agent_type, weight in compatible_weights.items():
            remaining = remaining_type_counts.get(agent_type, 0)
            if remaining > 0:
                candidate_types.append(agent_type)
                candidate_weights.append(weight * remaining)

        if not candidate_types:
            candidate_types = [atype for atype, remaining in remaining_type_counts.items() if remaining > 0]
            candidate_weights = [remaining_type_counts[atype] for atype in candidate_types]

        chosen_type = random.choices(candidate_types, weights=candidate_weights, k=1)[0]
        remaining_type_counts[chosen_type] -= 1
        assignments.append((role_key, chosen_type))

    return assignments
