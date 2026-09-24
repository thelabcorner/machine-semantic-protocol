# Research Agenda

## Primary hypothesis

A discrete reasoning IR can transfer **reusable knowledge and inference structure** between heterogeneous pretrained LLMs more efficiently than unconstrained natural-language messages, while preserving the receiver's ability to derive novel conclusions.

We should treat this as a falsifiable hypothesis.

## RQ0 — Can the representation support continued reasoning?

The sender must not see the eventual query. The receiver must derive a novel answer from the transmitted state.

Measure:
- answer accuracy by proof depth;
- symbolic execution accuracy;
- LLM-vs-symbolic receiver gap;
- proof dependency validity where available.

A representation that only paraphrases conclusions fails this requirement.

## RQ1 — Can models learn the protocol in context?

Given only:
- a protocol specification;
- a small number of worked examples;

can previously unseen models encode and decode novel messages without fine-tuning?

Measure:
- semantic accuracy;
- task success;
- syntax validity;
- learning curve vs examples supplied.

## RQ2 — Does it actually reduce communication cost?

Compare against:
- concise natural language;
- JSON;
- tool/function-call schemas;
- compressed/minified structured text;
- task-specific hand-written schemas.

Measure:
- tokenizer-specific transmitted tokens;
- bytes on wire;
- sender inference tokens;
- receiver inference tokens;
- wall-clock latency;
- total inference cost.

A protocol that saves wire tokens but requires a huge translation prompt may lose overall.

## RQ3 — Does meaning survive cross-model transfer?

Evaluate heterogeneous pairs:
- model family A → family A;
- A → B;
- B → A;
- large → small;
- small → large.

The protocol is valuable only if its semantics are not tied to one model's latent geometry.

## RQ4 — How compositional is the vocabulary?

Test unseen combinations of known atoms and relations.

A protocol that memorizes complete messages is not a semantic language.

## RQ5 — What is the right abstraction level?

Candidate levels:
1. fixed symbolic algebra;
2. graph IR with open vocabulary;
3. learned discrete codebook;
4. hybrid fixed operators + learned atoms;
5. hierarchical codebooks.

The current hypothesis favors #4 but this should be experimentally challenged.

## RQ6 — How much interpretability is necessary?

Compare:
- fully opaque learned IDs;
- named stable operators + opaque atoms;
- entirely human-readable symbolic representation.

Measure whether inspectability materially affects interoperability, robustness, or model learning.

## RQ7 — Can models negotiate extensions?

Experiment with session-local definitions:

```text
DEFINE atom:731 := COMPOSE(A,B,C)
```

Then test whether both agents use the extension consistently across a long interaction.

## RQ8 — Failure recovery

A production protocol needs repair primitives:
- UNKNOWN_ATOM
- MALFORMED
- AMBIGUOUS
- REQUEST_DEFINITION
- CONTRADICTION
- VERSION_UNSUPPORTED

Measure recovery cost and whether models can avoid falling back to full English.

## Milestones

### M0 — literature and taxonomy
- comprehensive prior-art map;
- terminology alignment;
- identify strongest baselines;
- collect protocol-design lessons.

### M1 — reasoning IR prototype
- MSP-R0 facts + explicit negation;
- variables and conjunctive Horn-like rules;
- deterministic parser and forward-chainer;
- TRUE / FALSE / UNKNOWN / BOTH query semantics;
- proof dependency capture;
- concise English and JSON baselines.

### M2 — benchmark harness
- equivalent-message dataset;
- multiple model families;
- natural-language / JSON / MSP conditions;
- semantic and task metrics.

### M3 — learned vocabulary
- discover recurring semantic atoms from agent traces;
- compare learned vs hand-designed codebooks;
- test compositional generalization.

### M4 — compact binary encoding
Only after semantics demonstrate value.

### M5 — adaptive/session dictionaries
Test whether dynamically negotiated concepts improve rate without destroying interoperability.

## Kill criteria

We should stop or significantly redirect if:

- concise structured natural language performs equivalently after accounting for all prompt overhead;
- cross-model semantic accuracy degrades too much;
- the codebook requires continual fine-tuning for each model;
- protocol learning consumes more context than it saves;
- opaque symbols yield unacceptable failure detection/recovery;
- gains disappear outside narrow benchmark tasks.

Negative results are valuable if measured cleanly.
