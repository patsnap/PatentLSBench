# Chemical NER Bench 参考说明

[数据集](README.zh.md) · [English](REFERENCE_NOTES.md) | **简体中文**

## 结构参考覆盖

**1.2.2** 版包含22份完整章节输入、6,334处实体参考提及。结构字段包含6,066个非空SMILES值和6,016个非空InChIKey值。6,016个Key均符合27字符标识符格式；格式检查不等于化学身份确认或结构转换成功。

两个结构字段并不保证每对参考都等价。使用RDKit **2024.3.2**及默认清洗设置时，17处提及涉及的8种SMILES无法解析。在其余同时提供两个字段的参考中，5,919处可复现给定的完整Key，80处不能：4处无法生成标准Key，19处仅标准／非标准标志不同，52处第一哈希块不同，5处第一哈希块相同但完整Key不同。这些类别不表示已证实的错误标注数量；金属配位与结构表示约定可能影响转换。

评价报告须说明所选结构字段、纳入与归一化规则、支持的结构表示及参考覆盖范围。若使用SMILES派生Key替代给定Key，须明确说明这一规则。结构参考不可用或不受支持，不影响该提及参与适用的实体识别评价。

[便携校验脚本](validate_dataset.py)使用Python标准库检查记录名单、字段、计数、标识符格式与原始HTML坐标。安装RDKit后，可选的结构诊断可复现上述类别，并报告实际使用的库版本：

```bash
python chemical-ner/validate_dataset.py chemical-ner/data/test.jsonl
python chemical-ner/validate_dataset.py chemical-ner/data/test.jsonl --chemistry
```

可通过位置参数显式指定JSONL路径。结构转换诊断不构成标注正确性或完备性证明。

## 空实体参考列表

3份权利要求输入的`ground_truth = []`，表示该章节未提供实体参考；不据此断言原文没有化学名称，也不表示经过完备核验的真负例。保留这些输入，并在每项评价中说明空参考记录的处理方式。

## 名称与坐标

参考名称可能包含HTML标签、首尾空白，且存在1对嵌套区间。`start`与`end`直接索引包含HTML标签的原始`text`，从0开始，按Unicode码点计数，采用左闭右开区间。去除HTML或裁剪名称空白后，原坐标不能直接套用。名称归一化、嵌套提及处理与去重规则须与坐标对齐分别说明。`ChemicalCompound`与`compound`表示同一化学实体类别。

## 1.2.2版修正

`chemner-US10065976B2-description`中从0开始计数的第`71`个实体为甲苯，其Key现为`YXFVVABEGXRONW-UHFFFAOYSA-N`。1.2.1版缺少末尾`N`。给定SMILES `CC1=CC=CC=C1`经标准InChI与直接分子转换两种方法均得到修正后的Key。其他记录值及记录／实体顺序均未改变。具体修正与验证方法见[data_corrections.json](data_corrections.json)。

报告要求见[评价说明](EVALUATION.zh.md)。
