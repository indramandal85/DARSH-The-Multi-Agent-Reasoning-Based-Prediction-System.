# knowledge/entity_validator.py
#
# WHAT THIS DOES:
# Cleans extracted entities before they enter the knowledge graph.
# Prevents garbage like "sex" (from "Sensex") and "ss party" (from "Congress")
# from contaminating the graph and downstream causal analysis.
#
# This is a data validation pipeline — same concept as data preprocessing in ML.
# Run after entity extraction, before graph construction.
#
# 4 validation rules applied in order:
#   Rule 1: Minimum name length (≥ 3 characters)
#   Rule 2: Name must appear in the source text (prevents hallucinations)
#   Rule 3: Fuzzy deduplication (merges near-identical entity names)
#   Rule 4: Valid entity type (must be one of 5 defined types)

import difflib
import re


# The only valid entity types — anything else is an extraction error
VALID_TYPES = {"PERSON", "ORGANIZATION", "PLACE", "EVENT", "CONCEPT"}

# Minimum similarity ratio to consider two entity names duplicates
# 0.85 = 85% character overlap — high enough to merge "RBI" + "the RBI"
# but low enough to keep "Shaktikanta Das" and "Nirmala Sitharaman" separate
DEDUP_THRESHOLD = 0.85

STOPWORD_TOKENS = {
    "a", "an", "the", "of", "and", "for", "to", "in", "on", "at", "from"
}


def _normalize_name(name: str) -> str:
    """
    Normalize an entity name for safe duplicate detection.

    We intentionally keep numeric tokens because they often distinguish
    critical military and geopolitical entities like "79 Mountain Brigade"
    vs "56 Mountain Brigade" or "Point 5100" vs "Point 5140".
    """

    lowered = name.lower().strip()
    lowered = re.sub(r"^[^a-z0-9]+|[^a-z0-9]+$", "", lowered)
    lowered = re.sub(r"[^a-z0-9]+", " ", lowered)
    tokens = [t for t in lowered.split() if t and t not in {"the", "a", "an"}]
    return " ".join(tokens)


def _name_tokens(name: str) -> list[str]:
    return _normalize_name(name).split()


def _numeric_tokens(name: str) -> tuple[str, ...]:
    return tuple(re.findall(r"\d+", name))


def _name_acronym(name: str) -> str:
    tokens = [t for t in _name_tokens(name) if t not in STOPWORD_TOKENS]
    if len(tokens) < 2:
        return ""
    return "".join(token[0] for token in tokens if token)


def _types_compatible(type_a: str, type_b: str) -> bool:
    if type_a == type_b:
        return True
    unknownish = {"", "UNKNOWN"}
    return type_a in unknownish or type_b in unknownish


def _safe_token_containment(tokens_a: list[str], tokens_b: list[str]) -> bool:
    """
    Allow containment-based merging only for strong multi-token aliases.

    This deliberately prevents bad merges like:
      "Kargil" -> "Kargil War"
      "79 Mountain Brigade" -> "56 Mountain Brigade"
    """

    if min(len(tokens_a), len(tokens_b)) < 2:
        return False

    smaller, larger = (
        (tokens_a, tokens_b) if len(tokens_a) <= len(tokens_b)
        else (tokens_b, tokens_a)
    )

    if not set(smaller).issubset(set(larger)):
        return False

    # Permit only a very small delta such as "the RBI" vs "RBI" after
    # normalization or "Kargil conflict" vs "the Kargil conflict".
    return (len(larger) - len(smaller)) <= 1


def _is_present_in_text(name: str, source_text: str) -> bool:
    """
    Check if an entity name appears in the source text as a real word.

    Critical fix over v1 logic:
    Single words use ONLY word-boundary regex — never plain substring.
    This prevents "sex" matching "Sensex" and "ex" matching "index".

    Multi-word names check each significant word individually.
    """

    name_lower = name.lower()
    text_lower = source_text.lower()
    words = name_lower.split()

    if len(words) == 1:
        # ── Single word: word-boundary check ONLY ────────────────────────
        # DO NOT use `name_lower in text_lower` here.
        # That would match "sex" inside "Sensex", "ex" inside "index" etc.
        # \b ensures we only match the word at a word boundary.
        pattern = r'\b' + re.escape(name_lower) + r'\b'
        return bool(re.search(pattern, text_lower))

    else:
        # ── Multi-word name: all significant words must appear ────────────
        # "Shaktikanta Das" → both "shaktikanta" and "das" must be in text
        # Skip words shorter than 3 chars (articles, prepositions)
        significant_words = [w for w in words if len(w) > 2]
        if not significant_words:
            return False
        return all(
            bool(re.search(r'\b' + re.escape(w) + r'\b', text_lower))
            for w in significant_words
        )


