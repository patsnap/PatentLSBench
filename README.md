<p align="center">
  <img src="assets/brand-logos.svg" alt="PatentLSBench and PatSnap" width="704">
</p>

<h1 align="center">PatentLSBench</h1>

**English** | [简体中文](README.zh.md)

PatentLSBench evaluates large language models and AI agents on life-science tasks grounded in patent evidence, including chemical entity recognition, chemical structure recognition, structure–activity extraction, lead candidate analysis, and research synthesis.

**A Patent-Grounded Benchmark for Life Science Models and Agents**

[GitHub](https://github.com/patsnap/PatentLSBench) | [🤗 Chemical NER](https://huggingface.co/datasets/PatSnap/chemical-ner-bench) | [🤗 Chemical OCSR](https://huggingface.co/datasets/PatSnap/chemical-ocsr-bench)

## Core evaluation tasks

| Task | Input | Output | Resources |
| --- | --- | --- | --- |
| [Chemical NER](chemical-ner/README.md) | Patent claims or description text | Chemical entities and associated molecular structures | [Test data](chemical-ner/data/test.jsonl) |
| [Chemical OCSR](chemical-ocsr/README.md) | Chemical structure image or single-page PDF | Molecular structures; PDF mode also includes chemical-region boxes | [Data and assets](chemical-ocsr/data/README.md) |
| [SAR](sar/README.md) | Small-molecule patent materials | Activity records linked to structures and evidence locations | Task definition |
| [LCA](lca/README.md) | A patent identifier or drug code | Candidate molecules, relevant patents and supporting evidence | Task definition |
| [LS Research](ls-research/README.md) | A research question | An answer or report with source citations | Task definition |

## Available datasets

Chemical NER and Chemical OCSR provide data in this GitHub repository and on Hugging Face. Both platforms contain the same core records, references and source assets; Hugging Face also provides Parquet views. SAR, LCA and LS Research currently provide task definitions, with datasets to follow in separate releases.

[Chemical NER v1.2.2](chemical-ner/README.md) contains **22 complete claim or description inputs from 11 patent publications, with 6,334 entity reference mentions** in Chinese, English, Japanese and Korean. Read the [JSONL](chemical-ner/data/test.jsonl) locally or use the [Hugging Face dataset](https://huggingface.co/datasets/PatSnap/chemical-ner-bench). Reference applicability is described in the [reference notes](chemical-ner/REFERENCE_NOTES.md).

[Chemical OCSR v1.0.0](chemical-ocsr/README.md) contains **50 single-page raster PDFs, 536 annotated chemical regions, 277 MOL references and 272 paired SMILES/InChIKey references**. The PDFs have no embedded text layer. The [GitHub data directory](chemical-ocsr/data/README.md) includes the PDF inputs, crops and molecular references; [Hugging Face](https://huggingface.co/datasets/PatSnap/chemical-ocsr-bench) provides page, region and molecular-reference views.

## Capability expansion

PatentLSBench will expand to integrated chemical-information workflows, sequence and modification profiling, macromolecule sequence–activity evidence, competitive landscape and asset comparison, and agent execution behavior.

## Evaluation

| Task | Evaluation criteria |
| --- | --- |
| Chemical NER | Entity-recognition and structure-normalization precision, recall and F1, reported separately with declared matching units |
| Chemical OCSR | Image: InChIKey recognition P/R/F1. PDF: Layout IoU matching and OCSR InChIKey recognition P/R/F1, reported separately |
| SAR | Field-level and aligned record-group precision, recall and F1 |
| LCA | Patent relevance, complete-structure hits and evidence support; patent and drug-code modes reported separately |
| LS Research | Key-point coverage, factual quality and citation support |

Each task reports its own metrics, coverage and uncertainty. Models and agents are compared within their respective tracks using consistent materials, tool scope and budgets. See the [evaluation protocol](docs/evaluation-protocol.md) for task-specific definitions.

## Directory structure

| Path | Contents |
| --- | --- |
| `README.md` | English project overview |
| `README.zh.md` | Chinese overview |
| `<task>/README.md` / `README.zh.md` | English / Chinese task documentation |
| `chemical-ner/data/test.jsonl` | Chemical NER section inputs and entity references |
| `chemical-ner/schema.json`, `load_records.py` | NER schema and standard-library reader |
| `chemical-ocsr/data/` | OCSR JSONL records, PDF/image/MOL assets, schema and protocols |
| `docs/evaluation-protocol.md` / `evaluation-protocol.zh.md` | English / Chinese evaluation protocol |
| `LICENSE` | Code and project documentation license |

## Citation

```bibtex
@misc{patsnap_patentlsbench_2026,
  title  = {PatentLSBench},
  author = {PatSnap},
  year   = {2026},
  url    = {https://github.com/patsnap/PatentLSBench}
}
```

## License

Code and project documentation are licensed under the [MIT License](LICENSE). Datasets, annotations and accompanying materials use [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/), subject to the applicable terms and rights of third-party source materials.

Copyright (c) 2026 PatSnap.
