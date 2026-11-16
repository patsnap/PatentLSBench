# Chemical OCSR

[PatentLSBench](https://github.com/patsnap/PatentLSBench) · **English** | [简体中文](README.zh.md) · [Evaluation Protocol](../docs/evaluation-protocol.md)

Chemical OCSR evaluates molecular recognition from chemical structure images, and chemical-region detection and recognition from single-page patent PDFs. The dataset provides annotated region boxes, labels, crops and complete-structure molecular references.

[Data and assets](data/README.md) · [Schema](data/schema.json) · [Evaluation protocol](data/EVALUATION.md) · [🤗 Dataset](https://huggingface.co/datasets/PatSnap/chemical-ocsr-bench)

## Dataset

**v1.0.0** contains 50 single-page raster PDF inputs from 50 patent publication numbers. The supplied PDFs have no embedded text layer. Each page record links its supplied region annotations and molecular references.

| Resource | Count |
| --- | ---: |
| Single-page raster PDFs | 50 |
| Chemical regions and annotated crops | 536 |
| MOL reference files | 277 |
| Valid canonical-SMILES references | 272 |
| Valid standard-InChIKey references | 272 |
| Label dimensions | 9 |

## Examples

Page preview and supplied chemical-region crops. The page task uses the supplied PDF input.

<img src="assets/AU2022204980A1_page_156.jpg" alt="Patent page preview" width="350">

<img src="assets/img-dc-2240.jpg" alt="Markush region" width="260"> <img src="assets/img-dc-1642.jpg" alt="Complete molecular structure" width="260">

## Input and references

| Mode | Model input | References |
| --- | --- | --- |
| Image | An annotated chemical-region crop | Complete molecular structures on the fixed valid-InChIKey list |
| PDF | A supplied single-page raster PDF | The supplied chemical-region bounding boxes and complete-structure molecular references |

The supplied PDFs are the page task's model input; page images provide previews. The image task uses the supplied annotated crops. Keep image recognition and PDF results separate.

Layout references include complete structures, substituents, Markush structures and other non-complete chemical expressions. Molecular recognition uses the 272 complete-structure references with valid InChIKeys. The 277 MOL references and the identifier scoring populations are recorded separately.

Boxes use normalized `[x1, y1, x2, y2]` coordinates with a top-left origin. `coordinate_reference_size` records the original annotation raster size. Normalize predictions against the model's aligned page rendering and preserve the page geometry.

## Evaluation

| Layer | Matching criteria | Metrics |
| --- | --- | --- |
| Layout · PDF | One-to-one bounding-box matching; this edition uses IoU ≥ 0.5 | Precision, recall, F1 |
| OCSR · image and PDF | Full standard-InChIKey equality on the fixed Key-reference population | Precision, recall, F1 |
| Joint page recovery · supplementary | Correct molecular identity under the fixed Layout assignment | Recovered targets / fixed molecular targets |

Report Layout and molecular recognition separately, including actual target populations and micro-aggregated counts. Repeated occurrences retain their multiplicity. Preserve components, charge, isotopes, explicit hydrogens and specified stereochemistry when deriving identifiers.

Canonical-SMILES exact match is a supplementary metric evaluated on its own fixed target list. The complete rules, format-specific masks and molecular normalization settings are in [evaluation protocol](data/EVALUATION.md) and [molecular reference protocol](data/MOLECULAR_GT_PROTOCOL.md).

Feed only the supplied PDF or crop bytes to the evaluated model. Keep reference boxes, structures and annotation labels in the evaluator.

## Labels

| Field | Dimension | Examples |
| --- | --- | --- |
| `type` | Structure type | Complete structure, substituent, Markush structure |
| `chemical_family` | Chemical family | Organic, peptide, nucleic-acid, coordination/organometallic |
| `component_features` | Component form | Salt/ion pair, hydrate, solvate |
| `atom_bond_features` | Atom and bond features | Isotope, charge, coordination bond |
| `stereo_features` | Stereochemical notation | Wedge bonds, double-bond geometry, axial chirality |
| `notation_features` | Abbreviations and generalized notation | Fixed abbreviation, variable group, repeat notation |
| `topology_features` | Ring topology | Macrocycle, fused, spiro, bridged |
| `scene` | Page context | Reaction scheme, structure table, grouped structures |
| `image_defects` | Image quality | Blur, broken bonds, text interference |

The original Chinese label values remain unchanged in the data. The dictionary contains 68 values; observed feature coverage counts `(dimension, label)` pairs. Regions can carry multiple features. See the [schema](data/schema.json) and [statistics](data/statistics.json) for definitions and counts.

## Read the data

GitHub `chemical-ocsr/data/` and Hugging Face `public-50-pages/` contain the same core JSONL records, reference files and PDF/image/MOL assets. Hugging Face additionally provides embedded-image Parquet views.

### Local files

From the repository root, read and verify the data with Python's standard library:

```bash
python chemical-ocsr/examples/inspect_dataset.py chemical-ocsr/data --verify
```

| Path | Contents |
| --- | --- |
| `data/pages.jsonl` | Page records and nested region/molecular references |
| `data/regions.jsonl` | Region records, bounding boxes and labels |
| `data/ocsr.jsonl` | Molecular references linked by page and region IDs |
| `data/assets/` | Supplied PDFs, page previews, region crops and MOL files |
| `data/schema.json`, `data/evaluation_masks.json` | Schema and fixed reference lists |
| `data/EVALUATION.md`, `data/MOLECULAR_GT_PROTOCOL.md` | Evaluation and molecular reference protocols |

The [data README](data/README.md) describes all files. Asset paths are relative to `data/`. Link `regions.page_id` to `pages.id`, and `ocsr.region_id` to `regions.id`; `ocsr.page_id` also links to `pages.id`.

### Hugging Face

Each configuration provides a `test` split:

| Configuration | Rows | Contents |
| --- | ---: | --- |
| `pages` · default | 50 | Page records, nested references and embedded `page_image` previews |
| `regions` | 536 | Region records, labels and embedded `region_image` crops |
| `molecules` | 277 | MOL-reference records and nullable standard identifiers |

Sign in with an HF account that has repository access:

```bash
hf auth login
```

```python
from datasets import load_dataset

pages = load_dataset("PatSnap/chemical-ocsr-bench", "pages", split="test", revision="v1.0.0", token=True)
regions = load_dataset("PatSnap/chemical-ocsr-bench", "regions", split="test", revision="v1.0.0", token=True)
molecules = load_dataset("PatSnap/chemical-ocsr-bench", "molecules", split="test", revision="v1.0.0", token=True)
print(pages[0]["id"], regions[0]["region_image"].size)
```

Download the PDF inputs and reference assets:

```python
import json
from pathlib import Path
from huggingface_hub import snapshot_download

snapshot = snapshot_download(
    repo_id="PatSnap/chemical-ocsr-bench",
    repo_type="dataset",
    revision="v1.0.0",
    token=True,
    allow_patterns="public-50-pages/**",
)
edition = Path(snapshot) / "public-50-pages"
with (edition / "pages.jsonl").open(encoding="utf-8") as stream:
    page = json.loads(next(stream))
pdf_bytes = (edition / page["pdf_path"]).read_bytes()
```

Use only the PDF bytes or region image as model input; the reference tables are used separately for evaluation.

## Citation and license

```bibtex
@misc{patsnap_patent_page_ocsr_2026,
  title   = {Patent Page Chemical Structure Detection and Recognition Benchmark},
  author  = {PatSnap},
  year    = {2026},
  version = {1.0.0},
  url     = {https://huggingface.co/datasets/PatSnap/chemical-ocsr-bench}
}
```

The public dataset and annotations use [CC BY-NC 4.0](data/LICENSE.txt). Code and project documentation use the [MIT License](../LICENSE). Third-party source materials retain their applicable rights and terms; normalization resources include their own notices.
