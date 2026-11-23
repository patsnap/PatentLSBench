# Chemical OCSR

[PatentLSBench](../README.zh.md) · [English](README.md) | **简体中文**

Chemical OCSR 评价化学区域裁图中的分子识别，以及单页专利图像 PDF 中的化学区域定位与识别。**V1.0 数据版本**包含来自50个专利公开号的50页，也可通过 [Hugging Face](https://huggingface.co/datasets/PatSnap/chemical-ocsr-bench/blob/main/README.zh.md) 获取。

## 识别评测范围与计划

当前版本的分子识别评测仅覆盖具有适用参考标识符的完整化学结构；片段与 Markush 主核目前仅参与 Layout 评测。

| 计划上线时间 | 识别评测范围 |
| --- | --- |
| 2026 年 12 月底 | 片段与 Markush 主核 |
| 2027 年 3 月底 | 更完整的 Markush 结构，包含 R 基团具体定义、链接路径及约束关系 |

人工审核的分类标签计划于 2026 年 12 月底上线。

## 数据集概览

| 资源 | 数量 |
| --- | ---: |
| 单页图像 PDF | 50 |
| 化学区域及裁图 | 536 |
| 原始 MOL 参考 | 277 |
| 规范 SMILES／标准 InChIKey 参考 | 各272 |

[`data/test.jsonl`](data/test.jsonl) 一行一页。[`assets/`](assets/) 包含50个PDF、50张预览、536张裁图和277个MOL。PDF仅包含页面栅格图像，没有文字层；预览用于查看。

## 读取数据

从仓库根目录运行。记录中的所有附件路径，包括嵌套参考中的路径，都相对于 `chemical-ocsr/`。

```python
import json
from pathlib import Path

root = Path("chemical-ocsr")
with (root / "data/test.jsonl").open(encoding="utf-8") as file:
    page = json.loads(next(file))

pdf_bytes = (root / page["pdf_path"]).read_bytes()
region = page["layout_gt"][0]
crop_bytes = (root / region["image"]).read_bytes()
print(page["id"], len(pdf_bytes), region["region_id"], len(crop_bytes))
```

整页任务使用PDF字节，图像识别使用裁图字节；`layout_gt` 和 `ocsr_gt` 是评估参考。

Hugging Face 的Parquet视图固定读取数据版本 `V1.0`。下方评测配置链接指向当前 `main` 文档。

```python
from datasets import load_dataset

regions = load_dataset(
    "PatSnap/chemical-ocsr-bench", "regions", split="test",
    revision="V1.0",
)
print(regions[0]["id"], regions[0]["region_image"].size)
```

## 数据字段

| 字段 | 内容 |
| --- | --- |
| `id`, `patent_no`, `page_no` | 页面ID、公开号和来源专利中的页码；每个交付PDF本身只有一页 |
| `pdf_path`, `preview_image` | PDF输入与预览路径 |
| `coordinate_reference_size` | 原标注栅格的 `[宽,高]` |
| `layout_count`, `ocsr_count` | 区域数与原始MOL参考数，不能代替标识符计分分母 |
| `layout_gt` | `region_id`、归一化 `bbox` 和裁图 `image` |
| `ocsr_gt` | `region_id`、`molfile`、可空 `smiles` 和 `inchikey`，通过 `region_id` 关联定位参考 |

框为左上角原点、范围 `[0,1]` 的 `[x1,y1,x2,y2]`。预测须按与交付页面对齐的渲染结果归一化。

## 评价

**评价规则**： 细则见[评价规则](https://huggingface.co/datasets/PatSnap/chemical-ocsr-bench/blob/main/public-50-pages/EVALUATION.zh.md)和[分子参考规则](https://huggingface.co/datasets/PatSnap/chemical-ocsr-bench/blob/main/public-50-pages/MOLECULAR_GT_PROTOCOL.zh.md)。

- **图像模式**： 按输入裁图对应参考，只评分子识别，不能把不同裁图答案汇总后匹配。
- **PDF模式**： 以 **IoU ≥ 0.5** 做一对一匹配，先最大化匹配数，再最大化总IoU；并列时按GT `region_id` 和预测稳定序号确定。固定该对应关系后再比较分子答案，不得按SMILES或Key重配。全部536个区域参加Layout P/R/F1。
- **分子识别**： 规范SMILES与完整标准InChIKey分别报告P/R/F1，各自使用发布的非空参考，目前各272条。每个适用目标最多1个TP；额外、重复、无效或错误的非空候选均为FP，未恢复的适用目标为FN。未匹配PDF框中的分子候选计FP。匹配到无适用参考区域的预测在该分子指标中忽略，仍评价Layout。空输出或拒识保留FN，不虚造FP。

非完整结构仅评 Layout。分子计分使用各字段的固定参考名单。数据集提供 277 条 MOL 参考与 272 对受支持标识符；5 条仅有 MOL 的参考不参加相应标识符计分，不能作为分子识别负例。

微汇总计数后计算：`P=TP/(TP+FP)`、`R=TP/(TP+FN)`、`F1=2TP/(2TP+FP+FN)`；TP+FP=0时P取0。目标恢复率 `TP/272` 等于Recall，不能替代PRF。

SMILES采用 RDKit **2024.03.2** 的规范异构输出，显式设置 `removeHs=False`, `sanitize=True`, `parseName=False`, `allowCXSMILES=False`；不额外去盐、不中和、不归一互变、不修立体。标准InChI仍有固有规范化；完整Key一致不证明绘图键序、氢表达或坐标完全相同。

## 引用

```bibtex
@dataset{patsnap_chemical_ocsr_2026,
  title   = {Patent Page Chemical Structure Detection and Recognition Benchmark},
  author  = {PatSnap},
  year    = {2026},
  version = {1.0},
  url     = {https://huggingface.co/datasets/PatSnap/chemical-ocsr-bench}
}
```

## 许可证与免责声明

代码和项目文档采用 [MIT 许可证](../LICENSE)。本数据集、标注及配套附件采用 [CC BY-NC 4.0](../LICENSE.data)。第三方材料保留其适用权利和单独条款，并附有[来源声明](https://huggingface.co/datasets/PatSnap/chemical-ocsr-bench/blob/main/public-50-pages/normalization/NOTICE.md)。

数据集及相关输出可能存在错误或遗漏，不构成法律、专利、医疗或监管意见，也不构成专业认证。在依赖这些材料前，应进行审查与验证；详见[完整免责声明](../DISCLAIMER.zh.md)。
