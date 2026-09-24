# Research Notes: Reasoning as Communication

## ProofWriter

Tafjord, Dalvi, and Clark (Findings ACL 2021) showed generative logical reasoning over natural-language theories, including implication generation, proofs, and constrained abduction.

Relevance to MSP:
- proof depth is a natural difficulty axis;
- proofs can be represented as dependency graphs rather than prose;
- implication generation tests reusable theory understanding rather than only classification;
- open-world True / False / Unknown semantics fit incomplete agent knowledge.

https://aclanthology.org/2021.findings-acl.317/

## RuleTaker

RuleTaker generates theories and assertions for logical reasoning and includes theorem-prover-based labeling.

Relevance:
- controlled theory generation can eventually scale MSP beyond a hand-written seed set;
- the distinction between theory and assertion maps directly onto sender-state vs receiver-query separation.

https://github.com/allenai/ruletaker

## FOLIO

FOLIO contains human-annotated natural-language reasoning examples paired with FOL annotations whose logical correctness is checked by an inference engine.

Relevance:
- good later test of whether MSP can move beyond synthetic Horn clauses;
- useful NL-to-formal translation benchmark;
- too expressive to adopt as the first protocol core.

https://aclanthology.org/2024.emnlp-main.1229/

## Logic-LM

Logic-LM translates natural-language problems to symbolic formulations and then invokes deterministic solvers. The paper reports substantial average gains over direct and chain-of-thought prompting across five logical reasoning datasets.

Relevance:
- validates separating semantic translation from deterministic inference;
- solver errors can feed back into representation refinement;
- MSP can measure the formalization stage independently through symbolic receiver mode.

https://aclanthology.org/2023.findings-emnlp.248/

## LINC

LINC treats the LLM as a semantic parser into first-order logic and uses an external theorem prover.

Relevance:
- heterogeneous LLMs do not need to share a latent space if they share a formal interface;
- logic can serve as an interoperability layer;
- MSP differs by treating that representation as an inter-model communication protocol.

https://aclanthology.org/2023.emnlp-main.313/

## Faithful Chain-of-Thought

Faithful CoT separates translation into a symbolic reasoning chain from deterministic problem solving.

Relevance:
- proof-like symbolic state is more mechanically checkable than prose reasoning;
- supports our decision not to optimize for natural-language chain-of-thought transmission.

https://arxiv.org/abs/2301.13379

## Design consequence

The central object should be a **reasoning state**, not a sentence:

```text
K = (F, R, A, G)
```

where initially:

- F = explicit facts;
- R = rules;
- A = assumptions / explicit negative knowledge;
- G = externally supplied goal/query.

For MSP-R0 the sender communicates F and R. The receiver receives G independently and continues inference.

This is intentionally narrower than a full cognitive architecture.
