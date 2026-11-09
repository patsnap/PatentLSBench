# Chemical NER

[LSBench](../README.md) · [Evaluation Protocol](../docs/evaluation-protocol.md)

Chemical NER evaluates extraction of chemical names and molecular structures from complete patent text.

## Input

The complete text of a chemical patent.

## Output

Chemical names and their associated molecular structures, represented as patent-level collections.

## Evaluation

- Patent-level set precision, recall, and F1.
- Separate reporting for chemical names and molecular structures.
- Deduplication of repeated occurrences of the same structure within a patent.
- Name-based fallback for reference annotations without a molecular structure.

The evaluation unit is the patent.

## License

See the [project licensing information](../README.md#license) and [MIT License](../LICENSE).
