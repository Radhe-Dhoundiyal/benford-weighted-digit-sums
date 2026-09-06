"""Fail-closed publication/reproducibility preflight for v1.0.0."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path

from pypdf import PdfReader

from generate_checksums import intended_files

ROOT = Path(__file__).resolve().parents[1]
TITLE = "Benford-Weighted Digit Sums and Second-Order Asymptotics for Exponential Sequences"
AUTHOR = "Radhe Dhoundiyal"
VERSION = "1.0.0"
RELEASE_DATE = "2026-09-05"
LICENSE_ID = "MIT"
REPOSITORY_URL = "https://github.com/Radhe-Dhoundiyal/benford-weighted-digit-sums"
VERSION_DOI = "10.5281/zenodo.22466698"
CONCEPT_DOI = "10.5281/zenodo.22466697"
FROZEN_MANUSCRIPT_SHA256 = "2666a5b38b9880628c301d003b0fcd9fb7a9c4c433bc154ef12701ec77981c60"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def cff_scalar(text: str, key: str) -> str:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*[\"']?([^\n\"']+)", text)
    require(match is not None, f"missing CITATION.cff field: {key}")
    return match.group(1).strip()


def verify_metadata() -> None:
    cff = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    code = json.loads((ROOT / "codemeta.json").read_text(encoding="utf-8"))
    require(cff_scalar(cff, "title") == TITLE, "CFF title mismatch")
    require(cff_scalar(cff, "version") == VERSION, "CFF version mismatch")
    require(cff_scalar(cff, "date-released") == RELEASE_DATE, "CFF date mismatch")
    require(cff_scalar(cff, "license") == LICENSE_ID, "CFF license mismatch")
    require("family-names: Dhoundiyal" in cff and "given-names: Radhe" in cff, "CFF author mismatch")
    require(code["name"] == TITLE, "CodeMeta title mismatch")
    require(code["version"] == VERSION, "CodeMeta version mismatch")
    require(code["datePublished"] == RELEASE_DATE, "CodeMeta date mismatch")
    require(code["author"]["givenName"] + " " + code["author"]["familyName"] == AUTHOR, "CodeMeta author mismatch")
    require(code["author"]["affiliation"]["name"] == "Independent Researcher", "CodeMeta affiliation mismatch")
    require(code["license"].endswith("/MIT.html"), "CodeMeta license mismatch")
    require(code.get("codeRepository") == REPOSITORY_URL, "CodeMeta repository URL mismatch")
    require(cff_scalar(cff, "repository-code") == REPOSITORY_URL, "CFF repository URL mismatch")
    require(code.get("identifier") == f"https://doi.org/{VERSION_DOI}", "CodeMeta version DOI mismatch")
    require(code.get("isPartOf", {}).get("identifier") == f"https://doi.org/{CONCEPT_DOI}", "CodeMeta concept DOI mismatch")
    require("arxiv" not in json.dumps(code).lower(), "unverified arXiv identifier in CodeMeta")
    require(cff_scalar(cff, "doi") == VERSION_DOI, "CFF version DOI mismatch")
    require(f"value: {CONCEPT_DOI}" in cff, "CFF concept DOI mismatch")
    require("arxiv" not in cff.lower(), "unverified arXiv identifier in CFF")


def verify_manuscript() -> None:
    paper = ROOT / "manuscript" / "paper.pdf"
    tex = ROOT / "manuscript" / "paper.tex"
    bib = ROOT / "manuscript" / "references4.bib"
    require(tex.is_file() and bib.is_file(), "frozen manuscript sources missing")
    require("\\bibliography{references4}" in tex.read_text(encoding="utf-8"), "bibliography source declaration mismatch")
    require(hashlib.sha256(paper.read_bytes()).hexdigest() == FROZEN_MANUSCRIPT_SHA256, "frozen manuscript hash mismatch")
    reader = PdfReader(paper)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    compact = " ".join(text.split())
    require(TITLE in compact, "manuscript title mismatch")
    require(AUTHOR in compact and "Independent Researcher" in compact, "manuscript author/status mismatch")
    require("September 5, 2026" in compact, "manuscript date mismatch")
    require("|εb,L|≤" in compact.replace(" ", "") or "|εb,L|≤" in text.replace(" ", ""), "A10 non-strict bound not found")
    require("??" not in text, "manuscript contains extracted ?? marker")


def verify_claims_and_outputs() -> None:
    spec = (ROOT / "THEOREM_SPEC.md").read_text(encoding="utf-8")
    report = (ROOT / "outputs/reports/FINAL_VERIFICATION_REPORT.md").read_text(encoding="utf-8")
    require(report.startswith("OVERALL VERDICT:\nPASS\n"), "final report verdict is not PASS")
    require("| A10 |" in spec and "| PASS |" in spec, "theorem specification is incomplete")
    with (ROOT / "outputs/reports/CLAIM_STATUS.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    require(len(rows) == 16, "claim status count is not 16")
    require({row["claim"] for row in rows} == {*(f"A{i}" for i in range(1, 11)), *(f"D{i}" for i in range(1, 7))}, "claim identifiers mismatch")
    require(all(row["status"] == "PASS" for row in rows), "not all claims are PASS")
    required = [
        "bias_constants.csv", "bias_convergence.csv", "expectation_residuals.csv",
        "digit_asymptotic_scaled_residuals.csv", "tail_bound_ratios.csv",
        "digit_extraction_mismatches.csv", "deterministic_residuals_and_bounds.csv",
        "discrepancy_values.csv",
    ]
    require(all((ROOT / "outputs/tables" / name).is_file() for name in required), "required table missing")
    require((ROOT / "outputs/reports/NUMERICAL_RESIDUALS.csv").stat().st_size > 0, "residual index empty")


def verify_checksums() -> None:
    manifest = ROOT / "checksums.sha256"
    entries: dict[str, str] = {}
    for line in manifest.read_text(encoding="ascii").splitlines():
        digest, rel = line.split("  ", 1)
        require(rel not in entries, f"duplicate checksum entry: {rel}")
        entries[rel] = digest
    expected = {path.relative_to(ROOT).as_posix() for path in intended_files()}
    require(set(entries) == expected, "checksum manifest coverage mismatch")
    for rel, expected_digest in entries.items():
        actual = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
        require(actual == expected_digest, f"checksum mismatch: {rel}")


def verify_clean_content() -> None:
    for path in intended_files():
        require("source-material" not in path.parts, "local source material entered public manifest")
        require("__pycache__" not in path.parts and path.suffix != ".pyc", "cache entered public manifest")
        if path.suffix.lower() in {".md", ".py", ".toml", ".json", ".cff", ".txt"} or path.name in {"LICENSE", ".gitignore", ".gitattributes"}:
            text = path.read_text(encoding="utf-8")
            require(not re.search(r"[A-Za-z]:\\(?:Users|Projects)\\", text), f"absolute Windows path in {path.relative_to(ROOT)}")
            user_root = "/" + "Users" + "/"
            home_root = "/" + "home" + "/"
            require(user_root not in text and home_root not in text, f"absolute POSIX path in {path.relative_to(ROOT)}")


def main() -> int:
    checks = (verify_metadata, verify_manuscript, verify_claims_and_outputs, verify_checksums, verify_clean_content)
    for check in checks:
        check()
        print(f"PASS {check.__name__}")
    print("PUBLICATION PREFLIGHT: PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"PUBLICATION PREFLIGHT: FAIL: {exc}", file=sys.stderr)
        raise
