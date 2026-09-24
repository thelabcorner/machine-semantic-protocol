"""Reasoning-state transfer benchmark.

The sender sees a theory but not the eventual query. A receiver must answer a
novel query from the transmitted representation.

Modes:
- receiver=llm: a receiver model reasons directly over the wire message.
- receiver=symbolic: MSP-R0 is parsed/executed by the tiny deterministic reasoner.

The symbolic mode isolates sender formalization quality from receiver reasoning.
"""

from __future__ import annotations

from pathlib import Path

from inspect_ai import Task, task
from inspect_ai.dataset import Sample, json_dataset
from inspect_ai.model import get_model
from inspect_ai.scorer import CORRECT, INCORRECT, Score, Target, accuracy, scorer, stderr
from inspect_ai.solver import Generate, Solver, TaskState, solver

from msp.reasoner import ParseError, reason
from msp.reasoning import (
    build_reasoning_receiver_prompt,
    build_reasoning_sender_prompt,
    get_reasoning_condition,
)

DATASET = Path(__file__).resolve().parents[1] / "data" / "reasoning_transfer.jsonl"
_VALID_ANSWERS = ("TRUE", "FALSE", "UNKNOWN", "BOTH")


def _record_to_sample(record: dict) -> Sample:
    return Sample(
        id=record["id"],
        input=record["theory"],
        target=record["answer"],
        metadata={
            "query": record["query"],
            "query_atom": record["query_atom"],
            "depth": record["depth"],
            "tags": record.get("tags", []),
        },
    )


def _normalize_answer(text: str) -> str:
    upper = text.strip().upper()
    for answer in _VALID_ANSWERS:
        if upper == answer or upper.startswith(answer + "\n") or upper.startswith(answer + " "):
            return answer
    return upper


@solver
def communicate_and_reason(condition: str, receiver: str = "llm") -> Solver:
    config = get_reasoning_condition(condition)

    if receiver not in {"llm", "symbolic"}:
        raise ValueError("receiver must be 'llm' or 'symbolic'")
    if receiver == "symbolic" and condition != "msp":
        raise ValueError("symbolic receiver currently executes MSP only")

    async def solve(state: TaskState, generate: Generate) -> TaskState:
        sender_model = get_model(role="sender")
        sender_prompt = build_reasoning_sender_prompt(config.name, state.input_text)
        sender_output = await sender_model.generate(sender_prompt)
        wire = sender_output.completion.strip()

        state.store.set("condition", config.name)
        state.store.set("receiver_mode", receiver)
        state.store.set("wire", wire)
        state.store.set("wire_bytes", len(wire.encode("utf-8")))
        state.store.set("sender_instruction_bytes", len(config.sender_spec.encode("utf-8")))

        if receiver == "symbolic":
            try:
                result = reason(wire, state.metadata["query_atom"])
                state.store.set("answer", result.status)
                state.store.set("proof", result.proof)
                state.store.set("closure_size", len(result.closure))
            except (ParseError, ValueError) as exc:
                state.store.set("answer", "ERROR")
                state.store.set("symbolic_error", str(exc))
            state.output = sender_output
            return state

        receiver_model = get_model(role="receiver")
        receiver_prompt = build_reasoning_receiver_prompt(
            config.name,
            wire,
            state.metadata["query"],
        )
        receiver_output = await receiver_model.generate(receiver_prompt)
        state.store.set(
            "receiver_instruction_bytes",
            len(config.receiver_description.encode("utf-8")),
        )
        state.output = receiver_output
        return state

    return solve


@scorer(metrics=[accuracy(), stderr()])
def reasoning_answer() -> object:
    async def score(state: TaskState, target: Target) -> Score:
        mode = state.store.get("receiver_mode")
        if mode == "symbolic":
            answer = state.store.get("answer")
        else:
            answer = _normalize_answer(state.output.completion)

        expected = target.text.strip().upper()
        correct = answer == expected

        metadata = {
            "condition": state.store.get("condition"),
            "receiver_mode": mode,
            "wire": state.store.get("wire"),
            "wire_bytes": state.store.get("wire_bytes"),
            "sender_instruction_bytes": state.store.get("sender_instruction_bytes"),
            "depth": state.metadata["depth"],
            "query_atom": state.metadata["query_atom"],
        }

        if mode == "symbolic":
            metadata["proof"] = state.store.get("proof")
            metadata["closure_size"] = state.store.get("closure_size")
            metadata["symbolic_error"] = state.store.get("symbolic_error")
        else:
            metadata["receiver_instruction_bytes"] = state.store.get(
                "receiver_instruction_bytes"
            )

        return Score(
            value=CORRECT if correct else INCORRECT,
            answer=answer,
            explanation=None if correct else f"expected {expected}, received {answer}",
            metadata=metadata,
        )

    return score


@task
def reasoning_transfer(
    condition: str = "msp",
    receiver: str = "llm",
) -> Task:
    get_reasoning_condition(condition)
    return Task(
        dataset=json_dataset(str(DATASET), sample_fields=_record_to_sample),
        solver=communicate_and_reason(condition, receiver),
        scorer=reasoning_answer(),
    )
