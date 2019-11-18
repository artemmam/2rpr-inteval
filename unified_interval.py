import sympy as sym
import interval as ival
from plot_workspace_area import uni_plotter
from box_class import BoxPoints
from kravchik_operator import get_unified_krav_eval
import numpy as np
from check_box import check_box_uni


def unified_krav_eval(U, Vin, param, p=10):
    V = []
    for i in range(len(Vin)):
        V.append(ival.Interval([Vin[i][0], Vin[i][1]]))
    Vmid = []
    for i in range(len(V)):
        Vmid.append(V[i].mid())
    #print('квадратик U', U)
    for k in range(p):
        C = []
        for i in range(len(V)):
            C.append(V[i].mid())
        v_krav = unified_krav_func(U, V, Vmid, C, param)  # Calculate Kravchik evaluation for u1, u2
        #print('old V', V)
        #print('new V', v_krav)
        check = True
        for i in range(len(V)):
            if not(v_krav[i][0].isIn(V[i])):
                check = False
        if check:
            return 'inside'  # if it is inside previous interval, then it's inside the workspace area
        if k == p - 1:
            return 'border'  # if we achieve max of the iterations, then it's border
        for i in range(len(V)):
            if V[i].isNoIntersec(v_krav[i][0]):
                return 'outside'
            else:
                V[i].intersec(v_krav[i][0])  # if our evalution not fully inside, then intersect it and repeat


def func_robot():
    Vmid = sym.symbols('v1mid, v2mid')
    V = sym.symbols('v1, v2')
    U = sym.symbols('u1, u2')
    C = sym.symbols('c1, c2')
    f = sym.Matrix([[U[0] - V[0]*sym.sin(V[1])],
                    [U[1] - V[0]*sym.cos(V[1])]])
    return f, U, V, Vmid, C


def func_sin_cos():
    Vmid = sym.symbols('v1mid, v2mid')
    V = sym.symbols('v1, v2')
    U = sym.symbols('u1, u2')
    C = sym.symbols('c1, c2')
    f = sym.Matrix([[U[0] - sym.sin(V[0])],
                    [U[1] - sym.cos(V[1])]])
    return f, U, V, Vmid, C

def func_2rpr():
    Vmid = sym.symbols('v1mid, v2mid')
    V = sym.symbols('v1, v2')
    U = sym.symbols('u1, u2')
    C = sym.symbols('c1, c2')
    param_sym = sym.symbols('d')
    param_sym = [param_sym]
    f = sym.Matrix([[V[0] ** 2 - U[0] ** 2 - U[1] ** 2],
         [V[1] ** 2 - (U[0] - param_sym[0]) ** 2 - U[1] ** 2]])
    return f, U, V, Vmid, C, param_sym


def func_dextar():
    Vmid = sym.symbols('v1mid, v2mid, v3mid, v4mid')
    V = sym.symbols('v1, v2, v3, v4')
    U = sym.symbols('u1, u2')
    C = sym.symbols('c1, c2, c3, c4')
    param_sym = sym.symbols('L, l, d')
    f = sym.Matrix([[U[0] - param_sym[0] * sym.cos(V[0]) - param_sym[1] * sym.cos(V[2]) + param_sym[2]],
                    [U[0] - param_sym[0] * sym.cos(V[1]) - param_sym[1] * sym.cos(V[3]) - param_sym[2]],
                    [U[1] - param_sym[0] * sym.sin(V[0]) - param_sym[1] * sym.sin(V[2])],
                    [U[1] - param_sym[0] * sym.sin(V[1]) - param_sym[1] * sym.sin(V[3])]])
    return f, U, V, Vmid, C, param_sym


### Setting params
def set_param(L2, N):
    l1 = -L2  # Left and lower border of uniform grid
    l2 = L2  # Right and upper border of uniform grid
    X1 = np.linspace(l1, l2, N)
    Y1 = np.linspace(l1, l2, N)
    X, Y = np.meshgrid(X1, Y1)  # Build X and Y of uniform grid
    return (X, Y)

N = 50  # The number of nodes on uniform grid



#"""
##### 2-RPR
f, U, V, Vmid, C, param_sym = func_2rpr()
L1v = 3  # Lower range of row
L2v = 15  # Upper range of row
v1 = ival.Interval([L1v, L2v])
v2 = ival.Interval([L1v, L2v])
V_ival = [v1, v2]
L2u = L2v
d = 6
X, Y = set_param(L2u, N)
param = [d]
unified_krav_func = get_unified_krav_eval(f, U, V, Vmid, C, param_sym)
#####
#"""
"""
##### sin-cos func
f, U, V, Vmid, C = func_sin_cos()
L1u = -2  # Lower range of box U
L2u = 2  # Upper range of box U
#L1v = 0  # Lower range of box V
#L2v = np.pi/2  # Upper range of box V
v1 = ival.Interval([0, 2*np.pi])
v2 = ival.Interval([0, 2*np.pi])
V_ival = [v1, v2]
X, Y = set_param(L2u, N)
param = []
unified_krav_func = get_unified_krav_eval(f, U, V, Vmid, C)
#####
"""
"""
##### robot func
f, U, V, Vmid, C = func_robot()
L1u = -15  # Lower range of box U
L2u = 15  # Upper range of box U
v1 = ival.Interval([3, 15])
v2 = ival.Interval([0, np.pi/2])
V_ival = [v1, v2]
X, Y = set_param(L2u, N)
param = []
unified_krav_func = get_unified_krav_eval(f, U, V, Vmid, C)
#####
"""
"""
#####  dextar
f, U, V, Vmid, C, sym_param = func_dextar()
L = 7.2
l = 2.0
d = 3.0
d1 = d*2
L1u = d-(L + l)  # Lower range of box U
L2u = d+(L + l)  # Upper range of box U
l1 = 0
l2 = 2*np.pi
v1 = ival.Interval([l1, l2])
v2 = ival.Interval([l1, l2])
v3 = ival.Interval([l1, l2])
v4 = ival.Interval([l1, l2])
V_ival = [v1, v2, v3, v4]
X, Y = set_param(L2u, N)
param = [L, l, d]
unified_krav_func = get_unified_krav_eval(f, U, V, Vmid, C, sym_param)
#####
"""
k = 10  # Max number of iterations
coef = 1
area_points = BoxPoints()
border_points = BoxPoints()


area_points_uni, border_points_uni = check_box_uni(X, Y, N, V_ival, param, unified_krav_eval, coef, k)
uni_plotter(area_points_uni, border_points_uni, L2u)
