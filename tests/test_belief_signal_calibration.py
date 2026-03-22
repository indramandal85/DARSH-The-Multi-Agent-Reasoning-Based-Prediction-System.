from agents.belief_state import _calibrate_likelihoods_from_evidence


def test_positive_policy_signal_boosts_optimistic_over_cautious():
    base = {
        "panic": 0.16,
        "cautious": 0.53,
        "optimistic": 0.20,
        "divided": 0.11,
    }
    evidence = (
        "Government announces a surprise corporate tax cut and pro-growth stimulus. "
        "Markets rally, foreign allocation increased, and the improved outlook supports recovery."
    )

    calibrated = _calibrate_likelihoods_from_evidence(
        evidence=evidence,
        likelihoods=base,
        agent_personality="rational market participant"
    )

    assert calibrated["optimistic"] > calibrated["cautious"]
    assert calibrated["optimistic"] > base["optimistic"]


def test_clear_shock_signal_boosts_panic():
    base = {
        "panic": 0.18,
        "cautious": 0.46,
        "optimistic": 0.22,
        "divided": 0.14,
    }
    evidence = (
        "Nationwide lockdown triggers crash fears, severe stress, lower circuits, "
        "and a rush toward defensive positioning."
    )

    calibrated = _calibrate_likelihoods_from_evidence(
        evidence=evidence,
        likelihoods=base,
        agent_personality="emotional market participant"
    )

    assert calibrated["panic"] > calibrated["cautious"]
    assert calibrated["panic"] > base["panic"]
