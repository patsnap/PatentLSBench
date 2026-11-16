#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Validate Chemical NER Bench v1.2.2 and optionally report RDKit diagnostics.

Core validation needs only Python's standard library. Chemistry diagnostics do
not adjudicate whether a reference chemical annotation is correct.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
VERSION = '1.2.2'
PUBLICATIONS = {
    'CN108452553B', 'CN117229131A', 'US20110151089A1', 'US10065976B2',
    'KR1020220102156A', 'JP7371738B2', 'TWI822756B', 'CN121108339A',
    'JP2023552219A', 'US20200215266A1', 'CN113754674B',
}
EXPECTED_IDS = {f'chemner-{pn}-{section}' for pn in PUBLICATIONS for section in ('claim', 'description')}
RECORD_FIELDS = {'record_id', 'publication_number', 'language', 'section', 'text', 'ground_truth'}
ENTITY_FIELDS = {'start', 'end', 'text', 'label', 'smiles', 'inchikey', 'mention_form'}
LANGUAGES = {'CN', 'CNT', 'EN', 'JP', 'KR'}
LABELS = {'ChemicalCompound', 'compound'}
FORMS = {None, 'SYSTEMATIC_NAME', 'TRIVIAL_COMMON_NAME', 'UNAMBIGUOUS_ABBREVIATION', 'UNAMBIGUOUS_FORMULA'}
KEY_SHAPE = re.compile(r'[A-Z]{14}-[A-Z]{10}-[A-Z]')


def object_without_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'duplicate JSON object key: {key}')
        result[key] = value
    return result


def read_records(path):
    records, errors = [], []
    try:
        lines = path.read_text(encoding='utf-8').splitlines()
    except (OSError, UnicodeError) as error:
        return records, [{'error': str(error)}]
    for number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line, object_pairs_hook=object_without_duplicate_keys))
        except (ValueError, TypeError) as error:
            errors.append({'line': number, 'error': str(error)})
    return records, errors


def validate_core(records, read_errors):
    errors = list(read_errors)
    identifiers, publications, languages = [], [], collections.Counter()
    mentions = 0
    empty_references = []
    nonempty_smiles = nonempty_keys = shaped_keys = 0
    for row_index, row in enumerate(records):
        locator = {'row_index': row_index}
        if not isinstance(row, dict) or set(row) != RECORD_FIELDS:
            errors.append({**locator, 'error': 'record must contain exactly the six declared fields'})
            continue
        if any(not isinstance(row[key], str) for key in RECORD_FIELDS - {'ground_truth'}):
            errors.append({**locator, 'error': 'record metadata and text must be strings'})
            continue
        locator['record_id'] = row['record_id']
        identifiers.append(row['record_id'])
        publications.append(row['publication_number'])
        languages[row['language']] += 1
        if row['language'] not in LANGUAGES or row['section'] not in {'claim', 'description'}:
            errors.append({**locator, 'error': 'unknown language or section code'})
        if row['record_id'] != f"chemner-{row['publication_number']}-{row['section']}":
            errors.append({**locator, 'error': 'record_id does not match publication_number and section'})
        if not row['text']:
            errors.append({**locator, 'error': 'complete-section text is empty'})
        entities = row['ground_truth']
        if not isinstance(entities, list):
            errors.append({**locator, 'error': 'ground_truth must be a list'})
            continue
        mentions += len(entities)
        if not entities:
            empty_references.append(row['record_id'])
        for entity_index, entity in enumerate(entities):
            position = {**locator, 'entity_index': entity_index}
            if not isinstance(entity, dict) or set(entity) != ENTITY_FIELDS:
                errors.append({**position, 'error': 'entity must contain exactly the seven declared fields'})
                continue
            if (type(entity['start']) is not int or type(entity['end']) is not int or
                    any(not isinstance(entity[key], str) for key in ('text', 'label', 'smiles', 'inchikey')) or
                    (entity['mention_form'] is not None and not isinstance(entity['mention_form'], str))):
                errors.append({**position, 'error': 'entity field types are invalid'})
                continue
            if entity['label'] not in LABELS or entity['mention_form'] not in FORMS:
                errors.append({**position, 'error': 'unknown label or name-form code'})
            start, end = entity['start'], entity['end']
            if not (0 <= start < end <= len(row['text']) and row['text'][start:end] == entity['text']):
                errors.append({**position, 'error': 'span does not exactly index the original HTML using Unicode code points'})
            nonempty_smiles += bool(entity['smiles'])
            nonempty_keys += bool(entity['inchikey'])
            shaped_keys += bool(KEY_SHAPE.fullmatch(entity['inchikey']))
            if entity['inchikey'] and not KEY_SHAPE.fullmatch(entity['inchikey']):
                errors.append({**position, 'error': 'nonempty InChIKey does not match the 27-character identifier shape'})
    if len(records) != 22:
        errors.append({'error': 'v1.2.2 requires exactly 22 complete-section records', 'actual': len(records)})
    if len(identifiers) != len(set(identifiers)) or set(identifiers) != EXPECTED_IDS:
        errors.append({'error': 'record IDs are duplicated, missing or outside the public v1.2.2 release',
                       'missing': sorted(EXPECTED_IDS - set(identifiers)),
                       'unexpected': sorted(set(identifiers) - EXPECTED_IDS)})
    if set(publications) != PUBLICATIONS:
        errors.append({'error': 'publication membership differs from public v1.2.2'})
    if mentions != 6334:
        errors.append({'error': 'v1.2.2 requires 6,334 entity-reference mentions', 'actual': mentions})
    return {'status': 'FAIL' if errors else 'PASS', 'records': len(records),
            'publications': len(set(publications)), 'entity_mentions': mentions,
            'language_record_counts': dict(languages), 'empty_reference_records': empty_references,
            'nonempty_smiles_mentions': nonempty_smiles, 'nonempty_inchikey_mentions': nonempty_keys,
            'format_matching_inchikey_mentions': shaped_keys, 'errors': errors}


