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

## Status

Early research / protocol design. No claim is made yet that the proposed approach outperforms natural-language communication. The purpose of this repository is to make that claim experimentally testable.

## License

GPL-3.0-or-later.
