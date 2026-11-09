<p align="center">
  <img src="assets/brand-logos.svg" alt="LSBench and PatSnap" width="572">
</p>

<h1 align="center">LSBench</h1>

**English** | [简体中文](README.zh.md)

LSBench evaluates large language models and AI agents on professional life-science tasks, including chemical entity recognition, chemical structure recognition, structure–activity extraction, lead candidate analysis, and research synthesis.

**Life-science task evaluation · Chemical recognition · Patent evidence · Research synthesis**

[GitHub](https://github.com/patsnap/LSBench) | [🤗 Hugging Face](https://huggingface.co/datasets/PatSnap/lsbench)

## Core evaluation tasks

| Task | Input | Output |
| --- | --- | --- |
| [Chemical NER](chemical-ner/README.md) | Whole patent text | Chemical names and molecular structure sets |
| [Chemical OCSR](chemical-ocsr/README.md) | Pre-cropped chemical structure images | Complete molecular structures |
| [SAR](sar/README.md) | A complete small-molecule patent | Activity records linked to structures and evidence locations |
| [LCA](lca/README.md) | A patent identifier or drug code | Candidate molecules, relevant patents and supporting evidence |
| [Hiro LS Research](hiro-ls-research/README.md) | A research question | An answer or report with source citations |

## Capability expansion

LSBench will expand to integrated chemical-information workflows, sequence and modification profiling, macromolecule sequence–activity evidence, competitive landscape and asset comparison, and agent execution behavior.

## Evaluation

| Task | Evaluation criteria |
| --- | --- |
| Chemical NER | Patent-level set precision, recall and F1; names and structures scored separately |
| Chemical OCSR | Page-grouped, one-to-one complete-structure precision, recall and F1; repeated occurrences retained |
| SAR | Field and relationship precision, recall and F1 after record alignment |
| LCA | Patent relevance, complete-structure hits and evidence support; patent and drug-code modes reported separately |
| Hiro LS Research | Key-point coverage, factual quality and citation support |

Each task reports its own metrics, coverage and uncertainty. Models and agents are compared within their respective tracks using consistent materials, tool scope and budgets. See the [evaluation protocol](docs/evaluation-protocol.md) for task-specific definitions.

## Directory structure

| Path | Contents |
| --- | --- |
| `README.md` / `README.zh.md` | English / Chinese overview |
| `<task>/README.md` | Task definition, inputs, outputs and evaluation |
| `docs/evaluation-protocol.md` | Shared evaluation conditions and task-specific criteria |
| `LICENSE` | Code and project documentation license |

## Citation

```bibtex
@misc{patsnap_lsbench_2026,
  title  = {LSBench},
  author = {PatSnap},
  year   = {2026},
  url    = {https://github.com/patsnap/LSBench}
}
```

## License

Code and project documentation are licensed under the [MIT License](LICENSE). Datasets, annotations and accompanying materials use [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/), subject to the applicable terms and rights of third-party source materials.

Copyright (c) 2026 PatSnap.
