#!/usr/bin/env python3
"""Replay exact certificate implementations and compare all stored evidence.

No external packages or network needed. Scientific guards remain enabled under -O.
The JSON log is a reproduction record, not a universal proof certificate.
"""
from pathlib import Path
from datetime import datetime, timezone
from fractions import Fraction
import json
import platform
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent

def run(script, baseline):
    started = time.perf_counter()
    proc = subprocess.run([sys.executable, "-B", *(["-O"] if sys.flags.optimize else []), str(ROOT / script)], cwd=ROOT,
                          check=True, text=True, capture_output=True)
    actual = json.loads(proc.stdout)
    expected = json.loads((ROOT / baseline).read_text())
    if actual != expected:
        raise AssertionError(f"{script} differs from recorded {baseline}")
    return actual, {"script": script, "baseline": baseline,
                    "all_recorded_fields_match": True,
                    "elapsed_seconds": round(time.perf_counter() - started, 6),
                    "stderr": proc.stderr}

primary, p_record = run("optimisation_exact_checks.py", "optimisation_exact_checks.json")
independent, i_record = run("independent_exact_verifier.py", "independent_exact_report.json")
ninth, n_record = run("optimisation_hinge_n9_exact.py", "optimisation_hinge_n9_exact.json")
reviewer_ninth, r_record = run("reviewer_hinge_check.py", "reviewer_hinge_check.json")
if not (Fraction(ninth["normalised_residual2"]) > Fraction(1, 81)
        and ninth["last_y1"] == "0" and ninth["earlier_y1_strictly_positive"]):
    raise AssertionError("Ninth-evaluation branch or residual certificate failed")

comparisons = [
    (primary["rotation_N20"]["residual2"]["exact"],
     independent["simple_counterexample"]["residual_squared_at_N20_exact"]),
    (primary["scalar_N2"]["residual2"]["exact"],
     independent["scalar_counterexample"]["residual_squared"]),
    (primary["hinge_N10_lambda1"]["normalised_residual2"]["exact"],
     independent["hinge_counterexample_N10"]["normalized_residual_squared_exact"]),
    (primary["hinge_N3_lambda19over10"]["normalised_residual2"]["exact"],
     independent["hinge_counterexample_N3"]["normalized_residual_squared_exact"]),
    (ninth["normalised_residual2"], reviewer_ninth["normalised_residual2"]),
]
for left, right in comparisons:
    if Fraction(left) != Fraction(right):
        raise AssertionError(f"Exact implementation disagreement: {left} vs {right}")
if independent["minimax_penalty"]["rational_schedule_checks"] != 360:
    raise AssertionError("Unexpected finite schedule coverage")

record = {
    "time_utc": datetime.now(timezone.utc).isoformat(),
    "python": sys.version,
    "platform": platform.platform(),
    "assertions_enabled": __debug__,
    "scientific_guards": "explicit exceptions; optimization-safe",
    "runs": [p_record, i_record, n_record, r_record],
    "additional_ninth_evaluation_certificate": True,
    "exact_counterexample_cross_comparisons": len(comparisons),
    "finite_schedule_identity_combinations": 360,
    "result": "PASS",
    "scope": "finite rational certificates and finite identity checks; not formal universal proof",
}
log_dir = ROOT / "logs"
log_dir.mkdir(exist_ok=True)
output = log_dir / ("replay_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f") + ".json")
output.write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record, indent=2))

