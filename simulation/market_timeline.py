# simulation/market_timeline.py
#
# Structured market propagation timeline for Phase 4.

from copy import deepcopy


MARKET_TIMELINE_STAGES = [
    {
        "round_number": 1,
        "label": "Headline Shock",
        "time_window": "0-2 hours",
        "focus": (
            "Immediate headline parsing, first price discovery, and the fastest "
            "sentiment reaction from desks and traders."
        ),
    },
    {
        "round_number": 2,
        "label": "Institutional Interpretation",
        "time_window": "2-12 hours",
        "focus": (
            "Broker notes, treasury desks, fund managers, and policy watchers "
            "translate the event into sector-level implications."
        ),
    },
    {
        "round_number": 3,
        "label": "Social and Media Amplification",
        "time_window": "8-24 hours",
        "focus": (
            "Financial media, social channels, and public narratives amplify, "
            "distort, or stabilize the first reaction."
        ),
    },
    {
        "round_number": 4,
        "label": "Positioning and Rotation",
        "time_window": "1-2 trading sessions",
        "focus": (
            "Participants rotate across sectors, hedge exposures, and reassess "
            "the durability of the first move."
        ),
    },
    {
        "round_number": 5,
        "label": "Policy Clarity and Second-Order Effects",
        "time_window": "2-5 trading sessions",
        "focus": (
            "Second-order effects become visible through policy clarifications, "
            "balance-sheet implications, and broader macro interpretation."
        ),
    },
]


BRANCH_NARRATIVE_TEMPLATES = [
    {
        "branch_id": "base_case_balanced",
        "label": "Base Case",
        "summary": "Markets digest the event with a balanced mix of caution and selective rotation.",
    },
    {
        "branch_id": "panic_overreaction",
        "label": "Panic Overreaction",
        "summary": "The market initially overprices downside risk before a slower reassessment begins.",
    },
    {
        "branch_id": "institutional_stabilization",
        "label": "Institutional Stabilization",
        "summary": "Institutions and policy communication help stabilize early volatility and narrow dispersion.",
    },
    {
        "branch_id": "policy_reversal_relief",
        "label": "Policy Reversal Relief",
        "summary": "Participants increasingly price in relief, moderation, or a less severe downstream path.",
    },
    {
        "branch_id": "misinformation_amplification",
        "label": "Misinformation Amplification",
        "summary": "Narrative distortion and incomplete information widen uncertainty before clarity returns.",
    },
]


def build_market_timeline(
    num_rounds: int,
    events_per_round: list,
    topic: str = "",
    event_type: str = "general",
) -> list:
    """
    Create structured round metadata for the simulation loop.

    The first five rounds map to the explicit market propagation stages.
    If fewer rounds are requested, the timeline is truncated.
    """
    timeline = []

    for idx in range(num_rounds):
        template = deepcopy(MARKET_TIMELINE_STAGES[min(idx, len(MARKET_TIMELINE_STAGES) - 1)])
        event_text = (
            events_per_round[idx]
            if idx < len(events_per_round) and events_per_round[idx]
            else "Situation continues to develop."
        )

        template["event"] = event_text
        template["event_type"] = event_type
        template["topic"] = topic
        template["context_prompt"] = (
            f"Market timeline stage: {template['label']} ({template['time_window']}). "
            f"Focus for this round: {template['focus']} "
            f"Scenario type: {event_type.replace('_', ' ')}."
        )
        timeline.append(template)

    return timeline


def get_branch_narratives(num_branches: int) -> list:
    """Return a deterministic sequence of branch narrative metadata."""
    narratives = []
    if num_branches <= 0:
        return narratives

    for idx in range(num_branches):
        template = deepcopy(BRANCH_NARRATIVE_TEMPLATES[idx % len(BRANCH_NARRATIVE_TEMPLATES)])
        template["sequence_number"] = idx + 1
        narratives.append(template)

    return narratives
