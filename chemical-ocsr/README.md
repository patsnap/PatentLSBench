# Chemical OCSR

[PatentLSBench](https://github.com/patsnap/PatentLSBench) · **English** | [简体中文](README.zh.md) · [Evaluation Protocol](../docs/evaluation-protocol.md)

Chemical OCSR evaluates molecular recognition from chemical structure images, and chemical-region detection and recognition from single-page PDF documents.

## Input and output

| Mode | Input | Output |
| --- | --- | --- |
| Image | A chemical structure image | Machine-readable molecular structures |
| PDF | A single PDF page | Chemical-region bounding boxes and recognized molecular structures |

Molecular structures preserve atom connectivity, bond information, and stereochemistry.

## Evaluation

| Layer | Applicable mode | Matching criteria | Metrics |
| --- | --- | --- | --- |
| Layout | PDF | One-to-one IoU matching of chemical-region bounding boxes | Precision, recall, F1 |
| OCSR | Image and PDF | Complete InChIKey matching of recognized and reference molecular structures | Precision, recall, F1 |

PDF mode reports Layout localization and OCSR recognition separately. Layout covers annotated chemical regions; molecular recognition is scored against complete-structure references with valid InChIKeys. Distinct occurrences of the same structure retain their multiplicity.

## License

See the [project licensing information](https://github.com/patsnap/PatentLSBench#license) and [MIT License](../LICENSE).
