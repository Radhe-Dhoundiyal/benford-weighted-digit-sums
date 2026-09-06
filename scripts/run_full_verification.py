"""Run the complete deterministic v1.0.0 verification workflow."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if Path.cwd().resolve() != ROOT:
    raise SystemExit("run this command from the repository root")

steps = (
    "scripts/run_all_tests.py",
    "scripts/build_manuscript.py",
    "scripts/run_all_experiments.py",
    "scripts/build_figures.py",
    "scripts/build_verification_report.py",
    "scripts/generate_checksums.py",
    "scripts/verify_repository.py",
)
for script in steps:
    print(f"\n=== {script} ===", flush=True)
    subprocess.run([sys.executable, script], cwd=ROOT, check=True)
print("\nFULL VERIFICATION: PASS")
