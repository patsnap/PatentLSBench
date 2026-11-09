# Chemical OCSR

[LSBench](https://github.com/patsnap/LSBench#简体中文) · [English](README.md) | **简体中文** · [评价协议](../docs/evaluation-protocol.zh.md)

Chemical OCSR 评价从化学结构图像中识别完整分子结构的能力。

## 输入

从专利页面中预裁的化学结构图像。

## 输出

保留原子连接关系、键信息与立体化学信息的机器可读分子结构。

## 评价

- 按来源页分组，对预测结构与参考结构进行一对一匹配。
- 完整结构匹配的精确率（Precision）、召回率（Recall）与 F1。
- 保留同一页面中相同结构重复出现的次数。

输入裁图数与参考结构数属于不同的评价单位。本任务评价预裁图的结构识别；整页检测与切分需单独评价。

## 许可证

参见[项目许可说明](https://github.com/patsnap/LSBench#许可证)和 [MIT License](../LICENSE)。
