"""Exact nine-step unrelaxed hinge counterexample from the analytic family.

Uses t=1/100, beta=1, gamma=1/2, lambda=1. No optional dependencies.
The hinge coefficient is defined by a finite rational matrix expression.
"""

from fractions import Fraction as F
import json

def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def multiply(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def mv(a, x):
    return [sum(a[i][j]*x[j] for j in range(2)) for i in range(2)]


def main():
    t = F(1, 100)
    denominator = 4 + 9*t*t
    q = [[(4+6*t*t)/denominator, 2*t/denominator],
         [-2*t/denominator, (4+6*t*t)/denominator]]
    identity = [[F(1), F(0)], [F(0), F(1)]]
    r = [[2*q[i][j]-identity[i][j] for j in range(2)] for i in range(2)]
    power = identity
    geometric_sum = [[F(0), F(0)], [F(0), F(0)]]
    for _ in range(8):
        geometric_sum = [[geometric_sum[i][j]+power[i][j] for j in range(2)] for i in range(2)]
        power = multiply(q, power)
    initial = [F(1), t/2]
    d = multiply(r, geometric_sum)[0][0] + 1
    delta = mv(multiply(r, power), initial)[0] / d
    require(delta > 0, 'Scientific guard: delta > 0')

    w = initial
    active_first_coordinates = []
    for k in range(1, 10):
        x = mv(q, w)
        reflected = mv(r, w)
        y = [max(F(0), reflected[0]-delta) if reflected[0] > 0 else reflected[0], reflected[1]]
        if k < 9:
            require(y[0] > 0, 'Scientific guard: y[0] > 0')
        else:
            require(reflected[0] == delta, 'Scientific guard: reflected[0] == delta')
            require(y[0] == 0, 'Scientific guard: y[0] == 0')
        active_first_coordinates.append(y[0])
        next_w = [w[i]+y[i]-x[i] for i in range(2)]
        residual2 = sum((next_w[i]-w[i])**2 for i in range(2))
        w = next_w
    initial_norm2 = sum(x*x for x in initial)
    normalised = residual2/initial_norm2
    bound = F(1, 81)
    require(normalised > bound, 'Scientific guard: normalised > bound')
    print(json.dumps({
        "t": str(t),
        "hinge_coefficient": str(2*delta),
        "initial_point": [str(x) for x in initial],
        "last_y1": str(active_first_coordinates[-1]),
        "earlier_y1_strictly_positive": all(x > 0 for x in active_first_coordinates[:-1]),
        "normalised_residual2": str(normalised),
        "normalised_residual2_decimal": float(normalised),
        "bound": str(bound),
        "ratio_decimal": float(normalised/bound),
        "exact_gap": str(normalised-bound),
    }, indent=2))


if __name__ == "__main__":
    main()
