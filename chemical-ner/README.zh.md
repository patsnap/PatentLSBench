# Chemical NER

[LSBench](https://github.com/patsnap/LSBench#简体中文) · [English](README.md) | **简体中文** · [评价协议](../docs/evaluation-protocol.zh.md)

Chemical NER 评价从完整专利文本中抽取化学名称与分子结构的能力。

## 输入

化学专利的完整文本。

## 输出

化学名称及其对应的分子结构，以专利级集合表示。

## 评价

- 专利级集合的精确率（Precision）、召回率（Recall）与 F1。
- 化学名称与分子结构分别报告成绩。
- 同一专利中重复出现的相同结构去重。
- 对不含分子结构的参考标注，采用名称匹配回退。

评价单位为专利。

## 许可证

参见[项目许可说明](https://github.com/patsnap/LSBench#许可证)和 [MIT License](../LICENSE)。
