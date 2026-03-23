import json
import os
from datetime import datetime


REGISTRY_PATH = "data/graph_artifact_registry.json"


def _empty_registry() -> dict:
    return {"graphs": {}}


def _normalize_path(path: str) -> str:
    normalized = os.path.normpath((path or "").strip())
    if not normalized or normalized == ".":
        return ""
    return normalized.replace("\\", "/")


def _unique(values: list) -> list:
    seen = set()
    ordered = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return ordered


def _load_registry() -> dict:
    if not os.path.exists(REGISTRY_PATH):
        return _empty_registry()

    try:
        with open(REGISTRY_PATH, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except Exception:
        return _empty_registry()

    if not isinstance(data, dict):
        return _empty_registry()

    graphs = data.get("graphs")
    if not isinstance(graphs, dict):
        return _empty_registry()

    return {"graphs": graphs}


def _save_registry(registry: dict):
    os.makedirs(os.path.dirname(REGISTRY_PATH), exist_ok=True)
    with open(REGISTRY_PATH, "w", encoding="utf-8") as handle:
        json.dump(registry, handle, indent=2, ensure_ascii=False)


def ensure_graph_registry_entry(graph_name: str) -> dict:
    registry = _load_registry()
    entry = registry["graphs"].get(graph_name, {})

    entry["graph_name"] = graph_name
    entry["graph_path"] = f"data/graphs/{graph_name}.json"
    entry["causal_path"] = f"data/graphs/{graph_name}_causal.json"
    entry["report_paths"] = _unique([_normalize_path(path) for path in entry.get("report_paths", []) if _normalize_path(path)])
    entry["memory_namespaces"] = _unique([value for value in entry.get("memory_namespaces", []) if value])
    entry["simulation_ids"] = _unique([value for value in entry.get("simulation_ids", []) if value])
    entry["db_paths"] = _unique([_normalize_path(path) for path in entry.get("db_paths", []) if _normalize_path(path)])
    entry["topics"] = _unique([value for value in entry.get("topics", []) if value])
    entry["updated_at"] = datetime.utcnow().isoformat()

    registry["graphs"][graph_name] = entry
    _save_registry(registry)
    return entry


def attach_graph_artifacts(
    graph_name: str,
    *,
    report_paths: list | None = None,
    memory_namespaces: list | None = None,
    simulation_ids: list | None = None,
    db_paths: list | None = None,
    topic: str | None = None,
) -> dict:
    registry = _load_registry()
    entry = registry["graphs"].get(graph_name, {})

    entry["graph_name"] = graph_name
    entry["graph_path"] = f"data/graphs/{graph_name}.json"
    entry["causal_path"] = f"data/graphs/{graph_name}_causal.json"

    merged_reports = entry.get("report_paths", []) + [
        _normalize_path(path) for path in (report_paths or []) if _normalize_path(path)
    ]
    merged_memories = entry.get("memory_namespaces", []) + [value for value in (memory_namespaces or []) if value]
    merged_sim_ids = entry.get("simulation_ids", []) + [value for value in (simulation_ids or []) if value]
    merged_db_paths = entry.get("db_paths", []) + [
        _normalize_path(path) for path in (db_paths or []) if _normalize_path(path)
    ]
    merged_topics = entry.get("topics", []) + ([topic] if topic else [])

    entry["report_paths"] = _unique(merged_reports)
    entry["memory_namespaces"] = _unique(merged_memories)
    entry["simulation_ids"] = _unique(merged_sim_ids)
    entry["db_paths"] = _unique(merged_db_paths)
    entry["topics"] = _unique([value for value in merged_topics if value])
    entry["updated_at"] = datetime.utcnow().isoformat()

    registry["graphs"][graph_name] = entry
    _save_registry(registry)
    return entry


def get_graph_artifact_entry(graph_name: str) -> dict | None:
    registry = _load_registry()
    return registry["graphs"].get(graph_name)


def pop_graph_artifact_entry(graph_name: str) -> dict | None:
    registry = _load_registry()
    entry = registry["graphs"].pop(graph_name, None)
    _save_registry(registry)
    return entry
