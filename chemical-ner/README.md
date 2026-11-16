# Chemical NER Bench

[PatentLSBench](../README.md) · **English** | [简体中文](README.zh.md)

Chemical NER Bench provides patent claims and descriptions for **chemical entity recognition and structure normalization**. Each record contains one complete section and its supplied entity references. The `test` split is available in [`data/test.jsonl`](data/test.jsonl) and on [Hugging Face](https://huggingface.co/datasets/PatSnap/chemical-ner-bench).

## Dataset overview

| Property | Version 1.2.2 |
| --- | ---: |
| Patent publication numbers | 11 |
| Complete section inputs | 22 |
| Claims / description inputs | 11 / 11 |
| Entity-reference mentions | 6,334 |

Inputs cover Chinese, English, Japanese and Korean, including Traditional Chinese. Each claim or description section is an independent input; mention, distinct-name and distinct-structure counts are different units.

## Data fields

| Record field | Type | Meaning |
| --- | --- | --- |
| `record_id` | string | Unique section-record identifier |
| `publication_number` | string | Source patent publication number |
| `language` | string | `CN`: Chinese; `CNT`: Traditional Chinese; `EN`: English; `JP`: Japanese; `KR`: Korean |
| `section` | string | `claim` or `description` |
| `text` | string | Complete section HTML |
| `ground_truth` | list[object] | Supplied entity-reference mentions; an empty list is `[]` |

| Entity field | Type | Meaning |
| --- | --- | --- |
| `start`, `end` | integer | Inclusive start and exclusive end in the record's `text` |
| `text` | string | Reference name text |
| `label` | string | `ChemicalCompound` and `compound` denote the same chemical-entity category |
| `smiles` | string | Supplied SMILES reference; `""` means unavailable |
| `inchikey` | string | Supplied InChIKey reference; `""` means unavailable |
| `mention_form` | string or null | Name-form category below; null means no category information |

Offsets are zero-based, half-open Unicode code-point intervals `[start, end)` in the **original HTML string, including markup characters**. Reference names can contain markup or surrounding whitespace. Removing HTML or trimming names changes coordinate alignment.

| `mention_form` | Meaning |
| --- | --- |
| `SYSTEMATIC_NAME` | Full or explicit structural name, including IUPAC names |
| `TRIVIAL_COMMON_NAME` | Common chemical name, generic drug name or single-ingredient trade name |
| `UNAMBIGUOUS_ABBREVIATION` | Chemical abbreviation unambiguous in context, such as DMSO; excludes development codes and sequence symbols |
| `UNAMBIGUOUS_FORMULA` | Unambiguous condensed structural formula or element symbol, such as CH3COOH or Cu |
| `null` | No name-form category information |

## Quick start

Read the JSONL from the repository root using Python's standard library:

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

Hugging Face provides version **1.2.2** in the `default` configuration and `test` split. After signing in with `hf auth login`:

```python
from datasets import load_dataset

records = load_dataset("PatSnap/chemical-ner-bench", split="test", revision="v1.2.2", token=True)
model_inputs = records.select_columns([
    "record_id", "publication_number", "language", "section", "text"
])
```

Keep `ground_truth` separate from model requests.

## Evaluation and reference scope

Report entity-recognition and structure-normalization precision, recall and F1 separately. State the matching unit, reference eligibility, deduplication, normalization, aggregation and dataset revision. Present claims and description results separately; compare scores only under the same evaluation rules.

Three inputs have empty entity-reference lists; these are **not certified chemical-free negative examples**. Among the 6,334 reference mentions, **268 have both structure fields empty** and **50 have SMILES without an InChIKey**. Nonempty identifiers do not guarantee that the supplied SMILES and Key are equivalent or that a particular RDKit version reproduces the Key. Declare the chosen structure field and its eligible population; unavailable structure references do not remove mentions from applicable entity-recognition evaluation.

## License

Dataset and reference annotations: [CC BY-NC 4.0](../LICENSE.data), subject to applicable third-party rights. Project code and documentation: [MIT](../LICENSE).

## Citation

```bibtex
@dataset{patsnap_chemical_ner_bench_2026,
  title   = {Chemical NER Bench},
  author  = {PatSnap},
  year    = {2026},
  version = {1.2.2},
  url     = {https://huggingface.co/datasets/PatSnap/chemical-ner-bench}
}
```
