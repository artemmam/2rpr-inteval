import numpy as np
import interval as ival
from check_box import check_box, check_box_uni
from plot_workspace_area import plot_workspace
from box_class import BoxPoints
from kravchik_operator import get_krav_func, get_rec_func_optim, get_krav_func_bicentered, get_unified_krav_eval
import sympy as sym


krav_transform = get_krav_func()
rec_func = get_rec_func_optim()


def classical_krav_eval(u1, u2, l1, l2, d, coef, p=10):
    """
    Check the cell u with classical Krawczyk operator if it is inside of the workspace area,
    outside or on the border
    :param u1: the X coordinates of cell u
    :param u2: the Y coordinates of cell u
    :param l1: the lowest range of 2-RPR rod
    :param l2: the highest range of 2-RPR rod
    :param d: the distance between rods
    :param coef: coeff to change lambda-matrix
    :param p: the max number of iterations
    :return: the string 'inside', 'outside' or 'border'
    """
    v1 = ival.Interval([l1, l2])  # Interval form of X-coordinate for box v
    v2 = ival.Interval([l1, l2])  # Interval form of Y-coordinate for box v
    v1mid = coef * v1.mid()
    v2mid = coef * v2.mid()
    for k in range(p):
        c1 = v1.mid()
        c2 = v2.mid()
        v_krav = krav_transform(u1, u2, v1, v2, v1mid, v2mid, c1, c2, d)  # Calculate Kravchik evaluation for u1, u2
        if (v_krav[0][0].isIn(v1)) and (v_krav[1][0].isIn(v2)):  # Compare Kravchik evaluation with v
            return 'inside'  # if it is inside previous interval, then it's inside the workspace area
        if k == p - 1:
            return 'border'  # if we achieve max of the iterations, then it's border
        if v1.isNoIntersec(v_krav[0][0]) or v2.isNoIntersec(v_krav[1][0]):
            return 'outside'
        else:
            v1.intersec(v_krav[0][0])  # if our evalution not fully inside, then intersect it and repeat
            v2.intersec(v_krav[1][0])


def exact_eval(u1, u2, l1, l2, d, coef, p=10):
    """
    Check the cell u with exact interval enclosure (see function zzf and rec_func in kravchik_operator.py) if it is
    inside if the workspace area, outside or on the border
    :param u1: the X coordinates of cell u
    :param u2: the Y coordinates of cell u
    :param l1: the lowest range of 2-RPR rod
    :param l2: the highest range of 2-RPR rod
    :param d: the distance between rods
    :param coef: coeff to change lambda-matrix
    :param p: the max number of iterations
    :return: the string 'inside', 'outside' or 'border'
    """
    v1 = ival.Interval([l1, l2])  # Interval form of X-coordinate for box v
    v2 = ival.Interval([l1, l2])  # Interval form of Y-coordinate for box v
    v1mid = coef * v1.mid()
    v2mid = coef * v2.mid()
    for k in range(p):
        v_exact = rec_func(u1, u2, v1, v2, v1mid, v2mid, d) # Calculate exact_inclusion for u1, u2
        if (v_exact[0][0].isIn(v1)) and (v_exact[1][0].isIn(v2)):  # Compare Kravchik evaluation with v
            return 'inside'  # if it is inside previous interval, then it's inside the workspace area
        if k == p - 1:
            return 'border'  # if we achieve max of the iterations, then it's border
        if v1.isNoIntersec(v_exact[0][0]) or v2.isNoIntersec(v_exact[1][0]):
            return 'outside'
        else:
            v1.intersec(v_exact[0][0])  # if our evalution not fully inside, then intersect it and repeat
            v2.intersec(v_exact[1][0])


