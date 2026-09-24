# Evaluation Harness Survey

The goal was not to find the largest benchmark framework. It was to find the smallest existing substrate that prevents us from rebuilding provider adapters, token accounting, logging, retries, model roles, and result analysis.

## Inspect AI — adopted substrate

https://inspect.aisi.org.uk/

Why it fits:
- explicit `Task = dataset + solver + scorer` model;
- named model roles, which maps directly to sender / receiver / grader experiments;
- OpenAI, Anthropic, Google, OpenRouter, local and OpenAI-compatible model support;
- per-model token usage including cached and reasoning-token fields when providers expose them;
- cost and token limits;
- structured eval logs and dataframe analysis;
- custom deterministic scorers;
- transcript/store instrumentation.

MSP therefore builds a thin task on Inspect rather than a second evaluation framework.

## EleutherAI lm-evaluation-harness — reference, not dependency

https://github.com/EleutherAI/lm-evaluation-harness

Excellent for standardized academic LM benchmarks, reproducible task definitions, model backends, and leaderboard-style evaluation. Its abstraction is primarily "evaluate one LM on a task," whereas MSP's first-class object is a two-endpoint communication channel.

Useful ideas to borrow:
- version task definitions;
- preserve sample-level outputs;
- treat tokenizer/model backend as explicit configuration;
- keep task configuration reproducible.

## Hugging Face LightEval — reference, not dependency

https://github.com/huggingface/lighteval

Strong modern multi-backend evaluator with 1000+ tasks, custom metrics, sample-level results, and LiteLLM/provider support.

It is attractive for ordinary model intelligence benchmarking. MSP still needs custom sender/receiver orchestration, so adopting it would not remove as much custom code as Inspect's model-role and solver abstractions do.

## Promptfoo — useful operational baseline

https://www.promptfoo.dev/

Promptfoo directly reports latency, input/output tokens, estimated cost, errors, and assertion results. It is excellent for lightweight prompt/application regression testing.

We should borrow its practical reporting mindset. We do not need to make it the core research runtime because semantic-transfer experiments need role-aware multi-call sample state and custom scientific scoring.

## HELM — methodology reference

https://github.com/stanford-crfm/helm

HELM emphasizes standardized scenarios, broad metrics, transparency, and reproducibility across providers. It entered maintenance mode on June 1, 2026, so it should be treated as a methodology/reference source rather than a new dependency.

Useful idea: report efficiency alongside capability rather than collapsing everything into one score.

## OpenAI Evals — design reference

https://github.com/openai/evals

Useful precedent for dataset-driven custom evals, recorders, metrics, completion functions, and model-graded evaluation.

MSP's initial semantic-transfer benchmark intentionally avoids model grading: the receiver emits canonical structured semantics and a deterministic scorer compares it with ground truth.

## Decision

Use **Inspect AI** for execution and logs.

Keep MSP-owned code limited to:
- protocol definitions;
- sender/receiver prompts;
- semantic fixtures;
- deterministic semantic normalization/scoring;
- analysis specific to communication rate.

Do not build:
- provider SDK adapters;
- retry/concurrency infrastructure;
- generic eval registries;
- generic dashboards;
- generic model-grading frameworks.
