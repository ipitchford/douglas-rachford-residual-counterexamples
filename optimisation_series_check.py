"""Symbolically verify the hinge-family local coefficient.

Optional dependency: SymPy. This checks an algebraic expansion, not the
global mixed-class minimax conjecture. Run with `python optimisation_series_check.py`.
"""

import sympy as sp

def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def product(a, b):
    return [sum((a[j] * b[k-j] for j in range(k + 1)), sp.zeros(2)) for k in range(3)]


def main():
    m, lam, s = sp.symbols("m lambda s", positive=True)
    identity = sp.eye(2)
    rotation = sp.Matrix([[0, -1], [1, 0]])
    zero = sp.zeros(2)
    e1 = sp.Matrix([1, 0])
    u = lam * s
    b = lam * s * (1 + s)

    q_power = [identity, -m*u*rotation, -(m*b + m*(m-1)*u*u/2)*identity]
    reflected = [identity, -2*s*rotation, -2*s*(1+s)*identity]
    geometric_sum = [
        m*identity,
        -u*m*(m-1)/2*rotation,
        -(b*m*(m-1)/2 + u*u*m*(m-1)*(m-2)/6)*identity,
    ]
    rs = product(reflected, geometric_sum)
    d = [rs[0][0, 0] + 1/lam, rs[1][0, 0], rs[2][0, 0]]
    require(d[1] == 0, 'Scientific guard: d[1] == 0')
    inv_d = [1/d[0], 0, -d[2]/d[0]**2]
    rq = product(reflected, q_power)
    outer = [e1 * mat[0, :] for mat in rq]
    fraction = [sum((inv_d[j] * outer[k-j] for j in range(k+1)), zero) for k in range(3)]
    h = [zero, u*rotation, b*identity]
    middle = [h[k] + fraction[k] for k in range(3)]
    k_matrix = product(q_power, middle)
    gram = product([mat.T for mat in k_matrix], k_matrix)

    # Perturbation coefficient for the simple leading eigenvalue of K^T K.
    eig0 = gram[0][0, 0]
    coefficient = sp.factor(gram[2][0, 0] + gram[1][0, 1]**2/eig0)
    n = m + 1
    z = 1 + lam*m
    target = lam**2*s/(3*z**3) * (lam**2*n*(n-1)*(lam*s*(n+1)-3*(s+1))-6)
    require(sp.factor(coefficient-target) == 0, 'Scientific guard: sp.factor(coefficient-target) == 0')
    require(sp.factor(eig0-lam**2/z**2) == 0, 'Scientific guard: sp.factor(eig0-lam**2/z**2) == 0')
    print("Exact symbolic identities verified.")
    print("Coefficient of a:", sp.factor(coefficient))
    print("At lambda=1, s=1/2, N=9:", sp.factor(coefficient.subs({lam:1, s:sp.Rational(1,2), m:8})))
    print("At lambda=1, s=1/2, N=10:", sp.factor(coefficient.subs({lam:1, s:sp.Rational(1,2), m:9})))


if __name__ == "__main__":
    main()
