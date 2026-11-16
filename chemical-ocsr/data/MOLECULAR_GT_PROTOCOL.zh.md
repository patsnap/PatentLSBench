# 分子参考协议

[版本概览](README.zh.md) · [English](MOLECULAR_GT_PROTOCOL.md) | **简体中文**

版本：1.0.0 · RDKit 2024.03.2

## 来源与范围

提供的原始 MOL 按原始字节保留。规范 SMILES 与标准 InChIKey 是受支持参考图的确定性派生表示，不是重新绘制的结构。各格式规模见 `dataset_manifest.json`，固定目标名单见 `evaluation_masks.json`；原始 MOL、SMILES 和 InChIKey 覆盖范围分别记录。

## 固定缩写展开

冻结字典和连接规则的机器可读文件为 `normalization/fixed_abbreviations.json`，本版实际完成展开的参考区域名单见 `normalization_manifest.json`。来自 MolScribe 的映射在 `normalization/` 保留 MIT 许可和来源说明。

只支持下表区分大小写的固定标签，操作在图副本上进行。缩写须位于中性、无同位素、无自由基、单邻接、单键连接且未指定原子手性的哑原子上，片段第 0 个原子为连接根。保留原子顺序、已有键及方向/立体、原子手性标签和组分数。新添原子没有来源坐标，因此仅在派生图中移除构象；原 MOL 坐标保留。片段连接根为开放价态而带的人工自由基在形成既定连接后清除，来源结构的自由基不被修改。

| 精确标签 | 片段 SMILES；第 0 个原子为连接根 |
| --- | --- |
| `Me` | `C` |
| `Et` | `CC` |
| `iPr` | `C(C)C` |
| `OMe` | `OC` |
| `OCH3` | `OC` |
| `H3CO` | `OC` |
| `MeO` | `OC` |
| `OEt` | `OCC` |
| `EtO` | `OCC` |
| `OBn` | `OCc1ccccc1` |
| `BnO` | `OCc1ccccc1` |
| `Bn` | `Cc1ccccc1` |
| `Ph` | `c1ccccc1` |
| `CF3` | `C(F)(F)F` |
| `F3C` | `C(F)(F)F` |
| `CCl3` | `C(Cl)(Cl)Cl` |
| `NO2` | `[N+](=O)[O-]` |
| `O2N` | `[N+](=O)[O-]` |
| `CN` | `C#N` |
| `NC` | `C#N` |
| `CHO` | `C=O` |
| `OSiEt3` | `O[Si](CC)(CC)CC` |
| `Boc` | `[C](=O)OC(C)(C)C` |
| `Cbz` | `[C](=O)OCc1ccccc1` |
| `Fmoc` | `[C](=O)OCC1c(cccc2)c2c3c1cccc3` |
| `NHBoc` | `[NH1]C(=O)OC(C)(C)C` |
| `CO2Et` | `[C](=O)OCC` |
| `COOEt` | `[C](=O)OCC` |
| `OtBu` | `[O]C(C)(C)C` |
| `OMs` | `[O]S(=O)(=O)C` |
| `OTf` | `[O]S(=O)(=O)C(F)(F)F` |
| `OAc` | `[O]C(=O)C` |
| `Ac` | `[C](=O)C` |
| `CO2H` | `[C](=O)O` |
| `COOH` | `[C](=O)O` |
| `HO2C` | `[C](=O)O` |
| `SO3H` | `[S](=O)(=O)O` |

不猜测未知、复合或歧义标签。展开须通过严格 sanitize、无残余哑原子/查询/缩写、原图不变量检查、规范 SMILES 往返稳定、原图与 SMILES 生成的标准 Key 一致，以及存在原参考 Key 时完整匹配原 Key。上述验收针对参考构建；预测直接与冻结参考比较，不借助答案修复预测。

## 解析与序列化

原始 MOL 使用 `Chem.MolFromMolFile(path, sanitize=True, removeHs=False, strictParsing=True)` 解析。规范序列化使用 `Chem.MolToSmiles(mol, canonical=True, isomericSmiles=True)`。发布参考与预测 SMILES 均须按下列显式设置解析：

```python
from rdkit import Chem
from rdkit.Chem import rdinchi

params = Chem.SmilesParserParams()
params.removeHs = False
params.sanitize = True
params.parseName = False
params.allowCXSMILES = False
mol = Chem.MolFromSmiles(smiles, params)
if mol is None:
    raise ValueError("Invalid SMILES")
canonical_smiles = Chem.MolToSmiles(mol, canonical=True, isomericSmiles=True)
inchi, code, message, log, aux = rdinchi.MolToInchi(mol, '')
standard_inchikey = rdinchi.InchiToInchiKey(inchi) if inchi else None
```

标准 InChI 使用空选项及 `InChI=1S/` 结果。每条非空 SMILES 均重新解析并检查规范序列化稳定性，每条非空 Key 均由对应发布 SMILES 独立复现。设置 `removeHs=False`，保留显式氢原子。保留组分、形式电荷、同位素、显式氢及已指定立体；不去盐、不中和、不归一互变、不放宽 sanitize、不修立体。

上述限制指额外的输入图预处理，不关闭标准 InChI 自身的规范化；参见[标识符指标范围](EVALUATION.zh.md)。

## 缺失值与计分

标准字段 null 表示本协议未建立安全且受支持的表示，原始 MOL 仍保留，不以原缩写伪 SMILES 填充标准字段。有效规范 SMILES 可能没有受支持的标准 InChIKey，尤其是含配位键的图；SMILES 和 InChIKey 指标分别使用各自的固定名单。

按 `evaluation_masks.json` 固定名单计分。未输出、拒识、无效和错误预测均计失败，不移除分母。MOL 文本相等不等于分子身份相等，Key 相等也不等于绘图几何相等。整页与图像识别的评价范围、联合恢复规则和报告要求见[评测协议](EVALUATION.zh.md)。
