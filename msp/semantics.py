"""Small semantic-normalization helpers used by the prototype scorer."""

from __future__ import annotations

import json
from typing import Any

_UNORDERED_FIELDS = frozenset({"facts", "constraints", "post", "epistemics"})


def extract_json_object(text: str) -> Any:
    """Extract the first JSON object from a model completion.

    Receivers are instructed to return JSON only, but this tolerates a code fence
    or a small amount of accidental prose without turning scoring into an LLM judge.
    """
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if len(lines) >= 3 and lines[-1].strip().startswith("```"):
            stripped = "\n".join(lines[1:-1]).strip()
            if stripped.lower().startswith("json\n"):
                stripped = stripped[5:].lstrip()

    start = stripped.find("{")
    if start < 0:
        raise ValueError("no JSON object found")

    decoder = json.JSONDecoder()
    value, _ = decoder.raw_decode(stripped[start:])
    return value


def canonicalize(value: Any, parent_key: str | None = None) -> Any:
    """Canonicalize semantic objects while preserving relation argument order."""
    if isinstance(value, dict):
        return {
            key: canonicalize(value[key], key)
            for key in sorted(value)
        }

    if isinstance(value, list):
        normalized = [canonicalize(item) for item in value]
        if parent_key in _UNORDERED_FIELDS:
            return sorted(
                normalized,
                key=lambda item: json.dumps(
                    item,
                    sort_keys=True,
                    separators=(",", ":"),
                    ensure_ascii=False,
                ),
            )
        return normalized

    return value


def semantic_equal(left: Any, right: Any) -> bool:
    return canonicalize(left) == canonicalize(right)


def compact_json(value: Any) -> str:
    return json.dumps(
        canonicalize(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
