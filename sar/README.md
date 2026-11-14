# SAR

[PatentLSBench](https://github.com/patsnap/PatentLSBench) · **English** | [简体中文](README.zh.md) · [Evaluation Protocol](../docs/evaluation-protocol.md)

SAR evaluates extraction of disclosed structure–activity evidence from small-molecule patents.

## Input

Source patent material containing compound structures, experimental descriptions and activity measurements.

## Output

Activity records linked to compound structures, experimental context and evidence locations.

## Evaluation

Records are matched one to one within each patent by compound and experimental context. Evaluation uses field-level and joint-field record-level precision, recall and F1, aggregated from counts across patents. Compound–experiment–measurement associations are checked through record alignment and field assessment.

| Field | Evaluation focus |
|---|---|
| Compound identifier | Association with the compound described in the patent |
| Assay endpoint | Identity of the reported measurement |
| Value | Meaning of the reported result, including qualifiers and ranges |
| Unit | Unit and dimension associated with the measurement |
| Experimental model | Experimental system or context |
| Target | Target associated with the experiment |
| Method | Reported experimental method |
| Structure identity | Complete molecular identity |
| Activity source location | Traceability of the activity evidence |
| Structure source location | Traceability of the structure evidence |

Equivalent terminology and valid unit conversions are assessed in the context of the reported experiment, preserving the meaning of values, qualifiers, ranges and conditions.

Results are reported separately for:

- **SAR fields:** compound identifier, assay endpoint, value, unit, experimental model, target and method.
- **Structure–activity records:** SAR fields together with chemical identity.
- **End-to-end records:** structure–activity records together with activity and structure source locations.

A record-group match requires the corresponding fields to agree within the same aligned record. Per-field results and record-group results are reported separately.

## License

See the [project licensing information](https://github.com/patsnap/PatentLSBench#license) and [MIT License](../LICENSE).
