"""Tiny deterministic forward-chainer for MSP-R0.

This is intentionally not a general theorem prover. It implements the exact
reasoning fragment we want to test first:

- ground facts
- explicit negation
- universally quantified Horn-like rules
- conjunction in rule bodies
- unary/binary/n-ary predicates
- open-world TRUE / FALSE / UNKNOWN answers

The engine is useful as an executable oracle for sender-produced MSP programs.
"""

from __future__ import annotations

import csv
import io
import re
from dataclasses import dataclass
from typing import Iterable

_PREDICATE = r"[A-Za-z_][A-Za-z0-9_]*"
_ATOM_RE = re.compile(rf"^(!)?({_PREDICATE})\((.*)\)$")
_RULE_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):(.*)=>(.*)$")


@dataclass(frozen=True, order=True)
class Atom:
    predicate: str
    args: tuple[str, ...]
    negated: bool = False

    def complement(self) -> "Atom":
        return Atom(self.predicate, self.args, not self.negated)

    def __str__(self) -> str:
        prefix = "!" if self.negated else ""
        return f"{prefix}{self.predicate}({','.join(self.args)})"


@dataclass(frozen=True)
class Rule:
    id: str
    body: tuple[Atom, ...]
    head: Atom


@dataclass(frozen=True)
class Program:
    facts: tuple[Atom, ...]
    rules: tuple[Rule, ...]


@dataclass(frozen=True)
class Proof:
    kind: str
    rule_id: str | None = None
    premises: tuple[Atom, ...] = ()


@dataclass(frozen=True)
class ReasoningResult:
    status: str
    query: Atom
    closure: frozenset[Atom]
    proof: dict | None


class ParseError(ValueError):
    pass


def _strip_fence(text: str) -> str:
    stripped = text.strip()
    if not stripped.startswith("```"):
        return stripped

    lines = stripped.splitlines()
    if len(lines) < 3 or not lines[-1].strip().startswith("```"):
        return stripped

    return "\n".join(lines[1:-1]).strip()


def _parse_args(raw: str) -> tuple[str, ...]:
    if not raw.strip():
        return ()

    try:
        row = next(csv.reader(io.StringIO(raw), skipinitialspace=True))
    except (csv.Error, StopIteration) as exc:
        raise ParseError(f"invalid argument list: {raw!r}") from exc

    args = tuple(value.strip() for value in row)
    if any(not value for value in args):
        raise ParseError(f"empty argument in: {raw!r}")
    return args


def parse_atom(text: str) -> Atom:
    text = text.strip()
    match = _ATOM_RE.fullmatch(text)
    if not match:
        raise ParseError(f"invalid atom: {text!r}")

    negated, predicate, args = match.groups()
    parsed_args = _parse_args(args)

    for arg in parsed_args:
        if arg.startswith("?") and not re.fullmatch(r"\?[A-Za-z_][A-Za-z0-9_]*", arg):
            raise ParseError(f"invalid variable: {arg!r}")

    return Atom(predicate, parsed_args, bool(negated))


def _variables(atom: Atom) -> set[str]:
    return {arg for arg in atom.args if arg.startswith("?")}


