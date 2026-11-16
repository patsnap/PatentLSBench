# Patent Page Chemical Structure Detection and Recognition Benchmark

[Chemical OCSR Bench](../README.md) · **English** | [简体中文](README.zh.md)

**Version: 1.0.0 · Public 50-page edition**

## Overview

This benchmark evaluates chemical-region localization and molecular recognition from single-page PDFs and provides annotated crops for image-based OCSR. Every supplied PDF is a raster-only image PDF containing one page image and no text layer. Each page retains every annotated chemical region, normalized boxes, nine chemical/image label dimensions, and original MOL references plus supported canonical identifiers for designated complete structures.

## Edition size

| Population | Count |
| --- | ---: |
| Single-page image PDFs | 50 |
| Source publication numbers | 50 |
| Chemical Layout targets | 536 |
| Preserved original MOL references | 277 |
| Canonical-SMILES targets | 272 |
| Standard-InChIKey targets | 272 |
| Consistent paired identifiers | 272 |
| SMILES without standard Key | 0 |
| Original MOL without canonical SMILES | 5 |
| Label dimensions | 9 |
| Dictionary values | 68 |
| Observed Layout feature values | 62 |
| Observed MOL-reference feature values | 48 |

Counts are recomputed from this edition's `pages.jsonl`, `regions.jsonl` and `ocsr.jsonl`. Original-MOL, SMILES and InChIKey coverage are distinct populations. Use `evaluation_masks.json` for fixed target lists and `dataset_manifest.json` for counts and licensing metadata.

## Files and fields

| File | Contents |
| --- | --- |
| `pages.jsonl` | One page per row: `id`, `patent_no`, `page_no`, `pdf_path`, `preview_image`, `coordinate_reference_size`, `layout_count`, `ocsr_count`, `layout_gt`, `ocsr_gt`. |
| `regions.jsonl` | One region per row, identified by `id` and linked by `page_id`; includes `bbox`, `image`, nullable `molfile`, nine label dimensions, and nullable auxiliary fields such as `atom_count`, `bond_count`, `component_count`. |
| `ocsr.jsonl` | One original-MOL reference per row: `page_id`, `region_id`, `molfile`, `smiles`, `inchikey`; the last two fields are nullable. |
| `schema.json` | JSON Schema for page records, nested Layout/OCSR references and the nine label dictionaries. |
| `statistics.json` | Page, region, per-format populations and overlapping feature statistics. |
| `evaluation_masks.json` | Fixed IDs for Layout pages/regions, MOL, SMILES, InChIKey and paired identifiers. |
| `dataset_manifest.json` | Version, license, reference populations and input representation. |
| `normalization_manifest.json, normalization/` | Frozen abbreviations, attachment rules, expanded region IDs, parser settings and third-party license/source notices. |
| `attachments.manifest.jsonl` | Relative asset paths, sizes, media types and SHA-256 hashes. |
| `assets/pages/` | Raster-only single-page image PDFs; the PDF-mode input. |
| `assets/page_previews/` | Derived page previews for inspection. |
| `assets/images/` | Supplied annotated-region crops for inspection and image-based OCSR. |
| `assets/molfiles/` | Unmodified original MOL files. |
| `LICENSE.txt` | License and edition scope. |

The [evaluation protocol](EVALUATION.md) defines scope, Layout matching, fixed reference lists and reporting requirements. The [molecular reference protocol](MOLECULAR_GT_PROTOCOL.md) defines parsing and reference construction.

Each `layout_gt` entry has `region_id`, `bbox`, `image`, `labels`; each `ocsr_gt` entry has `region_id`, `molfile`, `smiles`, `inchikey`. Join on `region_id`. Boxes use a top-left origin and normalized `[x1,y1,x2,y2]` coordinates in `[0,1]`. `coordinate_reference_size=[width,height]` records the annotation raster, not a required model-rendering size. All asset paths are relative to the edition root.

## Minimal reader

The Python 3 standard library is sufficient to read manifests. Molecular comparison uses RDKit **2024.03.2**, with the explicit settings in the [molecular reference protocol](MOLECULAR_GT_PROTOCOL.md).

```python
import json
from pathlib import Path

root = Path(".")  # run from the extracted edition directory
with (root / "pages.jsonl").open(encoding="utf-8") as stream:
    page = json.loads(next(stream))
pdf_path = root / page["pdf_path"]
assert pdf_path.is_file()
pdf_bytes = pdf_path.read_bytes()  # primary model input
print(page["id"], len(pdf_bytes), page["layout_count"], page["ocsr_count"])
for target in page["layout_gt"]:
    print(target["region_id"], target["bbox"], target["labels"]["type"])
```

## Reference annotation

Pages and their annotated region crops include nine-dimensional labels and normalized boxes. Complete-structure references retain their original MOL files. Canonical identifiers follow the frozen abbreviation dictionary, strict parsing and consistency checks in the molecular reference protocol.

## Labels and counting

The nine fields listed above use multi-label semantics. A region can contribute to multiple features, so feature counts are not additive. A page is a feature hit when any child region has that feature. Dimension percentages use non-null records for that dimension; molecular slices use their respective MOL, SMILES or Key populations.

`[]` means assessed with no current-dictionary feature; technical `null` means unavailable or not established and is not a negative label. Null auxiliary fields indicate unavailable information. Null molecular identifiers neither negate a chemical region nor remove it from Layout evaluation.

## Evaluation and license

Layout uses one-to-one matching at IoU >= 0.5 and reports P/R/F1. Molecular identity matching uses the fixed InChIKey list; canonical-SMILES exact match is a supplementary metric on its own list. End-to-end recovery requires both correct localization and molecular identity; misses, refusals, invalid and wrong outputs remain in the fixed denominator. Image recognition uses the original annotated crops and is reported separately from PDF recognition. Parse SMILES with explicit `removeHs=False`, `sanitize=True`, `parseName=False`, `allowCXSMILES=False`; preserve components, charges, isotopes and specified stereo without salt stripping, neutralization, tautomer standardization or stereo repair.

This release provides the data, reference populations and evaluation scope; it does not include an executable recognition scorer. For reported molecular precision, recall and F1, identify the complete evaluation profile: the prediction unit and its input-page or crop association, treatment of multiple and duplicate outputs, invalid and empty outputs, matching procedure, and TP/FP/FN counts and denominators. Do not present results from different counting or matching profiles as directly equivalent. The fixed Layout assignment and joint-recovery rules above remain applicable to the joint-recovery metric.

This edition uses **CC BY-NC 4.0**; see [LICENSE.txt](LICENSE.txt) for the complete terms. Attribute the dataset title, version and edition and retain the license. Obtain separate authorization for commercial use.