def bicentered_krav_eval(u1, u2, l1, l2, d, coef, p=10):
    """
    Check the cell u with classical Krawczyk operator if it is inside of the workspace area,
    outside or on the border
    :param u1: the X coordinates of cell u
    :param u2: the Y coordinates of cell u
    :param l1: the lowest range of 2-RPR rod
    :param l2: the highest range of 2-RPR rod
    :param d: the distance between rods
    :param coef: coeff to change lambda-matrix
    :param p: the max number of iterations
    :return: the string 'inside', 'outside' or 'border'
    """
    v1 = ival.Interval([l1, l2])  # Interval form of X-coordinate for box v
    v2 = ival.Interval([l1, l2])  # Interval form of Y-coordinate for box v
    v1mid = coef * v1.mid()
    v2mid = coef * v2.mid()
    for k in range(p):
        v_min, v_max = get_krav_func_bicentered(u1, u2, v1, v2, v1mid, v2mid, d)
        v_min[0][0].intersec(v_max[0][0])  # Intersec Krav evalutaion for v_min and v_max
        v_min[1][0].intersec(v_max[1][0])
        if (v_min[0][0].isIn(v1)) and (v_min[1][0].isIn(v2)):  # Compare bicentered Kravchik evaluation with v
            return 'inside'  # if it is inside previous interval, then it's inside the workspace area
        if k == p - 1:
            return 'border'  # if we achieve max of the iterations, then it's border
        if v1.isNoIntersec(v_min[0][0]) or v2.isNoIntersec(v_min[1][0]):
            return 'outside'
        else:
            v1.intersec(v_min[0][0])  # if our evalution not fully inside, then intersect it and repeat
            v2.intersec(v_min[1][0])


def unified_krav_eval(U, l1, l2, param, coef = 1, p=10):
    v1 = ival.Interval([l1, l2])
    v2 = ival.Interval([l1, l2])
    V = [v1, v2]
    v1mid = coef * v1.mid()
    v2mid = coef * v2.mid()
    Vmid = [v1mid, v2mid]
    for k in range(p):
        c1 = v1.mid()
        c2 = v2.mid()
        C = [c1, c2]
        v_krav = unified_krav_func(U, V, Vmid, C, param)  # Calculate Kravchik evaluation for u1, u2
        if (v_krav[0][0].isIn(v1)) and (v_krav[1][0].isIn(v2)):  # Compare Kravchik evaluation with v
            return 'inside'  # if it is inside previous interval, then it's inside the workspace area
        if k == p - 1:
            return 'border'  # if we achieve max of the iterations, then it's border
        if v1.isNoIntersec(v_krav[0][0]) or v2.isNoIntersec(v_krav[1][0]):
            return 'outside'
        else:
            v1.intersec(v_krav[0][0])  # if our evalution not fully inside, then intersect it and repeat
            v2.intersec(v_krav[1][0])




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

### Setting params
def set_param(L2, N):
    l1 = -L2  # Left and lower border of uniform grid
    l2 = L2  # Right and upper border of uniform grid
    X1 = np.linspace(l1, l2, N)
    Y1 = np.linspace(l1, l2, N)
    X, Y = np.meshgrid(X1, Y1)  # Build X and Y of uniform grid
    return (X, Y)


f, U, V, Vmid, C, param_sym = func_2rpr()

unified_krav_func = get_unified_krav_eval(f, U, V, Vmid, C, param_sym)

k = 10  # Max number of iterations
coef = 1
L1 = 3  # Lower range of row
L2 = 15  # Upper range of row
d = 6
N = 12  # The number of nodes on uniform grid
X, Y = set_param(L2, N)
param = [d]

area_points = BoxPoints()
border_points = BoxPoints()
#area_points, border_points = check_box(X, Y, N, L1, L2, d, exact_eval, coef, k)  # Calculate workspace area and border coordinates
area_points_def, border_points_def = check_box(X, Y, N, L1, L2, d, classical_krav_eval, coef, k)  # Calculate workspace area and border coordinates
area_points_uni, border_points_uni = check_box_uni(X, Y, N, L1, L2, param, unified_krav_eval, coef, k)  # Calculate workspace area and border coordinates
#area_points_bic, border_points_bic = check_box(X, Y, N, L1, L2, d, bicentered_krav_eval, coef, k)
#plot_workspace(L1, L2, d, area_points, border_points)  # Plotting
#plot_workspace(L1, L2, d, area_points_bic, border_points_bic)
plot_workspace(L1, L2, d, area_points_def, border_points_def)