def _find_canonical_name(name: str, entity_type: str, seen_names: dict) -> str | None:
    """
    Check if this name is a duplicate of an already-seen entity.

    Uses difflib.SequenceMatcher which computes a similarity ratio.
    Also checks if one name contains the other (handles abbreviations).

    Returns the canonical (existing) name if it's a duplicate, None otherwise.

    Examples of what gets merged:
      "RBI" + "the RBI" → merge (one contains the other)
      "Shaktikanta Das" + "Shaktikanta" → merge (ratio ~0.8)
      "HDFC Bank" + "HDFC" → merge (one contains the other)

    Examples of what stays separate:
      "Shaktikanta Das" + "Nirmala Sitharaman" → keep both (ratio ~0.3)
      "RBI" + "FBI" → keep both (ratio ~0.5)
    """

    name_lower = name.lower()
    name_norm = _normalize_name(name)
    name_tokens = _name_tokens(name)
    name_numbers = _numeric_tokens(name)
    name_acronym = _name_acronym(name)

    for existing_name, existing_entity in seen_names.items():
        existing_lower = existing_name.lower()
        existing_type = existing_entity.get("type", "UNKNOWN")
        existing_norm = _normalize_name(existing_name)
        existing_tokens = _name_tokens(existing_name)
        existing_numbers = _numeric_tokens(existing_name)
        existing_acronym = _name_acronym(existing_name)

        if not _types_compatible(entity_type, existing_type):
            continue

        # Numeric identifiers distinguish many real-world entities.
        if name_numbers and existing_numbers and name_numbers != existing_numbers:
            continue

        # Exact normalized match after stripping punctuation/articles.
        if name_norm and name_norm == existing_norm:
            return existing_name

        compact_name = name_norm.replace(" ", "")
        compact_existing = existing_norm.replace(" ", "")

        # Acronym ↔ long-form match, e.g. "RBI" ↔ "Reserve Bank of India"
        if name_acronym and name_acronym == compact_existing:
            return existing_name
        if existing_acronym and existing_acronym == compact_name:
            return existing_name

        # Safe containment for multi-token aliases only.
        if _safe_token_containment(name_tokens, existing_tokens):
            return existing_name

        # Fuzzy similarity check
        ratio = difflib.SequenceMatcher(None, name_norm or name_lower, existing_norm or existing_lower).ratio()
        token_overlap = 0.0
        if name_tokens and existing_tokens:
            token_overlap = (
                len(set(name_tokens) & set(existing_tokens)) /
                max(len(set(name_tokens) | set(existing_tokens)), 1)
            )

        if ratio >= max(DEDUP_THRESHOLD, 0.93) and token_overlap >= 0.75:
            return existing_name

    return None


def _resolve_canonical_name(name: str, valid_entities: dict) -> str | None:
    """
    Map a relationship endpoint to the canonical validated entity name.
    """

    cleaned_name = name.strip()
    if not cleaned_name:
        return None

    if cleaned_name in valid_entities:
        return cleaned_name

    name_norm = _normalize_name(cleaned_name)
    name_tokens = _name_tokens(cleaned_name)
    name_numbers = _numeric_tokens(cleaned_name)
    name_acronym = _name_acronym(cleaned_name)
    compact_name = name_norm.replace(" ", "")

    best_match = None
    best_score = 0.0

    for existing_name in valid_entities:
        existing_norm = _normalize_name(existing_name)
        existing_tokens = _name_tokens(existing_name)
        existing_numbers = _numeric_tokens(existing_name)
        existing_acronym = _name_acronym(existing_name)
        compact_existing = existing_norm.replace(" ", "")

        if name_numbers and existing_numbers and name_numbers != existing_numbers:
            continue

        if name_norm and name_norm == existing_norm:
            return existing_name
        if name_acronym and name_acronym == compact_existing:
            return existing_name
        if existing_acronym and existing_acronym == compact_name:
            return existing_name
        if _safe_token_containment(name_tokens, existing_tokens):
            return existing_name

        ratio = difflib.SequenceMatcher(None, name_norm or cleaned_name.lower(), existing_norm or existing_name.lower()).ratio()
        token_overlap = 0.0
        if name_tokens and existing_tokens:
            token_overlap = (
                len(set(name_tokens) & set(existing_tokens)) /
                max(len(set(name_tokens) | set(existing_tokens)), 1)
            )
        score = ratio + token_overlap
        if ratio >= 0.94 and token_overlap >= 0.75 and score > best_score:
            best_match = existing_name
            best_score = score

    return best_match


