from sympy import Symbol, Add, Pow, Mul
from sympy import symbols, expand, log, exp, diff
from sympy import sin, cos, tan, asin, acos, atan, csc, sec, cot


""" Useful math functions """


def isint(i):
    """ Checks if 'i' is an int because sympy has its own Integer implementation """
    try:
        int(i)
        return True
    except TypeError:
        return False
    return


def islinear(f):
    """ Checks if the function is in the form y=mx+q """
    if type(f) == Symbol or isint(f):
        return True
    elif type(f) == Mul:
        for e in f.args:
            if not islinear(e):
                return False
        return True
    else:
        return False


""" Main function """


def integrate(f):
    """
    Integrate the function 'f' where 'f' is any function defined in the sympy
    module.
    The function must have a single variable called 'x'.
    Returns the integrated function if it finds a way to integrate
    (it may be wrong), and False if it doesn't.
    """

    # defines the variable to be used on the known functions
    x = symbols("x")

    # expands the function to make it easier to integrate
    f = expand(f)

    # list of known function integrals
    known_f = {x: x**2/2,
               x**-1: log(x),
               (1+x**2)**-1: atan(x),
               (1-x**2)**(-1/2): asin(x),
               -(1-x**2)**(-1/2): acos(x),
               log(x): x*log(x)-x,
               sin(x): -cos(x),
               cos(x): sin(x),
               tan(x): -log(cos(x)),
               exp(x): exp(x),
               csc(x)**2: -cot(x),
               sec(x)**2: tan(x),
               cot(x)**2: -cot(x)-x
               }

    """ FIRST TRY: checks if the function is a known one """
    for e in known_f.keys():
        if f == e:
            return known_f[e]

    """ SECOND TRY: use the elementary techniques of integration for basic
    integrals """
    # y = a
    if isint(f):
        return f * x

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

        # y = a**f(x) where f is linear
        elif isint(f.args[0]) and islinear(f.args[1]):
            # integration by substitution
            u = f.args[1]
            i = integrate(f.args[0]**x / diff(u))
            return i.subs(x, u)

    # y = Mul(a, b, c, ...)
    elif type(f) == Mul:
        # y = a*x
        if isint(f.args[0]):
            print("\tq")
            return f.args[0] * Mul(*[integrate(e) for e in f.args[1:]])

    # y = exp(a) where 'a' is linear
    elif type(f) == exp and islinear(f.args[0]):
        u = f.args[0]
        i = integrate(exp(x) / diff(u))
        return i.subs(x, u)

    # y = sin(x)
    elif type(f) == sin:
        u = f.args[0]
        i = integrate(sin(x) / diff(u))
        return i.subs(x, u)

    # y = cos(x)
    elif type(f) == cos:
        u = f.args[0]
        i = integrate(cos(x) / diff(u))
        return i.subs(x, u)

    # y = tan(x)
    elif type(f) == tan:
        u = f.args[0]
        i = integrate(tan(x) / diff(u))
        return i.subs(x, u)

    """ THIRD TRY: known transformation within the funtction """
    # TODO: trigonometric identities
    tr_identities = {cos(x)**2: 0.5*(1+cos(2*x)),
                     sin(x)**2: 0.5*(1-cos(2*x)),
                     tan(x)**2: (1-cos(2*x))/(1+cos(2*x)),
                     tan(x): sin(x) / cos(x),
                     1/sin(x)**2: csc(x)**2,
                     csc(x): 1/sin(x),
                     sec(x): 1/cos(x),
                     cot(x): 1/tan(x)}

    # checks whether the function contains a known identity and substitutes it
    # it may create more than one route, the first working one is taken
    possibilities = []
    for i in tr_identities.keys():
        # TODO VA IN RECURSION PERCHE NON SA RISOLVERE csc(x) E COMUNQUE NON RITORNA LA FUNZIONE CONTESTUALIZZATA
        if i in f.args or i == f:
            possibilities.append(tr_identities[i])

    solved_pos = list(map(integrate, possibilities))
    for e in solved_pos:
        if e:
            return e

    return False
