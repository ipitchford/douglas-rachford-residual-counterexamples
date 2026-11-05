"""Independent rational reconstruction of Appendix A's t=1/100 instance.

Unlike the author certificate, this starts from B and a generic inverse, finds
the hinge height by propagating two affine coefficient vectors, and evaluates
all updates using the proximal definition. Standard library only; no asserts.
"""

from fractions import Fraction as F
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def mv(matrix, vector):
    return [sum(a * b for a, b in zip(row, vector)) for row in matrix]


def inverse(matrix):
    a, b = matrix[0]
    c, d = matrix[1]
    determinant = a * d - b * c
    require(determinant != 0, "Singular resolvent matrix")
    return [[d / determinant, -b / determinant],
            [-c / determinant, a / determinant]]


def main():
    t = F(1, 100)
    initial = [F(1), t / 2]
    identity = [[F(1), F(0)], [F(0), F(1)]]
    b = [[t * t / (1 + t * t), -t / (1 + t * t)],
         [t / (1 + t * t), t * t / (1 + t * t)]]
    for i in range(2):
        for j in range(2):
            gram = sum(b[k][i] * b[k][j] for k in range(2))
            require(gram == (b[i][j] + b[j][i]) / 2,
                    "Cocoercivity matrix identity failed")
    q = inverse([[identity[i][j] + b[i][j] / 2
                  for j in range(2)] for i in range(2)])

    # Candidate w^9 = constant - delta * coefficient. Propagating vectors
    # avoids assuming the closed matrix power/geometric-sum expression.
    constant, coefficient = initial[:], [F(0), F(0)]
    for _ in range(8):
        constant = mv(q, constant)
        coefficient = mv(q, coefficient)
        coefficient[0] += 1
    reflected_constant = [2 * x - y for x, y in zip(mv(q, constant), constant)]
    reflected_coefficient = [2 * x - y for x, y in
                             zip(mv(q, coefficient), coefficient)]
    delta = reflected_constant[0] / (reflected_coefficient[0] + 1)
    require(delta > 0, "Hinge coefficient must be positive")

    w = initial[:]
    branches = []
    for step in range(1, 10):
        x = mv(q, w)
        v = [2 * x[i] - w[i] for i in range(2)]
        if v[0] < 0:
            y = v[:]
        elif v[0] <= delta:
            y = [F(0), v[1]]
        else:
            y = [v[0] - delta, v[1]]
        if step <= 8:
            require(y[0] > 0, f"Active branch failed at step {step}")
            branches.append("positive")
        else:
            require(v[0] == delta and y[0] == 0, "Terminal boundary failed")
            branches.append("boundary")
        difference = [y[i] - x[i] for i in range(2)]
        w = [w[i] + difference[i] for i in range(2)]

    norm_initial = sum(x * x for x in initial)
    normalised = sum(x * x for x in difference) / norm_initial
    gap = normalised - F(1, 81)
    require(gap > 0, "Strict conjecture violation failed")
    author_record = json.loads(Path(__file__).with_name(
        "optimisation_hinge_n9_exact.json").read_text())
    require(F(author_record["normalised_residual2"]) == normalised,
            "Independent residual does not match author record")
    require(F(author_record["hinge_coefficient"]) == 2 * delta,
            "Independent hinge height does not match author record")
    print(json.dumps({
        "status": "PASS",
        "parameter": str(t),
        "cocoercivity_matrix_identity": True,
        "branches": branches,
        "hinge_coefficient": str(2 * delta),
        "normalised_residual2": str(normalised),
        "normalised_residual2_decimal": float(normalised),
        "conjectured_bound": "1/81",
        "ratio_decimal": float(81 * normalised),
        "exact_gap": str(gap),
        "author_record_matches": True,
    }, indent=2))


if __name__ == "__main__":
    main()
