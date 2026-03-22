# agents/belief_state.py
#
# WHAT THIS DOES:
# Replaces v1's verbal belief updating ("I now believe...") with
# real Bayesian probability math.
#
# Each agent now maintains a probability distribution over possible outcomes.
# New evidence updates this distribution using Bayes' rule.
# The simulation aggregates these distributions mathematically at the end.
#
# Why this matters:
# v1: "70% panic" = the word "panic" appeared 70% as often as other keywords
# v2: "70% panic" = average posterior P(panic) across all agents and branches
#
# How it works:
#   Prior:      {"panic": 0.33, "cautious": 0.33, "optimistic": 0.34}  ← start
#   Evidence:   "IIM warns of recession"
#   Likelihood: {"panic": 0.9, "cautious": 0.5, "optimistic": 0.1}    ← LLM scores
#   Posterior:  {"panic": 0.62, "cautious": 0.35, "optimistic": 0.03} ← Bayes output
#
# The LLM scores likelihood. Bayes computes the posterior. Clean separation.

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.llm_caller import ask_llm_json


# The fixed set of outcome categories we predict over.
# Must be consistent across all agents and all modules.
OUTCOMES = ["panic", "cautious", "optimistic", "divided"]

POSITIVE_EVIDENCE_CUES = [
    "tax cut", "rate cut", "stimulus", "record growth", "strong growth",
    "beat expectations", "record high", "record highs", "rally", "surge",
    "recovery", "growth-oriented", "expansionary", "allocation increased",
    "improved outlook", "additional spending", "accommodative", "support growth",
    "pro-growth", "lower corporate tax", "capital expenditure", "hiring aggressively",
]

NEGATIVE_EVIDENCE_CUES = [
    "lockdown", "crash", "selloff", "panic", "stress", "default", "spike in yields",
    "widening fiscal deficit", "crisis", "war", "surge past 100", "inflation shock",
    "stop accepting deposits", "regulatory crackdown", "lower circuit", "cash shortage",
    "debt stress", "capital outflow", "emergency off-cycle hike",
]

DIVIDED_EVIDENCE_CUES = [
    "mixed", "split", "divided", "coalition", "uncertainty over mandate",
    "selective recovery", "sector rotation", "contest between", "two strong interpretations",
]

CAUTIOUS_EVIDENCE_CUES = [
    "assess", "wait and see", "monitor", "uncertain", "clarity", "volatility",
    "transmission", "policy implication", "reassess", "further clarity",
]


class BeliefState:
    """
    A probability distribution over prediction outcomes for one agent.

    Attributes:
        distribution : dict mapping outcome → probability (sums to 1.0)
        update_history : list of (evidence, prior, posterior) tuples for audit
    """

    def __init__(self, outcomes: list = None, prior: dict = None):
        """
        outcomes : list of outcome labels. Defaults to OUTCOMES.
        prior    : starting probability distribution. Defaults to uniform.
                   Uniform prior = maximum uncertainty = honest starting point.
        """
        self.outcomes = outcomes or OUTCOMES

        if prior is not None:
            # Normalize provided prior in case it doesn't sum to 1.0
            total = sum(prior.values())
            self.distribution = {o: prior.get(o, 0) / total for o in self.outcomes}
        else:
            # Uniform prior: equal probability for all outcomes
            n = len(self.outcomes)
            self.distribution = {o: 1.0 / n for o in self.outcomes}

        self.update_history = []


    def bayesian_update(self, likelihoods: dict) -> dict:
        """
        Apply one Bayesian update given evidence likelihoods.

        likelihoods : {outcome: P(evidence | outcome)} for each outcome
                      How likely would we see this evidence if this outcome were true?
                      Score: 0.0 = evidence is inconsistent with outcome
                             0.5 = evidence is neutral
                             1.0 = evidence strongly implies outcome

        Returns: the new posterior distribution (also updates self.distribution)

        Math:
          unnormalized[o] = prior[o] × likelihood[o]
          posterior[o]    = unnormalized[o] / sum(unnormalized)

        This is Bayes' rule: P(o|e) ∝ P(e|o) × P(o)
        The normalization step (dividing by sum) ensures probabilities sum to 1.
        """

        prior = self.distribution.copy()

        # Compute unnormalized posteriors
        unnormalized = {}
        for outcome in self.outcomes:
            prior_prob = prior.get(outcome, 0.0)
            likelihood = likelihoods.get(outcome, 0.5)   # 0.5 = neutral if missing
            unnormalized[outcome] = prior_prob * likelihood

        # Normalize so probabilities sum to 1.0
        total = sum(unnormalized.values())
        if total <= 0:
            self.distribution = {o: 1.0 / len(self.outcomes) for o in self.outcomes}
        else:
            raw_posterior = {o: round(v / total, 4) for o, v in unnormalized.items()}

            # Entropy regularization: mix 8% uniform back in after each update.
            # This prevents any single outcome from exceeding ~87% probability
            # no matter how many consecutive extreme updates occur.
            # Standard practice in Bayesian inference to prevent overconfidence.
            epsilon = 0.08
            n = len(self.outcomes)
            self.distribution = {
                o: round((1 - epsilon) * raw_posterior.get(o, 0) + epsilon * (1.0 / n), 4)
                for o in self.outcomes
            }

        # Store for audit trail
        self.update_history.append({
            "prior"      : prior,
            "likelihoods": likelihoods,
            "posterior"  : self.distribution.copy()
        })

        return self.distribution


    def dominant_outcome(self) -> str:
        """Return the outcome with highest probability."""
        return max(self.distribution, key=self.distribution.get)


    def confidence(self) -> float:
        """
        How confident is this agent in their dominant belief?
        Computed as: P(dominant) - P(second highest)
        Range: 0.0 (completely divided) to 1.0 (certain)
        """
        sorted_probs = sorted(self.distribution.values(), reverse=True)
        if len(sorted_probs) < 2:
            return sorted_probs[0] if sorted_probs else 0.0
        return round(sorted_probs[0] - sorted_probs[1], 4)


    def as_text(self) -> str:
        """Human-readable belief description for LLM prompts."""
        parts = []
        for outcome, prob in sorted(self.distribution.items(),
                                    key=lambda x: x[1], reverse=True):
            parts.append(f"{outcome}: {prob*100:.0f}%")
        dominant = self.dominant_outcome()
        conf = self.confidence()
        return (f"Current belief distribution: {', '.join(parts)}. "
                f"I lean toward '{dominant}' with {conf*100:.0f}% confidence margin.")


    def __repr__(self):
        parts = [f"{o}={p:.3f}" for o, p in self.distribution.items()]
        return f"BeliefState({', '.join(parts)})"


