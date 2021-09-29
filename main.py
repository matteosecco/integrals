from sympy import integrate as intg
from sympy.abc import x, y
from sympy import Symbol, Add, Pow, Mul
from sympy import expand, log, exp, diff, solve, symbols
from sympy import sin, cos, tan, asin, acos, atan, csc, sec, cot


""" Useful math functions """


def isint(n):
    """ Checks if 'i' is an int because sympy has its own Integer implementation """
    try:
        int(n)
        return True
    except TypeError:
        return False
    return


def islinear(f):
    """ Checks if the function is in the form y=mx+q """
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
    l = [e for e in f.args]
    for e in f.args:
        l.extend(getargs(e))

    l = list(set(l))
    for e in l:
        if type(e) == Symbol or type(e) == bool or isint(e):
            l.remove(e)
    return l


def subst(f, p, v=x):
    """ Function integration by substitution using 'p' which is a subpart of 'f' """
    # f: function
    # p: piece to substitute with dummy variable
    # v: default variable
    u = symbols("u")
    p_inv = solve(p - u, v)[-1]

    new_f = f / diff(p)
    new_f = new_f.subs(x, p_inv)
    new_f = integrate(new_f, v=u)
    new_f = new_f.subs(u, p)

    return new_f


""" Main function """


def integrate(f, v=x):
    """
    Integrate the function 'f' where 'f' is any function defined in the sympy
    module.
    The function must have a single variable called 'x'.
    Returns the integrated function if it finds a way to integrate
    (it may be wrong), and False if it doesn't.
    v: variable used to integrate (usually x)
    """

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
    # y = a
    if isint(f):
        return f * v

    # there is only a symbol, which is not the one to integrate
    # which has not be found in known_f
    elif type(f) == Symbol:
        return f * v

    # y = Sum(a, b, c, ...)
    elif type(f) == Add:
        return Add(*[integrate(e) for e in f.args])

    # y = Pow(a, b)
    elif type(f) == Pow:

        # y = x**a
        if type(f.args[0]) == Symbol and isint(f.args[1]):
            return Pow(f.args[0], f.args[1] + 1) / (f.args[1] + 1)

        # y = a**x
        elif isint(f.args[0]) and type(f.args[1]) == Symbol:
            return f / log(f.args[0])

        # y = a**f(x) where f is linear  # TODO: to remove after substitution implementation
        elif isint(f.args[0]) and islinear(f.args[1]):
            # integration by substitution
            u = f.args[1]
            i = integrate(f.args[0]**v / diff(u))
            return i.subs(v, u)

    # y = Mul(a, b, c, ...)
    elif type(f) == Mul:
        # y = a*x
        if isint(f.args[0]):
            return f.args[0] * Mul(*[integrate(e) for e in f.args[1:]])

    # y = exp(a) where 'a' is linear # TODO: to remove after substitution implementation
    elif type(f) == exp and islinear(f.args[0]):
        u = f.args[0]
        i = integrate(exp(v) / diff(u))
        return i.subs(v, u)

    # y = sin(x) # TODO: to remove after substitution implementation
    elif type(f) == sin:
        u = f.args[0]
        i = integrate(sin(v) / diff(u))
        return i.subs(v, u)

    # y = cos(x) # TODO: to remove after substitution implementation
    elif type(f) == cos:
        u = f.args[0]
        i = integrate(cos(v) / diff(u))
        return i.subs(v, u)

    # y = tan(x) # TODO: to remove after substitution implementation
    elif type(f) == tan:
        u = f.args[0]
        i = integrate(tan(v) / diff(u))
        return i.subs(v, u)

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

    """ FOURTH TRY: substitution for each subset of the function """  # TODO

    # gets the list of all possible pieces of function to substitute
    possibilities = getargs(f)

    return False
