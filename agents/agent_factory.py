# agents/agent_factory.py
#
# AGENT FACTORY
#
# Creates a diverse population of agents for simulation.
# The simulator in Module 5 calls create_agent_population()
# with a count and topic, and gets back a ready-to-run list of agents.
#
# Why a factory? Because in Module 5 you'll run simulations with
# 20-50 agents. Creating each one manually would be impractical.
# The factory handles name generation, type distribution, and
# background variation automatically.

import sys
import os
import random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.rational_agent import RationalAgent
from agents.emotional_agent import EmotionalAgent
from agents.tribal_agent import TribalAgent
from agents.contrarian_agent import ContrarianAgent
from agents.institutional_agent import InstitutionalAgent
from agents.market_roles import (
    assign_roles_to_agent_types,
    build_market_role_background,
    get_market_role_definition,
)
from agents.semantic_memory import create_shared_chroma_client


# ── AGENT TEMPLATES ───────────────────────────────────────────────────────────
# Pre-defined diverse backgrounds for realistic population generation.
# Module 5 will use the LLM to generate these dynamically.
# For now, we use these templates for speed.

BACKGROUNDS = [
    ("Arjun Mehta",      "software engineer from Bangalore, owns mutual funds"),
    ("Priya Nair",       "economics postgrad from Kerala, has student loans"),
    ("Vikram Singh",     "retired army officer from Delhi, fixed deposits only"),
    ("Sunita Krishnan",  "small business owner from Chennai, 3 bank loans"),
    ("Rahul Agarwal",    "MBA student from Mumbai, learning to invest"),
    ("Deepa Pillai",     "school teacher from Kochi, government employee"),
    ("Amit Sharma",      "startup founder from Pune, equity-heavy portfolio"),
    ("Kavitha Reddy",    "nurse from Hyderabad, supports family of 6"),
    ("Sanjay Patel",     "textile merchant from Surat, imports from China"),
    ("Meera Iyer",       "journalist from Bangalore, covers financial news"),
    ("HDFC Bank",        "major private sector bank, 8 crore customers"),
    ("SBI Branch",       "public sector bank, serves rural and urban India"),
    ("TechCorp India",   "mid-size IT company, 2000 employees, USD revenues"),
    ("Farmers Union",    "agricultural cooperative, 50000 members, crop loans"),
]

INSTITUTION_BACKGROUNDS = [
    ("Axis Treasury Desk", "private bank treasury desk managing rates, liquidity, and customer book risk"),
    ("SBI Economic Cell", "public sector bank desk tracking policy transmission across broad customer segments"),
    ("Finance Ministry Unit", "economic affairs team reviewing growth, fiscal optics, and sector spillovers"),
    ("SEBI Policy Desk", "market regulator policy group monitoring stability, flows, and compliance"),
    ("Reliance Treasury", "large corporate treasury managing funding costs, FX exposure, and market risk"),
    ("Bharat Defence Systems", "defence-sector operating firm monitoring policy, procurement, and execution risks"),
    ("Nova FMCG India", "consumer goods operating firm focused on demand, margin, and distribution trends"),
    ("Zenith Tech Services", "technology-sector treasury and planning team tracking global demand and currency risk"),
]

TRIBAL_GROUPS = [
    "middle class urban professionals",
    "rural agricultural community",
    "startup and tech ecosystem",
    "government employees and pensioners",
    "opposition supporters",
    "ruling party supporters",
    "student and youth community",
    "senior citizens and retirees",
]

# Distribution of agent types in a realistic population
# Emotional agents are most common (like real social media)
# Institutional agents are least common but most influential
TYPE_DISTRIBUTION = {
    "rational":      0.20,   # 20% — analysts, educated professionals
    "emotional":     0.35,   # 35% — most common, social media driven
    "tribal":        0.25,   # 25% — group-identity driven
    "contrarian":    0.10,   # 10% — skeptics and critics
    "institutional": 0.10,   # 10% — banks, corps, bodies
}


