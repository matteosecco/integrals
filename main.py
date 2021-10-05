from sympy.abc import x
from sympy import Symbol, Add, Pow, Mul
from sympy import expand, log, exp, diff, solve, symbols
from sympy import sin, cos, tan, asin, acos, atan, csc, sec, cot

import mathf


""" Main function """


def integrate(f, v=x):
    """
    Integrate the function 'f' where 'f' is any function defined in the sympy
    module.
    The function must have a single variable.
    Returns the integrated function if it finds a way to integrate
    (it may be wrong), and False if it doesn't.
    v: variable used to integrate (usually x)
    """
    print(f"Function: {f}\t\tv: {v}")
    # expands the function to make it easier to integrate
    f = expand(f)

    # list of known function integrals
    known_f = {v: v**2/2,
               v**-1: log(v),
               (1+v**2)**-1: atan(v),
               (1-v**2)**(-1/2): asin(v),
               -(1-v**2)**(-1/2): acos(v),
               log(v): x*log(v)-v,
               sin(v): -cos(v),
               cos(v): sin(v),
               tan(v): -log(cos(v)),
               exp(v): exp(v),
               csc(v)**2: -cot(v),
               sec(v)**2: tan(v),
               cot(v)**2: -cot(x)-v
               }

    """ FIRST TRY: checks if the function is a known one """
    for e in known_f.keys():
        if f == e:
            return known_f[e]

    """ SECOND TRY: use the elementary techniques of integration for basic
    integrals """
    # y = a where isint(a)
    if mathf.isint(f):
        return f * v

    # y = a where type(a) == Symbol
    elif type(f) == Symbol:
        return f * v

    # y = Sum(a, b, c, ...)
    elif type(f) == Add:
        return Add(*[integrate(e, v=v) for e in f.args])

    # y = Pow(a, b)
    elif type(f) == Pow:

        # y = x**a where isint(a)
        if type(f.args[0]) == Symbol and mathf.isint(f.args[1]):
            return Pow(f.args[0], f.args[1] + 1) / (f.args[1] + 1)

        # y = a**x where isint(a)
        elif mathf.isint(f.args[0]) and type(f.args[1]) == Symbol:
            return f / log(f.args[0])

    # y = Mul(a, b, c, ...)
    elif type(f) == Mul:
        # y = a*x where isint(a)
        if mathf.isint(f.args[0]):
            return f.args[0] * Mul(*[integrate(e, v=v) for e in f.args[1:]])

    """ THIRD TRY: known transformation within the function """
    # TODO: trigonometric identities
    tr_identities = {cos(v)**2: 0.5*(1+cos(2*v)),
                     sin(v)**2: 0.5*(1-cos(2*v)),
                     tan(v)**2: (1-cos(2*v))/(1+cos(2*v)),
                     tan(v): sin(v) / cos(v),
                     1/sin(v)**2: csc(v)**2,
                     csc(v): 1/sin(v),
                     sec(v): 1/cos(v),
                     cot(v): 1/tan(v)}

    """ FOURTH TRY: substitution for each subset of the function """
    # TODO: remove the risk of infinite recursion by expanding the function more and more
    # TODO: sort out unlikely possibilities / rank them by usefulness
    # gets the list of all possible pieces of function to substitute
    possibilities = mathf.getargs(f)

    # each 'p' is a subpart of 'f'
    for p in possibilities:
        u = symbols("u")
        p_inv = solve(p - u, v)[-1]

        # 'new_f' is a temp variable to perform integration by substitution
        new_f = f / diff(p)
        new_f = new_f.subs(x, p_inv)
        new_f = integrate(new_f, v=u)
        new_f = new_f.subs(u, p)

        # in the case in which the function is not integrated, the loop goes on
        if new_f:
            return new_f

    return False
