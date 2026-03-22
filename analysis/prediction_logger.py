# analysis/prediction_logger.py
#
# Phase 7 — persistent prediction logging and calibration summary.

import json
import os
from datetime import datetime


PREDICTION_LOG_PATH = "data/reports/prediction_log.json"
TRACK_RECORD_TABLE_PATH = "data/reports/track_record_table.md"

OUTCOME_RESOLUTION_PROTOCOLS = {
    "monetary_policy": {"window_hours": 48, "basis": "close_to_close"},
    "fiscal_policy": {"window_hours": 72, "basis": "close_to_close"},
    "global_shock": {"window_hours": 72, "basis": "close_to_close"},
    "regulatory_action": {"window_hours": 24, "basis": "intraday_close"},
    "macro_data": {"window_hours": 24, "basis": "same_day_close"},
    "general": {"window_hours": 48, "basis": "close_to_close"},
    "rbi_rate_hike": {"window_hours": 48, "basis": "close_to_close"},
    "budget_fiscal_expansion": {"window_hours": 72, "basis": "close_to_close"},
    "oil_price_spike": {"window_hours": 72, "basis": "close_to_close"},
}


def _ensure_reports_dir():
    os.makedirs(os.path.dirname(PREDICTION_LOG_PATH), exist_ok=True)


