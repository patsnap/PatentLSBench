# Chemical NER

[LSBench](https://github.com/patsnap/LSBench#english) · **English** | [简体中文](README.zh.md) · [Evaluation Protocol](../docs/evaluation-protocol.md)

Chemical NER evaluates extraction of chemical names and their associated molecular structures from patent claims or description text.

## Input

The claims or description text of a patent.

## Output

Chemical names and their associated molecular structures identified from the supplied text.

## Evaluation

- Chemical name-set precision, recall and F1.
- Molecular structure-set precision, recall and F1, reported separately from name scores.
- Repeated occurrences of the same name or structure are represented once in the corresponding set.

Matching is bounded by the supplied claims or description.

## License

See the [project licensing information](https://github.com/patsnap/LSBench#license) and [MIT License](../LICENSE).
