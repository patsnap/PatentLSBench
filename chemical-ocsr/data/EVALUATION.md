# Evaluation protocol

[Edition overview](README.md) · **English** | [简体中文](EVALUATION.zh.md)

Version: 1.0.0

## 1. Input and coordinates

The PDF mode takes the supplied single-page PDF referenced by `pages.jsonl:pdf_path`. Every PDF in this edition is a raster-only image PDF containing one page image and no text layer. `page_no` is the page number in the source patent; every supplied PDF itself has one page. Page previews support inspection. The supplied annotated crops are the input for image-based OCSR, reported separately from PDF recognition.

GT boxes are normalized `[x1, y1, x2, y2]` in `[0,1]`, with a top-left origin. `coordinate_reference_size` is `[width, height]` of the original annotation raster. Divide pixel predictions by the width and height of the model's own aligned page rendering. Apply PDF rotation and visible-page geometry consistently, without applying DPI scaling twice.

## 2. Layout detection

Evaluate every `layout_region_ids` target on every `layout_page_ids` page in `evaluation_masks.json`. Complete structures, substituents, Markush structures and other non-complete chemical expressions are all chemical-region targets. Molecular-identifier availability does not define the Layout scope.

On each page, create candidate prediction–GT edges where IoU >= 0.5. Find a one-to-one assignment that first maximizes matched-pair count, then total IoU. Resolve any remaining tie deterministically by GT `region_id` and the prediction's stable output index; molecular correctness must not influence assignment. A prediction and a GT region can each match at most once. Duplicate or unmatched predictions are false positives; unmatched GT regions are false negatives. Aggregate TP, FP and FN over all pages and report `P = TP/(TP+FP)`, `R = TP/(TP+FN)` and `F1 = 2TP/(2TP+FP+FN)`. If there are no predictions, use P = 0; this dataset has nonzero GT.

## 3. Molecular structure recognition

Use `inchikey_region_ids` for full standard InChIKey identity matching. Canonical-SMILES exact match is a supplementary structure metric on `smiles_region_ids`; each metric uses its own fixed target list. `paired_identifier_region_ids` is their intersection. `mol_region_ids` records the population with preserved original MOL files and is not an interchangeable denominator for either standard-format metric.

Use RDKit 2024.03.2 and canonical isomeric serialization. Parse both reference and predicted SMILES with the following explicit settings, then compare `MolToSmiles(..., canonical=True, isomericSmiles=True)`:

```python
from rdkit import Chem

params = Chem.SmilesParserParams()
params.removeHs = False
params.sanitize = True
params.parseName = False
params.allowCXSMILES = False

def canonical_structure(smiles):
    mol = Chem.MolFromSmiles(smiles, params)
    if mol is None:
        return None
    return Chem.MolToSmiles(mol, canonical=True, isomericSmiles=True)
```

Set `removeHs=False` to retain explicit hydrogen atoms. Preserve disconnected components, formal charge, isotopes and specified stereochemistry. Do not strip salts, neutralize charges, standardize tautomers or repair stereochemistry. Invalid, absent, refused or incorrect predictions score zero within the frozen target list. Do not filter the denominator by prediction validity or model support. Compare molecular representations, not MOL text bytes. If the model returns MOL, use strict sanitization with `removeHs=False`; supported aliases must follow [molecular reference protocol](MOLECULAR_GT_PROTOCOL.md) before comparison.

For InChIKey identity matching, compare the full standard InChIKey string, or derive it using `rdkit.Chem.rdinchi.MolToInchi(mol, '')` and `InchiToInchiKey`. Report the fixed Key-list denominator separately. InChIKey equality does not demonstrate atom-coordinate or drawing-geometry accuracy. Connectivity-only or stereo-removed scores may be supplied as explicitly named supplementary metrics with the exact transformation specified; report them separately from full-identity matching.

These preservation rules apply before identifier generation. Standard InChI still applies its own normalization and can merge recognized mobile-H tautomers. Key equality does not establish identical drawing bonds, hydrogen placement or coordinates. See the [InChI technical FAQ](https://www.inchi-trust.org/technical-faq/).

## 4. Page-level end-to-end recovery

For each molecular-format list, a target is recovered only if its predicted region is matched by the fixed Layout assignment and the molecular answer is correct under the corresponding format protocol. Report `recovered targets / fixed format-list targets` across every supplied PDF. A single prediction cannot recover multiple targets. Layout misses, routing errors, refusal, absent output, invalid output and incorrect structures all remain in the denominator. A Layout match to an unscored region cannot be reassigned to improve molecular accuracy.

Regions outside a molecular scoring list still participate in Layout evaluation. Identifier nulls are not negative chemical answers, and unsupported molecular formats do not turn a chemical region into background.

## 5. Reporting and slices

Report edition, version, model input, matching rule, toolkit version and the actual target numerator and denominator for every metric. Use micro aggregation across regions for the main metrics; label any page-macro result separately. Score feature slices using the relevant fixed-format list intersected with that feature. Dimensions are multi-label, so slices overlap. For a dimension, `[]` is assessed with no listed feature; `null` is technically unavailable and is excluded from that dimension's denominator.

## 6. Evaluation implementation and result comparability

This release provides the data, reference populations and evaluation scope; it does not include an executable recognition scorer. For reported molecular precision, recall and F1, identify the complete evaluation profile: the prediction unit and its input-page or crop association, treatment of multiple and duplicate outputs, invalid and empty outputs, matching procedure, and TP/FP/FN counts and denominators. Do not present results from different counting or matching profiles as directly equivalent. The fixed Layout assignment and joint-recovery rules above remain applicable to the joint-recovery metric.
