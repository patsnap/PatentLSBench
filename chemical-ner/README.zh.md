# Chemical NER

[PatentLSBench](https://github.com/patsnap/PatentLSBench/blob/main/README.zh.md) · [English](README.md) | **简体中文** · [评价协议](../docs/evaluation-protocol.zh.md)

Chemical NER Bench 提供完整专利权利要求与说明书，用于化学实体识别和结构归一化，并包含实体级评测参考答案及分子结构标识。

[🤗 数据集](https://huggingface.co/datasets/PatSnap/chemical-ner-bench/blob/main/README.zh.md) · [数据文件](https://huggingface.co/datasets/PatSnap/chemical-ner-bench/tree/main)

## 数据集概览

**v1.2.1** 包含以下数据：

| 资源 | 数量 |
| --- | --- |
| 专利公开号 | 11 |
| 完整章节输入 | 22 |
| 权利要求 / 说明书输入 | 11 / 11 |
| 实体参考提及 | 6,334 |
| 实体参考列表为空的输入 | 3 |

覆盖中文、英语、日语和韩语，中文包括繁体文本。

| 语言 | 编码 | 章节数 |
| --- | --- | --- |
| 中文 | `CN` | 8 |
| 繁体中文 | `CNT` | 2 |
| 英语 | `EN` | 6 |
| 日语 | `JP` | 4 |
| 韩语 | `KR` | 2 |

## 输入与参考答案

每条记录是一份完整的 `claim`（权利要求章节）或 `description`（说明书章节），各章节独立作为输入。模型输入包含 `record_id`、`publication_number`、`language`、`section` 和 `text` 五个字段。`ground_truth` 为实体级评测参考答案，用于与模型预测比较。

## 字段

| 记录字段 | 业务含义 |
| --- | --- |
| `record_id` | 章节记录的唯一标识。 |
| `publication_number` | 本条章节所属专利的公开号。 |
| `language` | 章节语言代码：CN＝中文，CNT＝繁体中文，EN＝英文，JP＝日文，KR＝韩文。 |
| `section` | 章节类型：claim＝完整权利要求章节；description＝完整说明书章节。 |
| `text` | 完整权利要求章节或说明书章节的HTML文本。 |
| `ground_truth` | 实体级评测参考答案列表，每个对象对应一处实体提及；无参考实体时为[]。 |

| 实体字段 | 业务含义 |
| --- | --- |
| `start` | 实体在本条text中的起始位置，包含该位置；从0开始，按Unicode码点计数，HTML标签字符也计入。 |
| `end` | 实体在本条text中的结束位置，不包含该位置；与start构成左闭右开区间。 |
| `text` | 实体在章节中的名称文本。 |
| `label` | 化学实体类别编码。ChemicalCompound与compound均表示化学实体，不区分化学对象子类。 |
| `smiles` | 实体结构的SMILES参考表示；空字符串表示无可用的SMILES参考。 |
| `inchikey` | 实体结构的InChIKey参考标识；空字符串表示无可用的InChIKey参考。 |
| `mention_form` | 实体名称在文本中的表达类型，取值含义见下表；null表示无名称表达类型信息。 |

`ChemicalCompound` 与 `compound` 都表示化学实体，不表示不同的化学对象子类。`text` 为完整章节 HTML；坐标按全部 HTML 字符的 Unicode 码点计数，使用从 0 开始、左闭右开的 `[start, end)` 区间。

`ground_truth = []` 表示该章节无参考实体。结构字段的空字符串表示无对应结构参考，`mention_form = null` 表示无名称表达类型信息。

## 名称表达类型

| 取值 | 名称 | 含义 |
| --- | --- | --- |
| `SYSTEMATIC_NAME` | 全称 | 全称或明确结构名称，包括IUPAC名称及能确定化学身份的短名称。 |
| `TRIVIAL_COMMON_NAME` | 俗名 | 化合物惯用名、药物通用名或明确指向单一成分的商品名。 |
| `UNAMBIGUOUS_ABBREVIATION` | 缩写 | 当前语境中化学身份明确的名称缩写，例如DMSO、DCM。研发代码、编号和氨基酸序列符号不属于此类。 |
| `UNAMBIGUOUS_FORMULA` | 结构简式 | 化学身份明确的结构简式或元素符号，例如CH3COOH、Cu；不能确定具体结构的分子式不属于此类。 |
| `null` | 无类型信息 | 无名称表达类型信息。 |

[完整 Schema](https://huggingface.co/datasets/PatSnap/chemical-ner-bench/blob/main/raw/schema.json)定义字段类型、可选值与必填规则。

## 评价

实体参考答案支持名称、化学实体类别和边界比对；结构归一化使用所选结构字段中适用的非空参考值。名称识别与结构归一化的 Precision、Recall、F1 分别报告。

报告须明确匹配单位与条件、去重规则、结构参考纳入条件和覆盖范围、聚合方式及零分母处理。权利要求与说明书结果分开呈现。提及数、名称数和结构数分别计数；结构参考为空的实体仍参与适用的名称识别评价。

具体要求见[评价说明](https://huggingface.co/datasets/PatSnap/chemical-ner-bench/blob/main/EVALUATION.zh.md)。

## 配置与使用

Hugging Face 提供 `default` 配置，`test` split 含 22 条记录。使用具有仓库访问权限的 HF 账号登录：

```bash
hf auth login
```

```python
from datasets import load_dataset

records = load_dataset("PatSnap/chemical-ner-bench", split="test", token=True)
input_fields = [
    "record_id", "publication_number", "language", "section", "text"
]
model_inputs = records.select_columns(input_fields)
model_input = model_inputs[0]
```

`ground_truth` 单独用于评价，不进入模型请求。

## 引用与许可证

```bibtex
@dataset{patsnap_chemical_ner_bench_2026,
  title   = {Chemical NER Bench},
  author  = {PatSnap},
  year    = {2026},
  version = {1.2.1},
  url     = {https://huggingface.co/datasets/PatSnap/chemical-ner-bench}
}
```

数据集与参考答案采用 [CC BY-NC 4.0](https://huggingface.co/datasets/PatSnap/chemical-ner-bench/blob/main/LICENSE)，第三方材料保留其适用权利。读取器和项目文档采用 [MIT 许可证](../LICENSE)。
