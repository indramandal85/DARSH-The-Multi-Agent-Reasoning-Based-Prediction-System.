import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "data" / "historical_events" / "index.json"
DOCS_DIR = ROOT / "data" / "historical_events" / "docs"


def test_historical_event_index_has_balanced_outcome_coverage():
    events = json.loads(INDEX_PATH.read_text(encoding="utf-8"))

    assert events, "Historical event index is empty"

    event_ids = [event["event_id"] for event in events]
    assert len(event_ids) == len(set(event_ids)), "Duplicate historical event IDs found"

    documented_outcomes = {event["actual_outcome"] for event in events}
    assert {"panic", "cautious", "optimistic", "divided"}.issubset(documented_outcomes), (
        "Historical events should cover panic, cautious, optimistic, and divided cases"
    )

    for event in events:
        document_path = DOCS_DIR / event["document_file"]
        assert document_path.exists(), f"Missing historical document: {event['document_file']}"
        word_count = len(document_path.read_text(encoding="utf-8").split())
        assert word_count >= 120, f"Historical document is too short for backtesting: {event['document_file']}"
