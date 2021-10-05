from sympy.abc import x
from sympy import Symbol, Add, Mul, solve, diff, symbols
from sympy import integrate as intg

import main


""" Useful math functions """


def isint(n):
    """ Checks if 'i' is an int because sympy has its own Integer implementation """
    try:
        int(n)
        return True
    except TypeError:
        return False


def islinear(f):
    """ Checks if the function is in the form y = mx + q """
    if type(f) == Symbol or isint(f):
        return True
    elif type(f) == Mul or type(f) == Add:
        for e in f.args:
            if not islinear(e):
                return False
        return True
    else:
        return False


def getargs(f):
    """ Returns a list of all args of the function and of its components """
    l = [e for e in f.args if type(e) != Symbol and not isint(e)]
    for e in l:
        l.extend(getargs(e))

    return list(set(l))


def subst(f, p, v=x):
    """ Function integration by substitution using 'p' which is a subpart of 'f'
    # f: function
    # p: piece to substitute with dummy variable
    # v: default variable
    """
    u = symbols("u")
    p_inv = solve(p - u, v)[-1]

    new_f = f / diff(p)
    new_f = new_f.subs(x, p_inv)
    new_f = main.integrate(new_f, v=u)
    new_f = new_f.subs(u, p)

    return new_f


def check(f):
    """ Checks if the integration is correct by running the
    implementation made by Sympy """

    if not main.integrate(f):
        return f"{str(f)} --> {str(intg(f))}, instead got {str(main.intergrate(f))}"
    else:
        return True
