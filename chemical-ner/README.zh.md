# Chemical NER Bench

[PatentLSBench](../README.zh.md) · [English](README.md) | **简体中文**

Chemical NER Bench 提供专利权利要求与说明书，用于**化学实体识别和结构归一化**。每条记录包含一份完整章节及所提供的实体参考答案。`test` split 可通过本仓库 [`data/test.jsonl`](data/test.jsonl) 或 [Hugging Face](https://huggingface.co/datasets/PatSnap/chemical-ner-bench/blob/main/README.zh.md) 获取。

## 数据集概览

| 项目 | V1.0 |
| --- | ---: |
| 专利公开号 | 11 |
| 完整章节输入 | 22 |
| 权利要求 / 说明书输入 | 11 / 11 |
| 实体参考提及 | 6,334 |

输入覆盖中文、英文、日文和韩文，中文包括繁体文本。每份权利要求或说明书独立作为输入；提及数、去重名称数和去重结构数分别计数。

## 数据字段

| 记录字段 | 类型 | 含义 |
| --- | --- | --- |
| `record_id` | string | 章节记录唯一标识 |
| `publication_number` | string | 来源专利公开号 |
| `language` | string | `CN`：中文；`CNT`：繁体中文；`EN`：英文；`JP`：日文；`KR`：韩文 |
| `section` | string | `claim`（权利要求）或 `description`（说明书） |
| `text` | string | 完整章节 HTML |
| `ground_truth` | list[object] | 所提供的实体参考提及；空列表为 `[]` |

| 实体字段 | 类型 | 含义 |
| --- | --- | --- |
| `start`、`end` | integer | 在本条 `text` 中的起始位置（含）与结束位置（不含） |
| `text` | string | 参考名称文本 |
| `label` | string | `ChemicalCompound` 与 `compound` 表示同一化学实体类别 |
| `smiles` | string | 所提供的 SMILES 参考；`""` 表示不可用 |
| `inchikey` | string | 所提供的 InChIKey 参考；`""` 表示不可用 |
| `mention_form` | string 或 null | 下表名称表达类型；null 表示无类型信息 |

坐标从 0 开始，采用左闭右开的 Unicode 码点区间 `[start, end)`，直接索引**包含标签字符的原始 HTML 字符串**。参考名称可能包含 HTML 标签或首尾空白；去除标签或裁剪名称空白会改变坐标对应关系。

| `mention_form` | 含义 |
| --- | --- |
| `SYSTEMATIC_NAME` | 全称或明确结构名称，包括 IUPAC 名称 |
| `TRIVIAL_COMMON_NAME` | 化合物惯用名、药物通用名或指向单一成分的商品名 |
| `UNAMBIGUOUS_ABBREVIATION` | 语境中身份明确的化学缩写，如 DMSO；不含研发代码和序列符号 |
| `UNAMBIGUOUS_FORMULA` | 身份明确的结构简式或元素符号，如 CH3COOH、Cu |
| `null` | 无名称表达类型信息 |

## 快速读取

在仓库根目录使用 Python 标准库读取 JSONL：

```python
import json
from pathlib import Path

with Path("chemical-ner/data/test.jsonl").open(encoding="utf-8") as stream:
    records = [json.loads(line) for line in stream if line.strip()]
input_fields = ("record_id", "publication_number", "language", "section", "text")
model_input = {field: records[0][field] for field in input_fields}
references = records[0]["ground_truth"]
print(len(records))  # 22
```

Hugging Face 提供 **V1.0** 版，配置为 `default`，split 为 `test`：

```python
from datasets import load_dataset

records = load_dataset("PatSnap/chemical-ner-bench", split="test", revision="V1.0")
model_inputs = records.select_columns([
    "record_id", "publication_number", "language", "section", "text"
])
```

`ground_truth` 单独用于评价，不进入模型请求。

## 评价与参考范围

实体识别与结构归一化的 Precision、Recall、F1 分别报告。注明匹配单位、参考纳入条件、去重、归一化、聚合方式及数据版本。权利要求与说明书结果分别呈现；只有评价规则相同的成绩才可直接比较。

3 条输入的实体参考列表为空，**不代表已确证的无化学实体真负例**。6,334 处参考提及中，**268 处的两个结构字段均为空**，另有 **50 处仅有 SMILES、无 InChIKey**。标识符非空不保证所提供的 SMILES 与 Key 等价，也不保证特定 RDKit 版本可复现该 Key。评价须声明所选结构字段及其适用参考范围；结构参考不可用，不排除该提及参与适用的实体识别评价。

## 许可证

数据集与参考标注采用 [CC BY-NC 4.0](../LICENSE.data)，第三方材料保留适用权利。项目代码与文档采用 [MIT 许可证](../LICENSE)。

## 引用

```bibtex
@dataset{patsnap_chemical_ner_bench_2026,
  title   = {Chemical NER Bench},
  author  = {PatSnap},
  year    = {2026},
  version = {1.0},
  url     = {https://huggingface.co/datasets/PatSnap/chemical-ner-bench}
}
```
