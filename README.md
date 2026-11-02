# Benford-Weighted Digit Sums and Second-Order Asymptotics for Exponential Sequences

Public reproducibility repository for the paper by **Radhe Dhoundiyal**, Independent Researcher. The current release is **v1.0.0**, dated **2026-09-05**.

Manuscript: [authoritative PDF](manuscript/paper.pdf) · [LaTeX source](manuscript/paper.tex) · [BibTeX references](manuscript/references4.bib)

Public preprint: [SSRN DOI 10.2139/ssrn.7492000](https://doi.org/10.2139/ssrn.7492000).

The repository provides an adversarial verification package for exact and asymptotic formulas concerning significant base-`b` digits under the Benford mantissa measure and their transfer to leading windows of deterministic exponential sequences. It does not claim that computation proves the paper. Analytic proofs live in the manuscript; the software supplies independent exact-integer, interval, Gamma-function, arbitrary-precision, discrepancy, and numerical checks.

## Scope

`THEOREM_SPEC.md` records sixteen audited claims:

- **A1-A10** cover exact significant-digit laws, Gamma forms, finite digit-sum and cumulative-bias identities, the closed constant `c_b`, deep-position asymptotics, and the rigorously bounded finite-length tail.
- **D1-D6** cover interval-component counts, ordinary discrepancy bounds, leading-window observables, finite deterministic transfer, and the conditional second-order asymptotic for multiplicatively independent `a` and `b`.

All sixteen claims have status `PASS` in the final audit. “PASS” combines independent derivation with exact or high-precision checks as appropriate; it is not a claim that numerical evidence replaces the manuscript proofs or cited classical inputs. The repository makes no claim of independence, mixing, a central limit theorem, or a full-digit-sum asymptotic.

## Repository map

- `manuscript/paper.pdf` - frozen authoritative manuscript for this release.
- `manuscript/paper.tex` and `manuscript/references4.bib` - frozen compilable manuscript sources.
- `THEOREM_SPEC.md` - authoritative claim definitions, proof dependencies, and statuses.
- `outputs/reports/FINAL_VERIFICATION_REPORT.md` - final adversarial audit report.
- `src/` - independent mathematical implementations.
- `tests/` - deterministic pytest suite.
- `experiments/` - cross-base, asymptotic, discrepancy, and deterministic-pair checks.
- `scripts/` - test, experiment, figure, report-index, checksum, and repository validation entry points.
- `outputs/tables/` and `outputs/figures/` - reproducible verification products.
- `checksums.sha256` - SHA-256 manifest for the intended v1.0.0 archive state.

Historical referee and roadmap PDFs are retained locally under `source-material/` for provenance but are intentionally excluded from the public archive. The public manuscript is a byte-identical copy of the authoritative `source-material/Paper-4.pdf` at packaging time.

## Installation

Python 3.10 or newer is required. The validated environment used Python 3.12.

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

POSIX shells:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Dependencies are pinned to the versions used for the v1.0.0 verification run.

## Reproduce

Run the automated suite from the repository root:

```powershell
.\.venv\Scripts\python.exe scripts\run_all_tests.py
```

Expected result: `16 passed`.

Run the complete workflow, including experiments, figures, report indexes, checksums, and repository validation:

```powershell
.\.venv\Scripts\python.exe scripts\run_full_verification.py
```

The full workflow also compiles the manuscript with the standard sequence `pdflatex`, `bibtex`, `pdflatex`, `pdflatex`. A MiKTeX or TeX Live installation is required; the wrapper uses executables on `PATH` and also detects a standard per-user MiKTeX installation on Windows. To compile and compare the PDF independently:

```powershell
.\.venv\Scripts\python.exe scripts\build_manuscript.py
```

Build auxiliaries and the comparison PDF are isolated under `build/manuscript/` and excluded from the archive. The source uses the literal bibliography file `references4.bib`.

Individual commands:

```powershell
.\.venv\Scripts\python.exe scripts\run_all_experiments.py
.\.venv\Scripts\python.exe scripts\build_figures.py
.\.venv\Scripts\python.exe scripts\build_verification_report.py
.\.venv\Scripts\python.exe scripts\generate_checksums.py
.\.venv\Scripts\python.exe scripts\verify_repository.py
```

## Precision and numerical boundaries

The A10 cross-base tail experiment uses **220 decimal digits** (`mpmath.mp.dps = 220`) to prevent cancellation in differences of large log-Gamma terms. Unit tests use explicit 60-100 digit precision. Randomized discrepancy cross-checks use the fixed seed `20260905`.

Mantissa-based digit extraction can land just below an exact integer boundary (for example, prefixes corresponding to 8 or 64). `src/mantissa_digits.py` uses high precision plus a near-integer guard, while exact Python-integer extraction remains ground truth.

## Manuscript and compilation status

The frozen manuscript is `manuscript/paper.pdf`; its sources are `manuscript/paper.tex` and `manuscript/references4.bib`. The validated build produces a 35-page PDF with identical extracted text and pixel-identical rendered pages. Its byte hash differs because pdfTeX writes the build creation/modification timestamp (and derived internal PDF identifiers); the authoritative PDF is not replaced.

## Archival and citation

The public repository is <https://github.com/Radhe-Dhoundiyal/benford-weighted-digit-sums>. Use `CITATION.cff` for software citation metadata.

- Version 1.0.0 archive (the exact archived state associated with this paper): <https://doi.org/10.5281/zenodo.22466698>
- All versions: <https://doi.org/10.5281/zenodo.22466697>

No arXiv identifier is asserted.

## License

Software in this repository is released under the MIT License; see `LICENSE`. The manuscript and its textual content are © 2026 Radhe Dhoundiyal unless otherwise stated and are not granted that software license.

## A10 reference

The analytic tail bound uses the positive-real Stirling-series remainder theorem in the [NIST Digital Library of Mathematical Functions, equation 5.11.1 and section 5.11(ii)](https://dlmf.nist.gov/5.11).
