# Chemical OCSR

[PatentLSBench](https://github.com/patsnap/PatentLSBench#简体中文) · [English](README.md) | **简体中文** · [评价协议](../docs/evaluation-protocol.zh.md)

Chemical OCSR 评价化学结构图像中的分子识别能力，以及单页 PDF 中化学结构区域的定位与识别能力。

## 输入与输出

| 模式 | 输入 | 输出 |
| --- | --- | --- |
| 图像 | 化学结构图像 | 机器可读分子结构 |
| PDF | 单页 PDF | 化学结构区域边界框及识别出的分子结构 |

分子结构保留原子连接关系、键信息与立体化学信息。

## 评价

| 层级 | 适用模式 | 匹配依据 | 指标 |
| --- | --- | --- | --- |
| Layout | PDF | 化学结构区域边界框的一对一 IoU 匹配 | Precision、Recall、F1 |
| OCSR | 图像与 PDF | 识别结构与参考结构的完整 InChIKey 匹配 | Precision、Recall、F1 |

PDF 模式分别报告 Layout 定位与 OCSR 识别指标。Layout 覆盖已标注的化学结构区域，分子识别基于具有有效完整 InChIKey 的完整结构参考计分。相同结构在不同位置的重复出现保留其次数。

## 许可证

参见[项目许可说明](https://github.com/patsnap/PatentLSBench#许可证)和 [MIT License](../LICENSE)。