def chemistry_diagnostics(records):
    from rdkit import Chem, RDLogger, rdBase
    from rdkit.Chem import inchi
    if not inchi.INCHI_AVAILABLE:
        raise RuntimeError('the installed RDKit does not include InChI support')
    # Parsing failures and conversion failures are retained in the JSON counts.
    RDLogger.DisableLog('rdApp.*')
    cache = {}
    entities = [{'record_id': row['record_id'], 'entity_index': index, **entity}
                for row in records for index, entity in enumerate(row['ground_truth'])]
    for smiles in sorted({entity['smiles'] for entity in entities if entity['smiles']}):
        molecule = Chem.MolFromSmiles(smiles)  # default sanitization; no representation repair
        cache[smiles] = {'parsed': molecule is not None,
                         'key': inchi.MolToInchiKey(molecule) if molecule is not None else None}
    counts = collections.Counter()
    differences, parse_failures = [], []
    for entity in entities:
        smiles, reference = entity['smiles'], entity['inchikey']
        locator = {'record_id': entity['record_id'], 'entity_index': entity['entity_index']}
        if smiles and not cache[smiles]['parsed']:
            parse_failures.append(locator)
        if not (smiles and reference):
            continue
        result = cache[smiles]
        if not result['parsed']:
            counts['smiles_parse_failed'] += 1
            continue
        generated = result['key']
        if generated == reference:
            counts['full_key_equal'] += 1
            continue
        if not generated:
            category = 'standard_key_generation_failed'
        elif not KEY_SHAPE.fullmatch(reference):
            category = 'malformed_reference_key'
        elif reference[:23] == generated[:23] and reference[24:] == generated[24:] and reference[23] != generated[23]:
            category = 'standard_nonstandard_flag_only'
        elif reference[:14] == generated[:14]:
            category = 'same_first_hash_block_different_full_key'
        else:
            category = 'different_first_hash_block'
        counts[category] += 1
        differences.append({**locator, 'category': category})
    return {'status': 'DIAGNOSTICS', 'rdkit_version': rdBase.rdkitVersion,
            'inchi_version': inchi.GetInchiVersion() if hasattr(inchi, 'GetInchiVersion') else None,
            'settings': 'MolFromSmiles default sanitization; MolToInchiKey default standard InChI; no repair or substitution',
            'unique_nonempty_smiles': len(cache),
            'unique_smiles_parse_failures': sum(not item['parsed'] for item in cache.values()),
            'smiles_parse_failure_mentions': len(parse_failures),
            'nonempty_inchikey_mentions': sum(bool(entity['inchikey']) for entity in entities),
            'format_matching_inchikey_mentions': sum(bool(KEY_SHAPE.fullmatch(entity['inchikey'])) for entity in entities),
            'paired_identifier_counts': dict(counts), 'not_reproduced_full_keys': len(differences),
            'parse_failure_locations': parse_failures, 'different_key_locations': differences,
            'interpretation': 'Tool-specific conversion and identifier-comparison diagnostics; not proof of chemical identity, annotation error or annotation completeness.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('records', nargs='?', type=Path,
                        default=Path(__file__).resolve().parent / 'data/test.jsonl')
    parser.add_argument('--chemistry', action='store_true', help='also report diagnostics using an installed RDKit')
    args = parser.parse_args()
    records, read_errors = read_records(args.records)
    core = validate_core(records, read_errors)
    result = {'dataset_version': VERSION, 'status': core['status'], 'python_version': sys.version.split()[0],
              'records_file': str(args.records), 'records_sha256': hashlib.sha256(args.records.read_bytes()).hexdigest() if args.records.is_file() else None,
              'core': core}
    exit_code = 0 if core['status'] == 'PASS' else 1
    if args.chemistry and not exit_code:
        try:
            result['chemistry'] = chemistry_diagnostics(records)
        except (ImportError, RuntimeError) as error:
            result['status'] = 'FAIL'
            result['chemistry'] = {'status': 'UNAVAILABLE', 'error': str(error)}
            exit_code = 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return exit_code


if __name__ == '__main__':
    raise SystemExit(main())
