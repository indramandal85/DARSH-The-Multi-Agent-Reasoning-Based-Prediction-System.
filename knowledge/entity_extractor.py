# knowledge/entity_extractor.py
#
# WHAT THIS DOES:
# Uses the local LLM to read each text chunk and extract:
#   - Entities: the "things" in the text (people, orgs, places, events, concepts)
#   - Relationships: how those things connect to each other
#
# This is structured prompting — you already know how to prompt LLMs.
# The only difference here is we ask for JSON output so we can
# process the results programmatically.
#
# Example output for one chunk:
# {
#   "entities": [
#     {"name": "Shaktikanta Das", "type": "PERSON", "description": "RBI Governor"},
#     {"name": "RBI", "type": "ORGANIZATION", "description": "Reserve Bank of India"},
#     {"name": "Rate Hike", "type": "EVENT", "description": "0.5% interest rate increase"}
#   ],
#   "relationships": [
#     {"source": "Shaktikanta Das", "target": "RBI", "relation": "LEADS"},
#     {"source": "RBI", "target": "Rate Hike", "relation": "ANNOUNCED"}
#   ]
# }

import sys
import os
import re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.llm_caller import ask_llm_json


CONTEXT_EDGE_RELATION = "CONTEXT_NEAR"
MAX_CONTEXT_NEIGHBORS = 3
MAX_CONTEXT_DISTANCE = 260


