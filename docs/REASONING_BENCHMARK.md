# Reasoning-Transfer Benchmark

## Central change

The sender no longer knows what question will eventually be asked.

That prevents it from transmitting only a conclusion and forces the wire message to preserve a reusable reasoning state.

```text
                   hidden from sender
                         query
                           |
theory -> sender -> wire -+-> receiver -> answer
```

## Two receiver modes

### LLM receiver

```text
theory -> sender LLM -> wire -> receiver LLM -> TRUE/FALSE/UNKNOWN
```

This measures whether the representation is a useful **reasoning language for another model**.

### Symbolic receiver

```text
theory -> sender LLM -> MSP-R0 -> deterministic forward-chainer -> answer
```

This isolates the sender's semantic/formalization quality.

If symbolic succeeds but the LLM receiver fails, the representation is executable but awkward for the model.

If both fail, the sender likely mistranslated or the IR is insufficient.

If both succeed, we can compare communication rate against English/JSON.

## Why this resembles ProofWriter / RuleTaker

ProofWriter and RuleTaker established a useful controlled shape for evaluating rule-based reasoning over facts and implications. ProofWriter additionally provides proof supervision and open-world True / False / Unknown tasks.

Primary sources:

- RuleTaker: https://github.com/allenai/ruletaker
- ProofWriter: https://aclanthology.org/2021.findings-acl.317/

We are not copying their benchmark wholesale yet. The initial hand-written set is intentionally tiny so protocol iteration remains cheap.

Once the harness is stable, importing a small stratified subset of ProofWriter is the obvious next scaling step.

## Why not FOLIO yet

FOLIO provides human-written natural-language premises paired with first-order logic annotations and verified inference. It is a strong later benchmark:

https://aclanthology.org/2024.emnlp-main.1229/

But full FOL introduces significantly more parsing and solver complexity than we need to test the core hypothesis.

## Neurosymbolic precedent

Logic-LM and LINC both support the architectural split we care about:

```text
language model -> formal representation -> deterministic inference
```

- Logic-LM: https://aclanthology.org/2023.findings-emnlp.248/
- LINC: https://aclanthology.org/2023.emnlp-main.313/

Faithful Chain-of-Thought similarly separates natural-language translation from deterministic symbolic execution:

https://arxiv.org/abs/2301.13379

Our twist is that the formal representation is not merely an internal scratchpad. It is the **communication medium between models**.

## Initial dataset

The first 12 samples cover:

- one-, two-, and three-hop deduction;
- explicit negative conclusions;
- unknown under an open-world assumption;
- conjunction;
- negative premises;
- binary relation joins;
- rule direction;
- no contraposition;
- distractors.

The benchmark should remain small until failures tell us which semantic features are actually missing.

## Measurements

For each run:

- answer accuracy;
- proof depth;
- wire bytes;
- sender input/output tokens;
- receiver input/output tokens;
- protocol instruction overhead;
- parse failure rate;
- symbolic-vs-LLM receiver gap.

The most informative early comparison is:

```text
english / LLM
json    / LLM
msp     / LLM
msp     / symbolic
```

across the same sender models.

## Success signal

MSP is interesting if it can simultaneously show:

1. high symbolic execution accuracy;
2. high cross-model LLM reasoning accuracy;
3. lower warm communication rate than concise English / structured JSON;
4. manageable cold-start protocol overhead;
5. stable performance as proof depth increases.

## Failure signal

A useful negative result would be:

- MSP parses cleanly but receiver LLMs reason worse than from concise English;
- JSON matches MSP at effectively the same rate;
- sender formalization errors dominate;
- gains vanish beyond trivial one-hop rules.

Any of those outcomes should change the design before more features are added.


## Shared symbol table

The controlled benchmark gives both endpoints a small shared symbol table containing only:

- predicate names and arities;
- constant/entity identifiers.

Example:

```text
Predicates: red/1, hot/1, unsafe/1
Constants: key
```

The table does **not** reveal facts, rules, the query, or the answer.

This prevents lexical choices such as `unsafe` vs `dangerous` from being mis-scored as logical failures. It is also an explicit prototype of MSP's shared semantic-atom dictionary.

The harness records `vocabulary_bytes` separately. In a warm/shared-dictionary regime those bytes can be amortized; in a cold-start comparison they must be counted.
