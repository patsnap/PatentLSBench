# Chemical NER

[PatentLSBench](https://github.com/patsnap/PatentLSBench) · **English** | [简体中文](README.zh.md) · [Evaluation Protocol](../docs/evaluation-protocol.md)

Chemical NER Bench provides complete patent claims and descriptions for chemical entity recognition and structure normalization, with entity-level reference answers and molecular structure identifiers.

[🤗 Dataset](https://huggingface.co/datasets/PatSnap/chemical-ner-bench) · [Data files](https://huggingface.co/datasets/PatSnap/chemical-ner-bench/tree/main)

## Dataset overview

**Version 1.2.1** contains:

| Resource | Count |
| --- | --- |
| Patent publication numbers | 11 |
| Complete section inputs | 22 |
| Claims / description inputs | 11 / 11 |
| Entity reference mentions | 6,334 |
| Inputs with an empty entity reference list | 3 |

The dataset covers Chinese, English, Japanese and Korean, including Traditional Chinese text.

| Language | Code | Sections |
| --- | --- | --- |
| Chinese | `CN` | 8 |
| Traditional Chinese | `CNT` | 2 |
| English | `EN` | 6 |
| Japanese | `JP` | 4 |
| Korean | `KR` | 2 |

## Input and reference answers

Each record is one complete `claim` or `description` section, evaluated as an independent input. Model inputs contain five fields: `record_id`, `publication_number`, `language`, `section` and `text`. `ground_truth` contains entity-level reference answers for comparison with model predictions.

## Fields

| Record field | Meaning |
| --- | --- |
| `record_id` | Unique identifier for a section record. |
| `publication_number` | Publication number of the patent containing this section. |
| `language` | Section language code: CN = Chinese, CNT = Traditional Chinese, EN = English, JP = Japanese, KR = Korean. |
| `section` | Section type: claim = complete claims section; description = complete description section. |
| `text` | HTML text of a complete claims or description section. |
| `ground_truth` | Entity-level evaluation reference answers, with one object per entity mention; [] when there are no reference entities. |

| Entity field | Meaning |
| --- | --- |
| `start` | Inclusive, zero-based start offset of the entity in this record's text, measured in Unicode code points including HTML markup characters. |
| `end` | Exclusive end offset of the entity in this record's text, forming a half-open interval with start. |
| `text` | Entity name text in the section. |
| `label` | Chemical entity class code. ChemicalCompound and compound both denote chemical entities and do not distinguish chemical object subtypes. |
| `smiles` | SMILES representation of the entity's reference structure; an empty string indicates no available SMILES reference. |
| `inchikey` | InChIKey identifier of the entity's reference structure; an empty string indicates no available InChIKey reference. |
| `mention_form` | How the entity name is expressed in the text; values are defined below. null indicates no name-form category information. |

`ChemicalCompound` and `compound` both denote chemical entities rather than different chemical object subtypes. Record `text` contains the complete section HTML. Offsets count all HTML characters in Unicode code points using zero-based, half-open `[start, end)` intervals.

`ground_truth = []` indicates a section with no reference entities. Empty structure strings indicate no reference for the corresponding identifier; `mention_form = null` indicates no name-form category information.

## Name forms

| Value | Name | Meaning |
| --- | --- | --- |
| `SYSTEMATIC_NAME` | Full name | Full or explicit structural name, including IUPAC names and short names with a definite chemical identity. |
| `TRIVIAL_COMMON_NAME` | Common name | Conventional chemical name, generic drug name, or trade name identifying a single ingredient. |
| `UNAMBIGUOUS_ABBREVIATION` | Abbreviation | Name abbreviation with an unambiguous chemical identity in context, such as DMSO or DCM. Development codes, identifiers, and amino-acid sequence symbols are excluded. |
| `UNAMBIGUOUS_FORMULA` | Condensed structural formula | Unambiguous condensed structural formula or chemical element symbol, such as CH3COOH or Cu. Molecular formulas that do not identify a definite structure are excluded. |
| `null` | No category information | No name-form category information. |

The [schema](https://huggingface.co/datasets/PatSnap/chemical-ner-bench/blob/main/raw/schema.json) defines field types, allowed values and required fields.

## Evaluation

Entity reference answers support comparison of names, chemical entity classes and boundaries. Structure normalization uses eligible nonempty references in the selected structure field. Report precision, recall and F1 separately for entity recognition and structure normalization.

Reports specify matching units and conditions, deduplication, structure-reference eligibility and coverage, aggregation and zero-denominator conventions. Present claims and description results separately. Mentions, names and structures are distinct counting units; an entity without a structure reference remains available for applicable entity-recognition evaluation.

See the [evaluation guide](https://huggingface.co/datasets/PatSnap/chemical-ner-bench/blob/main/EVALUATION.md) for reporting requirements.

## Configuration and use

Hugging Face provides the `default` configuration with 22 records in the `test` split. Sign in with an HF account that has repository access:

```bash
hf auth login
```

```python
from datasets import load_dataset

records = load_dataset("PatSnap/chemical-ner-bench", split="test", token=True)
input_fields = [
    "record_id", "publication_number", "language", "section", "text"
]
model_inputs = records.select_columns(input_fields)
model_input = model_inputs[0]
```

Use `ground_truth` separately for evaluation, excluding it from model requests.

## Citation and license

```bibtex
@dataset{patsnap_chemical_ner_bench_2026,
  title   = {Chemical NER Bench},
  author  = {PatSnap},
  year    = {2026},
  version = {1.2.1},
  url     = {https://huggingface.co/datasets/PatSnap/chemical-ner-bench}
}
```

The dataset and reference answers use [CC BY-NC 4.0](https://huggingface.co/datasets/PatSnap/chemical-ner-bench/blob/main/LICENSE), subject to applicable third-party rights. The reader and project documentation use the [MIT License](../LICENSE).
