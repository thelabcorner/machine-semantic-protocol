# MSP-R0: Reasoning IR

## Why the protocol changed

The initial MSP prototype tested whether a compact semantic representation could preserve information across models. That is necessary but not sufficient.

A useful machine-native language should let the receiving model **continue reasoning from the transmitted state**.

MSP-R0 therefore represents a small executable theory:

```text
facts + rules + explicit negation
```

rather than only a collection of semantic fields.

## Design target

The first reasoning fragment is deliberately close to a safe Horn-clause / Datalog-like core:

- ground facts;
- n-ary predicates;
- variables local to rules;
- conjunction in rule bodies;
- one-way implication;
- explicit negation;
- open-world query semantics;
- deterministic forward chaining.

No disjunction, existential quantification, function symbols, arithmetic theory, recursion through negation, or unrestricted FOL yet.

## Syntax

### Facts

```text
+red(key)
+follows(ada,bo)
+!blocked(worker_7)
```

The leading `+` asserts a fact into the reasoning state.

`!` is **explicit negation**:

```text
+!blocked(worker_7)
```

means "worker_7 is known not to be blocked."

Merely failing to derive `blocked(worker_7)` does not mean the worker is unblocked.

### Rules

```text
r1:red(?x)=>hot(?x)
r2:permitted(?x)&!blocked(?x)=>schedulable(?x)
r3:follows(?x,?y)&follows(?y,?z)=>reachable(?x,?z)
```

Variables begin with `?` and are implicitly universally quantified within the rule.

Rule direction is strict. From:

```text
square(?x)=>blue(?x)
```

and `blue(q)`, the system may **not** infer `square(q)`.

Contraposition is also not available.

## Four query states

The executor internally supports:

```text
TRUE
FALSE
UNKNOWN
BOTH
```

For query `p(a)`:

- TRUE: `p(a)` is derivable and `!p(a)` is not.
- FALSE: `!p(a)` is derivable and `p(a)` is not.
- UNKNOWN: neither is derivable.
- BOTH: both are derivable.

The initial benchmark avoids contradictory theories, but representing BOTH prevents the implementation from silently collapsing inconsistent knowledge.

## Why open-world semantics

The protocol must distinguish:

```text
unknown
```

from:

```text
known false
```

This is particularly important for agents operating on incomplete observations.

MSP-R0 therefore uses explicit negative facts rather than negation-as-failure.

## Proof DAGs

The reference forward-chainer records the dependency graph for each derived fact.

For:

```text
+red(key)
r1:red(?x)=>hot(?x)
r2:hot(?x)=>unsafe(?x)
```

the proof of `unsafe(key)` is structurally:

```text
unsafe(key)
└─ r2
   └─ hot(key)
      └─ r1
         └─ red(key)
```

This matters because a reasoning protocol should eventually be able to transmit or continue a proof state without transmitting prose chain-of-thought.

## What MSP-R0 is not

It is not intended as a new theorem prover or a universal logic language.

It is an experimental minimum for answering:

> Can a pretrained LLM encode a reusable logical state compactly enough that either another LLM or a deterministic executor can continue reasoning from it?

If this fragment does not show value, expanding its logic would be premature.
