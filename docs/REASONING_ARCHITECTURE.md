# Reasoning Architecture

## Principle

MSP should be a **portable reasoning-state protocol**, not a universal solver.

The core job is to let one model hand another model a compact state that can still be *operated on*.

```text
encode state -> transmit -> continue inference
```

not merely:

```text
encode answer -> transmit -> decode answer
```

## Three layers

### 1. Core reasoning algebra

Keep this extremely small:

- predicates over constants;
- variables;
- explicit positive/negative facts;
- conjunction;
- directional rules;
- goals;
- derivation dependencies.

MSP-R0 implements the first four operational pieces today.

### 2. Reasoning-control state

Real collaboration needs more than propositions.

Future candidates:

- GOAL — what is currently being established;
- ASSUME — scoped hypothetical state;
- BRANCH — alternative world/context;
- DERIVE — explicit dependency edge;
- RETRACT — invalidate stale state;
- CONFLICT — preserve contradictory evidence instead of silently picking one;
- UNKNOWN — preserve absence of knowledge explicitly at the query layer.

This begins to look more like a reasoning VM or proof-state protocol than a serialization format.

### 3. Typed solver extensions

Do not expand the core every time a new reasoning domain appears.

Use adapters.

#### Constraint / arithmetic reasoning

SMT-LIB already standardizes common solver input/output languages and theories including Booleans, integers, reals, strings, arrays, floating point, and bitvectors.

Reference: https://smt-lib.org/

A future MSP message could contain something conceptually like:

```text
EXT smt {
  ...
}
```

without making every LLM reasoner implement those theories itself.

#### Planning

PDDL established a common representation for planning domains/problems with action-oriented semantics.

Reference: https://www.isi.edu/results/publications/62624/pddl-the-planning-domain-definition-language/

A future planning extension could carry actions, preconditions, and effects while MSP handles references, goals, provenance, and inter-agent handoff.

## Why not simply use SMT-LIB for everything?

SMT-LIB solves a different problem.

It is designed to communicate formal satisfiability problems to solvers. MSP is intended to communicate **partially formalized cognitive/reasoning state between pretrained models**, including:

- incomplete knowledge;
- provenance;
- assumptions;
- current goals;
- proof dependencies;
- reusable semantic atoms;
- literal natural-world references;
- extension negotiation.

MSP should therefore be able to *embed or target* mature solver languages without becoming identical to them.

## Why not simply use English plus tool calls?

That is one of the primary baselines.

If concise English plus typed tools matches MSP on:
- rate;
- cross-model accuracy;
- proof-depth robustness;
- cold-start overhead;

then MSP has not demonstrated enough value.

## Staged expressivity

### R0 — implemented

```text
facts
explicit negation
variables
AND
IMPLIES
open-world query state
proof DAG from executor
```

### R1 — only if R0 succeeds

Potential additions:

```text
GOAL
ASSUME
DERIVE
RETRACT
named contexts
```

### R2 — only if demanded by tasks

Potential Boolean branching:

```text
OR
branch scopes
case split
constraints
```

### R3 — adapters, not core bloat

```text
SMT
planning
temporal reasoning
probabilistic/defeasible reasoning
richer theorem proving
```

This staged design is intentional. Every increase in expressivity must justify its decoding cost, protocol-learning cost, and new failure modes.
