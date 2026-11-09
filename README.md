<p align="center">
  <img src="assets/brand-logos.svg" alt="LSBench and PatSnap" width="572">
</p>

<h1 align="center">LSBench</h1>

[English](#english) | [简体中文](#简体中文)

## English

LSBench evaluates large language models and AI agents on professional life-science tasks, including chemical entity recognition, chemical structure recognition, structure–activity extraction, lead candidate analysis, and research synthesis.

**Life-science task evaluation · Chemical recognition · Patent evidence · Research synthesis**

[GitHub](https://github.com/patsnap/LSBench#english) | [🤗 Hugging Face](https://huggingface.co/datasets/PatSnap/lsbench#english)

### Core evaluation tasks

| Task | Input | Output |
| --- | --- | --- |
| [Chemical NER](chemical-ner/README.md) | Patent claims or description text | Chemical names and molecular structure sets |
| [Chemical OCSR](chemical-ocsr/README.md) | Chemical structure image or single-page PDF | Molecular structures; PDF mode also includes chemical-region boxes |
| [SAR](sar/README.md) | Small-molecule patent materials | Activity records linked to structures and evidence locations |
| [LCA](lca/README.md) | A patent identifier or drug code | Candidate molecules, relevant patents and supporting evidence |
| [LS Research](ls-research/README.md) | A research question | An answer or report with source citations |

### Capability expansion

LSBench will expand to integrated chemical-information workflows, sequence and modification profiling, macromolecule sequence–activity evidence, competitive landscape and asset comparison, and agent execution behavior.

### Evaluation

| Task | Evaluation criteria |
| --- | --- |
| Chemical NER | Name-set and molecular structure-set precision, recall and F1, reported separately |
| Chemical OCSR | Image: InChIKey recognition P/R/F1. PDF: Layout IoU matching and OCSR InChIKey recognition P/R/F1, reported separately |
| SAR | Field-level and aligned record-group precision, recall and F1 |
| LCA | Patent relevance, complete-structure hits and evidence support; patent and drug-code modes reported separately |
| LS Research | Key-point coverage, factual quality and citation support |

Each task reports its own metrics, coverage and uncertainty. Models and agents are compared within their respective tracks using consistent materials, tool scope and budgets. See the [evaluation protocol](docs/evaluation-protocol.md) for task-specific definitions.

### Directory structure

| Path | Contents |
| --- | --- |
| `README.md` | Bilingual project overview |
| `README.zh.md` | Chinese overview |
| `<task>/README.md` / `README.zh.md` | English / Chinese task documentation |
| `docs/evaluation-protocol.md` / `evaluation-protocol.zh.md` | English / Chinese evaluation protocol |
| `LICENSE` | Code and project documentation license |

### Citation

```bibtex
@misc{patsnap_lsbench_2026,
  title  = {LSBench},
  author = {PatSnap},
  year   = {2026},
  url    = {https://github.com/patsnap/LSBench}
}
```

### License

Code and project documentation are licensed under the [MIT License](LICENSE). Datasets, annotations and accompanying materials use [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/), subject to the applicable terms and rights of third-party source materials.

Copyright (c) 2026 PatSnap.

## 简体中文

[English](#english) | **简体中文**

LSBench 用于评测大语言模型与 AI Agent 的生命科学专业任务能力，涵盖化学实体识别、化学结构识别、结构—活性关系抽取、先导候选分析与科研证据综合。

**生命科学专业任务评测 · 化学信息识别 · 专利证据分析 · 科研问题研究**

[GitHub](https://github.com/patsnap/LSBench#简体中文) | [🤗 Hugging Face](https://huggingface.co/datasets/PatSnap/lsbench#简体中文)

### 核心评测任务

| 任务 | 输入 | 交付 |
| --- | --- | --- |
| [Chemical NER](chemical-ner/README.zh.md) | 专利权利要求或说明书文本 | 化学名称与分子结构集合 |
| [Chemical OCSR](chemical-ocsr/README.zh.md) | 化学结构图像或单页 PDF | 分子结构；PDF 模式另含化学结构区域框 |
| [SAR](sar/README.zh.md) | 小分子专利材料 | 关联结构与证据位置的活性记录 |
| [LCA](lca/README.zh.md) | 专利号或药物代号 | 候选分子、相关专利与支持证据 |
| [LS Research](ls-research/README.zh.md) | 研究问题 | 完整回答或报告及来源引用 |

### 能力扩展

LSBench 将持续扩展化学信息联合交付、序列与修饰档案、大分子序列—活性证据整理、竞争格局与资产对标，并逐步纳入 Agent 执行行为评价。

### 评价方式

| 任务 | 评价对象与指标 |
| --- | --- |
| Chemical NER | 名称集合与分子结构集合 Precision、Recall、F1，分别报告 |
| Chemical OCSR | 图像：InChIKey 识别 P/R/F1；PDF：Layout IoU 匹配与 OCSR InChIKey 识别分别报告 P/R/F1 |
| SAR | 记录对齐后的字段级与记录组 Precision、Recall、F1 |
| LCA | 专利相关性、完整结构命中与证据支持；专利号和药物代号模式分别报告 |
| LS Research | 要点覆盖、事实质量与引用支持 |

各任务分别报告指标、覆盖范围与不确定性。模型与 Agent 按同类型比较，使用一致的任务材料、工具范围与预算。具体口径见[评价协议](docs/evaluation-protocol.zh.md)。

### 目录结构

| 路径 | 内容 |
| --- | --- |
| `README.md` | 中英文项目总览 |
| `README.zh.md` | 中文总览 |
| `<task>/README.md` / `README.zh.md` | 英文 / 中文任务说明 |
| `docs/evaluation-protocol.md` / `evaluation-protocol.zh.md` | 英文 / 中文评价协议 |
| `LICENSE` | 代码与项目文档许可证 |

### 引用

```bibtex
@misc{patsnap_lsbench_2026,
  title  = {LSBench},
  author = {PatSnap},
  year   = {2026},
  url    = {https://github.com/patsnap/LSBench}
}
```

### 许可证

代码和项目文档采用 [MIT 许可证](LICENSE)。数据集、标注及配套材料采用 [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)，第三方材料保留其来源条款与权利约束。

Copyright (c) 2026 PatSnap.
