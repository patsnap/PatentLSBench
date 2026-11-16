# Chemical NER Bench Evaluation

[Dataset](README.md) · **English** | [简体中文](EVALUATION.zh.md)

Version 1.2.2 provides independent complete `claim` and `description` inputs with entity-level reference answers.

This release provides reference data and reporting requirements, rather than a canonical executable scorer or a frozen default matching profile. Scores are comparable only when the matching, eligibility and aggregation profile is identical.

See the [reference notes](REFERENCE_NOTES.md) for annotation coverage and structure representation limits. Empty reference lists are not certified chemical-free negatives.

## Input and reference fields

Model requests contain `record_id`, `publication_number`, `language`, `section` and `text`. Use `ground_truth` separately for evaluation.

Record `text` is the complete section HTML. Entity boundaries use zero-based, half-open Unicode code-point intervals `[start, end)` in that string, including markup characters. Empty entity-reference lists are valid records.

Each reference entity supplies its name (`text`), chemical entity class (`label`), boundaries (`start`, `end`), structure identifiers (`smiles`, `inchikey`) and name form (`mention_form`). `ChemicalCompound` and `compound` both denote chemical entities. Empty structure strings indicate unavailable reference identifiers; a null name form indicates no category information.

## Entity recognition and structure normalization

| Evaluation | Reference fields | Reporting scope |
| --- | --- | --- |
| Entity recognition | Name, class and boundaries | State the matching unit and which fields are required for a match |
| Structure normalization | Eligible nonempty `smiles` or `inchikey` values | State the identifier field, eligibility checks, normalization and reference coverage |

Report precision, recall and F1 separately for entity recognition and structure normalization. The reference list supports entity-mention comparison. Any deduplication or chapter-local name/structure aggregation must be specified with the evaluation rules; it does not change the dataset's entity-mention count.

For InChIKey comparison, use full identifier strings. State how malformed or unavailable references and predictions outside the eligible population are handled. An entity without an eligible structure reference still participates in applicable entity-recognition evaluation.

## Counts and aggregation

For the declared matching unit, report true positives (TP), predicted items and reference items. Precision is `TP / predicted`, recall is `TP / reference`, and F1 is `2 × TP / (predicted + reference)`.

Present claims and description results separately. Identify any combined result and its aggregation method, including zero-denominator and failed-request conventions. Micro aggregation, when used, sums the corresponding counts before computing ratios.

Each report identifies the dataset version and split, evaluated record IDs, prediction format, matching conditions, normalization, deduplication, reference eligibility and aggregation rules. The dataset contains 6,334 entity mentions; mention, name and structure counts are different units.

## License

Dataset and reference answers: [CC BY-NC 4.0](data/LICENSE). Reader and project documentation: [MIT](../LICENSE).
