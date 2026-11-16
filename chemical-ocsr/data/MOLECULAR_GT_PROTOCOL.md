# Molecular ground-truth protocol

[Edition overview](README.md) · **English** | [简体中文](MOLECULAR_GT_PROTOCOL.zh.md)

Version: 1.0.0 · RDKit 2024.03.2

## Source and scope

Supplied original MOL files are preserved byte for byte. Canonical SMILES and standard InChIKeys are deterministic derived serializations of supported reference graphs; they are not newly drawn structures. `dataset_manifest.json` records per-format populations and `evaluation_masks.json` supplies the exact fixed target lists. MOL coverage, SMILES coverage and InChIKey coverage are separate quantities.

## Fixed abbreviation expansion

Only the exact, case-sensitive labels in the frozen dictionary below are supported. The machine-readable dictionary and attachment rules are in `normalization/fixed_abbreviations.json`; `normalization_manifest.json` lists the actual expanded reference region IDs for this edition. MolScribe-derived mappings retain their MIT notice and license in `normalization/`.

Expansion operates on a graph copy. An alias must occupy a neutral, non-isotopic dummy atom with no radical, one neighbor, one single attachment bond and no specified atom chirality. Fragment atom 0 is the attachment root. Original atom order, existing bonds and their directions/stereo, atom chiral tags and component count are retained. Added fragment atoms have no source coordinates, so conformers are removed only on the derived graph; source MOL coordinates are preserved. The artificial open-valence root radical of a dictionary fragment is cleared on forming its declared attachment; source radicals are not changed.

| Exact label | Fragment SMILES; root = atom 0 |
| --- | --- |
| `Me` | `C` |
| `Et` | `CC` |
| `iPr` | `C(C)C` |
| `OMe` | `OC` |
| `OCH3` | `OC` |
| `H3CO` | `OC` |
| `MeO` | `OC` |
| `OEt` | `OCC` |
| `EtO` | `OCC` |
| `OBn` | `OCc1ccccc1` |
| `BnO` | `OCc1ccccc1` |
| `Bn` | `Cc1ccccc1` |
| `Ph` | `c1ccccc1` |
| `CF3` | `C(F)(F)F` |
| `F3C` | `C(F)(F)F` |
| `CCl3` | `C(Cl)(Cl)Cl` |
| `NO2` | `[N+](=O)[O-]` |
| `O2N` | `[N+](=O)[O-]` |
| `CN` | `C#N` |
| `NC` | `C#N` |
| `CHO` | `C=O` |
| `OSiEt3` | `O[Si](CC)(CC)CC` |
| `Boc` | `[C](=O)OC(C)(C)C` |
| `Cbz` | `[C](=O)OCc1ccccc1` |
| `Fmoc` | `[C](=O)OCC1c(cccc2)c2c3c1cccc3` |
| `NHBoc` | `[NH1]C(=O)OC(C)(C)C` |
| `CO2Et` | `[C](=O)OCC` |
| `COOEt` | `[C](=O)OCC` |
| `OtBu` | `[O]C(C)(C)C` |
| `OMs` | `[O]S(=O)(=O)C` |
| `OTf` | `[O]S(=O)(=O)C(F)(F)F` |
| `OAc` | `[O]C(=O)C` |
| `Ac` | `[C](=O)C` |
| `CO2H` | `[C](=O)O` |
| `COOH` | `[C](=O)O` |
| `HO2C` | `[C](=O)O` |
| `SO3H` | `[S](=O)(=O)O` |

Unknown, composite or ambiguous aliases are not guessed. Accepted expansions require strict sanitization, no residual dummy/query/alias graph, preserved source graph invariants, stable canonical-SMILES roundtrip, equality of the graph-derived and SMILES-derived standard InChIKeys, and full equality with the pre-existing source Key when one is available. These acceptance checks concern reference construction; prediction correctness is judged against the frozen reference, without using the answer to repair the prediction.

## Parsing and serialization

Original MOL parsing uses `Chem.MolFromMolFile(path, sanitize=True, removeHs=False, strictParsing=True)`. Canonical serialization uses `Chem.MolToSmiles(mol, canonical=True, isomericSmiles=True)`. Both published reference and predicted SMILES must be parsed using these explicit settings:

```python
from rdkit import Chem
from rdkit.Chem import rdinchi

params = Chem.SmilesParserParams()
params.removeHs = False
params.sanitize = True
params.parseName = False
params.allowCXSMILES = False
mol = Chem.MolFromSmiles(smiles, params)
if mol is None:
    raise ValueError("Invalid SMILES")
canonical_smiles = Chem.MolToSmiles(mol, canonical=True, isomericSmiles=True)
inchi, code, message, log, aux = rdinchi.MolToInchi(mol, '')
standard_inchikey = rdinchi.InchiToInchiKey(inchi) if inchi else None
```

Standard InChI generation uses empty options and an `InChI=1S/` result. Every non-null published SMILES is reparsed and checked for canonical stability. Every non-null published Key is independently reproduced from its paired published SMILES. Set `removeHs=False` to retain explicit hydrogen atoms. Preserve disconnected components, formal charge, isotopes, explicit hydrogens and specified stereochemistry. No salt stripping, charge neutralization, tautomer standardization, permissive sanitization fallback or stereo repair is applied.

The exclusions above refer to additional input-graph preprocessing; standard-InChI normalization still applies. See the [identifier metric scope](EVALUATION.md).

## Missing values and scoring

A null standard field means that a safe, supported representation was not established under this protocol. The original MOL remains available. No original shorthand pseudo-SMILES is substituted into a standards-compliant field. A valid canonical SMILES may lack a supported standard InChIKey, particularly for coordination-bond graphs. Use the fixed SMILES and InChIKey lists for their respective metrics.

Use the versioned fixed masks in `evaluation_masks.json`. Missing, refused, invalid and wrong predictions remain failures within the relevant fixed list. Original MOL text equality is not a molecular-identity metric; Key equality is not a drawing-geometry metric. See the [evaluation protocol](EVALUATION.md) for page-level and image-recognition scope, joint-recovery rules and reporting requirements.
