#!/usr/bin/env python3
"""Read or verify an extracted Chemical OCSR edition using Python's standard library."""
import argparse
import hashlib
import json
from pathlib import Path


def read_rows(root, name):
    with (root / name).open(encoding='utf-8') as stream:
        return [json.loads(line) for line in stream if line.strip()]


def asset(root, name):
    path = (root / name).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError(f'Invalid asset path: {name}')
    return path


def inspect(root, verify=False):
    root = root.resolve()
    pages = read_rows(root, 'pages.jsonl')
    regions = read_rows(root, 'regions.jsonl')
    molecules = read_rows(root, 'ocsr.jsonl')
    masks = json.loads((root / 'evaluation_masks.json').read_text(encoding='utf-8'))
    for page in pages:
        asset(root, page['pdf_path'])
        if page['layout_count'] != len(page['layout_gt']):
            raise ValueError(f"Layout count mismatch: {page['id']}")
        if page['ocsr_count'] != len(page['ocsr_gt']):
            raise ValueError(f"Molecular reference count mismatch: {page['id']}")
    expected = {
        'layout_page_ids': {p['id'] for p in pages},
        'layout_region_ids': {r['id'] for r in regions},
        'mol_region_ids': {m['region_id'] for m in molecules},
        'smiles_region_ids': {m['region_id'] for m in molecules if m['smiles']},
        'inchikey_region_ids': {m['region_id'] for m in molecules if m['inchikey']},
        'paired_identifier_region_ids': {m['region_id'] for m in molecules if m['smiles'] and m['inchikey']},
    }
    for name, ids in expected.items():
        if len(ids) != len(masks[name]) or ids != set(masks[name]):
            raise ValueError(f'Scoring mask mismatch: {name}')
    checked = 0
    if verify:
        for line in (root / 'SHA256SUMS').read_text(encoding='utf-8').splitlines():
            expected_hash, name = line.split(None, 1)
            path = asset(root, name.lstrip('*'))
            if hashlib.sha256(path.read_bytes()).hexdigest() != expected_hash:
                raise ValueError(f'Checksum mismatch: {name}')
            checked += 1
    # Feed only the original PDF bytes to a page model. layout_gt/ocsr_gt are evaluator references.
    first = pages[0]
    return {
        'pages': len(pages), 'publications': len({p['patent_no'] for p in pages}),
        'regions': len(regions), 'mol_references': len(molecules),
        'smiles_targets': len(expected['smiles_region_ids']),
        'inchikey_targets': len(expected['inchikey_region_ids']),
        'verified_files': checked,
        'example_input': {'id': first['id'], 'pdf_path': str(asset(root, first['pdf_path']))},
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('edition_root', type=Path, help='Directory containing pages.jsonl and assets/')
    parser.add_argument('--verify', action='store_true', help='Verify every source checksum')
    args = parser.parse_args()
    print(json.dumps(inspect(args.edition_root, args.verify), ensure_ascii=False, indent=2))
