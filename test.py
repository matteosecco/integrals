from sympy import symbols, sin, cos, exp
from sympy import integrate as intg
import main

x = symbols("x")

def check(f):
    """ Checks if the integration is correct by running the
    implementation made by Sympy """
    
    if not main.integrate(f):
        return "%s --> %s" % (str(f), str(intg(f)))
    else:
        return True

set_1 = [5*x**2-8*x+5,
         x**(3/2)+2*x+3,
         x**(1/2)+1/(3*x**(1/2)),
         (x**2+4)/x**2,
         -6*x**3+9*x**2+4*x-3,
         8/x-5/x**2+6/x**3,
         12*x**(3/4)-9*x**(5/3),
         1/(x*x**(1/2)),
         (1+3*x)*x**2,
         (2*x**2-1)**2,
         x**2*x**(1/3),
         1,
         7*sin(x),
         5*cos(x),
         9*sin(3*x),
         12*cos(4*x),
         4*exp(-7*x),
         9*exp(x/4),
         -13*exp(6*x)   
         ]

solved = list(map(check, set_1))