def _load_prediction_history() -> list:
    if not os.path.exists(PREDICTION_LOG_PATH):
        return []
    with open(PREDICTION_LOG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_prediction_history(history: list):
    _ensure_reports_dir()
    with open(PREDICTION_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def _normalize_probs(predicted_probs: dict) -> dict:
    cleaned = {}
    for key, value in (predicted_probs or {}).items():
        try:
            cleaned[key] = float(value)
        except (TypeError, ValueError):
            cleaned[key] = 0.0

    total = sum(cleaned.values()) or 1.0
    if any(value > 1.0 for value in cleaned.values()):
        return {key: round(value / total, 4) for key, value in cleaned.items()}
    return {key: round(value / total, 4) for key, value in cleaned.items()}


def _compute_sector_direction_accuracy(predicted_sector_impacts: dict, actual_sector_moves: dict) -> dict:
    if not predicted_sector_impacts or not actual_sector_moves:
        return {"available": False, "scored": 0, "correct": 0, "accuracy": None}

    scored = 0
    correct = 0
    details = []

    for sector, actual_direction in actual_sector_moves.items():
        predicted = predicted_sector_impacts.get(sector)
        if not predicted:
            continue

        predicted_direction = predicted.get("direction", "neutral")
        scored += 1
        is_correct = predicted_direction == actual_direction
        if is_correct:
            correct += 1

        details.append({
            "sector": sector,
            "predicted_direction": predicted_direction,
            "actual_direction": actual_direction,
            "correct": is_correct
        })

    return {
        "available": scored > 0,
        "scored": scored,
        "correct": correct,
        "accuracy": round(correct / scored, 3) if scored else None,
        "details": details
    }


def get_resolution_protocol(event_type: str) -> dict:
    return OUTCOME_RESOLUTION_PROTOCOLS.get(event_type, OUTCOME_RESOLUTION_PROTOCOLS["general"])


def log_prediction(
    event_id: str,
    topic: str,
    predicted_probs: dict,
    actual_outcome: str,
    dominant_predicted: str,
    brier_score: float,
    interpretation: str,
    correct: bool,
    event_type: str = "general",
    event_date: str = "",
    domain: str = "",
    model_version: str = "v3",
    phase_config: list = None,
    branch_count: int = 0,
    agent_count: int = 0,
    used_market_roles: bool = True,
    market_impact: dict = None,
    actual_sector_moves: dict = None,
) -> dict:
    """
    Persist one prediction evaluation event and regenerate the track record table.
    """
    normalized_probs = _normalize_probs(predicted_probs)
    resolution = get_resolution_protocol(event_type)
    sector_accuracy = _compute_sector_direction_accuracy(
        predicted_sector_impacts=(market_impact or {}).get("sector_impacts", {}),
        actual_sector_moves=actual_sector_moves or {}
    )

    history = _load_prediction_history()
    history = [entry for entry in history if entry.get("event_id") != event_id]

    entry = {
        "event_id": event_id,
        "topic": topic,
        "event_type": event_type,
        "event_date": event_date,
        "domain": domain,
        "timestamp_logged": datetime.now().isoformat(),
        "predicted_probs": normalized_probs,
        "dominant_predicted": dominant_predicted,
        "actual_outcome": actual_outcome,
        "brier_score": round(float(brier_score), 4),
        "interpretation": interpretation,
        "correct": bool(correct),
        "model_version": model_version,
        "phase_config": phase_config or ["phase1", "phase2", "phase4", "phase3", "phase6_partial", "phase7"],
        "branch_count": branch_count,
        "agent_count": agent_count,
        "used_market_roles": used_market_roles,
        "resolution_protocol": resolution,
        "sector_direction_accuracy": sector_accuracy,
        "market_regime": (market_impact or {}).get("market_regime"),
    }

    history.append(entry)
    history.sort(key=lambda item: (item.get("event_date", ""), item.get("timestamp_logged", "")), reverse=True)
    _save_prediction_history(history)
    build_track_record_table(history)
    return entry


def build_track_record_table(history: list = None) -> str:
    history = history if history is not None else _load_prediction_history()
    header = "| Event | Date | Predicted | Actual | Brier Score | Sector Accuracy |\n|---|---|---|---|---|---|"
    rows = []

    for entry in history:
        sector_acc = entry.get("sector_direction_accuracy", {})
        sector_text = (
            f"{round((sector_acc.get('accuracy') or 0) * 100)}%"
            if sector_acc.get("available") and sector_acc.get("accuracy") is not None
            else "N/A"
        )
        rows.append(
            f"| {entry.get('topic', entry.get('event_id', 'Unknown'))} | "
            f"{entry.get('event_date') or 'N/A'} | "
            f"{entry.get('dominant_predicted', 'unknown')} | "
            f"{entry.get('actual_outcome', 'unknown')} | "
            f"{entry.get('brier_score', 'N/A')} | "
            f"{sector_text} |"
        )

    markdown = header + ("\n" + "\n".join(rows) if rows else "\n| No logged predictions yet | - | - | - | - | - |")
    _ensure_reports_dir()
    with open(TRACK_RECORD_TABLE_PATH, "w", encoding="utf-8") as f:
        f.write(markdown)
    return markdown


def compute_track_record_summary() -> dict:
    history = _load_prediction_history()
    if not history:
        return {
            "total_predictions": 0,
            "correct_predictions": 0,
            "accuracy": 0.0,
            "average_brier_score": None,
            "sector_direction_accuracy": None,
            "resolution_protocols": {},
            "latest_predictions": [],
            "track_record_markdown": build_track_record_table(history),
        }

    total = len(history)
    correct = sum(1 for item in history if item.get("correct"))
    avg_brier = round(sum(item.get("brier_score", 1.0) for item in history) / total, 4)

    sector_entries = [
        item["sector_direction_accuracy"]["accuracy"]
        for item in history
        if item.get("sector_direction_accuracy", {}).get("available")
        and item.get("sector_direction_accuracy", {}).get("accuracy") is not None
    ]
    sector_accuracy = round(sum(sector_entries) / len(sector_entries), 4) if sector_entries else None

    protocols = {}
    for item in history:
        protocol = item.get("resolution_protocol", {})
        key = f"{protocol.get('window_hours', 'unknown')}h_{protocol.get('basis', 'unknown')}"
        protocols[key] = protocols.get(key, 0) + 1

    return {
        "total_predictions": total,
        "correct_predictions": correct,
        "accuracy": round(correct / total, 4),
        "average_brier_score": avg_brier,
        "sector_direction_accuracy": sector_accuracy,
        "resolution_protocols": protocols,
        "latest_predictions": history[:5],
        "track_record_markdown": build_track_record_table(history),
    }
