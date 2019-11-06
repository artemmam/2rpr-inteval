import sympy as sym
from sympy.utilities.lambdify import implemented_function
import interval as ival
v1, v2, u1, u2, d = sym.symbols('v1, v2, u1, u2, d')


def derive_matrix(g, v):
    """
    Function for calculating partial derivative of matrix G
    :param g : array to be derived
    :return gv: derived matrix
    """
    g_v_all = []
    for i in range(g.shape[0]):
        g_v_all.append(sym.diff(g, v[i]))  # Calculate derivative of G with respect to v1
    gv = sym.Matrix()
    for i in range(len(g_v_all)):
        gv = sym.Matrix([gv, g_v_all[i]])
    gv = gv.reshape(g.shape[0], g.shape[0]).T
    return gv


def get_krav_func():
    """
    Function for calculating classical Kravchik evaluation in symbol format for parallel robot 2-RPR
    :return: function of  classical Kravchik evaluation in numerical format
    """
    v1mid, v2mid = sym.symbols('v1mid, v2mid')
    f = sym.Matrix([[v1**2 - u1**2 - u2**2], [v2**2 - (u1 - d)**2 - u2**2]])  # System of kinematic equations
    v = sym.Matrix([[v1], [v2]])# Vector v
    f_v = derive_matrix(f, v)  # Calculate matrix of partial derivatives of kinematic matrix

    lam = f_v**(-1)
    lam = lam.subs([(v1, v1mid), (v2, v2mid)])  # Calculate lambda function for recurrent transformation
    g = v - lam * f  # Equivalent recurrent transformation
    g_v = derive_matrix(g, v)  # Calculate matrix of partial derivatives of matrix g
    c1, c2 = sym.symbols('c1, c2')
    c = sym.Matrix([[c1], [c2]]) # Vector of v-middles
    v_c = v - c
    g_eval = g.subs([(v1, c1), (v2, c2)]) + g_v * v_c  # Calculates classical Kravchik evaluation
    return sym.lambdify([u1, u2, v1, v2, v1mid, v2mid, c1, c2, d], g_eval)


