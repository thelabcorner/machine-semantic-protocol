# Experimental Plan

## Principle

Do not evaluate the protocol by asking whether it can reproduce English.

Evaluate whether the receiver acquired the **same information necessary to act correctly**.

## Experiment 1 — proposition transfer

Create source propositions containing:
- entities;
- relations;
- negation;
- quantities;
- uncertainty;
- temporal ordering;
- causal relationships;
- nested constraints.

Conditions:
1. concise English;
2. JSON;
3. MSP debug syntax.

Receiver answers canonical semantic questions.

Primary metric:
```text
correct semantic facts / transmitted tokens
```

## Experiment 2 — instruction execution

Use sandboxed tasks where sender has hidden information and receiver must modify or classify an artifact.

Example communication:

```text
"Change parser ordering, preserve API, do not touch unrelated code, then test."
```

Evaluate resulting actions rather than paraphrases.

Metrics:
- task success;
- violated constraints;
- message tokens;
- total system tokens;
- latency.

## Experiment 3 — compositional generalization

Training/examples expose:
```text
A+B
A+C
D+B
```

Evaluation requires:
```text
D+C
```

This distinguishes compositional semantics from memorized message templates.

## Experiment 4 — cross-model interoperability matrix

For N models, evaluate directed pairs:

```text
M_i → M_j
```

Report a matrix rather than only same-model communication.

Important controls:
- same specification;
- same examples;
- temperature / decoding policy;
- no hidden shared conversation context.

## Experiment 5 — dynamic dictionary

Allow sender to define session-local concepts and reuse them.

Measure break-even point:

```text
definition overhead < repeated-message savings
```

Also measure whether the receiver drifts in interpretation over long sessions.

## Experiment 6 — corruption and repair

Inject:
- missing fields;
- unknown atoms;
- reordered frames;
- contradictory statements;
- truncated literals;
- version mismatch.

Measure:
- detection;
- repair success;
- added communication cost.

## Cost accounting

Every benchmark should report at least:

```text
wire_bytes
sender_input_tokens
sender_output_tokens
receiver_input_tokens
receiver_output_tokens
protocol_spec_tokens
latency
task_score
semantic_score
```

Tokenizer-specific metrics should be reported for every participating model because a supposedly compact textual representation may tokenize badly on another vocabulary.

## Baselines

Minimum baselines:
- natural English, unconstrained;
- natural English, explicitly optimized for brevity;
- minified JSON;
- JSON with short keys;
- task-specific schema/tool call;
- gzip/zstd of wire bytes where meaningful.

The strongest baseline is not verbose chat prose. It is **carefully optimized structured communication**.

## Rate–utility framing

A useful summary curve is:

```text
utility / communication rate
```

rather than one arbitrary token target.

For lossless semantic tasks, utility can approach exact semantic equivalence.

For action tasks, utility is downstream task success subject to constraints.

## Reproducibility

Every experiment should pin:
- model identifier/version;
- protocol version;
- prompt/spec version;
- decoding parameters;
- benchmark dataset hash;
- evaluator version.
