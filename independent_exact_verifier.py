#!/usr/bin/env python3
"""Independent, standard-library-only checks of the exact DRS certificates.

The decisions in this program use fractions.Fraction; decimal output is cosmetic.
The finite schedule checks are consistency checks of an algebraic identity, not a
replacement for its general proof or for the cited sharp PPA upper theorem.
"""

from fractions import Fraction as F
import json

def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))


def mt(a):
    return tuple(tuple(a[j][i] for j in range(2)) for i in range(2))


def add(a, b):
    return tuple(tuple(a[i][j] + b[i][j] for j in range(2)) for i in range(2))


def scale(s, a):
    return tuple(tuple(s * a[i][j] for j in range(2)) for i in range(2))


def inv(a):
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    return scale(1 / det, ((a[1][1], -a[0][1]), (-a[1][0], a[0][0])))


I = ((F(1), F(0)), (F(0), F(1)))


def check_simple_counterexample():
    b = scale(F(1, 50), ((F(1), F(-7)), (F(7), F(1))))
    require(mm(mt(b), b) == scale(F(1, 50), I), 'Scientific guard: mm(mt(b), b) == scale(F(1, 50), I)')
    require(scale(F(1, 2), add(b, mt(b))) == scale(F(1, 50), I), 'Scientific guard: scale(F(1, 2), add(b, mt(b))) == scale(F(1, 50), I)')
    j = inv(add(I, scale(F(1, 2), b)))
    require(j == scale(F(2, 205), ((F(101), F(7)), (F(-7), F(101)))), 'Scientific guard: j == scale(F(2, 205), ((F(101), F(7)), (F(-7), F(101))))')
    g = add(I, scale(F(-1), j))
    require(mm(mt(j), j) == scale(F(40, 41), I), 'Scientific guard: mm(mt(j), j) == scale(F(40, 41), I)')
    require(mm(mt(g), g) == scale(F(1, 205), I), 'Scientific guard: mm(mt(g), g) == scale(F(1, 205), I)')
    p = I
    first_failure = None
    residual20 = None
    for n in range(1, 21):
        gp = mm(g, p)
        residual = gp[0][0] ** 2 + gp[1][0] ** 2
        require(residual == F(1, 205) * F(40, 41) ** (n - 1), 'Scientific guard: residual == F(1, 205) * F(40, 41) ** (n - 1)')
        require(residual == F(1, 200) * F(40, 41) ** n, 'Scientific guard: residual == F(1, 200) * F(40, 41) ** n')
        if residual > F(1, n * n) and first_failure is None:
            first_failure = n
        if n == 20:
            residual20 = residual
        p = mm(j, p)
    require(first_failure == 18, 'Scientific guard: first_failure == 18')
    require(residual20 > F(1, 400), 'Scientific guard: residual20 > F(1, 400)')
    require(F(40, 41) ** 20 >= F(21, 41) > F(1, 2), 'Scientific guard: F(40, 41) ** 20 >= F(21, 41) > F(1, 2)')
    return {
        "first_violating_N": first_failure,
        "residual_squared_at_N20_exact": str(residual20),
        "conjectured_bound_at_N20_exact": "1/400",
        "residual_squared_at_N20_decimal": float(residual20),
    }


def check_scalar_counterexample():
    relaxation = F(9, 5)
    resolvent = F(1, 6)
    t = 1 - relaxation + relaxation * resolvent
    require(t == F(-1, 2), 'Scientific guard: t == F(-1, 2)')
    w2 = t
    residual_squared = ((t - 1) * w2) ** 2
    conjectured = relaxation ** 2 / (relaxation + 1) ** 2
    require(residual_squared == F(9, 16) > conjectured == F(81, 196), 'Scientific guard: residual_squared == F(9, 16) > conjectured == F(81, 196)')
    return {"residual_squared": str(residual_squared),
            "conjectured_bound": str(conjectured),
            "ratio": str(residual_squared / conjectured)}


