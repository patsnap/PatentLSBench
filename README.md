<p align="center">
  <img src="assets/brand-logos.svg" alt="PatentLSBench and PatSnap" width="704">
</p>

<h1 align="center">PatentLSBench</h1>

**English** | [简体中文](README.zh.md)

**A Patent-Grounded Benchmark for Life Science Models and Agents**

PatentLSBench evaluates large language models and AI agents on life-science tasks grounded in patent evidence.

[GitHub](https://github.com/patsnap/PatentLSBench) | [🤗 Chemical NER](https://huggingface.co/datasets/PatSnap/chemical-ner-bench) | [🤗 Chemical OCSR](https://huggingface.co/datasets/PatSnap/chemical-ocsr-bench)

## Evaluation tasks

| Task | Input | Output | Resources |
| --- | --- | --- | --- |
| [Chemical NER](chemical-ner/README.md) | Patent claims or description text | Chemical entities and associated molecular structures | [Test data](chemical-ner/data/test.jsonl) |
| [Chemical OCSR](chemical-ocsr/README.md) | Chemical structure image or single-page PDF | Molecular structures; PDF mode also includes chemical-region boxes | [Test data](chemical-ocsr/data/test.jsonl) |

## Datasets

Chemical NER and Chemical OCSR provide datasets on GitHub and Hugging Face, with the same core records, references and source assets. Hugging Face also provides Parquet views, with each dataset maintained in a separate repository.

- **Chemical NER V1.0:** 11 patent publications, 22 complete claim or description inputs and 6,334 entity reference mentions, covering Chinese, English, Japanese and Korean.
- **Chemical OCSR V1.0:** 50 single-page raster PDFs, 536 annotated chemical regions, 277 MOL references and 272 paired SMILES/InChIKey references.

## Evaluation

Task READMEs describe the inputs, outputs and evaluation criteria. Reports identify the evaluated system, dataset and reference versions, matching or rubric criteria, evaluation units, coverage and limitations. Comparisons within model or agent tracks use consistent task materials, evidence scope, information cutoff, permitted tools and execution budgets. Scores are reported separately for each task; PatentLSBench defines no cross-task overall score.

## Capability expansion

Upcoming datasets: [SAR](sar/), [LCA](lca/) and [LS Research](ls-research/).

PatentLSBench will expand to integrated chemical-information workflows, sequence and modification profiling, macromolecule sequence–activity evidence, competitive landscape and asset comparison, and agent execution behavior.

## Citation

```bibtex
@misc{patsnap_patentlsbench_2026,
  title  = {PatentLSBench},
  author = {PatSnap},
  year   = {2026},
  url    = {https://github.com/patsnap/PatentLSBench}
}
```

## License and Disclaimer

Code and project documentation are licensed under the [MIT License](LICENSE). Datasets, annotations and accompanying assets are released under [CC BY-NC 4.0](LICENSE.data), subject to applicable third-party rights and separate source terms.

PatentLSBench materials and related outputs may contain errors or omissions and do not constitute legal, patent, medical or regulatory advice or professional certification. Users must review and validate them before relying on them, ensure they have the necessary rights to process materials, and comply with applicable licenses and access terms; see the [full disclaimer](DISCLAIMER.md).

Copyright (c) 2026 PatSnap.
