# Chemical OCSR

[PatentLSBench](../README.md) · **English** | [简体中文](README.zh.md)

Chemical OCSR evaluates molecular recognition from annotated region crops, and chemical-region detection and recognition from single-page patent image PDFs. The **V1.0 data release** contains 50 pages from 50 patent publication numbers and is also available on [Hugging Face](https://huggingface.co/datasets/PatSnap/chemical-ocsr-bench).

## Recognition scope and roadmap

Molecular recognition evaluation in the current release is limited to complete chemical structures with applicable reference identifiers. Fragments and Markush cores are currently evaluated only for Layout.

| Planned release | Recognition evaluation |
| --- | --- |
| End of December 2026 | Fragments and Markush cores |
| End of March 2027 | More complete Markush structures, including explicit R-group definitions, linkage paths and constraints |

Manually reviewed classification labels are planned for release at the end of December 2026.

## Dataset overview

| Resource | Count |
| --- | ---: |
| Single-page image PDFs | 50 |
| Chemical regions and crops | 536 |
| Original MOL references | 277 |
| Canonical SMILES / standard InChIKey references | 272 each |

[`data/test.jsonl`](data/test.jsonl) has one page per line. [`assets/`](assets/) contains the 50 PDFs, 50 previews, 536 crops and 277 MOL files. PDFs are raster-only page images without a text layer; previews are for inspection.

## Load the data

Run from the repository root. Every asset path in a record is relative to `chemical-ocsr/`, including paths inside nested references.

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

Use PDF bytes for the page task or crop bytes for image recognition. `layout_gt` and `ocsr_gt` are evaluator references.

The Hugging Face Parquet view pins revision `V1.0`. Evaluation-profile links below point to the current `main` documentation.

```python
from datasets import load_dataset

regions = load_dataset(
    "PatSnap/chemical-ocsr-bench", "regions", split="test",
    revision="V1.0",
)
print(regions[0]["id"], regions[0]["region_image"].size)
```

## Data fields

| Field | Contents |
| --- | --- |
| `id`, `patent_no`, `page_no` | Page ID, publication number and page number in the source patent; each supplied PDF itself has one page |
| `pdf_path`, `preview_image` | PDF input and preview paths |
| `coordinate_reference_size` | Annotation-raster `[width, height]` |
| `layout_count`, `ocsr_count` | Region count and original-MOL-reference count, not identifier-scoring denominators |
| `layout_gt` | `region_id`, normalized `bbox` and crop `image` |
| `ocsr_gt` | `region_id`, `molfile`, nullable `smiles` and `inchikey`; joined to Layout by `region_id` |

Boxes are `[x1,y1,x2,y2]` in `[0,1]` with a top-left origin. Normalize predictions against an aligned rendering of the supplied page.

## Evaluation

**Evaluation:** See the [evaluation rules](https://huggingface.co/datasets/PatSnap/chemical-ocsr-bench/blob/main/public-50-pages/EVALUATION.md) and [molecular reference rules](https://huggingface.co/datasets/PatSnap/chemical-ocsr-bench/blob/main/public-50-pages/MOLECULAR_GT_PROTOCOL.md) for details.

- **Image:** associate each prediction with its input crop. Evaluate molecular recognition; do not pool answers across crops.
- **PDF:** match boxes one to one at **IoU ≥ 0.5**, first maximizing match count, then total IoU; resolve ties by GT `region_id` and stable prediction order. Fix this assignment before molecular comparison; never rematch using SMILES or Keys. All 536 regions participate in Layout P/R/F1.
- **Molecular:** report canonical-SMILES and full standard-InChIKey P/R/F1 separately. Each uses its published non-null reference population, currently 272. One eligible target can yield at most one TP. Every additional, duplicate, invalid or incorrect nonempty candidate is FP; an unrecovered eligible target is FN. Molecular candidates in unmatched PDF boxes are FP. Predictions matched to regions without an applicable reference are ignored for that molecular metric, while Layout still applies. Empty output or refusal leaves FN without inventing an FP.

Noncomplete structures are evaluated only for Layout. Molecular scoring uses each field's fixed reference list. The dataset provides 277 MOL references and 272 paired supported identifiers; the five MOL-only references are unscored for the corresponding identifier metrics and are not molecular negatives.

Micro-aggregate counts: `P=TP/(TP+FP)`, `R=TP/(TP+FN)`, `F1=2TP/(2TP+FP+FN)`; use P=0 when TP+FP=0. Target recovery `TP/272` equals Recall and does not replace PRF.

For SMILES, use RDKit **2024.03.2**, canonical isomeric output and explicit parser settings `removeHs=False`, `sanitize=True`, `parseName=False`, `allowCXSMILES=False`. Apply no additional salt stripping, charge neutralization, tautomer standardization or stereo repair. Standard InChI nevertheless applies its intrinsic normalization; full Key equality does not establish identical drawn bond orders, hydrogen representation or coordinates.

## Citation

```bibtex
@dataset{patsnap_chemical_ocsr_2026,
  title   = {Patent Page Chemical Structure Detection and Recognition Benchmark},
  author  = {PatSnap},
  year    = {2026},
  version = {1.0},
  url     = {https://huggingface.co/datasets/PatSnap/chemical-ocsr-bench}
}
```

## License and Disclaimer

Code and project documentation use the [MIT License](../LICENSE). This dataset, its annotations and accompanying assets use [CC BY-NC 4.0](../LICENSE.data). Third-party materials retain their applicable rights and separate terms and [source notices](https://huggingface.co/datasets/PatSnap/chemical-ocsr-bench/blob/main/public-50-pages/normalization/NOTICE.md).

The dataset and related outputs may contain errors or omissions and do not constitute legal, patent, medical or regulatory advice or professional certification. Review and validate them before relying on them; see the [full disclaimer](../DISCLAIMER.md).
