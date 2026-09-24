"""MSP-R0 reasoning-state wire format and benchmark prompts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

MSP_R0_SPEC = """MSP-R0 transmits a reusable logical theory, not an answer.

One statement per line.

Ground fact:
+predicate(arg,...)
+!predicate(arg,...)        explicit negative fact

Rule:
rID:atom&atom=>atom

Terms:
- constants: identifiers such as key, worker_7, node_a
- variables: ?x, ?y
- variables are implicitly universally quantified within a rule
- predicate and argument order are significant

Semantics:
- rule bodies are conjunctions
- rules are one-way implications
- ! is explicit negation, NOT negation-as-failure
- missing facts are UNKNOWN, not false
- do not infer contrapositives
- do not encode a conclusion that is not stated or derivable as a rule schema

Example:
+red(key)
r1:red(?x)=>hot(?x)
r2:hot(?x)=>!safe_touch(?x)

Output MSP-R0 only. No prose and no code fence."""

JSON_REASONING_SPEC = """Transmit the complete reusable theory as minified JSON.

Schema:
{"f":[ATOM...],"r":[{"b":[ATOM...],"h":ATOM}...]}

ATOM is a string using predicate syntax, e.g.:
"red(key)"
"!blocked(worker_7)"
"follows(?x,?y)"

Rules use b=conjunctive body and h=head.
Do not include any unstated query or solve a query.
Output minified JSON only."""

ENGLISH_REASONING_SPEC = """Transmit every stated fact and general rule in maximally concise natural English.
Preserve explicit negative facts and rule direction exactly.
Do not solve or anticipate an unstated question.
Output only the reusable theory; no commentary."""


@dataclass(frozen=True)
class ReasoningCondition:
    name: str
    sender_spec: str
    receiver_description: str


CONDITIONS: dict[str, ReasoningCondition] = {
    "english": ReasoningCondition(
        name="english",
        sender_spec=ENGLISH_REASONING_SPEC,
        receiver_description="The wire contains a concise natural-language theory.",
    ),
    "json": ReasoningCondition(
        name="json",
        sender_spec=JSON_REASONING_SPEC,
        receiver_description=JSON_REASONING_SPEC,
    ),
    "msp": ReasoningCondition(
        name="msp",
        sender_spec=MSP_R0_SPEC,
        receiver_description=MSP_R0_SPEC,
    ),
}


def get_reasoning_condition(name: str) -> ReasoningCondition:
    try:
        return CONDITIONS[name]
    except KeyError as exc:
        valid = ", ".join(sorted(CONDITIONS))
        raise ValueError(f"unknown reasoning condition {name!r}; choose one of: {valid}") from exc


def format_vocabulary(vocabulary: Mapping[str, Sequence[str]] | None) -> str:
    if not vocabulary:
        return "No explicit shared symbol table."
    predicates = ", ".join(vocabulary.get("predicates", ())) or "(none)"
    constants = ", ".join(vocabulary.get("constants", ())) or "(none)"
    return f"Predicates: {predicates}\nConstants: {constants}"


def build_reasoning_sender_prompt(
    condition: str,
    theory: str,
    vocabulary: Mapping[str, Sequence[str]] | None = None,
) -> str:
    spec = get_reasoning_condition(condition).sender_spec
    symbols = format_vocabulary(vocabulary)
    return f"""You are the sender in a reasoning-state communication benchmark.

You see THEORY but you will never see the receiver's later query.
Transmit a reusable representation containing every stated fact and rule.
Do not add conclusions merely because they are derivable.
Do not invent facts.

WIRE FORMAT
{spec}

SHARED SYMBOL TABLE
{symbols}

For structured formats, use the shared predicate names and constants exactly.
The symbol table defines names only; it does not state which facts are true.

THEORY
{theory}

WIRE"""


def build_reasoning_receiver_prompt(
    condition: str,
    wire: str,
    query: str,
    vocabulary: Mapping[str, Sequence[str]] | None = None,
) -> str:
    description = get_reasoning_condition(condition).receiver_description
    symbols = format_vocabulary(vocabulary)
    return f"""You are the receiver in a reasoning-state communication benchmark.

Reason only from WIRE and answer QUERY.

Answer semantics:
TRUE    QUERY is derivable.
FALSE   the explicit negation of QUERY is derivable.
UNKNOWN neither QUERY nor its explicit negation is derivable.
BOTH    both are derivable.

This is open-world reasoning: failure to prove something does not make it false.
Rules are directional. Do not use contraposition.

WIRE FORMAT
{description}

SHARED SYMBOL TABLE
{symbols}

WIRE
{wire}

QUERY
{query}

Return exactly one word: TRUE, FALSE, UNKNOWN, or BOTH."""