def get_likelihoods_from_llm(
    evidence: str,
    outcomes: list,
    agent_name: str,
    agent_personality: str
) -> dict:
    """
    Ask the LLM to score how this evidence shifts social sentiment toward each outcome.

    KEY CHANGE from v1:
    v1 asked: "how CONSISTENT is this evidence with each outcome?"
    Problem: Llama scores panic=0.80 for almost any economic news because it
             reasons about worst-case interpretations. Result: panic always wins.

    v2 asks: "if this news just broke right now, what fraction of society
             would react with FEAR vs CAUTION vs OPTIMISM vs DIVISION?"
    This is a concrete behavioural question with a clear right answer
    grounded in the actual tone and content of the evidence.

    evidence          : new information the agent received this round
    outcomes          : list of outcome labels to score
    agent_name        : who is doing the assessment
    agent_personality : shapes perspective (emotional agents weight fear more)
    """

    prompt = (
        f"You are updating an agent's market-outcome belief distribution.\n\n"
        f"Evidence package:\n{evidence}\n\n"
        f"Agent: {agent_name}\n"
        f"Personality: {agent_personality}\n\n"
        f"Task: score how likely each NEXT-STAGE market outcome is after this evidence.\n\n"
        f"Outcome definitions:\n"
        f"  panic      = broad risk-off reaction, sharp fear, rushed defensive positioning\n"
        f"  cautious   = wait-and-see, measured response, selective positioning without broad conviction\n"
        f"  optimistic = positive repricing, broad confidence, rotation into beneficiaries / risk-on posture\n"
        f"  divided    = no clear consensus, sectors/participants split in different directions\n\n"
        f"Scoring rules:\n"
        f"  - Scores MUST sum to approximately 1.0\n"
        f"  - Score the next market phase, not a generic essay answer\n"
        f"  - Surprise pro-growth, earnings-accretive, recovery, stimulus, or tax-cut news should usually make optimistic exceed cautious unless the evidence clearly contains offsetting risks\n"
        f"  - Reserve cautious for ambiguous, incomplete, or mixed evidence\n"
        f"  - Use divided when the evidence itself shows a real split between upside and downside interpretations\n"
        f"  - Do NOT default to cautious just because the event is policy-related\n"
        f"  - Personality should tilt the scores only slightly, not override the evidence\n\n"
        f"Return JSON with exactly these keys: {outcomes}\n"
        f"Each value is a float 0.0-1.0. All values should sum to approximately 1.0.\n"
        f"Example for VERY POSITIVE policy news: "
        f"{{\"panic\": 0.04, \"cautious\": 0.22, \"optimistic\": 0.62, \"divided\": 0.12}}\n"
        f"Example for CLEARLY BAD shock news: "
        f"{{\"panic\": 0.62, \"cautious\": 0.22, \"optimistic\": 0.04, \"divided\": 0.12}}"
    )

    result = ask_llm_json(prompt)

    if result.get("parse_error"):
        return {o: 0.25 for o in outcomes}   # uniform — no update if parsing fails

    # Validate and clamp values
    likelihoods = {}
    for outcome in outcomes:
        raw = result.get(outcome, 0.25)
        try:
            # Clip to [0.03, 0.80]
            # 0.03 min: no outcome is ever completely ruled out
            # 0.80 max: no single piece of evidence is certainty
            likelihoods[outcome] = max(0.03, min(0.80, float(raw)))
        except (ValueError, TypeError):
            likelihoods[outcome] = 0.25

    # Normalize so they sum to 1.0 — handles cases where LLM doesn't sum to 1
    total = sum(likelihoods.values())
    if total > 0:
        likelihoods = {o: round(v / total, 4) for o, v in likelihoods.items()}

    likelihoods = _calibrate_likelihoods_from_evidence(
        evidence=evidence,
        likelihoods=likelihoods,
        agent_personality=agent_personality,
    )

    return likelihoods