def parse_program(text: str) -> Program:
    facts: list[Atom] = []
    rules: list[Rule] = []
    seen_rule_ids: set[str] = set()

    for line_number, raw in enumerate(_strip_fence(text).splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue

        if line.startswith("+"):
            atom = parse_atom(line[1:])
            if any(arg.startswith("?") for arg in atom.args):
                raise ParseError(f"line {line_number}: facts must be ground")
            facts.append(atom)
            continue

        match = _RULE_RE.fullmatch(line)
        if not match:
            raise ParseError(f"line {line_number}: expected +fact(...) or id:body=>head")

        rule_id, body_raw, head_raw = match.groups()
        if rule_id in seen_rule_ids:
            raise ParseError(f"line {line_number}: duplicate rule id {rule_id!r}")
        seen_rule_ids.add(rule_id)

        body_parts = [part.strip() for part in body_raw.split("&") if part.strip()]
        if not body_parts:
            raise ParseError(f"line {line_number}: rule body cannot be empty")

        body = tuple(parse_atom(part) for part in body_parts)
        head = parse_atom(head_raw)

        body_vars: set[str] = set()
        for atom in body:
            body_vars.update(_variables(atom))

        unbound = _variables(head) - body_vars
        if unbound:
            raise ParseError(
                f"line {line_number}: head variables not bound in body: {sorted(unbound)}"
            )

        rules.append(Rule(rule_id, body, head))

    if not facts and not rules:
        raise ParseError("program is empty")

    return Program(tuple(facts), tuple(rules))


def _unify(pattern: Atom, fact: Atom, env: dict[str, str]) -> dict[str, str] | None:
    if (
        pattern.predicate != fact.predicate
        or pattern.negated != fact.negated
        or len(pattern.args) != len(fact.args)
    ):
        return None

    next_env = dict(env)
    for expected, actual in zip(pattern.args, fact.args):
        if expected.startswith("?"):
            bound = next_env.get(expected)
            if bound is None:
                next_env[expected] = actual
            elif bound != actual:
                return None
        elif expected != actual:
            return None

    return next_env


def _instantiate(atom: Atom, env: dict[str, str]) -> Atom:
    args: list[str] = []
    for arg in atom.args:
        if arg.startswith("?"):
            if arg not in env:
                raise ValueError(f"unbound variable {arg!r}")
            args.append(env[arg])
        else:
            args.append(arg)
    return Atom(atom.predicate, tuple(args), atom.negated)


def _matches_for_rule(
    body: tuple[Atom, ...],
    facts: set[Atom],
) -> Iterable[tuple[dict[str, str], tuple[Atom, ...]]]:
    partial: list[tuple[dict[str, str], tuple[Atom, ...]]] = [({}, ())]

    for pattern in body:
        next_partial: list[tuple[dict[str, str], tuple[Atom, ...]]] = []
        for env, premises in partial:
            for fact in facts:
                unified = _unify(pattern, fact, env)
                if unified is not None:
                    next_partial.append((unified, premises + (fact,)))
        partial = next_partial
        if not partial:
            break

    yield from partial


def closure(program: Program) -> tuple[set[Atom], dict[Atom, Proof]]:
    facts = set(program.facts)
    proofs: dict[Atom, Proof] = {
        atom: Proof(kind="fact") for atom in program.facts
    }

    changed = True
    while changed:
        changed = False
        additions: list[tuple[Atom, Proof]] = []

        for rule in program.rules:
            for env, premises in _matches_for_rule(rule.body, facts):
                head = _instantiate(rule.head, env)
                if head not in facts:
                    additions.append(
                        (
                            head,
                            Proof(
                                kind="rule",
                                rule_id=rule.id,
                                premises=premises,
                            ),
                        )
                    )

        for atom, proof in additions:
            if atom not in facts:
                facts.add(atom)
                proofs[atom] = proof
                changed = True

    return facts, proofs


def _proof_tree(
    atom: Atom,
    proofs: dict[Atom, Proof],
    visiting: set[Atom] | None = None,
) -> dict | None:
    proof = proofs.get(atom)
    if proof is None:
        return None

    visiting = set() if visiting is None else set(visiting)
    if atom in visiting:
        return {"atom": str(atom), "kind": "cycle"}

    visiting.add(atom)
    if proof.kind == "fact":
        return {"atom": str(atom), "kind": "fact"}

    return {
        "atom": str(atom),
        "kind": "rule",
        "rule": proof.rule_id,
        "premises": [
            _proof_tree(premise, proofs, visiting)
            for premise in proof.premises
        ],
    }


def reason(program: Program | str, query: Atom | str) -> ReasoningResult:
    if isinstance(program, str):
        program = parse_program(program)
    if isinstance(query, str):
        query = parse_atom(query)

    if any(arg.startswith("?") for arg in query.args):
        raise ValueError("queries must be ground")

    derived, proofs = closure(program)
    positive = query in derived
    negative = query.complement() in derived

    if positive and negative:
        status = "BOTH"
        proof_atom = query
    elif positive:
        status = "TRUE"
        proof_atom = query
    elif negative:
        status = "FALSE"
        proof_atom = query.complement()
    else:
        status = "UNKNOWN"
        proof_atom = None

    return ReasoningResult(
        status=status,
        query=query,
        closure=frozenset(derived),
        proof=_proof_tree(proof_atom, proofs) if proof_atom is not None else None,
    )
