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

    c = sym.Matrix([[v1mid], [v2mid]]) # Vector of v-middles
    v_c = v - c
    g_eval = g.subs([(v1, v1mid), (v2, v2mid)]) + g_v * v_c  # Calculates classical Kravchik evaluation
    print(g_eval)
    return sym.lambdify([u1, u2, v1, v2, v1mid, v2mid, d], g_eval)

def get_rec_func():
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
    print("g_easy_comp = ", g)
   # return sym.lambdify([u1, u2, v1, v2, v1mid, v2mid, d], g)

def zzf(x, m):
    #print("zzf: ", x, m)
    zf = lambda x, m : x * (1 - x / (2 * m))
    #print('m=',m)
    #print('x=', x)
    if m <= x[0]:
        iv = ival.Interval([zf(x[1],m), zf(x[0],m)])
    elif m >= x[1]:
        iv = ival.Interval([zf(x[0],m), zf(x[1],m)])
        #print('2 случай')
    else:
        iv = ival.Interval([min(zf(x[0],m), zf(x[1],m)), max(zf(x[0],m), zf(x[1],m))])#zf(m,m)])
    #print("iv = ", iv)
    return iv

"""
def zzkrav(x, m):
    #print("zzf: ", x, m)
    zf = lambda x, m : x * (2 - x / m)
    if m <= x[0]:
        iv = ival.Interval([zf(x[1],m), zf(x[0],m)])
    elif m >= x[1]:
        iv = ival.Interval([zf(x[0],m), zf(x[1],m)])
    else:
        iv = ival.Interval([min(zf(x[0],m), zf(x[1],m)), zf(m,m)])
    #print("iv = ", iv)
    return iv
"""

def get_rec_func_optim():
    """
    :return: function of  classical Kravchik evaluation in numerical format
    """
    v1mid, v2mid = sym.symbols('v1mid, v2mid')
    # zf = sym.Function('zzf')
    hump = implemented_function(sym.Function('hump'), lambda x, m: zzf(x,m))
                                #ival.Interval(), ival.Interval([x[0] * x[1] / (x[0] + x[1]), (x[0] + x[1])/4]))
    # f = sym.Matrix([[v1*(1 - v1/(2*v1mid)) - (u1**2 + u2**2)/(2*v1mid)], [v2 - (-u2**2 + v2**2 - (-d + u1)**2)/(2*v2mid)]])  # System of kinematic equations
    f = sym.Matrix([[hump(v1, v1mid) - (-u1**2 - u2**2)/(2*v1mid)], [hump(v2, v2mid) - (-u2**2 - (u1 - d)**2)/(2*v2mid)]])  # System of kinematic equations
    print("g = ", f)
    return sym.lambdify([u1, u2, v1, v2, v1mid, v2mid, d], f)

"""

def get_krav_func_optim():
    :return: function of  classical Kravchik evaluation in numerical format
    v1mid, v2mid = sym.symbols('v1mid, v2mid')
    # zf = sym.Function('zzf')
    hump = implemented_function(sym.Function('hump'), lambda x, m: zzkrav(x,m))
                                #ival.Interval(), ival.Interval([x[0] * x[1] / (x[0] + x[1]), (x[0] + x[1])/4]))
    # f = sym.Matrix([[v1*(1 - v1/(2*v1mid)) - (u1**2 + u2**2)/(2*v1mid)], [v2 - (-u2**2 + v2**2 - (-d + u1)**2)/(2*v2mid)]])  # System of kinematic equations
    f = sym.Matrix([[hump(v1, v1mid) - (-u1**2 - u2**2+v1mid**2)/(2*v1mid)], [hump(v2, v2mid) - (-u2**2 + v2mid**2 - (-d + u1)**2)/(2*v2mid)]])  # System of kinematic equations
    print("g = ", f)
    return sym.lambdify([u1, u2, v1, v2, v1mid, v2mid, d], f)
    
"""