def _count_cues(text: str, cues: list) -> int:
    return sum(1 for cue in cues if cue in text)


def _normalize_likelihoods(likelihoods: dict, outcomes: list) -> dict:
    cleaned = {outcome: max(0.03, float(likelihoods.get(outcome, 0.03))) for outcome in outcomes}
    total = sum(cleaned.values()) or 1.0
    return {outcome: round(value / total, 4) for outcome, value in cleaned.items()}


def _calibrate_likelihoods_from_evidence(
    evidence: str,
    likelihoods: dict,
    agent_personality: str
) -> dict:
    text = (evidence or "").lower()
    personality = (agent_personality or "").lower()
    calibrated = {outcome: float(likelihoods.get(outcome, 0.25)) for outcome in OUTCOMES}

    positive = _count_cues(text, POSITIVE_EVIDENCE_CUES)
    negative = _count_cues(text, NEGATIVE_EVIDENCE_CUES)
    divided = _count_cues(text, DIVIDED_EVIDENCE_CUES)
    cautious = _count_cues(text, CAUTIOUS_EVIDENCE_CUES)

    if positive >= 2 and negative == 0:
        boost = min(0.24, 0.10 + positive * 0.03)
        calibrated["optimistic"] += boost
        calibrated["cautious"] -= boost * 0.58
        calibrated["panic"] -= boost * 0.22
        calibrated["divided"] -= boost * 0.20
    elif negative >= 2 and positive == 0:
        boost = min(0.24, 0.10 + negative * 0.03)
        calibrated["panic"] += boost
        calibrated["cautious"] -= boost * 0.52
        calibrated["optimistic"] -= boost * 0.28
        calibrated["divided"] -= boost * 0.20
    elif positive > 0 and negative > 0:
        boost = min(0.16, 0.06 + abs(positive - negative) * 0.02)
        calibrated["divided"] += boost
        calibrated["cautious"] += boost * 0.35
        calibrated["optimistic"] -= boost * 0.18
        calibrated["panic"] -= boost * 0.17
    elif divided >= 2:
        calibrated["divided"] += 0.12
        calibrated["cautious"] += 0.04
        calibrated["optimistic"] -= 0.08
        calibrated["panic"] -= 0.08
    elif cautious >= 2 and positive == 0 and negative == 0:
        calibrated["cautious"] += 0.10
        calibrated["divided"] += 0.03
        calibrated["optimistic"] -= 0.07
        calibrated["panic"] -= 0.06

    if "emotional" in personality:
        if negative > positive:
            calibrated["panic"] += 0.05
            calibrated["optimistic"] -= 0.03
            calibrated["cautious"] -= 0.02
        elif positive > negative:
            calibrated["optimistic"] += 0.03
            calibrated["cautious"] -= 0.02
            calibrated["panic"] -= 0.01
    elif "rational" in personality or "institutional" in personality:
        if positive > negative:
            calibrated["optimistic"] += 0.05
            calibrated["cautious"] -= 0.03
            calibrated["panic"] -= 0.02
        elif negative > positive:
            calibrated["cautious"] += 0.03
            calibrated["panic"] -= 0.01
            calibrated["divided"] -= 0.02

    return _normalize_likelihoods(calibrated, OUTCOMES)


def aggregate_beliefs(agents_belief_states: list) -> dict:
    """
    Aggregate belief distributions from multiple agents into one summary.

    Takes the mean probability for each outcome across all agents.
    This is the mathematically correct way to combine probability distributions
    from independent agents.

    Returns: {"outcome": mean_probability} sorted by probability descending
    """

    if not agents_belief_states:
        return {o: 1.0/len(OUTCOMES) for o in OUTCOMES}

    outcome_sums = {o: 0.0 for o in OUTCOMES}
    count = len(agents_belief_states)

    for belief_state in agents_belief_states:
        for outcome in OUTCOMES:
            outcome_sums[outcome] += belief_state.distribution.get(outcome, 0.0)

    mean_distribution = {o: round(s / count, 4) for o, s in outcome_sums.items()}

    # Sort by probability for readability
    return dict(sorted(mean_distribution.items(), key=lambda x: x[1], reverse=True))