def create_agent(agent_id: str, agent_type: str,
                 name: str, background: str, topic: str,
                 chroma_client=None, simulation_id: str = "default",
                 institution_type_override: str = None) -> object:
    """
    Create one agent of the specified type.

    agent_id   : unique ID string e.g. "agent_007"
    agent_type : "rational", "emotional", "tribal", "contrarian", "institutional"
    name       : agent's name
    background : agent's background description
    topic      : what the simulation is about (shapes personality)
    """

    # Personality is derived from type + topic
    personalities = {
        "rational": (
            f"analytical and evidence-based, carefully evaluates {topic}, "
            "slow to change opinion without data, does not panic"
        ),
        "emotional": (
            f"reacts strongly to {topic} news, gut-feeling driven, "
            "quick to share opinions, influenced by alarming headlines"
        ),
        "tribal": (
            f"interprets {topic} through group identity lens, "
            "loyal to community consensus, skeptical of outside views"
        ),
        "contrarian": (
            f"skeptical of mainstream {topic} narratives, "
            "looks for what others are missing, challenges consensus"
        ),
        "institutional": (
            f"approaches {topic} through risk management and procedure, "
            "formal communication, bound by regulatory obligations"
        ),
    }

    personality = personalities.get(agent_type, "balanced and thoughtful")

    if agent_type == "rational":
        return RationalAgent(agent_id, name, personality, background,
                            chroma_client=chroma_client, simulation_id=simulation_id)

    elif agent_type == "emotional":
        return EmotionalAgent(agent_id, name, personality, background,
                             chroma_client=chroma_client, simulation_id=simulation_id)

    elif agent_type == "tribal":
        tribe = random.choice(TRIBAL_GROUPS)
        return TribalAgent(agent_id, name, personality, background, tribe=tribe,
                          chroma_client=chroma_client, simulation_id=simulation_id)

    elif agent_type == "contrarian":
        return ContrarianAgent(agent_id, name, personality, background,
                              chroma_client=chroma_client, simulation_id=simulation_id)

    elif agent_type == "institutional":
        inst_type = institution_type_override or (
            "financial" if any(
                w in background.lower() for w in ["bank", "corp", "union", "company", "treasury", "fund"]
            ) else "government"
        )
        return InstitutionalAgent(agent_id, name, personality, background,
                                 institution_type=inst_type,
                                 chroma_client=chroma_client, simulation_id=simulation_id)

    else:
        return RationalAgent(agent_id, name, personality, background,
                            chroma_client=chroma_client, simulation_id=simulation_id)


def _calculate_type_counts(count: int) -> dict:
    """Preserve the original cognition distribution across the population."""
    exact_counts = {
        agent_type: count * weight
        for agent_type, weight in TYPE_DISTRIBUTION.items()
    }
    type_counts = {
        agent_type: int(exact)
        for agent_type, exact in exact_counts.items()
    }

    assigned = sum(type_counts.values())
    remaining = count - assigned
    remainders = sorted(
        [
            (
                exact_counts[agent_type] - type_counts[agent_type],
                agent_type
            )
            for agent_type in TYPE_DISTRIBUTION
        ],
        reverse=True
    )

    for _, agent_type in remainders[:remaining] if remaining > 0 else []:
        type_counts[agent_type] += 1

    return {agent_type: amount for agent_type, amount in type_counts.items() if amount > 0}


def _create_shared_memory_client(use_semantic_memory: bool):
    chroma_client = None
    if use_semantic_memory:
        try:
            chroma_client = create_shared_chroma_client()
            print("  Semantic memory: enabled (ChromaDB)")
        except Exception as e:
            print(f"  Semantic memory: disabled ({e})")
            chroma_client = None
    return chroma_client


def _get_background_pools():
    human_backgrounds = [
        item for item in BACKGROUNDS
        if not any(keyword in item[0].lower() for keyword in ["bank", "branch", "corp", "union", "india"])
    ]
    institutional_backgrounds = INSTITUTION_BACKGROUNDS.copy()
    return human_backgrounds, institutional_backgrounds


def _next_background(role_key: str, index: int, human_backgrounds: list, institutional_backgrounds: list):
    role = get_market_role_definition(role_key)
    if role["category"] == "institution":
        pool = institutional_backgrounds or human_backgrounds
    else:
        pool = human_backgrounds or institutional_backgrounds

    name, background = pool[index % len(pool)]
    suffix = "" if index < len(pool) else f" {index // len(pool) + 1}"
    return f"{name}{suffix}", background


