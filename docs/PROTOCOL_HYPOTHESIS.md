# Protocol Hypothesis

## Working name

**MSP — Machine Semantic Protocol** is a placeholder name for the protocol family being investigated.

The repository name is intentionally broader: `machine-semantic-protocol`.

## Current direction: reasoning state, not just semantic packets

The initial semantic-packet design remains useful as a serialization layer, but it is no longer the endpoint.

The protocol should primarily make **reasoning state portable**:

```text
knowledge + rules + assumptions + goals + derivations
```

A receiver should be able to derive something that the sender did not explicitly transmit as a conclusion.

The first executable fragment is MSP-R0, documented in [REASONING_IR.md](REASONING_IR.md).

## Design thesis

Natural language bundles several functions into one sequential stream:

- referents;
- propositions;
- speaker intent;
- confidence;
- causality;
- temporal relationships;
- constraints;
- exact literals;
- discourse structure.

An LLM-facing wire protocol can represent these explicitly rather than repeatedly expressing them through prose.

## Candidate semantic packet model

A message is a typed graph:

```text
Message {
  speech_act
  propositions[]
  entities[]
  relations[]
  constraints[]
  epistemics[]
  provenance[]
  literals[]
}
```

Serialization order is not semantic order.

## Layered design

### L0 — framing

Transport-independent framing:
- protocol version;
- feature bits;
- dictionary epoch;
- message length;
- integrity/checksum information.

### L1 — structural operators

A deliberately small stable instruction set, potentially tens rather than thousands of operators.

Candidate classes:

- ASSERT
- QUERY
- COMMAND
- OBSERVE
- HYPOTHESIZE
- DEFINE
- REFERENCE
- BIND
- NEGATE
- CONSTRAIN
- CAUSE
- BEFORE / AFTER
- REQUIRE
- PRESERVE
- COMPARE
- BRANCH
- ACK
- ERROR

The exact set must emerge from measurement, not aesthetic preference.

### L2 — semantic atoms

A shared vocabulary of discrete semantic concepts.

Important constraint: atoms should be **composable**. We do not want an ID for every sentence-sized concept.

Example:

```text
AGENT + ROLE(SUPERVISOR) + MODE(BACKGROUND)
```

instead of one monolithic concept for "background supervisory agent."

### L3 — session dictionary

Repeated task-specific concepts can be bound to short IDs:

```text
r1 := file("src/parser.ts")
r2 := symbol(r1,"normalizeBounds")
h1 := hypothesis(...)
```

Later packets reference `r1`, `r2`, and `h1` without restating them.

### L4 — literal escape

Exact surface forms remain exact:

- source code;
- identifiers;
- strings;
- numeric constants;
- hashes;
- URLs;
- arbitrary bytes.

A semantic codec should never "interpret" data whose exact byte sequence is part of the meaning.

## Epistemic metadata

Uncertainty should be encoded structurally rather than through phrases such as "I think," "probably," or "it seems."

Potential fields:

```text
confidence: 0..255
basis: observation | inference | assumption | external-source
verification: unverified | partial | verified | contradicted
```

These representations should be calibrated experimentally; arbitrary pseudo-probabilities from models are not automatically meaningful.

## Provenance

A receiver should be able to distinguish:

```text
OBSERVED(X)
INFERRED(X, from=Y)
REPORTED(X, source=Z)
ASSUMED(X)
```

This matters strongly in agent systems, where a repeated claim can otherwise lose track of whether anyone actually observed it.

## Canonical textual diagnostic form

During development we should have an unambiguous text form:

```text
@CMD {
  target: r2
  op: REORDER(bounds, normalize)
  invariant: PRESERVE(api)
  prohibit: MUTATE(unrelated)
  post: RUN(existing_tests)
}
```

This form exists for debugging and specification. It is not the intended compact wire format.

## Binary form

Once semantics stabilize:

- operator IDs: compact integers;
- atoms: dictionary IDs;
- references: varints;
- numeric values: typed encoding;
- graphs: node/edge tables or compact prefix encoding;
- repeated structures: local dictionaries;
- literals: length-prefixed raw content.

## Non-goals

MSP should not become:

- obfuscated English;
- a manually invented universal philosophical ontology;
- a model-specific hidden-state dump;
- a replacement for exact data serialization;
- an opaque protocol whose only evaluation is "the agents seemed to understand it."

## Central engineering tension

More structure improves:
- deterministic parsing;
- interoperability;
- compactness;
- validation.

But too much fixed structure can reduce:
- semantic coverage;
- model learnability;
- adaptability.

The protocol therefore likely needs a **small fixed algebra + learned/negotiated semantic vocabulary**, rather than either a completely fixed ontology or a completely unconstrained emergent language.


## Reasoning architecture boundary

MSP should own the **interchange layer for reasoning**, not attempt to replace every mature reasoning formalism.

A staged architecture is:

```text
LLM latent state
      |
      v
MSP reasoning state
      |
      +-- core Horn-like deduction
      |
      +-- typed extension: SMT / arithmetic / bitvectors / arrays
      |
      +-- typed extension: planning / actions / effects
      |
      +-- typed extension: richer theorem proving
      |
      v
LLM or deterministic executor
```

The core stays small and portable.

When a task needs a domain with mature solver semantics, MSP should carry a typed subproblem or reference an adapter rather than cloning the domain.

Examples:

- SMT-LIB-style adapter for satisfiability, arithmetic, arrays, strings, floating point, and bitvectors;
- PDDL-style adapter for planning state, actions, preconditions, and effects;
- future theorem-prover adapters when unrestricted quantification is genuinely required.

This prevents "machine-native reasoning language" from turning into an accidental universal theorem prover.

## Candidate reasoning-state operations

These are design candidates, not all implemented in R0:

```text
+P(a)                 assert explicit fact
+!P(a)                assert explicit negative fact
r1:A(?x)&B(?x)=>C(?x) reusable rule
?C(a)                 goal/query
~P(a)                 scoped assumption
|-C(a)[r1,f1,f2]      derivation/proof dependency
-P(a)                 retract previously asserted state
{ ... }               branch/context scope
```

The key distinction is between **logical content** and **reasoning-control state**.

MSP-R0 currently implements only facts and rules. Goals are supplied externally by the benchmark, and proof dependencies are produced by the reference executor. We should add more operations only when experiments demonstrate a need.

## Boolean logic is necessary but not sufficient

Boolean composition gives the core operators:

```text
NOT
AND
OR
IMPLIES
```

But useful model reasoning also requires binding predicates to entities and variables:

```text
active(worker_7)
blocked(worker_7)
active(?x)&!blocked(?x)=>schedulable(?x)
```

Therefore the useful minimum is closer to a tiny predicate-logic / logic-programming IR than a propositional bit language.

R0 intentionally supports conjunction and implication but not arbitrary disjunction. General OR introduces branching/search semantics; it should be added only with an explicit benchmark showing that the simpler Horn fragment is insufficient.
