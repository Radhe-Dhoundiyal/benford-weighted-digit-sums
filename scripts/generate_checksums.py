"""Generate the deterministic SHA-256 manifest for the public archive."""
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROOT_FILES = {
    ".gitattributes", ".gitignore", "CHANGELOG.md", "CITATION.cff",
    "LICENSE", "README.md", "THEOREM_SPEC.md", "codemeta.json",
    "pyproject.toml", "requirements.txt",
}
PUBLIC_DIRS = ("manuscript", "src", "tests", "experiments", "scripts")
OUTPUT_PATTERNS = (
    "outputs/figures/*.png",
    "outputs/tables/*.csv",
    "outputs/reports/CLAIM_STATUS.csv",
    "outputs/reports/FINAL_VERIFICATION_REPORT.md",
    "outputs/reports/NUMERICAL_RESIDUALS.csv",
)


def intended_files() -> list[Path]:
    files = [ROOT / name for name in ROOT_FILES]
    for directory in PUBLIC_DIRS:
        files.extend(
            path for path in (ROOT / directory).rglob("*")
            if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
        )
    for pattern in OUTPUT_PATTERNS:
        files.extend(ROOT.glob(pattern))
    unique = {path.resolve() for path in files if path.is_file()}
    return sorted(unique, key=lambda path: path.relative_to(ROOT).as_posix())


def main() -> None:
    lines = []
    for path in intended_files():
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        rel = path.relative_to(ROOT).as_posix()
        lines.append(f"{digest}  {rel}")
    (ROOT / "checksums.sha256").write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")
    print(f"wrote checksums.sha256 ({len(lines)} files)")


if __name__ == "__main__":
    main()
