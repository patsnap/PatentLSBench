# SAR

[LSBench](https://github.com/patsnap/LSBench#english) · **English** | [简体中文](README.zh.md) · [Evaluation Protocol](../docs/evaluation-protocol.md)

SAR evaluates extraction of disclosed structure–activity evidence from complete small-molecule patents.

## Input

A complete small-molecule patent containing compound structures, experimental descriptions, and activity measurements.

## Output

Activity records linked to compound structures, experimental context, and evidence locations.

## Evaluation

Records are aligned by compound and experiment. Assessment covers record completeness, field-level precision, recall, and F1, and the correctness of compound–experiment–measurement relationships.

| Field | Evaluation focus |
|---|---|
| Compound identifier | Association with the compound described in the patent |
| Assay endpoint | Identity of the reported measurement |
| Value | Faithful extraction of the reported result |
| Unit | Correct unit associated with the measurement |
| Experimental model | Experimental system or context |
| Target | Target associated with the experiment |
| Method | Reported experimental method |
| Structure identity | Complete molecular identity |
| Activity source location | Traceability of the activity evidence |
| Structure source location | Traceability of the structure evidence |

Field accuracy, relationship coverage and whole-patent completeness are reported separately.

## License

See the [project licensing information](https://github.com/patsnap/LSBench#license) and [MIT License](../LICENSE).
