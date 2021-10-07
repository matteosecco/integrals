from sympy.abc import x
import sympy as sp

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
    if type(f) == sp.Symbol or isint(f):
        return True
    elif type(f) == sp.Mul or type(f) == sp.Add:
        for e in f.args:
            if not islinear(e):
                return False
        return True
    else:
        return False


def getargs(f):
    """ Returns a list of all args of the function and of its components """
    l = [e for e in f.args if type(e) != sp.Symbol and not isint(e)]
    for e in l:
        l.extend(getargs(e))

    return list(set(l))


def subst(f, p, v=x):
    """ Function integration by substitution using 'p' which is a subpart of 'f'
    # f: function
    # p: piece to substitute with dummy variable
    # v: default variable
    """
    u = sp.symbols("u")
    for el in sp.solve(p - u, v):
        if "I" not in str(el):
            p_inv = el
            break
    else:
        return 0

    new_f = f / sp.diff(p)
    new_f = new_f.subs(x, p_inv)
    new_f = main.integrate(new_f, v=u, depth=1)

    if new_f:
        new_f = new_f.subs(u, p)
        return new_f
    return 0


def check(f):
    """ Checks if the integration is correct by running the
    implementation made by Sympy """
    a = sp.simplify(main.integrate(f))
    b = sp.simplify(sp.integrate(f, x))

    if not a == b:
        return f"{str(f)} --> {str(b)}, instead got {str(a)}"
    else:
        return True
