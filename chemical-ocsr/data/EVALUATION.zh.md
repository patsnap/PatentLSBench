# 评测协议

[版本概览](README.zh.md) · [English](EVALUATION.md) | **简体中文**

版本：1.0.0

## 1. 输入与坐标

PDF 模式输入为 `pages.jsonl` 中 `pdf_path` 指向的单页 PDF。本版每份 PDF 均为仅含一张页面图像、没有文字层的栅格图像 PDF。`page_no` 表示该页在来源专利中的页码，交付的 PDF 本身只有一页。页面预览用于查看；交付的标注裁图用于图像 OCSR，图像模式与 PDF 模式分别报告。

GT 框为左上角原点的归一化 `[x1, y1, x2, y2]`，取值范围 `[0,1]`。`coordinate_reference_size` 记录原始标注坐标系的 `[宽, 高]`。像素预测框应按模型自身已对齐页面渲染的宽高归一化，并一致处理 PDF 旋转及可见页面范围，避免重复使用 DPI 缩放。

## 2. 化学结构区域定位

按 `evaluation_masks.json` 中全部页面及区域计分。完整结构、取代基、马库什结构和其他非完整化学表达均为化学区域目标，不能以分子标识符是否存在决定定位范围。逐页建立 IoU >= 0.5 的候选匹配；一对一匹配先最大化匹配数量，再最大化 IoU 总和；仍有并列时按 GT `region_id` 和预测的稳定输出序号确定，分子答案不能影响匹配。重复或未匹配预测计 FP，未匹配 GT 计 FN。汇总全部页面的 TP/FP/FN 后计算 P/R/F1；无预测时 P 取 0。 每个预测与每个 GT 区域最多匹配一次。精确率 `P = TP/(TP+FP)`，召回率 `R = TP/(TP+FN)`，`F1 = 2TP/(2TP+FP+FN)`；本数据集的 GT 数非零。

## 3. 分子结构识别

完整标准 InChIKey 匹配使用 `inchikey_region_ids`，规范 SMILES 精确匹配作为补充结构指标使用 `smiles_region_ids`；各指标使用各自的固定名单。`paired_identifier_region_ids` 为两者交集。`mol_region_ids` 仅表示原始 MOL 参考范围，不得替代标准格式指标的分母。

采用 RDKit 2024.03.2 和规范异构序列化。参考与预测 SMILES 均按下列显式设置解析，再比较 `MolToSmiles(..., canonical=True, isomericSmiles=True)`：

```python
from rdkit import Chem

params = Chem.SmilesParserParams()
params.removeHs = False
params.sanitize = True
params.parseName = False
params.allowCXSMILES = False

def canonical_structure(smiles):
    mol = Chem.MolFromSmiles(smiles, params)
    if mol is None:
        return None
    return Chem.MolToSmiles(mol, canonical=True, isomericSmiles=True)
```

设置 `removeHs=False`，保留显式氢原子。保留所有组分、形式电荷、同位素与已指定立体信息，不去盐、不中和、不做互变异构标准化、不修复立体。未返回、拒识、无效或错误预测在固定名单内均计 0，不能按预测有效性或模型支持范围缩小分母。比较分子表示而非 MOL 文本字节；MOL 预测须严格解析并保留显式氢，固定缩写处理遵循分子参考协议。

InChIKey 身份匹配比较完整标准 InChIKey，或使用 `rdkit.Chem.rdinchi.MolToInchi(mol, '')` 与 `InchiToInchiKey` 生成，并独立报告固定名单分母。Key 一致不能证明原子坐标或绘图几何一致。去立体或仅连接性指标仅可作为明确说明变换规则的补充指标。

上述保留规则针对标识符生成前的输入图处理；标准 InChI 自身仍进行规范化，可能合并其支持的移动氢互变异构形式。Key 一致不证明绘图键序、氢位置或坐标完全相同，参见 [InChI 官方技术说明](https://www.inchi-trust.org/technical-faq/)。

## 4. 整页端到端恢复

各分子格式使用自身固定名单。只有预测区域按上述固定定位匹配规则与 GT 匹配、且分子答案按对应协议正确时，才视为恢复成功。按全部单页 PDF 汇总“成功恢复目标数 / 固定格式名单目标数”。一次预测不能恢复多个目标；漏检、路由错误、拒识、未输出、无效及错误结构均留在分母中。不能为提高分子得分而重新分配已匹配到其他区域的定位框。

不在分子计分名单中的区域仍参与定位评测。标识符为 null 不表示该区域没有化学结构，格式不支持也不能将其视为背景。

## 5. 报告与分层统计

每项结果报告版本、输入形式、匹配规则、工具版本及实际分子分母。主指标跨区域做微汇总；页面宏平均须另行标明。分层指标以对应固定格式名单和特征命中区域的交集为范围。九维标签均可多选，分层会重叠；某维度 `[]` 表示已评估且无当前词表特征，`null` 表示该维度技术上不可用，不进入该维度统计分母。

## 6. 评价实现与结果可比性

本次发布提供数据、参考范围和评价范围，不包含可执行的分子识别评分器。报告分子识别精确率、召回率和 F1 时，须说明完整评测配置：预测单元及其所属输入页面或裁图、多候选和重复输出的处理、无效与空输出的处理、匹配方法，以及 TP/FP/FN 计数和分母。不同计数或匹配配置的结果不能直接视为等价。上述固定 Layout 匹配及联合恢复规则仍用于联合恢复指标。
