# Chemical OCSR

[LSBench](../README.md) · [Evaluation Protocol](../docs/evaluation-protocol.md)

Chemical OCSR evaluates recognition of complete molecular structures from chemical structure images.

## Input

Pre-cropped chemical structure images from patent pages.

## Output

Machine-readable molecular structures preserving atom connectivity, bond information, and stereochemistry.

## Evaluation

- One-to-one matching of predicted and reference structures within source-page groups.
- Precision, recall, and F1 for complete structure matches.
- Preservation of repeated occurrences of the same structure within a page.

Input crop counts and reference structure counts are distinct evaluation units. The task covers recognition from pre-cropped images; whole-page detection and segmentation require separate evaluation.

## License

See the [project licensing information](../README.md#license) and [MIT License](../LICENSE).
