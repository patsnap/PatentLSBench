<p align="center">
  <img src="assets/brand-logos.svg" alt="PatentLSBench and PatSnap" width="704">
</p>

<h1 align="center">PatentLSBench</h1>

[English](README.md) | **简体中文**

**基于专利证据的生命科学模型与 Agent 评测基准**

PatentLSBench 以专利证据为基础，评测大语言模型与 AI Agent 的生命科学专业任务能力。

[GitHub](https://github.com/patsnap/PatentLSBench/blob/main/README.zh.md) | [🤗 Chemical NER](https://huggingface.co/datasets/PatSnap/chemical-ner-bench/blob/main/README.zh.md) | [🤗 Chemical OCSR](https://huggingface.co/datasets/PatSnap/chemical-ocsr-bench/blob/main/README.zh.md)

## 评测任务

| 任务 | 输入 | 交付 | 资源 |
| --- | --- | --- | --- |
| [Chemical NER](chemical-ner/README.zh.md) | 专利权利要求或说明书文本 | 化学实体及关联分子结构 | [测试数据](chemical-ner/data/test.jsonl) |
| [Chemical OCSR](chemical-ocsr/README.zh.md) | 化学结构图像或单页 PDF | 分子结构；PDF 模式另含化学结构区域框 | [测试数据](chemical-ocsr/data/test.jsonl) |
| [SAR](sar/README.zh.md) | 小分子专利材料 | 关联结构与证据位置的活性记录 | 任务定义 |
| [LCA](lca/README.zh.md) | 专利号或药物代号 | 候选分子、相关专利与支持证据 | 任务定义 |
| [LS Research](ls-research/README.zh.md) | 研究问题 | 完整回答或报告及来源引用 | 任务定义 |

## 数据集

Chemical NER 与 Chemical OCSR 在 GitHub 和 Hugging Face 均提供数据，核心记录、参考答案与源附件一致；Hugging Face 另提供 Parquet 视图，各数据集使用独立仓库与版本。SAR、LCA 与 LS Research 提供任务定义。

- **Chemical NER v1.2.2：**11个专利公开号、22条完整权利要求或说明书输入、6,334处实体参考提及，涵盖中文、英文、日文和韩文。
- **Chemical OCSR v1.0.0：**50个单页栅格PDF、536个已标注化学区域、277个MOL参考，以及272对SMILES/InChIKey参考。

## 评价

各任务README说明输入、输出与评价口径。报告明确被评系统、数据集与参考版本、匹配或评分量规标准、评价单位、覆盖范围与局限。同类模型或Agent组内比较采用一致的任务材料、证据范围、信息截止时点、可用工具与执行预算。各任务分项报告成绩，PatentLSBench不合成跨任务总分。

## 能力扩展

PatentLSBench 将持续扩展化学信息联合交付、序列与修饰档案、大分子序列—活性证据整理、竞争格局与资产对标，并逐步纳入 Agent 执行行为评价。

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

代码与项目文档采用 [MIT 许可证](LICENSE)。数据集、标注及配套附件采用 [CC BY-NC 4.0](LICENSE.data)，并受适用的第三方权利与来源特定条款约束。

Copyright (c) 2026 PatSnap.