def zzf(x, m):
    """
    It was noticed, that after recursion transformation, both functions with v1 and v2 don't have single inclusion,
    so function zzf is used to calculate exact interval enclosure for grouped v1 and v2 which form same functions for which
    we can easily calculate roots analytically
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
    return sym.lambdify([u1, u2, v1, v2, v1mid, v2mid, d], f)


def krav_interval(u1n, u2n, v1n, v2n, v1midn, v2midn, dn, cn):
    """
    Function for calculating classical Kravchik evaluation in interval format for parallel robot 2-RPR with
    variable c
    :param u1n: interval u1
    :param u2n: interval u2
    :param v1n: interval v1
    :param v2n: interval v2
    :param v1midn: v1mid
    :param v2midn: v2mid
    :param dn: distance between the points of bases
    :param cn: vector of mids
    :return: function of  classical Kravchik evaluation in numerical format
    """
    v1mid, v2mid = sym.symbols('v1mid, v2mid')
    f = sym.Matrix(
        [[v1 ** 2 - u1 ** 2 - u2 ** 2], [v2 ** 2 - (u1 - d) ** 2 - u2 ** 2]])  # System of kinematic equations
    f_v = derive_matrix(f)  # Calculate matrix of partial derivatives of kinematic matrix
    v = sym.Matrix([[v1], [v2]])  # Vector v
    lam = f_v ** (-1)
    lam = lam.subs([(v1, v1mid), (v2, v2mid)])  # Calculate lambda function for recurrent transformation
    g = v - lam * f  # Equivalent recurrent transformation
    g_v = derive_matrix(g)  # Calculate matrix of partial derivatives of matrix g
    c = sym.Matrix([[cn[0]], [cn[1]]])  # Vector of v-middles
    v_c = v - c
    g_eval = g.subs([(v1, cn[0]), (v2, cn[1])]) + g_v * v_c  # Calculates classical Kravchik evaluation
    F_min = sym.lambdify([u1, u2, v1, v2, v1mid, v2mid, d], g_eval)
    new_v = F_min(u1n, u2n, v1n, v2n, v1midn, v2midn, dn)
    return new_v


def krav_rec_func_number(u1n, u2n, v1n, v2n, v1midn, v2midn, dn):
    """
    Function for calculating recurrent function in interval format
    :param u1n: interval u1
    :param u2n: interval u2
    :param v1n: interval v1
    :param v2n: interval v2
    :param v1midn: v1mid
    :param v2midn: v2mid
    :param dn: distance between the points of bases
    :return: Interval vector of recurrent function
    """
    v1mid, v2mid = sym.symbols('v1mid, v2mid')
    f = sym.Matrix(
        [[v1 ** 2 - u1 ** 2 - u2 ** 2], [v2 ** 2 - (u1 - d) ** 2 - u2 ** 2]])  # System of kinematic equations
    f_v = derive_matrix(f)  # Calculate matrix of partial derivatives of kinematic matrix
    v = sym.Matrix([[v1], [v2]])  # Vector v
    lam = f_v ** (-1)
    lam = lam.subs([(v1, v1mid), (v2, v2mid)])  # Calculate lambda function for recurrent transformation
    g = v - lam * f  # Equivalent recurrent transformation
    g_v = derive_matrix(g)
    F = sym.lambdify([u1, u2, v1, v2, v1mid, v2mid, d], g_v)
    F1 = sym.lambdify([u1, u2, v1, v2, v1mid, v2mid, d], g)
    new_v = F(u1n, u2n, v1n, v2n, v1midn, v2midn, dn)
    new_v2 = [[new_v[0][0]],
               [new_v[1, 1]]]
    return new_v2


def calcul_new_c(u1n, u2n, v1n, v2n, v1midn, v2midn, dn):
    """
    Function for calculation cmin and cmax for bicentered Kravchik
    :param u1n: interval u1
    :param u2n: interval u2
    :param v1n: interval v1
    :param v2n: interval v2
    :param v1midn: v1mid
    :param v2midn: v2mid
    :param dn: distance between the points of bases
    :return: vectors cmin and cmax for bicnetered Kravchik
    """
    new_v = krav_rec_func_number(u1n, u2n, v1n, v2n, v1midn, v2midn, dn)  #Calculate vector of recurrent transformation
    vn = [v1n, v2n]
    c_min = [0, 0]
    c_max = [0, 0]
    for i in range(len(c_min)):
        if new_v[i][0][1]<=0:
            c_min[i] = vn[i][1]
        elif new_v[i][0][0]>=0:
            c_min[i] = vn[i][0]
        else:
            c_min[i] = (new_v[i][0][1]*vn[i][0] - new_v[i][0][0]*vn[i][1])/(new_v[i][0][1] - new_v[i][0][0])
    for i in range(len(c_max)):
        if new_v[i][0][1]<=0:
            c_max[i] = vn[i][0]
        elif new_v[i][0][0]>=0:
            c_max[i] = vn[i][1]
        else:
            c_max[i] = (new_v[i][0][0]*vn[i][0] - new_v[i][0][1]*vn[i][1])/(new_v[i][0][0] - new_v[i][0][1])
    return c_min, c_max


def get_krav_func_bicentered(u1n, u2n, v1n, v2n, v1midn, v2midn, dn):
    """
    Function for calculating bicentered Kravchik evaluation in interval format for parallel robot 2-RPR
    :param u1n: interval u1
    :param u2n: interval u2
    :param v1n: interval v1
    :param v2n: interval v2
    :param v1midn: v1mid
    :param v2midn: v2mid
    :param dn: distance between the points of bases
    :return: Interval vectors for Kravchik evaluation with cmin and cmax
    """
    cmin, cmax = calcul_new_c(u1n, u2n, v1n, v2n, v1midn, v2midn, dn)  # Calculate new c
    v_min = krav_interval(u1n, u2n, v1n, v2n, v1midn, v2midn, dn, cmin)  #Calculate new v1 and v2 with defualt Krav for cmin
    v_max = krav_interval(u1n, u2n, v1n, v2n, v1midn, v2midn, dn, cmax)  #Calculate new v1 and v2 with defualt Krav for cmax
    return (v_min, v_max)


def mysin(x):
    return ival.sin(x)


def mycos(x):
    return ival.cos(x)


def get_unified_krav_eval(f, U, V, Vmid, C, param = []):
    mysin1 = implemented_function(sym.Function('mysin1'), lambda x: mysin(x))
    mycos1 = implemented_function(sym.Function('mycos1'), lambda x: mycos(x))
    """
    Function for calculating classical Kravchik evaluation in symbol format for parallel robot 2-RPR
    :return: function of classical Kravchik evaluation in numerical format
    """
    v = sym.Matrix()
    vmid = sym.Matrix()
    for i in range(len(V)):
        v = v.row_insert(i, sym.Matrix([V[i]]))
        vmid = vmid.row_insert(i, sym.Matrix([Vmid[i]]))
    f_v = derive_matrix(f, v) # Calculate matrix of partial derivatives of kinematic matrix
    lam = f_v ** (-1)
    for i in range(len(v)):
        lam = lam.subs([(V[i], Vmid[i])]) # Calculate lambda function for recurrent transformation
    g = v - lam * f # Equivalent recurrent transformation
    g_v = derive_matrix(g, v) # Calculate matrix of partial derivatives of matrix g
    c = sym.Matrix()
    for i in range(len(v)):
        c = c.row_insert(i, sym.Matrix([C[i]]))
    v_c = v - c
    for i in range(len(V)):
        g = g.subs([(V[i], C[i])])
    g_eval = g + g_v * v_c # Calculates classical Kravchik evaluation
    g_eval = g_eval.replace(sym.sin, mysin1)
    g_eval = g_eval.replace(sym.cos, mycos1)
    return sym.lambdify([U, V, Vmid, C, param], g_eval)


