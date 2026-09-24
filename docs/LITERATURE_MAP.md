# Literature Map

This document maps the research areas most relevant to a discrete semantic protocol for LLM-to-LLM communication.

## 1. Emergent communication and emergent language

### Foerster et al. — DIAL / RIAL (NeurIPS 2016)

**Learning to Communicate with Deep Multi-Agent Reinforcement Learning**

Agents learn communication protocols end-to-end in cooperative partially observable environments. DIAL permits differentiable communication during centralized training and discretizes messages for execution.

Relevance: establishes that useful non-natural communication protocols can be learned directly from task reward.

- Paper: https://papers.neurips.cc/paper_files/paper/2016/file/c7635bfd99248a2cdef8249ef7bfbef4-Paper.pdf
- arXiv: https://arxiv.org/abs/1605.06676

### Sukhbaatar et al. — CommNet (NeurIPS 2016)

**Learning Multiagent Communication with Backpropagation**

Introduces continuous inter-agent communication integrated into a neural network trained by backpropagation.

Relevance: early evidence that communication channels optimized for coordination need not resemble human language.

### Mordatch & Abbeel (AAAI 2018)

**Emergence of Grounded Compositional Language in Multi-Agent Populations**

Agents develop streams of abstract discrete symbols with identifiable vocabulary and syntax while solving grounded cooperative tasks.

Relevance: unusually close to the discrete, compositional portion of this project's hypothesis.

- DOI: https://doi.org/10.1609/aaai.v32i1.11492
- arXiv: https://arxiv.org/abs/1703.04908

### Lazaridou et al.

Work on referential games and multi-agent language emergence studies arbitrary symbols, grounding, compositionality, and pressures that cause protocols to become more or less language-like.

Relevance: important for understanding failure modes in learned discrete protocols.

### Kottur et al. (EMNLP 2017)

**Natural Language Does Not Emerge 'Naturally' in Multi-Agent Dialog**

Shows that successful agent communication can diverge sharply from natural language when only task success is optimized.

Relevance: direct warning that task-optimal communication may become brittle, uninterpretable, or non-compositional without explicit inductive pressures.

## 2. Latent communication between LLM agents

### Interlat — Du et al. (ACL 2026)

**Enabling Agents to Communicate Entirely in Latent Space**

Transfers final hidden-state sequences between agents and learns compression in latent space. The authors report substantial communication/inference speedups while retaining task performance.

Relevance: strongest modern evidence that natural-language serialization can be a bottleneck for LLM agents.

- ACL Anthology: https://aclanthology.org/2026.acl-long.1248/
- arXiv identifier reported by secondary indexes: 2511.09149

### Beyond Tokens — latent communication survey (2026)

Surveys a growing collection of methods that exchange embeddings, hidden states, or KV-cache representations. A useful taxonomy separates:
- **what** representation is communicated,
- **which** latent spaces/layers are aligned,
- **how** transmitted state is fused into the receiver.

Relevance: helps define what our proposed discrete IR deliberately does differently.

### StateBridge (2026)

Research on bridging heterogeneous model latent spaces.

Relevance: exposes a core portability problem of direct hidden-state communication: model A's representational geometry is not naturally model B's representational geometry. A discrete standard may provide a stable interface between those spaces.

## 3. Semantic communication

Semantic communication research asks whether a channel should preserve the original symbol sequence or instead preserve meaning / task utility.

Relevance: provides the information-theoretic framing for evaluating an LLM protocol by **decision-relevant information preserved per transmitted bit/token**, rather than textual similarity.

## 4. Discrete latent representations

Vector-quantized representations, learned codebooks, latent actions, and discrete bottlenecks are relevant because they show how continuous internal states can be mapped into reusable discrete symbols.

Open question for this project: can those symbols remain sufficiently stable and compositional to work across independently trained foundation models?

## 5. Formal and executable intermediate representations

Compiler IRs, bytecode, symbolic planners, RDF-like graphs, logical forms, AMR, semantic parsing, and typed serialization formats provide engineering lessons even though they were not designed as learned LLM communication languages.

Particularly useful properties:

- typed operators and operands;
- canonical serialization;
- explicit references;
- graph structure separate from wire order;
- version negotiation;
- extension namespaces;
- literal escape;
- deterministic parsing;
- graceful handling of unknown extensions.

## 6. Main gap we are investigating

Existing work often occupies one of these regions:

```text
human-readable natural language / structured text
                         ↕
                discrete learned codes
                         ↕
                continuous latent states
```

The target here is specifically:

> a **standardized, discrete, task-general semantic IR** that heterogeneous pretrained LLMs can learn to read/write and that can be serialized compactly independent of either model's internal representation.

That exact combination is the research gap this repository will test.

## Reading priorities

High priority:
1. emergent discrete protocols and compositionality;
2. latent LLM communication and heterogeneous alignment;
3. semantic communication metrics;
4. learned discrete bottlenecks/codebooks;
5. formal semantic representations and canonical IR design.

Secondary:
- neural compression;
- rate-distortion theory;
- pragmatic communication / Rational Speech Acts;
- information bottleneck methods;
- schema induction;
- program synthesis representations;
- agent protocol standards.
