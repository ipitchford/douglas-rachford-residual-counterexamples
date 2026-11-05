"""Exact rational certificates for DRS counterexamples.

Standard-library only. All mathematical comparisons use fractions.Fraction.
Decimal output is supplied only to help readers inspect the result.
"""

from fractions import Fraction as F
import json

def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def matvec(matrix, vector):
    return [sum(row[j] * vector[j] for j in range(len(vector))) for row in matrix]


def norm2(vector):
    return sum(v * v for v in vector)


def show(value):
    return {"exact": str(value), "decimal": float(value)}


def hinge_case(q, w02, c, horizon, gamma, relaxation):
    """B=(I+qJ)/(1+q²), g=c max(x1,0), initial point (1,w02)."""
    a = F(1, 1 + q * q)
    b = q * a
    det = (1 + gamma * a) ** 2 + (gamma * b) ** 2
    resolvent = [
        [(1 + gamma * a) / det, gamma * b / det],
        [-gamma * b / det, (1 + gamma * a) / det],
    ]
    w = [F(1), w02]
    initial_norm2 = norm2(w)
    steps = []
    for k in range(1, horizon + 1):
        x = matvec(resolvent, w)
        z = [2 * x[j] - w[j] for j in range(2)]
        # Exact proximal map of gamma*c*max(x1,0).
        y = [max(F(0), z[0] - gamma * c) if z[0] > 0 else z[0], z[1]]
        w_next = [w[j] + relaxation * (y[j] - x[j]) for j in range(2)]
        residual2 = norm2([w_next[j] - w[j] for j in range(2)])
        steps.append({"k": k, "z1": show(z[0]), "y1": show(y[0])})
        w = w_next
    normalised_residual2 = residual2 / initial_norm2
    normalised_bound = relaxation ** 2 / (1 + (horizon - 1) * relaxation) ** 2
    require(normalised_residual2 > normalised_bound, 'Scientific guard: normalised_residual2 > normalised_bound')
    return {
        "q": q,
        "horizon": horizon,
        "gamma": str(gamma),
        "relaxation": str(relaxation),
        "hinge_coefficient": str(c),
        "initial_point": ["1", str(w02)],
        "normalised_residual2": show(normalised_residual2),
        "normalised_bound": show(normalised_bound),
        "exact_gap": show(normalised_residual2 - normalised_bound),
        "ratio": show(normalised_residual2 / normalised_bound),
        "steps": steps,
    }


def main():
    # Rotation-only example, beta=1, gamma=1/2, lambda=1, B=(I+7J)/50.
    n = 20
    rotation_residual = F(1, 200) * F(40, 41) ** n
    rotation_bound = F(1, n * n)
    require(rotation_residual > rotation_bound, 'Scientific guard: rotation_residual > rotation_bound')

    # Scalar example: B=0, A=10I, gamma=1/2, lambda=9/5, T=-I/2.
    scalar_residual = F(9, 16)
    scalar_bound = F(81, 196)
    require(scalar_residual / scalar_bound == F(49, 36), 'Scientific guard: scalar_residual / scalar_bound == F(49, 36)')

    report = {
        "rotation_N20": {
            "residual2": show(rotation_residual),
            "bound": show(rotation_bound),
            "ratio": show(rotation_residual / rotation_bound),
        },
        "scalar_N2": {
            "residual2": show(scalar_residual),
            "bound": show(scalar_bound),
            "ratio": show(scalar_residual / scalar_bound),
        },
        "hinge_N10_lambda1": hinge_case(8, F(2, 25), F(10, 59), 10, F(1, 2), F(1)),
        "hinge_N3_lambda19over10": hinge_case(7, F(3, 20), F(7, 36), 3, F(9, 10), F(19, 10)),
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
