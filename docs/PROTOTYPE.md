# Prototype

## Scope

The prototype answers one narrow question before we invest in a larger protocol:

> Can two pretrained LLMs transfer a small semantic object through a non-natural-language MSP wire message with competitive accuracy and lower communication rate than strong simple baselines?

It deliberately does **not** implement binary MSP, learned atoms, session dictionaries, fine-tuning, or agent execution.

## Pipeline

```text
natural-language source
        |
        v
     sender model
        |
        +---- english
        +---- minified JSON
        +---- MSP-v0
        |
        v
     wire message
        |
        v
    receiver model
        |
        v
canonical semantic JSON
        |
        v
deterministic scorer
```

Sender and receiver are separate Inspect model roles. They may be the same model or different model families.

## Why the target is canonical JSON

Canonical JSON is **not** the proposed protocol. It is an evaluation representation.

It gives the scorer an explicit ground truth and lets us measure whether semantic content survived without asking another LLM to judge the answer.

The current schema is:

```json
{
  "act": "command",
  "facts": [["before", "bounds", "normalization"]],
  "constraints": [["preserve", "public_api"]],
  "post": [["run", "existing_tests"]],
  "epistemics": []
}
```

Top-level relation groups are order-insensitive. Relation argument order is significant.

## MSP-v0

MSP-v0 is intentionally primitive. It replaces recurrent semantic grammar with numeric opcodes while leaving task-specific concepts as literal arguments.

Example:

```text
3|20("bounds","normalization");40("public_api");41("modify","unrelated_code");50("existing_tests")
```

This is a **stage-A protocol**, not the endpoint. If the approach survives benchmarking, later versions can investigate discrete learned semantic atoms and binary serialization.

## Cost model

There are two views of efficiency:

### Warm/shared protocol

Assume both endpoints already know the protocol.

Measure:
- wire bytes;
- eventual tokenizer-specific wire tokens;
- semantic accuracy.

### Cold start

Count the instructions/specification required to teach each model the protocol for the run.

Inspect already records role-specific model input/output usage and cost. The prototype additionally stores:
- `wire_bytes`;
- `sender_instruction_bytes`;
- `receiver_instruction_bytes`.

A protocol is not allowed to hide a giant dictionary in "free" context.

## Initial conditions

### `english`

A sender is asked for maximally concise natural English. This is the important human-language baseline, not ordinary verbose assistant prose.

### `json`

A sender uses short keys:
`a/f/c/p/e` for `act/facts/constraints/post/epistemics`.

This is deliberately strong. If MSP cannot beat a simple structured schema, that is useful evidence.

### `msp`

A numeric opcode grammar. No natural-language field names are sent on the wire.

## Running

```bash
inspect eval evals/semantic_transfer.py \
  -T condition=msp \
  --model none \
  --model-role sender=<provider>/<model> \
  --model-role receiver=<provider>/<model>
```

Use `-T condition=english` and `-T condition=json` for baselines.

For cheap iteration:

```bash
inspect eval evals/semantic_transfer.py \
  -T condition=msp \
  --limit 3 \
  --model none \
  --model-role sender=<provider>/<model> \
  --model-role receiver=<provider>/<model>
```

## Immediate next experiments

1. Run same-model pairs to debug protocol/scoring.
2. Run heterogeneous sender/receiver pairs.
3. Expand the dataset only where failures expose missing semantic primitives.
4. Add tokenizer-specific wire-token counting after the basic channel works.
5. Only then consider dynamic dictionaries or learned atoms.
