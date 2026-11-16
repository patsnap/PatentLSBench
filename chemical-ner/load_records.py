"""Read patent sections and keep reference answers out of model inputs.

The dataset and reference answers are licensed separately from this MIT reader.
"""
import argparse
import json
from pathlib import Path

INPUT_FIELDS = ("record_id", "publication_number", "language", "section", "text")


def load_records(path):
    """Yield JSON objects from a UTF-8 JSONL file, ignoring empty lines."""
    with Path(path).open(encoding="utf-8") as stream:
        for line in stream:
            if line.strip():
                yield json.loads(line)


def iter_inputs(records):
    """Yield only the five model-input fields; omit ground_truth."""
    for record in records:
        yield {field: record[field] for field in INPUT_FIELDS}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "records", nargs="?", type=Path,
        default=Path(__file__).parent / "data" / "test.jsonl",
        help="Path to the released section JSONL file",
    )
    args = parser.parse_args()
    records = list(load_records(args.records))
    summary = {
        "patents": len({row["publication_number"] for row in records}),
        "inputs": len(records),
        "input_unit": "patent_section",
        "input_characters": sum(len(row["text"]) for row in records),
        "ground_truth_entities": sum(len(row["ground_truth"]) for row in records),
        "empty_ground_truth_inputs": sum(not row["ground_truth"] for row in records),
    }
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
