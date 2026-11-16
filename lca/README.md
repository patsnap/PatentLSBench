# LCA

[PatentLSBench](https://github.com/patsnap/PatentLSBench) · **English** | [简体中文](README.zh.md)

LCA evaluates evidence-based identification of candidate molecules and tracing between drug codes, patents, and structures.

## Input and output

| Input mode | Input | Output |
|---|---|---|
| Patent identifier | A single patent identifier | Candidate molecules with structures, disclosed activity, source locations, and evidence grades |
| Drug code | A single drug code | Relevant patents and candidate molecules, with evidence supporting the drug–patent–structure relationship |

## Evaluation

- Patent relevance and object identity.
- Complete structure matches for cases with a disclosed reference target.
- Support for activity claims, source locations, and evidence grades.
- Completeness of candidate evidence and traceability between the requested objects.

The two input modes are reported separately. Known-target structure-hit results identify the applicable subset and do not establish exhaustive patent or candidate recall. Evidence grades describe verification depth; equally supported candidates do not require an arbitrary unique winner.



## License

See the [project licensing information](https://github.com/patsnap/PatentLSBench#license) and [MIT License](../LICENSE).