def check_hinge_counterexample(rotation=8, w02=F(2, 25), coefficient=F(10, 59),
                              horizon=10, gamma=F(1, 2), relaxation=F(1)):
    denominator = 1 + rotation * rotation
    b = scale(F(1, denominator),
              ((F(1), F(-rotation)), (F(rotation), F(1))))
    require(mm(mt(b), b) == scale(F(1, denominator), I), 'Scientific guard: mm(mt(b), b) == scale(F(1, denominator), I)')
    require(scale(F(1, 2), add(b, mt(b))) == scale(F(1, denominator), I), 'Scientific guard: scale(F(1, 2), add(b, mt(b))) == scale(F(1, denominator), I)')
    j = inv(add(I, scale(gamma, b)))
    w = (F(1), w02)
    initial_norm_squared = sum(t * t for t in w)
    threshold = gamma * coefficient
    branches = []
    normalized = None
    for k in range(1, horizon + 1):
        x = tuple(sum(j[i][s] * w[s] for s in range(2)) for i in range(2))
        v = tuple(2 * x[i] - w[i] for i in range(2))
        if v[0] < 0:
            first, branch = v[0], "negative"
        elif v[0] <= threshold:
            first, branch = F(0), "flat"
        else:
            first, branch = v[0] - threshold, "positive"
        y = (first, v[1])
        difference = tuple(relaxation * (y[i] - x[i]) for i in range(2))
        residual_squared = sum(t * t for t in difference)
        normalized = residual_squared / initial_norm_squared
        branches.append(branch)
        w = tuple(w[i] + difference[i] for i in range(2))
    bound = relaxation ** 2 / (1 + (horizon - 1) * relaxation) ** 2
    require(normalized > bound, 'Scientific guard: normalized > bound')
    c = 1 + 1 / gamma
    a = relaxation / (2 * c)
    if horizon >= 1 / (4 * a * (1 - a)):
        rotation_envelope = a / (1 - a) * F((horizon - 1) ** (horizon - 1),
                                          horizon ** horizon)
    else:
        rotation_envelope = 4 * a * a * (1 - 2 * a) ** (2 * horizon - 2)
    require(normalized > rotation_envelope, 'Scientific guard: normalized > rotation_envelope')
    return {"N": horizon,
            "branches": branches,
            "normalized_residual_squared_exact": str(normalized),
            "normalized_residual_squared_decimal": float(normalized),
            "conjectured_bound_exact": str(bound),
            "rotation_envelope_exact": str(rotation_envelope)}


class Quadratic:
    """Exact a+b*s, where s^2=-d and d is a nonnegative rational."""

    def __init__(self, a, b, d):
        self.a, self.b, self.d = F(a), F(b), F(d)

    def __add__(self, other):
        require(self.d == other.d, 'Scientific guard: self.d == other.d')
        return Quadratic(self.a + other.a, self.b + other.b, self.d)

    def __neg__(self):
        return Quadratic(-self.a, -self.b, self.d)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        require(self.d == other.d, 'Scientific guard: self.d == other.d')
        return Quadratic(self.a * other.a - self.d * self.b * other.b,
                         self.a * other.b + self.b * other.a, self.d)

    def times(self, scalar):
        return Quadratic(self.a * scalar, self.b * scalar, self.d)

    def norm_squared(self):
        return self.a * self.a + self.d * self.b * self.b

    def reciprocal(self):
        norm = self.norm_squared()
        require(norm != 0, 'Scientific guard: norm != 0')
        return Quadratic(self.a / norm, -self.b / norm, self.d)


def check_schedule_identities():
    checked = 0
    pairs = [(F(1), F(1, 2)), (F(2), F(3, 5)), (F(3, 7), F(9, 4))]
    for beta, gamma in pairs:
        c = (beta + gamma) / gamma
        for m in range(1, 31):
            one = Quadratic(1, 0, m)
            g = Quadratic(F(1, 1) / (c * (m + 1)),
                          F(1, 1) / (c * (m + 1)), m)
            q = g.norm_squared()
            require(q == F(1, 1) / (c * c * (m + 1)), 'Scientific guard: q == F(1, 1) / (c * c * (m + 1))')
            require(g.a == c * q, 'Scientific guard: g.a == c * q')
            b = (g * (one - g).reciprocal()).times(1 / gamma)
            require(b.a == beta * b.norm_squared(), 'Scientific guard: b.a == beta * b.norm_squared()')
            schedules = [
                [c] * m,
                [F(0)] * m,
                [F((-1) ** k * (k + 1), k + 2) for k in range(m)],
                [c + F(13 * k - 8, 7) for k in range(m)],
            ]
            for schedule in schedules:
                state = one
                penalty = F(1)
                for step in schedule:
                    state = (one - g.times(step)) * state
                    penalty *= 1 + (step / c - 1) ** 2 / m
                exact = (g * state).norm_squared()
                baseline = F(m ** m, (m + 1) ** (m + 1)) / (c * c)
                require(exact == baseline * penalty, 'Scientific guard: exact == baseline * penalty')
                require(exact >= baseline, 'Scientific guard: exact >= baseline')
                require((exact == baseline) == all(step == c for step in schedule), 'Scientific guard: (exact == baseline) == all(step == c for step in schedule)')
                checked += 1
    return {"rational_schedule_checks": checked,
            "identity": "exact equality and lower bound passed",
            "scope": "finite consistency checks; general proof remains algebraic"}


if __name__ == "__main__":
    report = {
        "arithmetic": "Python standard library fractions.Fraction",
        "scalar_counterexample": check_scalar_counterexample(),
        "simple_counterexample": check_simple_counterexample(),
        "hinge_counterexample_N10": check_hinge_counterexample(),
        "hinge_counterexample_N3": check_hinge_counterexample(
            rotation=7, w02=F(3, 20), coefficient=F(7, 36), horizon=3,
            gamma=F(9, 10), relaxation=F(19, 10)),
        "minimax_penalty": check_schedule_identities(),
        "result": "all exact checks passed",
    }
    print(json.dumps(report, indent=2))
