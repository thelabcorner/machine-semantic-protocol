"""MSP semantic-transfer benchmark built on Inspect AI."""

from __future__ import annotations

import json
from pathlib import Path

from inspect_ai import Task, task
from inspect_ai.dataset import Sample, json_dataset
from inspect_ai.model import get_model
from inspect_ai.scorer import CORRECT, INCORRECT, Score, Target, accuracy, scorer, stderr
from inspect_ai.solver import Generate, Solver, TaskState, solver

from msp.protocol import build_receiver_prompt, build_sender_prompt, get_condition
from msp.semantics import compact_json, extract_json_object, semantic_equal

DATASET = Path(__file__).resolve().parents[1] / "data" / "semantic_transfer.jsonl"


def _record_to_sample(record: dict) -> Sample:
    return Sample(
        id=record["id"],
        input=record["source"],
        target=compact_json(record["target"]),
        metadata={"tags": record.get("tags", [])},
    )


@solver
def communicate(condition: str) -> Solver:
    """Run source -> sender -> wire -> receiver for one communication condition."""
    config = get_condition(condition)

    async def solve(state: TaskState, generate: Generate) -> TaskState:
        sender = get_model(role="sender")
        receiver = get_model(role="receiver")

        sender_prompt = build_sender_prompt(config.name, state.input_text)
        sender_output = await sender.generate(sender_prompt)
        wire = sender_output.completion.strip()

        receiver_prompt = build_receiver_prompt(config.name, wire)
        receiver_output = await receiver.generate(receiver_prompt)

        state.store.set("condition", config.name)
        state.store.set("wire", wire)
        state.store.set("wire_bytes", len(wire.encode("utf-8")))
        state.store.set("sender_instruction_bytes", len(config.sender_spec.encode("utf-8")))
        state.store.set("receiver_instruction_bytes", len(config.receiver_spec.encode("utf-8")))
        state.output = receiver_output
        return state

    return solve


@scorer(metrics=[accuracy(), stderr()])
def semantic_exact() -> object:
    """Score decoded canonical semantics without an LLM judge."""

    async def score(state: TaskState, target: Target) -> Score:
        expected = json.loads(target.text)
        try:
            received = extract_json_object(state.output.completion)
            correct = semantic_equal(received, expected)
            explanation = None if correct else (
                f"expected={compact_json(expected)}\n"
                f"received={compact_json(received)}"
            )
        except (ValueError, json.JSONDecodeError, TypeError) as exc:
            received = None
            correct = False
            explanation = f"receiver output could not be parsed: {exc}"

        return Score(
            value=CORRECT if correct else INCORRECT,
            answer=state.output.completion,
            explanation=explanation,
            metadata={
                "condition": state.store.get("condition"),
                "wire": state.store.get("wire"),
                "wire_bytes": state.store.get("wire_bytes"),
                "sender_instruction_bytes": state.store.get("sender_instruction_bytes"),
                "receiver_instruction_bytes": state.store.get("receiver_instruction_bytes"),
            },
        )

    return score


@task
def semantic_transfer(condition: str = "msp") -> Task:
    """Evaluate whether meaning survives a two-model communication channel."""
    get_condition(condition)  # fail fast on typo
    return Task(
        dataset=json_dataset(str(DATASET), sample_fields=_record_to_sample),
        solver=communicate(condition),
        scorer=semantic_exact(),
    )
