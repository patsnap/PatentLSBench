# Evaluation Protocol

[PatentLSBench](https://github.com/patsnap/PatentLSBench) · **English** | [简体中文](evaluation-protocol.zh.md)

PatentLSBench evaluates the professional outputs of AI models and agents across its core life-science tasks. Each task has its own evaluation object, matching criteria, and metrics.

## Tasks and metrics

| Task | Evaluation object | Metrics |
|---|---|---|
| [Chemical NER](../chemical-ner/README.md) | Chemical names and structures from patent claims or description text | Name-set and structure-set precision, recall and F1, reported separately |
| [Chemical OCSR](../chemical-ocsr/README.md) | Image recognition, or single-page PDF localization and recognition | Image: InChIKey recognition P/R/F1. PDF: separate IoU-based Layout and InChIKey-based OCSR P/R/F1 |
| [SAR](../sar/README.md) | Disclosed activity records and their links to structures, experiments, and source locations | Field-level and aligned record-group precision, recall and F1 |
| [LCA](../lca/README.md) | Candidate evidence from a patent identifier, or patent-and-candidate tracing from a drug code | Patent relevance, known-target structure hits, and evidence support; two input modes reported separately |
| [LS Research](../ls-research/README.md) | Complete research answers or reports with source citations | Key-point coverage, factual quality, and citation support |

Chemical NER evaluates claims or description text. Chemical OCSR supports image-only recognition and single-page PDF Layout plus recognition, with the two PDF layers reported separately. SAR evaluates disclosed experimental records. LCA evaluates candidate identification and evidence-based tracing. LS Research evaluates complete answers and supporting sources.

## Matching and evidence

- **Chemical NER:** name and molecular-structure sets are evaluated within the supplied claims or description text. Repeated occurrences of the same item contribute once to the corresponding set; names and structures are reported separately.
- **Chemical OCSR:** image mode compares complete InChIKeys. PDF mode matches chemical-region boxes one to one using IoU and evaluates molecular identity using complete InChIKeys. Layout and OCSR precision, recall and F1 are reported separately. Distinct occurrences of the same structure retain their multiplicity.
- **SAR:** predicted and reference records are aligned by compound and experimental context. Field assessment covers compound identifier, assay endpoint, value, unit, experimental model, target, method, structure identity, activity source location, and structure source location. Record alignment and joint field checks preserve the association between the compound, experiment, measurement, and evidence.
- **LCA:** patent relevance, complete structure identity, activity evidence, source locations, and evidence grades are assessed for the applicable input mode. Evidence grades describe verification depth. Known-target hit metrics apply to the subset with a disclosed reference structure and do not establish exhaustive recall.
- **LS Research:** assessment covers whether the response answers the research question, includes the necessary findings, states facts accurately, and cites sources that support the corresponding claims.

## Comparable evaluation conditions

Comparisons use the same task materials, evidence scope, information cutoff, permitted tools, and execution budget. Model and agent submissions are reported within their respective tracks. Reports identify the evaluated system, task and reference versions, matching or rubric criteria, and applicable run conditions.

Each task reports its own evaluation units, metrics, coverage, and limitations. Patent, page, image, structure, record, and question counts remain distinct. NER names and structures are reported separately; LCA patent-identifier and drug-code results are reported separately. PatentLSBench does not combine different task units into a single overall score.

## License

Repository code and project documentation use the [MIT License](../LICENSE). Dataset content, annotations, and accompanying assets follow [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/), subject to applicable source-specific terms and third-party rights. See the [project licensing information](https://github.com/patsnap/PatentLSBench#license).
