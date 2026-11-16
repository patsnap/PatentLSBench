# 专利单页化学结构定位与识别评测数据集

[Chemical OCSR Bench](../README.zh.md) · [English](README.md) | **简体中文**

**版本：1.0.0 · 公开 50 页版**

## 简介

本数据集评价单页 PDF 中的化学区域定位与分子识别，并提供图像 OCSR 的标注裁图。本版 PDF 均为仅包含一张页面图像、没有文字层的栅格图像 PDF。每页保留全部已标注化学区域、归一化框、九维化学与图像标签，以及指定完整结构的原始 MOL 和受支持规范标识符。

## 实际规模

| 项目 | 数量 |
| --- | ---: |
| 单页图像 PDF | 50 |
| 来源专利公开号 | 50 |
| 化学区域定位目标 | 536 |
| 保留的原始 MOL 参考 | 277 |
| 规范 SMILES 目标 | 272 |
| 标准 InChIKey 目标 | 272 |
| 自洽配对标识符 | 272 |
| 有 SMILES、无标准 Key | 0 |
| 有原始 MOL、无规范 SMILES | 5 |
| 标签维度 | 9 |
| 词表值 | 68 |
| 实际区域特征值 | 62 |
| MOL 参考层实际特征值 | 48 |

数值由本包 `pages.jsonl`、`regions.jsonl` 和 `ocsr.jsonl` 重算。原始 MOL、SMILES、InChIKey 的覆盖范围不同，须分别报告。固定名单见 `evaluation_masks.json`，规模与许可元信息见 `dataset_manifest.json`。

## 文件与字段

| 文件 | 内容 |
| --- | --- |
| `pages.jsonl` | 一行一页：`id`, `patent_no`, `page_no`, `pdf_path`, `preview_image`, `coordinate_reference_size`, `layout_count`, `ocsr_count`, `layout_gt`, `ocsr_gt`。 |
| `regions.jsonl` | 一行一区域，以 `id` 标识、`page_id` 关联页面，含 `bbox`、`image`、可空 `molfile`、九维标签及可空 `atom_count`、`bond_count`、`component_count` 等辅助字段。 |
| `ocsr.jsonl` | 一行一条原始 MOL 参考：`page_id`, `region_id`, `molfile`, `smiles`, `inchikey`；后两字段可为 null。 |
| `schema.json` | 页面对象的 JSON Schema，含嵌套 Layout/OCSR 字段及九维标签词表。 |
| `statistics.json` | 页面、区域、各格式参考及重叠特征的统计。 |
| `evaluation_masks.json` | 定位页面／区域、MOL、SMILES、InChIKey 和配对标识符的固定 ID 名单。 |
| `dataset_manifest.json` | 版本、许可、参考范围及输入格式。 |
| `normalization_manifest.json, normalization/` | 冻结缩写映射、连接规则、展开区域 ID、解析设置和第三方许可／来源声明。 |
| `attachments.manifest.jsonl` | 附件相对路径、大小、媒体类型与 SHA-256。 |
| `assets/pages/` | 仅包含页面图像的单页 PDF，为 PDF 模式输入。 |
| `assets/page_previews/` | 用于查看的派生页面预览图。 |
| `assets/images/` | 交付的标注区域裁图，用于检查与图像 OCSR。 |
| `assets/molfiles/` | 未修改的原始 MOL。 |
| `LICENSE.txt` | 本版许可与适用范围。 |

[评测协议](EVALUATION.zh.md)说明评价范围、定位匹配、固定参考名单和报告要求；[分子参考协议](MOLECULAR_GT_PROTOCOL.zh.md)说明解析及参考构建规则。

`layout_gt` 每项为 `region_id`, `bbox`, `image`, `labels`；`ocsr_gt` 每项为 `region_id`, `molfile`, `smiles`, `inchikey`。同一 `region_id` 关联定位和分子参考。框为左上角原点、归一化至 `[0,1]` 的 `[x1,y1,x2,y2]`；`coordinate_reference_size=[宽,高]` 记录标注栅格，不要求模型按该像素尺寸渲染。所有附件路径相对版本根目录。

## 最小读取示例

Python 3 标准库可读取清单。分子比较采用 RDKit **2024.03.2**，显式解析选项见[分子参考协议](MOLECULAR_GT_PROTOCOL.zh.md)。

```python
import json
from pathlib import Path

root = Path(".")  # 从解压后的版本目录运行
with (root / "pages.jsonl").open(encoding="utf-8") as stream:
    page = json.loads(next(stream))
pdf_path = root / page["pdf_path"]
assert pdf_path.is_file()
pdf_bytes = pdf_path.read_bytes()  # PDF 模式输入
print(page["id"], len(pdf_bytes), page["layout_count"], page["ocsr_count"])
for target in page["layout_gt"]:
    print(target["region_id"], target["bbox"], target["labels"]["type"])
```

## 参考标注

页面与对应区域裁图附有九维标签及归一化框。完整结构保留原始 MOL；规范标识符按冻结缩写字典、严格解析和一致性检查生成，设置见分子参考协议。

## 特征与统计语义

九维字段为 `type`, `chemical_family`, `component_features`, `atom_bond_features`, `stereo_features`, `notation_features`, `topology_features`, `scene`, `image_defects`。字段可多选；区域／页面特征计数不能跨特征相加作为总数。页面命中指至少一个子区域命中。某维度的比例以该维度非 null 记录为分母；MOL、SMILES、Key 分层各用对应参考群体。

`[]` 表示该维已评估、无当前词表特征；技术值 `null` 表示不可用或未建立，不能解释为否定。可空辅助字段表示相应信息不可用；分子标识符 null 不表示没有化学结构，也不排除该区域的 Layout 评价。

## 评价与许可

定位使用 IoU >= 0.5 一对一匹配并报告 P/R/F1。分子识别使用固定有效 InChIKey 名单；规范 SMILES 精确匹配为对应名单上的补充指标。整页联合恢复要求固定 Layout 匹配与正确分子答案，漏检、拒识、无效、未输出和错误答案均留在固定分母中。图像与 PDF 模式分别报告。显式 SMILES 解析要求 `removeHs=False`, `sanitize=True`, `parseName=False`, `allowCXSMILES=False`，保留组分、电荷、同位素、显式氢与已指定立体；不去盐、不中和、不归一互变、不修立体。

本次发布提供数据、参考范围和评价范围，不包含可执行的分子识别评分器。报告分子识别精确率、召回率和 F1 时，须说明完整评测配置：预测单元及其所属输入页面或裁图、多候选和重复输出的处理、无效与空输出的处理、匹配方法，以及 TP/FP/FN 计数和分母。不同计数或匹配配置的结果不能直接视为等价。上述固定 Layout 匹配及联合恢复规则仍用于联合恢复指标。

本版采用 **CC BY-NC 4.0**，完整条款见 [LICENSE.txt](LICENSE.txt)。引用须注明名称、版本及版本范围，并保留许可；商业使用须另行取得授权。
