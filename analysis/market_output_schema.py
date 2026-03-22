from dataclasses import dataclass, field


MARKET_REGIMES = [
    "risk_on",
    "risk_off",
    "policy_shock",
    "relief_rally",
    "uncertainty_hold",
    "sector_rotation",
]

SECTOR_DIRECTIONS = [
    "strong_positive",
    "positive",
    "neutral",
    "negative",
    "strong_negative",
]

VOLATILITY_LEVELS = ["low", "moderate", "high", "extreme"]

INDIA_SECTORS = [
    "banking_private",
    "banking_psu",
    "nbfc",
    "insurance",
    "real_estate",
    "it_services",
    "fmcg",
    "pharma",
    "auto",
    "energy_oil_gas",
    "metals_mining",
    "infrastructure",
    "telecom",
    "defence",
    "fintech",
    "chemicals",
    "consumption",
    "capital_goods",
    "aviation",
]


@dataclass
class SectorImpact:
    sector: str
    direction: str
    confidence: float
    reasoning: str
    representative_stocks: list = field(default_factory=list)


@dataclass
class MarketImpactOutput:
    market_regime: str
    regime_confidence: float
    sector_impacts: dict
    volatility_expectation: str
    vix_direction: str
    likely_laggards: list = field(default_factory=list)
    likely_resilient: list = field(default_factory=list)
    likely_beneficiaries: list = field(default_factory=list)
    triggers_that_strengthen: list = field(default_factory=list)
    triggers_that_weaken: list = field(default_factory=list)
    monitoring_signals: list = field(default_factory=list)
    retail_narrative: str = ""
    institutional_narrative: str = ""
    media_narrative: str = ""
    expected_price_discovery_hours: int = 24
    second_order_effects: list = field(default_factory=list)
    behavioral_distribution: dict = field(default_factory=dict)
    branch_count: int = 0
    simulation_confidence: float = 0.0
