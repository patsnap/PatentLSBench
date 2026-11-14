# Chemical NER

[PatentLSBench](https://github.com/patsnap/PatentLSBench/blob/main/README.zh.md) · [English](README.md) | **简体中文** · [评价协议](../docs/evaluation-protocol.zh.md)

Chemical NER 评价从专利权利要求或说明书文本中抽取化学名称及其对应分子结构的能力。

## 输入

专利的权利要求或说明书文本。

## 输出

从给定文本中识别的化学名称及其对应分子结构。

## 评价

- 化学名称集合的精确率（Precision）、召回率（Recall）与 F1。
- 分子结构集合的精确率（Precision）、召回率（Recall）与 F1，与名称成绩分别报告。
- 同一名称或结构重复出现时，在对应集合中计为一项。

匹配范围限定于给定的权利要求或说明书。

## 许可证

参见[项目许可说明](https://github.com/patsnap/PatentLSBench/blob/main/README.zh.md#许可证)和 [MIT License](../LICENSE)。