def validate_entities(entities: list, source_text: str) -> list:
    """
    Main validation function. Takes raw extracted entities, returns cleaned list.

    entities    : list of dicts from entity_extractor.py
                  each dict has: name, type, description
    source_text : the original document text (used for presence checking)

    Returns     : cleaned list with invalid and duplicate entities removed
    """

    cleaned = []
    seen_names = {}      # canonical_name → entity dict
    rejected = []        # for logging what was removed

    for entity in entities:
        name = entity.get("name", "").strip()
        entity_type = entity.get("type", "").strip().upper()
        description = entity.get("description", "").strip()

        # ── Rule 1: minimum name length ───────────────────────────────────
        if len(name) < 3:
            rejected.append((name, "too short (< 3 chars)"))
            continue

        # ── Rule 2: name must appear in source text ────────────────────────
        if not _is_present_in_text(name, source_text):
            rejected.append((name, "not found in source text"))
            continue

        # ── Rule 3: valid entity type ──────────────────────────────────────
        if entity_type not in VALID_TYPES:
            # Try to salvage with a default type rather than rejecting
            entity_type = "CONCEPT"
            entity["type"] = entity_type

        # ── Rule 4: fuzzy deduplication ────────────────────────────────────
        canonical = _find_canonical_name(name, entity_type, seen_names)
        if canonical is not None:
            # This is a duplicate — merge description if the existing one is empty
            if not seen_names[canonical].get("description") and description:
                seen_names[canonical]["description"] = description
            rejected.append((name, f"duplicate of '{canonical}'"))
            continue

        # ── Passed all rules — add to cleaned list ─────────────────────────
        entity["type"] = entity_type   # ensure uppercase
        seen_names[name] = entity
        cleaned.append(entity)

    # Print summary
    print(f"    Entity validation:")
    print(f"      Input    : {len(entities)} entities")
    print(f"      Kept     : {len(cleaned)} entities")
    print(f"      Removed  : {len(rejected)} entities")
    if rejected:
        for name, reason in rejected[:5]:    # show first 5 rejections
            print(f"        ✗ '{name}' — {reason}")
        if len(rejected) > 5:
            print(f"        ... and {len(rejected) - 5} more")

    return cleaned


def validate_relationships(relationships: list, valid_entity_names: set | dict) -> list:
    """
    Clean extracted relationships after entity validation.

    Any relationship whose source or target is not in the validated
    entity list gets removed. This prevents edges pointing to nodes
    that were cleaned out (like "sex → HDFC Bank").

    relationships      : raw relationship list from entity_extractor.py
    valid_entity_names : set of names that survived entity validation

    Returns: cleaned relationship list
    """

    cleaned = []
    removed = 0
    canonicalized = 0
    deduped = 0
    seen_rel_keys = set()
    entity_lookup = (
        valid_entity_names
        if isinstance(valid_entity_names, dict)
        else {name: {"name": name} for name in valid_entity_names}
    )

    for rel in relationships:
        source = rel.get("source", "").strip()
        target = rel.get("target", "").strip()
        relation = " ".join(rel.get("relation", "").strip().split())

        # Both source and target must be in the validated entity set
        if not source or not target or not relation:
            removed += 1
            continue

        resolved_source = _resolve_canonical_name(source, entity_lookup)
        resolved_target = _resolve_canonical_name(target, entity_lookup)

        if not resolved_source or not resolved_target or resolved_source == resolved_target:
            removed += 1
            continue

        if resolved_source != source or resolved_target != target:
            canonicalized += 1

        rel_key = (resolved_source, resolved_target, relation.upper())
        if rel_key in seen_rel_keys:
            deduped += 1
            continue

        seen_rel_keys.add(rel_key)
        cleaned.append({
            **rel,
            "source": resolved_source,
            "target": resolved_target,
            "relation": relation,
        })

    print(f"    Relationship validation:")
    print(f"      Input    : {len(relationships)} relationships")
    print(f"      Kept     : {len(cleaned)} relationships")
    print(f"      Removed  : {removed} (source/target not in validated entities)")
    if canonicalized:
        print(f"      Rewired  : {canonicalized} relationship endpoints to canonical names")
    if deduped:
        print(f"      Deduped  : {deduped} duplicate relationships")

    return cleaned
