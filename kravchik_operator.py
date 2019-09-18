import sympy as sym
v1, v2, u1, u2, d = sym.symbols('v1, v2, u1, u2, d')


def derive_matrix(g):
    """
    Function for calculating partial derivative of matrix G
    :param G : array to be derived
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
    return sym.lambdify([u1, u2, v1, v2, v1mid, v2mid, d], g_eval)