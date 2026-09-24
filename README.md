# Machine Semantic Protocol

Research toward a **discrete, model-independent semantic communication protocol for LLMs**.

Natural language is a convenient interoperability layer for humans and language models, but it is not obviously an efficient wire format for machine-to-machine reasoning. This repository investigates whether heterogeneous pretrained LLMs can communicate through a compact semantic intermediate representation (IR) that preserves actionable meaning while reducing token count, ambiguity, and linguistic overhead.

## Core hypothesis

A useful machine-native protocol may exist between two common extremes:

1. **Natural-language communication** — interoperable and readable, but verbose, ambiguous, and expensive.
2. **Latent-state communication** — high-bandwidth and compact, but architecture-dependent, difficult to inspect, and hard to standardize across heterogeneous models.

We investigate a third point:

```text
Model A latent state
        ↓
discrete semantic IR
        ↓
Model B latent state
```

The protocol is intended to be:

- discrete and binary-serializable;
- compositional rather than phrasebook-based;
- model-independent;
- efficiently learnable in-context by previously unseen models;
- explicit about intent, relation, uncertainty, provenance, and references;
- extensible through session-local dictionaries;
- capable of lossless literal escape for identifiers, code, numbers, hashes, and arbitrary bytes;
- evaluated by preserved task-relevant information, not English reconstruction fidelity.

## Research question

> Can a standardized discrete semantic IR allow heterogeneous pretrained LLMs to exchange the same actionable information as natural language using substantially fewer transmitted tokens, without sharing model weights or latent spaces?

## Repository map

- [Literature map](docs/LITERATURE_MAP.md) — prior work and adjacent research.
- [Prior-art matrix](docs/PRIOR_ART_MATRIX.md) — comparison of adjacent approaches and the gap under test.
- [Protocol hypothesis](docs/PROTOCOL_HYPOTHESIS.md) — proposed architecture and design space.
- [Research agenda](docs/RESEARCH_AGENDA.md) — falsifiable questions and milestones.
- [Experimental plan](docs/EXPERIMENTS.md) — benchmarks and measurements.
- [Glossary](docs/GLOSSARY.md) — terminology used throughout the project.
- [References](references.bib) — machine-readable bibliography.

## Initial protocol sketch

The human-readable debug form might look like:

```text
OBS  ref:parser order(normalize,bounds)
HYP  conf:0.87 cause(order,defect)
CMD  reorder(bounds,normalize)
INV  preserve(api)
NEG  mutate(unrelated)
POST test(existing)
```

The actual wire representation need not contain English labels. Operators, semantic atoms, relation types, references, and literals can be represented with compact integer IDs and varints.

This is **not** intended to be encrypted English, shorthand prose, or a fixed ontology of every possible concept. The target is closer to a semantic bytecode or IR.


## Prototype

The first prototype is intentionally small. It uses [Inspect AI](https://inspect.aisi.org.uk/) as the execution/logging substrate and evaluates a two-model communication channel:

```text
source meaning -> sender -> wire message -> receiver -> canonical semantic object
```

Three conditions are currently compared:

- `english` — aggressively concise natural English;
- `json` — minified short-key structured JSON;
- `msp` — MSP-v0 numeric semantic opcodes.

Inspect records model-role token usage, cost, and timing. MSP additionally records wire bytes and shared protocol/schema overhead so we can distinguish **warm/shared-protocol efficiency** from **cold-start total cost**.

Quick start:

```bash
python -m venv .venv
# activate the environment, then:
pip install -e ".[dev]"

inspect eval evals/semantic_transfer.py \
  -T condition=msp \
  --model none \
  --model-role sender=<provider>/<model> \
  --model-role receiver=<provider>/<model>
```

During development, add `--limit 3` to keep runs cheap.

See [Prototype design](docs/PROTOTYPE.md) and [eval harness survey](docs/EVAL_HARNESS_SURVEY.md).

## Status

Early research / protocol design. No claim is made yet that the proposed approach outperforms natural-language communication. The purpose of this repository is to make that claim experimentally testable.

## License

GPL-3.0-or-later.
