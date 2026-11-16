<p align="center">
  <img src="assets/brand-logos.svg" alt="PatentLSBench and PatSnap" width="704">
</p>

<h1 align="center">PatentLSBench</h1>

[English](README.md) | **简体中文**

PatentLSBench 以专利证据为基础，评测大语言模型与 AI Agent 的生命科学专业任务能力，涵盖化学实体识别、化学结构识别、结构—活性关系抽取、先导候选分析与科研证据综合。

**基于专利证据的生命科学模型与 Agent 评测基准**

[GitHub](https://github.com/patsnap/PatentLSBench/blob/main/README.zh.md) | [🤗 Chemical NER](https://huggingface.co/datasets/PatSnap/chemical-ner-bench/blob/main/README.zh.md) | [🤗 Chemical OCSR](https://huggingface.co/datasets/PatSnap/chemical-ocsr-bench/blob/main/README.zh.md)

## 核心评测任务

| 任务 | 输入 | 交付 | 资源 |
| --- | --- | --- | --- |
| [Chemical NER](chemical-ner/README.zh.md) | 专利权利要求或说明书文本 | 化学实体及关联分子结构 | [测试数据](chemical-ner/data/test.jsonl) |
| [Chemical OCSR](chemical-ocsr/README.zh.md) | 化学结构图像或单页 PDF | 分子结构；PDF 模式另含化学结构区域框 | [数据与附件](chemical-ocsr/data/README.zh.md) |
| [SAR](sar/README.zh.md) | 小分子专利材料 | 关联结构与证据位置的活性记录 | 任务定义 |
| [LCA](lca/README.zh.md) | 专利号或药物代号 | 候选分子、相关专利与支持证据 | 任务定义 |
| [LS Research](ls-research/README.zh.md) | 研究问题 | 完整回答或报告及来源引用 | 任务定义 |

## 已提供的数据集

Chemical NER 与 Chemical OCSR 在本 GitHub 仓库及 Hugging Face 均提供数据，两端核心记录、参考答案与源附件一致；Hugging Face 另提供 Parquet 视图。SAR、LCA 与 LS Research 当前提供任务定义，数据将按独立版本陆续发布。

[Chemical NER v1.2.2](chemical-ner/README.zh.md) 包含 **11 个专利公开号的 22 条完整权利要求或说明书输入，以及 6,334 处实体参考提及**，涵盖中文、英文、日文和韩文。可读取本仓库 [JSONL](chemical-ner/data/test.jsonl)，或使用 [Hugging Face 数据集](https://huggingface.co/datasets/PatSnap/chemical-ner-bench/blob/main/README.zh.md)。参考答案的适用范围见[参考说明](chemical-ner/REFERENCE_NOTES.zh.md)。

[Chemical OCSR v1.0.0](chemical-ocsr/README.zh.md) 包含 **50 个单页栅格 PDF、536 个已标注化学区域、277 个 MOL 参考，以及 272 对 SMILES/InChIKey 参考**。PDF 不含嵌入式文本层。本仓库[数据目录](chemical-ocsr/data/README.zh.md)提供 PDF 输入、裁图与分子参考；[Hugging Face](https://huggingface.co/datasets/PatSnap/chemical-ocsr-bench/blob/main/README.zh.md)提供页面、区域与分子参考视图。

## 能力扩展

PatentLSBench 将持续扩展化学信息联合交付、序列与修饰档案、大分子序列—活性证据整理、竞争格局与资产对标，并逐步纳入 Agent 执行行为评价。

## 评价方式

| 任务 | 评价对象与指标 |
| --- | --- |
| Chemical NER | 实体识别与结构归一化 Precision、Recall、F1 分别报告，并明确匹配单位 |
| Chemical OCSR | 图像：InChIKey 识别 P/R/F1；PDF：Layout IoU 匹配与 OCSR InChIKey 识别分别报告 P/R/F1 |
| SAR | 记录对齐后的字段级与记录组 Precision、Recall、F1 |
| LCA | 专利相关性、完整结构命中与证据支持；专利号和药物代号模式分别报告 |
| LS Research | 要点覆盖、事实质量与引用支持 |

各任务分别报告指标、覆盖范围与不确定性。模型与 Agent 按同类型比较，使用一致的任务材料、工具范围与预算。具体口径见[评价协议](docs/evaluation-protocol.zh.md)。

## 目录结构

| 路径 | 内容 |
| --- | --- |
| `README.md` | 英文项目总览 |
| `README.zh.md` | 中文总览 |
| `<task>/README.md` / `README.zh.md` | 英文 / 中文任务说明 |
| `chemical-ner/data/test.jsonl` | Chemical NER 章节输入与实体参考答案 |
| `chemical-ner/schema.json`、`load_records.py` | NER 字段规范与标准库读取器 |
| `chemical-ocsr/data/` | OCSR JSONL、PDF/图像/MOL 附件、Schema 与协议 |
| `docs/evaluation-protocol.md` / `evaluation-protocol.zh.md` | 英文 / 中文评价协议 |
| `LICENSE` | 代码与项目文档许可证 |

## 引用

```bibtex
@misc{patsnap_patentlsbench_2026,
  title  = {PatentLSBench},
  author = {PatSnap},
  year   = {2026},
  url    = {https://github.com/patsnap/PatentLSBench}
}
```

## 许可证

代码和项目文档采用 [MIT 许可证](LICENSE)。数据集、标注及配套材料采用 [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)，第三方材料保留其来源条款与权利约束。

Copyright (c) 2026 PatSnap.
