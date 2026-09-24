# Prior-Art Matrix

This is a working comparison, not a novelty determination.

| Work / area | Discrete | Continuous latent | Learned protocol | Compositionality focus | Cross-model by design | Inspectable | Relevance |
|---|---:|---:|---:|---:|---:|---:|---|
| DIAL / RIAL (Foerster et al., 2016) | partial | yes | yes | limited | no | partial | learned inter-agent protocols |
| CommNet (Sukhbaatar et al., 2016) | no | yes | yes | no | no | low | continuous learned communication |
| Mordatch & Abbeel (2018) | **yes** | no | yes | **yes** | no | moderate | abstract discrete vocabulary + syntax |
| Kottur et al. (2017) | yes | no | yes | **failure analysis** | no | moderate | task success does not imply compositional language |
| Resnick et al. (2020) | yes | no | yes | **yes** | no | moderate | bandwidth/capacity/compositionality |
| Peters et al. survey (2025) | **focus** | field coverage | — | **yes** | — | — | taxonomy and metrics for discrete emergent language |
| Interlat (Du et al., 2026) | no | **yes** | yes | no | requires adaptation | low | modern non-language LLM communication |
| Beyond Tokens survey (Liu, 2026) | mostly no | **yes** | varies | no | identifies alignment as an open challenge | low | taxonomy of latent communication |
| MSP hypothesis | **yes** | no on wire | hybrid | **required** | **primary objective** | partial | standardized semantic IR |

## What is not new

The following ideas individually have substantial prior art:

- agents inventing arbitrary symbols;
- discrete emergent languages;
- continuous learned communication;
- compressing inter-agent messages;
- semantic/task-oriented communication;
- compositional communication;
- structured semantic representations.

## Combination under test

The repository is investigating whether this particular combination is useful:

```text
discrete
+ task-general
+ compositional
+ standardized semantics
+ heterogeneous pretrained LLMs
+ model-independent wire representation
+ learnable in context
+ compact serialization
+ exact literal escape
```

The project should claim value only if this combination produces a measurable advantage over strong structured-language baselines.

## Key lessons

### Effective protocols need not be compositional

Kottur et al. report agent-invented protocols with high task performance that are nevertheless not naturally interpretable or compositional. We therefore need separate metrics for task utility and language structure.

Primary source: https://aclanthology.org/D17-1321/

### Bandwidth pressure is itself an experimental variable

Resnick et al. study how communication bandwidth and model capacity affect efficacy and compositionality.

Primary source: https://www.ifaamas.org/Proceedings/aamas2020/pdfs/p1125.pdf

### Discrete emergent-language evaluation already has a taxonomy

Peters et al. survey discrete emergent language and organize established/recent metrics.

DOI: https://doi.org/10.1007/s10458-025-09691-y  
arXiv: https://arxiv.org/abs/2409.02645

### Latent communication demonstrates the bottleneck but complicates interoperability

Interlat demonstrates useful communication through hidden states rather than natural-language messages. The broader 2026 latent-communication survey identifies cross-architecture alignment as an important challenge.

Interlat: https://aclanthology.org/2026.acl-long.1248/  
Survey: https://arxiv.org/abs/2606.05711
