# core/llm_caller.py
#
# THE BRIDGE BETWEEN DARSH AND THE LOCAL LLM.
# Every module calls ask_llm() or ask_llm_json().
# Nothing in this project ever calls Ollama directly — always through here.

import ast
import json
import os
import re

import requests

# ── CONFIG ────────────────────────────────────────────────────────────────────

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")

# Change to "llama3.2:3b" if you pulled the smaller model
MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3.1")


def _strip_markdown_fences(text: str) -> str:
    stripped = text.strip()
    if not stripped.startswith("```"):
        return stripped

    lines = stripped.splitlines()
    if len(lines) >= 3 and lines[-1].strip().startswith("```"):
        return "\n".join(lines[1:-1]).strip()
    return stripped


def _strip_think_blocks(text: str) -> str:
    cleaned = re.sub(r"(?is)<think>.*?</think>", "", text).strip()
    if "</think>" in cleaned:
        cleaned = cleaned.split("</think>", 1)[-1].strip()
    return cleaned


def _strip_trailing_commas(text: str) -> str:
    return re.sub(r",(\s*[}\]])", r"\1", text)


def _extract_balanced_json(text: str) -> str:
    start = None
    opening = ""

    for index, char in enumerate(text):
        if char in "{[":
            start = index
            opening = char
            break

    if start is None:
        return ""

    closing = "}" if opening == "{" else "]"
    depth = 0
    in_string = False
    escape = False

    for index in range(start, len(text)):
        char = text[index]

        if escape:
            escape = False
            continue
        if char == "\\":
            escape = True
            continue
        if char == '"':
            in_string = not in_string
            continue
        if in_string:
            continue

        if char == opening:
            depth += 1
        elif char == closing:
            depth -= 1
            if depth == 0:
                return text[start:index + 1].strip()

    return text[start:].strip()


def _parse_candidate(candidate: str):
    if not candidate:
        return None

    for parser in (json.loads, ast.literal_eval):
        try:
            parsed = parser(candidate)
        except Exception:
            continue
        if isinstance(parsed, dict):
            return parsed

    return None


def _coerce_json_object(raw: str):
    attempts = []

    def add(candidate: str):
        cleaned = (candidate or "").strip()
        if cleaned and cleaned not in attempts:
            attempts.append(cleaned)

    add(raw)

    cleaned = _strip_markdown_fences(_strip_think_blocks(raw))
    add(cleaned)
    add(_extract_balanced_json(raw))
    add(_extract_balanced_json(cleaned))

    expanded_attempts = []
    for candidate in attempts:
        expanded_attempts.append(candidate)
        trimmed = _strip_trailing_commas(candidate)
        if trimmed not in expanded_attempts:
            expanded_attempts.append(trimmed)

    for candidate in expanded_attempts:
        parsed = _parse_candidate(candidate)
        if parsed is not None:
            return parsed

    return None

# ── FUNCTION 1: plain text response ───────────────────────────────────────────

def ask_llm(prompt: str, system_prompt: str = None) -> str:
    """
    Send a prompt to Llama. Get a plain text response back.

    prompt        : your question or instruction
    system_prompt : optional personality for the model this call only.
                    e.g. "You are a cautious economics student."
    Returns       : model response as a string
    """

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 512
        }
    }

    if system_prompt:
        payload["system"] = system_prompt

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        return response.json()["response"].strip()

    except requests.exceptions.ConnectionError:
        raise ConnectionError(
            "\n\nCannot reach Ollama.\n"
            "Fix: make sure Tab 1 is running 'ollama serve'\n"
        )

    except requests.exceptions.Timeout:
        raise TimeoutError(
            "\n\nOllama timed out.\n"
            "Model might still be loading. Wait 30s and retry.\n"
        )

    except Exception as e:
        raise RuntimeError(f"\n\nError: {e}\n")


# ── FUNCTION 2: structured JSON response ──────────────────────────────────────

def ask_llm_json(prompt: str, system_prompt: str = None) -> dict:
    """
    Same as ask_llm() but forces JSON output.

    Use this when you need structured data back — e.g. an agent
    returning both an 'action' and a 'reason' as separate fields.

    Returns: Python dict from parsed JSON.
             If parsing fails: {"raw": <text>, "parse_error": True}
    """

    json_rule = (
        "You must respond with a valid JSON object only. "
        "No explanation. No markdown. No code blocks. "
        "Start with { and end with }."
    )

    full_system = f"{system_prompt}\n\n{json_rule}" if system_prompt else json_rule

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "system": full_system,
        "options": {
            "temperature": 0.0,
            "num_predict": 768
        }
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        raw = response.json()["response"].strip()

        parsed = _coerce_json_object(raw)
        if parsed is not None:
            return parsed
        return {"raw": raw, "parse_error": True}

    except Exception as e:
        return {"error": str(e), "parse_error": True}


# ── SELF TEST ─────────────────────────────────────────────────────────────────
# Run: python core/llm_caller.py

if __name__ == "__main__":

    print("\n" + "="*50)
    print("  TESTING core/llm_caller.py")
    print("="*50)

    print("\nTest 1 — plain text call:")
    print("-"*35)
    answer = ask_llm(
        prompt="In one sentence, what is an AI agent?",
        system_prompt="You are a clear and concise AI teacher."
    )
    print(answer)

    print("\nTest 2 — JSON structured call:")
    print("-"*35)
    result = ask_llm_json(
        prompt=(
            "Return a JSON object with key 'causes' "
            "containing an array of exactly 3 short strings "
            "that are causes of inflation."
        )
    )
    print(result)

    if result.get("parse_error"):
        print("\nNote: JSON had a parsing issue but connection works.")
    else:
        print("\n✓ llm_caller.py working correctly.")
