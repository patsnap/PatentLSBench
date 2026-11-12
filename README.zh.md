<p align="center">
  <img src="assets/brand-logos.svg" alt="PatentLSBench and PatSnap" width="704">
</p>

<h1 align="center">PatentLSBench</h1>

[English](https://github.com/patsnap/PatentLSBench#english) | **简体中文**

PatentLSBench 以专利证据为基础，评测大语言模型与 AI Agent 的生命科学专业任务能力，涵盖化学实体识别、化学结构识别、结构—活性关系抽取、先导候选分析与科研证据综合。

**基于专利证据的生命科学模型与 Agent 评测基准**

[GitHub](https://github.com/patsnap/PatentLSBench#简体中文)

## 核心评测任务

| 任务 | 输入 | 交付 |
| --- | --- | --- |
| [Chemical NER](chemical-ner/README.zh.md) | 专利权利要求或说明书文本 | 化学名称与分子结构集合 |
| [Chemical OCSR](chemical-ocsr/README.zh.md) | 化学结构图像或单页 PDF | 分子结构；PDF 模式另含化学结构区域框 |
| [SAR](sar/README.zh.md) | 小分子专利材料 | 关联结构与证据位置的活性记录 |
| [LCA](lca/README.zh.md) | 专利号或药物代号 | 候选分子、相关专利与支持证据 |
| [LS Research](ls-research/README.zh.md) | 研究问题 | 完整回答或报告及来源引用 |

## 能力扩展

PatentLSBench 将持续扩展化学信息联合交付、序列与修饰档案、大分子序列—活性证据整理、竞争格局与资产对标，并逐步纳入 Agent 执行行为评价。

## 评价方式

| 任务 | 评价对象与指标 |
| --- | --- |
| Chemical NER | 名称集合与分子结构集合 Precision、Recall、F1，分别报告 |
| Chemical OCSR | 图像：InChIKey 识别 P/R/F1；PDF：Layout IoU 匹配与 OCSR InChIKey 识别分别报告 P/R/F1 |
| SAR | 记录对齐后的字段级与记录组 Precision、Recall、F1 |
| LCA | 专利相关性、完整结构命中与证据支持；专利号和药物代号模式分别报告 |
| LS Research | 要点覆盖、事实质量与引用支持 |

各任务分别报告指标、覆盖范围与不确定性。模型与 Agent 按同类型比较，使用一致的任务材料、工具范围与预算。具体口径见[评价协议](docs/evaluation-protocol.zh.md)。

## 目录结构

| 路径 | 内容 |
| --- | --- |
| `README.md` | 中英文项目总览 |
| `README.zh.md` | 中文总览 |
| `<task>/README.md` / `README.zh.md` | 英文 / 中文任务说明 |
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