def create_market_agent_population(
    count: int,
    topic: str,
    event_type: str = "general",
    use_semantic_memory: bool = True,
    simulation_id: str = "default"
) -> list:
    """
    Create a market-aware agent population by pairing cognition style
    with participant role.
    """
    agents = []
    type_counts = _calculate_type_counts(count)

    print(f"\n  Creating {count} market agents for topic: '{topic}'")
    print("  Cognition distribution target:")
    for agent_type, amount in type_counts.items():
        print(f"    {agent_type:15} : {amount}")

    role_assignments = assign_roles_to_agent_types(type_counts, event_type)
    role_counts = {}
    for role_key, _ in role_assignments:
        role_counts[role_key] = role_counts.get(role_key, 0) + 1

    print(f"  Market role mix ({event_type}):")
    for role_key, amount in sorted(role_counts.items(), key=lambda item: item[0]):
        print(f"    {role_key:22} : {amount}")

    chroma_client = _create_shared_memory_client(use_semantic_memory)
    human_backgrounds, institutional_backgrounds = _get_background_pools()
    random.shuffle(human_backgrounds)
    random.shuffle(institutional_backgrounds)

    for index, (role_key, agent_type) in enumerate(role_assignments):
        name, background = _next_background(
            role_key, index, human_backgrounds, institutional_backgrounds
        )
        role_meta = get_market_role_definition(role_key)
        role_overlay = build_market_role_background(role_key, event_type, topic)
        institution_override = None
        if role_key in {"PRIVATE_BANK_TREASURY", "PSU_BANK_DESK"}:
            institution_override = "financial"
        elif role_key in {"REGULATOR_POLICY_DESK", "MINISTRY_POLICY_TEAM"}:
            institution_override = "government"

        agent = create_agent(
            agent_id=f"agent_{index + 1:03d}",
            agent_type=agent_type,
            name=name,
            background=f"{background}. {role_overlay}",
            topic=topic,
            chroma_client=chroma_client,
            simulation_id=simulation_id,
            institution_type_override=institution_override
        )

        agent.market_role = role_key
        agent.market_role_label = role_meta["label"]
        agent.market_role_constraints = list(role_meta["constraints"])
        agent.market_role_sources = list(role_meta["information_sources"])
        agent.reaction_speed = role_meta["reaction_speed"]
        agent.personality = (
            f"{agent.personality}. You are currently acting as a "
            f"{role_meta['label'].lower()} with {role_meta['reaction_speed']} reaction speed."
        )
        agents.append(agent)

    print(f"  Created {len(agents)} market-aware agents successfully.")
    return agents


def create_agent_population(
    count: int,
    topic: str,
    event_type: str = "general",
    use_semantic_memory: bool = True,
    simulation_id: str = "default",
    use_market_roles: bool = True
    ) -> list:
    """
    Create a diverse population of agents for simulation.

    count : total number of agents to create
    topic : what the simulation is about
            e.g. "RBI interest rate hike and economic impact"

    Returns: list of agent objects ready for simulation
    """

    if use_market_roles:
        return create_market_agent_population(
            count=count,
            topic=topic,
            event_type=event_type,
            use_semantic_memory=use_semantic_memory,
            simulation_id=simulation_id
        )

    agents = []
    type_counts = _calculate_type_counts(count)

    print(f"\n  Creating {count} agents for topic: '{topic}'")
    print("  Type distribution:")
    for t, n in type_counts.items():
        print(f"    {t:15} : {n}")
    
    chroma_client = _create_shared_memory_client(use_semantic_memory)

    # Shuffle backgrounds for variety
    backgrounds = BACKGROUNDS.copy()
    random.shuffle(backgrounds)

    agent_index = 0
    for agent_type, type_count in type_counts.items():
        for i in range(type_count):
            if agent_index < len(backgrounds):
                name, background = backgrounds[agent_index]
            else:
                # Cycle through backgrounds if we need more agents than templates
                name, background = backgrounds[agent_index % len(backgrounds)]
                name = f"{name} Jr."  # differentiate duplicates

            agent_id = f"agent_{agent_index + 1:03d}"
            agent = agent = create_agent(
                agent_id, agent_type, name, background, topic,
                chroma_client=chroma_client,
                simulation_id=simulation_id
            )
            agents.append(agent)
            agent_index += 1

    print(f"  Created {len(agents)} agents successfully.")
    return agents
