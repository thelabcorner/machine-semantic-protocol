"""Prompt-side definitions for the three initial communication conditions."""

from __future__ import annotations

from dataclasses import dataclass

CANONICAL_SCHEMA = """Return exactly one JSON object with all five keys:
{"act":STRING,"facts":[RELATION...],"constraints":[RELATION...],"post":[RELATION...],"epistemics":[RELATION...]}
Each RELATION is a JSON array whose first item is its relation name and remaining items are ordered arguments.
Do not infer facts that were not transmitted. Use [] for empty groups."""

MSP_V0_SPEC = """MSP-v0 wire grammar:
<act>|<op>(<arg>,...);<op>(<arg>,...)
Arguments are JSON string/number literals. No prose. No field names.

act:
0 assert
1 observe
2 hypothesis
3 command
4 query

fact opcodes:
20 before
21 after
22 cause
23 equals
24 type
25 has
26 not
27 quantity
28 located
29 state
30 rename
31 greater_than
32 less_than

constraint opcodes:
40 preserve
41 prohibit
42 require

postcondition opcodes:
50 run
51 verify

epistemic opcodes:
60 confidence
61 basis
62 source
63 verification

Decoding:
20..32 -> facts
40..42 -> constraints
50..51 -> post
60..63 -> epistemics
The decoded relation name is the lowercase label listed beside the opcode.
Relation argument order is significant. Clause order within a group is not.
"""

JSON_WIRE_SPEC = """Short-key JSON wire schema:
{"a":ACT,"f":[REL...],"c":[REL...],"p":[REL...],"e":[REL...]}
a/f/c/p/e map to act/facts/constraints/post/epistemics.
REL is the same relation array used by the canonical schema.
Omit no semantic content; empty groups may be omitted.
Output minified JSON only."""

ENGLISH_WIRE_SPEC = """Transmit the complete meaning in maximally concise natural English.
Do not use JSON, MSP syntax, tables, or explanatory preambles. Output only the message."""


@dataclass(frozen=True)
class Condition:
    name: str
    sender_spec: str
    receiver_spec: str


CONDITIONS: dict[str, Condition] = {
    "english": Condition(
        name="english",
        sender_spec=ENGLISH_WIRE_SPEC,
        receiver_spec="The wire message is concise natural English.",
    ),
    "json": Condition(
        name="json",
        sender_spec=JSON_WIRE_SPEC,
        receiver_spec=JSON_WIRE_SPEC,
    ),
    "msp": Condition(
        name="msp",
        sender_spec=MSP_V0_SPEC,
        receiver_spec=MSP_V0_SPEC,
    ),
}


def get_condition(name: str) -> Condition:
    try:
        return CONDITIONS[name]
    except KeyError as exc:
        valid = ", ".join(sorted(CONDITIONS))
        raise ValueError(f"unknown condition {name!r}; choose one of: {valid}") from exc


def build_sender_prompt(condition: str, source: str) -> str:
    spec = get_condition(condition).sender_spec
    return f"""You are the sender in a communication benchmark.
Encode every decision-relevant fact in SOURCE using the wire format below.
Do not add facts. Do not explain your encoding.

WIRE FORMAT
{spec}

SOURCE
{source}

WIRE MESSAGE"""


def build_receiver_prompt(condition: str, wire: str) -> str:
    spec = get_condition(condition).receiver_spec
    return f"""You are the receiver in a communication benchmark.
Decode only the information present in WIRE MESSAGE.
Do not use outside assumptions.

WIRE FORMAT
{spec}

CANONICAL OUTPUT
{CANONICAL_SCHEMA}

WIRE MESSAGE
{wire}

CANONICAL JSON"""
