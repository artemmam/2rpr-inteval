import sympy as sym
from sympy.utilities.lambdify import implemented_function
import interval as ival
v1, v2, u1, u2, d = sym.symbols('v1, v2, u1, u2, d')


def derive_matrix(g):
    """
    Function for calculating partial derivative of matrix G
    :param g : array to be derived
    :return gv: derived matrix
    """
    g_v1 = sym.diff(g, v1)  # Calculate derivative of G with respect to v1
    g_v2 = sym.diff(g, v2)  # Calculate derivative of G with respect to v2
    gv = sym.Matrix([g_v1, g_v2])
    gv = gv.reshape(2, 2)
    return gv


def get_krav_func():
    """
    Function for calculating classical Kravchik evaluation in symbol format for parallel robot 2-RPR
    :return: function of  classical Kravchik evaluation in numerical format
    """
    v1mid, v2mid = sym.symbols('v1mid, v2mid')
    f = sym.Matrix([[v1**2 - u1**2 - u2**2], [v2**2 - (u1 - d)**2 - u2**2]])  # System of kinematic equations
    f_v = derive_matrix(f)  # Calculate matrix of partial derivatives of kinematic matrix
    v = sym.Matrix([[v1], [v2]])  # Vector v
    lam = f_v**(-1)
    lam = lam.subs([(v1, v1mid), (v2, v2mid)])  # Calculate lambda function for recurrent transformation
    g = v - lam * f  # Equivalent recurrent transformation
    g_v = derive_matrix(g)  # Calculate matrix of partial derivatives of matrix g
    c1, c2 = sym.symbols('c1, c2')
    c = sym.Matrix([[c1], [c2]]) # Vector of v-middles
    v_c = v - c
    g_eval = g.subs([(v1, c1), (v2, c2)]) + g_v * v_c  # Calculates classical Kravchik evaluation
    print(g_eval)
    return sym.lambdify([u1, u2, v1, v2, v1mid, v2mid, c1, c2, d], g_eval)


def zzf(x, m):
    """
    It was noticed, that after recursion transformation, both functions with v1 and v2 don't have single inclusion,
    so function zzf is used to calculate exact interval enclosure for grouped v1 and v2 which form same functions for which
    we easily can calculate roots analytically
    :param x: interval v (v1 or v2)
    :param m: the mid of v
    :return: Exact interval enclosure for function zf
    """
    zf = lambda x, m : x * (1 - x / (2 * m))
    if m <= x[0]:
        iv = ival.Interval([zf(x[1],m), zf(x[0],m)])
    elif m >= x[1]:
        iv = ival.Interval([zf(x[0],m), zf(x[1],m)])
    else:
        iv = ival.Interval([min(zf(x[0],m), zf(x[1],m)), zf(m,m)])
    return iv


def get_rec_func_optim():
    """
    Symbolic recursion function, which was calculated analytically
    :return: function of interval recursion evaluation in numerical format
    """
    v1mid, v2mid = sym.symbols('v1mid, v2mid')
    hump = implemented_function(sym.Function('hump'), lambda x, m: zzf(x,m))
    f = sym.Matrix([[hump(v1, v1mid) - (-u1**2 - u2**2)/(2*v1mid)], [hump(v2, v2mid) - (-u2**2 - (u1 - d)**2)/(2*v2mid)]])  # System of kinematic equations
    print("g = ", f)
    return sym.lambdify([u1, u2, v1, v2, v1mid, v2mid, d], f)