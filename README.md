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
| [Chemical NER](chemical-ner/README.md) | Whole patent text | Chemical names and molecular structure sets |
| [Chemical OCSR](chemical-ocsr/README.md) | Pre-cropped chemical structure images | Complete molecular structures |
| [SAR](sar/README.md) | A complete small-molecule patent | Activity records linked to structures and evidence locations |
| [LCA](lca/README.md) | A patent identifier or drug code | Candidate molecules, relevant patents and supporting evidence |
| [Hiro LS Research](hiro-ls-research/README.md) | A research question | An answer or report with source citations |

### Capability expansion

LSBench will expand to integrated chemical-information workflows, sequence and modification profiling, macromolecule sequence–activity evidence, competitive landscape and asset comparison, and agent execution behavior.

### Evaluation

| Task | Evaluation criteria |
| --- | --- |
| Chemical NER | Patent-level set precision, recall and F1; names and structures scored separately |
| Chemical OCSR | Page-grouped, one-to-one complete-structure precision, recall and F1; repeated occurrences retained |
| SAR | Field and relationship precision, recall and F1 after record alignment |
| LCA | Patent relevance, complete-structure hits and evidence support; patent and drug-code modes reported separately |
| Hiro LS Research | Key-point coverage, factual quality and citation support |

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
| [Chemical NER](chemical-ner/README.zh.md) | 整篇专利文本 | 化学名称与分子结构集合 |
| [Chemical OCSR](chemical-ocsr/README.zh.md) | 预裁化学结构图 | 完整分子结构 |
| [SAR](sar/README.zh.md) | 完整小分子专利 | 关联结构与证据位置的活性记录 |
| [LCA](lca/README.zh.md) | 专利号或药物代号 | 候选分子、相关专利与支持证据 |
| [Hiro LS Research](hiro-ls-research/README.zh.md) | 研究问题 | 完整回答或报告及来源引用 |

### 能力扩展

LSBench 将持续扩展化学信息联合交付、序列与修饰档案、大分子序列—活性证据整理、竞争格局与资产对标，并逐步纳入 Agent 执行行为评价。

### 评价方式

| 任务 | 评价对象与指标 |
| --- | --- |
| Chemical NER | 专利级集合 Precision、Recall、F1；名称与结构分别计分 |
| Chemical OCSR | 页内一对一完整结构匹配 Precision、Recall、F1；保留重复结构次数 |
| SAR | 记录对齐后的字段与关系 Precision、Recall、F1 |
| LCA | 专利相关性、完整结构命中与证据支持；专利号和药物代号模式分别报告 |
| Hiro LS Research | 要点覆盖、事实质量与引用支持 |

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
