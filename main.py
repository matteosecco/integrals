from sympy.abc import x
import sympy as sp

import mathf


""" Main function """


def integrate(f, v=x, depth=0, ex=True):
    """
    Integrate the function 'f' where 'f' is any function defined in the sympy
    module.
    The function must have a single variable called 'x'.
    Returns the integrated function if it finds a way to integrate and 0 if it doesn't.
    v: variable used to integrate (usually x)
    depth: by-part recursion depth
    ex: decide whether to start by expanding the function or not
    """
    print("\t" * depth, end="")
    print(f"Function: {f}\t\tv: {v}")
    # expands the function to make it easier to integrate
    if ex:
        f = sp.expand(f)  # TODO: capire come fare con simplyfy and expand

    # list of known function integrals
    known_f = {v: v**2/2,
               v**-1: sp.log(v),
               (1+v**2)**-1: sp.atan(v),
               (1-v**2)**(-1/2): sp.asin(v),
               -(1-v**2)**(-1/2): sp.acos(v),
               sp.log(v): x*sp.log(v)-v,
               sp.sin(v): -sp.cos(v),
               sp.cos(v): sp.sin(v),
               sp.tan(v): -sp.log(sp.cos(v)),
               sp.exp(v): sp.exp(v),
               sp.csc(v)**2: -sp.cot(v),
               sp.sec(v)**2: sp.tan(v),
               sp.cot(v)**2: -sp.cot(x)-v
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
    elif type(f) == sp.Symbol:
        return f * v

    # y = Sum(a, b, c, ...)
    elif type(f) == sp.Add:
        return sp.Add(*[integrate(e, v=v, depth=depth, ex=ex) for e in f.args])

    # y = Pow(a, b)
    elif type(f) == sp.Pow:
        # y = x**a where isint(a)
        if type(f.args[0]) == sp.Symbol and mathf.isint(f.args[1]):
            return sp.Pow(f.args[0], f.args[1] + 1) / (f.args[1] + 1)

        # y = a**x where isint(a)
        elif mathf.isint(f.args[0]) and type(f.args[1]) == sp.Symbol:
            return f / sp.log(f.args[0])

    # y = Mul(a, b, c, ...)
    elif type(f) == sp.Mul:
        # y = a*x where isint(a)
        if mathf.isint(f.args[0]):
            return f.args[0] * integrate(sp.Mul(*f.args[1:]), v=v, depth=depth, ex=ex)

    """ THIRD TRY: known transformation within the function """
    # TODO: trigonometric identities
    tr_identities = {sp.cos(v)**2: 0.5*(1+sp.cos(2*v)),
                     sp.sin(v)**2: 0.5*(1-sp.cos(2*v)),
                     sp.tan(v)**2: (1-sp.cos(2*v))/(1+sp.cos(2*v)),
                     sp.tan(v): sp.sin(v) / sp.cos(v),
                     1/sp.sin(v)**2: sp.csc(v)**2,
                     sp.csc(v): 1/sp.sin(v),
                     sp.sec(v): 1/sp.cos(v),
                     sp.cot(v): 1/sp.tan(v)}

    """ FOURTH TRY: substitution for each subset of the function """
    # TODO: sort out unlikely possibilities / rank them by usefulness

    # keeps track of recursion depth in order to avoid infinite loop
    if depth < 1:
        # gets the list of all possible pieces of function to substitute
        possibilities = mathf.getargs(f)

        # sort the parts by the shortest one (most probable to be right)
        possibilities = sorted(possibilities, key=lambda x: len(str(x)))

        # each 'p' is a subpart of 'f'
        for p in possibilities:
            print(f"\t\ti am inverting {p}")
            u = sp.symbols("u")

            # iterates the function inverses and exclude complex numbers
            for el in sp.solve(p - u, v):
                if "I" not in str(el):
                    p_inv = el
                    break
            else:
                # case where inverse coulnd't be found
                continue

            # 'new_f' is a temp variable to perform integration by substitution
            new_f = f / sp.diff(p)
            new_f = new_f.subs(x, p_inv)
            new_f = integrate(new_f, v=u, depth=depth+1, ex=ex)
            # in the case in which the function is not integrated, the loop goes on
            if new_f:
                new_f = new_f.subs(u, p)
                return new_f
            else:
                print("\t\tfallito")

    return 0
