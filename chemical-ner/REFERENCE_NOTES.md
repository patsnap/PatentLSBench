# Chemical NER Bench Reference Notes

[Dataset](README.md) · **English** | [简体中文](REFERENCE_NOTES.zh.md)

## Reference coverage

Version **1.2.2** contains 22 complete section inputs and 6,334 entity-reference mentions. Structure fields contain 6,066 nonempty SMILES values and 6,016 nonempty InChIKey values. All 6,016 Keys match the 27-character identifier shape; this format check does not establish chemical identity or successful conversion.

The two structure fields are not guaranteed to be equivalent for every reference. With RDKit **2024.3.2** and default sanitization, 17 mentions (8 distinct SMILES strings) do not parse. Among the remaining paired references, 5,919 reproduce the supplied full Key and 80 do not: 4 fail to generate a standard Key, 19 differ only in the standard/nonstandard flag, 52 have different first hash blocks, and 5 share the first block but differ in the full Key. These categories are not a count of proven annotation errors; metal coordination and representation conventions can affect conversion.

Evaluation reports must state the chosen structure field, eligibility and normalization, supported representations and reference coverage. Do not substitute SMILES-derived Keys for supplied Keys without declaring that policy. An unavailable or unsupported structure reference does not remove the mention from applicable entity-recognition evaluation.

The [portable validator](validate_dataset.py) checks record membership, fields, counts, identifier shape and exact HTML offsets using Python's standard library. Its optional chemistry diagnostics reproduce the categories above with an installed RDKit and report that library's version:

```bash
python chemical-ner/validate_dataset.py chemical-ner/data/test.jsonl
python chemical-ner/validate_dataset.py chemical-ner/data/test.jsonl --chemistry
```

An explicit JSONL path may be supplied as a positional argument. Conversion diagnostics do not establish annotation correctness or completeness.

## Empty entity-reference lists

Three claim inputs have `ground_truth = []`. This means the section has no supplied entity references; it does not establish that its text contains no chemical names or that it is an exhaustively verified negative example. Keep these inputs and state how empty-reference records are handled in each evaluation.

## Names and coordinates

Reference names may contain HTML markup or leading/trailing whitespace, and one nested span pair is present. Stored `start` and `end` index the original `text`, including markup, as zero-based, half-open Unicode code-point intervals. Removing HTML or trimming names does not preserve those coordinates. Any name normalization, nested-mention handling or deduplication must be stated separately from coordinate alignment. `ChemicalCompound` and `compound` denote the same chemical-entity category.

## Version 1.2.2 correction

The toluene reference in `chemner-US10065976B2-description`, entity index `71` (zero based), now uses `YXFVVABEGXRONW-UHFFFAOYSA-N`. Version 1.2.1 lacked the final `N`. Both standard InChI and direct molecule conversion from the supplied SMILES `CC1=CC=CC=C1` yield the corrected Key. All other record values and the record/entity order are unchanged. The exact correction and verification methods are recorded in [data_corrections.json](data_corrections.json).

See the [evaluation guide](EVALUATION.md) for reporting requirements.