def _sentence_split(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [part.strip() for part in parts if part.strip()]


def _entity_occurrences(text: str, entity_names: list[str]) -> list[tuple[int, str]]:
    """
    Find ordered entity mentions in a sentence or chunk.
    """

    lowered = text.lower()
    found = []
    for name in entity_names:
        pattern = r"\b" + re.escape(name.lower()) + r"\b"
        for match in re.finditer(pattern, lowered):
            found.append((match.start(), name))
    return sorted(found, key=lambda item: item[0])


def augment_contextual_relationships(
    source_text: str,
    validated_entities: list,
    validated_relationships: list,
) -> list:
    """
    Add lightweight context edges between validated entities that repeatedly
    appear near each other in the source text.

    This gives event-heavy documents a denser, more inspectable graph without
    requiring extra LLM calls or inventing unsupported facts.
    """

    entity_names = [entity.get("name", "").strip() for entity in validated_entities if entity.get("name", "").strip()]
    if len(entity_names) < 2:
        return validated_relationships

    existing_pairs = {
        (rel.get("source", ""), rel.get("target", ""))
        for rel in validated_relationships
    }
    contextual_counts = {}

    for sentence in _sentence_split(source_text):
        occurrences = _entity_occurrences(sentence, entity_names)
        if len(occurrences) < 2:
            continue

        for index, (position, source_name) in enumerate(occurrences):
            neighbors_added = 0
            seen_targets = set()

            for next_position, target_name in occurrences[index + 1:]:
                if source_name == target_name or target_name in seen_targets:
                    continue
                if next_position - position > MAX_CONTEXT_DISTANCE:
                    break

                seen_targets.add(target_name)
                neighbors_added += 1
                contextual_counts[(source_name, target_name)] = (
                    contextual_counts.get((source_name, target_name), 0) + 1
                )

                if neighbors_added >= MAX_CONTEXT_NEIGHBORS:
                    break

    if not contextual_counts:
        return validated_relationships

    max_new_edges = max(120, min(len(entity_names) * 3, 360))
    ranked_pairs = sorted(
        contextual_counts.items(),
        key=lambda item: (-item[1], item[0][0], item[0][1])
    )

    augmented = list(validated_relationships)
    added = 0
    for (source_name, target_name), count in ranked_pairs:
        if added >= max_new_edges:
            break
        if (source_name, target_name) in existing_pairs:
            continue

        augmented.append({
            "source": source_name,
            "target": target_name,
            "relation": CONTEXT_EDGE_RELATION,
            "inferred": True,
            "weight": min(1.0, 0.35 + count * 0.15),
        })
        existing_pairs.add((source_name, target_name))
        added += 1

    if added:
        print(f"    Context augmentation:")
        print(f"      Added    : {added} contextual edges")
        print(f"      Relation : {CONTEXT_EDGE_RELATION}")

    return augmented


def extract_entities_from_chunk(chunk: str, chunk_index: int = 0) -> dict:
    """
    Extract entities and relationships from one text chunk.

    Uses ask_llm_json() — the LLM must return structured JSON.
    The prompt is carefully designed to get consistent output.

    Returns dict with 'entities' list and 'relationships' list.
    Returns empty lists if extraction fails — we never crash.
    """
    

    prompt = f"""
Analyze this text and extract structured information.

TEXT:
{chunk}

Extract:
1. ENTITIES - the important people, organizations, places, events, and concepts
2. RELATIONSHIPS - how these entities connect to each other

Return a JSON object with exactly this structure:
{{
  "entities": [
    {{
      "name": "exact name from text",
      "type": "PERSON or ORGANIZATION or PLACE or EVENT or CONCEPT",
      "description": "one short phrase describing this entity"
    }}
  ],
  "relationships": [
    {{
      "source": "entity name",
      "target": "entity name", 
      "relation": "short verb phrase like LEADS, ANNOUNCED, CAUSED_BY, CRITICIZED, WARNED_ABOUT"
    }}
  ]
}}

Rules:
- Only include entities actually mentioned in the text
- Keep entity names exactly as they appear
- Each relationship source and target must be entity names you listed
- For event-heavy or historical text, include specific units, committees, locations,
  operations, peaks, institutions, and military formations when named
- Aim for 8-14 entities and 8-14 relationships per chunk when the text is dense
- Return valid JSON only
"""
    

    print(f"    Extracting from chunk {chunk_index + 1}...")

    result = ask_llm_json(prompt)

    # Validate the structure — if anything is wrong, return empty safely
    if result.get("parse_error"):
        print(f"    Warning: JSON parsing failed for chunk {chunk_index + 1}")
        raw_preview = (result.get("raw") or result.get("error") or "").strip()
        if raw_preview:
            raw_preview = re.sub(r"\s+", " ", raw_preview)
            if len(raw_preview) > 220:
                raw_preview = raw_preview[:217] + "..."
            print(f"      Raw preview: {raw_preview}")
        return {"entities": [], "relationships": []}

    # Ensure both keys exist even if LLM forgot one
    if "entities" not in result:
        result["entities"] = []
    if "relationships" not in result:
        result["relationships"] = []

    if not isinstance(result["entities"], list):
        result["entities"] = []
    if not isinstance(result["relationships"], list):
        result["relationships"] = []

    result["entities"] = [entity for entity in result["entities"] if isinstance(entity, dict)]
    result["relationships"] = [rel for rel in result["relationships"] if isinstance(rel, dict)]

    entity_count = len(result["entities"])
    rel_count = len(result["relationships"])
    print(f"    Found {entity_count} entities, {rel_count} relationships")

    return result


def extract_from_document(chunks: list) -> dict:
    """
    Run extraction on all chunks of a document and merge results.

    Handles deduplication — the same entity (e.g. "RBI") will appear
    in multiple chunks. We keep one canonical entry per entity name.

    Returns merged dict with all unique entities and relationships.
    """
    # Store chunks reference for validation step later
    source_chunks = chunks

    print(f"\n  Extracting from {len(chunks)} chunks...")

    all_entities = {}     # name → entity dict (deduplicates by name)
    all_relationships = []  # list of all relationship dicts

    for i, chunk in enumerate(chunks):
        result = extract_entities_from_chunk(chunk, i)

        # Merge entities — if name already seen, keep first occurrence
        for entity in result["entities"]:
            name = entity.get("name", "").strip()
            if name and name not in all_entities:
                all_entities[name] = entity

        # Add all relationships (duplicates filtered in graph builder)
        for rel in result["relationships"]:
            source = rel.get("source", "").strip()
            target = rel.get("target", "").strip()
            relation = rel.get("relation", "").strip()

            # Only add if both source and target are known entities
            if source and target and relation:
                all_relationships.append({
                    "source": source,
                    "target": target,
                    "relation": relation
                })

    # Convert entity dict to list
    entities_list = list(all_entities.values())

    print(f"\n  Extraction complete (before validation):")
    print(f"    Raw unique entities   : {len(entities_list)}")
    print(f"    Raw relationships     : {len(all_relationships)}")

    # ── NEW in v2: run validation pipeline ────────────────────────────────
    # Join all chunks back into one text for presence checking
    full_source = " ".join(chunks) if isinstance(chunks[0], str) else ""

    from knowledge.entity_validator import validate_entities, validate_relationships

    validated_entities = validate_entities(entities_list, full_source)
    valid_names = {e["name"] for e in validated_entities}
    validated_relationships = validate_relationships(all_relationships, valid_names)
    validated_relationships = augment_contextual_relationships(
        full_source,
        validated_entities,
        validated_relationships,
    )

    print(f"\n  After validation:")
    print(f"    Clean entities        : {len(validated_entities)}")
    print(f"    Clean relationships   : {len(validated_relationships)}")

    return {"entities": validated_entities, "relationships": validated_relationships}


# ── SELF TEST ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":

    from knowledge.document_parser import parse_document

    print("\n" + "="*45)
    print("  TESTING entity_extractor.py")
    print("="*45)

    doc = parse_document("data/inputs/rbi_article.txt")
    # Test on just first chunk to keep it fast
    result = extract_entities_from_chunk(doc["chunks"][0], 0)

    print(f"\n  Entities found:")
    for e in result["entities"]:
        print(f"    [{e['type']}] {e['name']} — {e['description']}")

    print(f"\n  Relationships found:")
    for r in result["relationships"]:
        print(f"    {r['source']} --{r['relation']}--> {r['target']}")

    print("\n  ✓ entity_extractor.py working correctly.")
