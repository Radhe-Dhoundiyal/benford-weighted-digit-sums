"""Compile the frozen manuscript and compare it with the authoritative PDF."""
from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "manuscript" / "paper.tex"
BIB = ROOT / "manuscript" / "references4.bib"
AUTHORITATIVE = ROOT / "manuscript" / "paper.pdf"
BUILD = ROOT / "build" / "manuscript"


def executable(name: str) -> str:
    value = shutil.which(name)
    if value is not None:
        return value
    if os.name == "nt":
        local_app_data = os.environ.get("LOCALAPPDATA")
        if local_app_data:
            candidate = (
                Path(local_app_data)
                / "Programs" / "MiKTeX" / "miktex" / "bin" / "x64"
                / f"{name}.exe"
            )
            if candidate.is_file():
                return str(candidate)
    raise RuntimeError(f"required executable not found: {name}")


def run(command: list[str], cwd: Path, env: dict[str, str] | None = None) -> None:
    print("RUN", " ".join(command), flush=True)
    subprocess.run(command, cwd=cwd, env=env, check=True)


def pdf_text(path: Path) -> tuple[int, str, dict[str, object]]:
    reader = PdfReader(path)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return len(reader.pages), text, dict(reader.metadata or {})


def main() -> int:
    if Path.cwd().resolve() != ROOT:
        raise RuntimeError("run this command from the repository root")
    if not SOURCE.is_file() or not BIB.is_file() or not AUTHORITATIVE.is_file():
        raise RuntimeError("paper.tex, references4.bib, or authoritative paper.pdf is missing")
    source_text = SOURCE.read_text(encoding="utf-8")
    if "\\bibliography{references4}" not in source_text:
        raise RuntimeError("paper.tex does not select references4.bib")

    pdflatex = executable("pdflatex")
    bibtex = executable("bibtex")
    BUILD.mkdir(parents=True, exist_ok=True)
    latex = [
        pdflatex, "-interaction=nonstopmode", "-halt-on-error",
        "-file-line-error", f"-output-directory={BUILD}", str(SOURCE),
    ]
    run(latex, ROOT)
    env = os.environ.copy()
    env["BIBINPUTS"] = str(BIB.parent) + os.pathsep + env.get("BIBINPUTS", "")
    run([bibtex, "paper"], BUILD, env)
    run(latex, ROOT)
    run(latex, ROOT)

    log = (BUILD / "paper.log").read_text(encoding="utf-8", errors="replace")
    forbidden = (
        r"Citation `[^']+' .* undefined",
        r"Reference `[^']+' .* undefined",
        r"There were undefined references",
        r"!  ==> Fatal error",
        r"Emergency stop",
    )
    for pattern in forbidden:
        if re.search(pattern, log, flags=re.IGNORECASE):
            raise RuntimeError(f"final LaTeX log failed check: {pattern}")
    if not (BUILD / "paper.bbl").is_file() or not (BUILD / "paper.bbl").read_text(encoding="utf-8", errors="replace").strip():
        raise RuntimeError("BibTeX did not produce a nonempty paper.bbl")

    compiled = BUILD / "paper.pdf"
    a_pages, a_text, a_meta = pdf_text(AUTHORITATIVE)
    b_pages, b_text, b_meta = pdf_text(compiled)
    if a_pages != b_pages or a_text != b_text or "??" in b_text:
        raise RuntimeError("compiled PDF document content differs from authoritative PDF")
    a_hash = hashlib.sha256(AUTHORITATIVE.read_bytes()).hexdigest()
    b_hash = hashlib.sha256(compiled.read_bytes()).hexdigest()
    print(f"MANUSCRIPT COMPILE: PASS ({b_pages} pages)")
    print(f"BIBLIOGRAPHY: PASS ({(BUILD / 'paper.bbl').stat().st_size} bytes)")
    print("UNDEFINED CITATIONS/REFERENCES: 0")
    print(f"PDF BYTEWISE EQUAL: {a_hash == b_hash}")
    print(f"AUTHORITATIVE SHA256: {a_hash}")
    print(f"COMPILED SHA256: {b_hash}")
    print(f"EXTRACTED TEXT EQUAL: {a_text == b_text}")
    if a_hash != b_hash:
        print("PDF METADATA DIFFERENCE:", a_meta.get("/CreationDate"), "!=", b_meta.get("/CreationDate"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"MANUSCRIPT COMPILE: FAIL: {exc}", file=sys.stderr)
        raise
