# Evaluation Protocol

[LSBench](../README.md) · [简体中文](../README.zh.md)

LSBench evaluates the professional outputs of AI models and agents across five life-sciences tasks. Each task has its own evaluation object, matching criteria, and metrics.

## Tasks and metrics

| Task | Evaluation object | Metrics |
|---|---|---|
| [Chemical NER](../chemical-ner/README.md) | Chemical names and molecular structure sets extracted from complete patent text | Patent-level set precision, recall, and F1; names and structures reported separately |
| [Chemical OCSR](../chemical-ocsr/README.md) | Complete molecular structures recognized from pre-cropped images | Page-grouped one-to-one structure matching precision, recall, and F1; repeated structures retain their multiplicity |
| [SAR](../sar/README.md) | Disclosed activity records and their links to structures, experiments, and source locations | Record alignment, field-level precision, recall, and F1, and relationship quality |
| [LCA](../lca/README.md) | Candidate evidence from a patent identifier, or patent-and-candidate tracing from a drug code | Patent relevance, known-target structure hits, and evidence support; two input modes reported separately |
| [Hiro LS Research](../hiro-ls-research/README.md) | Complete research answers or reports with source citations | Key-point coverage, factual quality, and citation support |

Chemical NER evaluates text extraction. Chemical OCSR evaluates recognition from pre-cropped structure images; whole-page detection and segmentation are separate tasks. SAR evaluates disclosed experimental evidence. LCA evaluates candidate identification and evidence-based tracing. Hiro LS Research evaluates the complete answer and its supporting sources.

## Matching and evidence

- **Chemical NER:** repeated occurrences of the same structure within a patent contribute one item to its structure set. Name-based fallback applies to reference annotations without a molecular structure. Name and structure matching are evaluated separately.
- **Chemical OCSR:** predictions and references are matched one to one within source-page groups. Structure identity includes atom connectivity, bond information, and stereochemistry. Repeated appearances of the same structure remain separate occurrences.
- **SAR:** predicted and reference records are aligned by compound and experimental context. Field assessment covers compound identifier, assay endpoint, value, unit, experimental model, target, method, structure identity, activity source location, and structure source location. Relationships preserve the association between the compound, experiment, measurement, and evidence.
- **LCA:** patent relevance, complete structure identity, activity evidence, source locations, and evidence grades are assessed for the applicable input mode. Evidence grades describe verification depth. Known-target hit metrics apply to the subset with a disclosed reference structure and do not establish exhaustive recall.
- **Hiro LS Research:** assessment covers whether the response answers the research question, includes the necessary findings, states facts accurately, and cites sources that support the corresponding claims.

## Comparable evaluation conditions

Comparisons use the same task materials, evidence scope, information cutoff, permitted tools, and execution budget. Model and agent submissions are reported within their respective tracks. Reports identify the evaluated system, task and reference versions, matching or rubric criteria, and applicable run conditions.

Each task reports its own evaluation units, metrics, coverage, and limitations. Patent, image, structure, record, and question counts remain distinct. NER names and structures are reported separately; LCA patent-identifier and drug-code results are reported separately. LSBench does not combine different task units into a single overall score.

## License

Repository code and project documentation use the [MIT License](../LICENSE). Dataset content, annotations, and accompanying assets follow [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/), subject to applicable source-specific terms and third-party rights. See the [project licensing information](../README.md#license).
