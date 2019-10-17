import numpy as np
import interval as ival
from check_box import check_box
from plot_workspace_area import plot_workspace
from box_class import BoxPoints
from kravchik_operator import get_krav_func, get_rec_func_optim


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
        elif boundary_krav_check(u1, u2, v1, v2, d):
            print("Ura!")
            return 'inside'
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


def boundary_krav_check(u1, u2, v1, v2, d):  # алгоритм с усиленной проверкой по 4 стороным
    """
    Check the cell u with boundary Krawczyk operator if it is inside of the workspace area
    :param u1: the X coordinates of cell u
    :param u2: the Y coordinates of cell u
    :param d: the distance between rods
    :param p: the max number of iterations
    :return: bool
    """
    check = True
    # 4 bounds of the checking box v
    v1_border = [ival.Interval([v1[0], v1[1]]), ival.Interval([v1[1], v1[1]]), ival.Interval([v1[0], v1[1]]), ival.Interval([v1[0], v1[0]])]
    v2_border = [ival.Interval([v2[0], v2[0]]), ival.Interval([v2[0], v2[1]]), ival.Interval([v2[1], v2[1]]), ival.Interval([v2[0], v2[1]])]
    for s in range(4):  # Check all 4 boxes
        v1mid = v1_border[s].mid()
        v2mid = v2_border[s].mid()
        v_krav = krav_transform(u1, u2, v1_border[s], v2_border[s], v1mid, v2mid, v1mid, v2mid, d) # Calculate Kravchik evaluation for u1, u2
        if not ((v_krav[0][0].isIn(v1_border[s])) and (v_krav[1][0].isIn(v2_border[s]))): # Compare Kravchik evaluation with v
            check = False
            break
    return check


d = 6
L1 = 3  # Lower range of row
L2 = 15  # Upper range of row
N = 25  # The number of nodes on uniform grid
l1 = -L2  # Left and lower border of uniform grid
l2 = L2  # Right and upper border of uniform grid
X1 = np.linspace(l1, l2, N)
Y1 = np.linspace(l1, l2, N)
X, Y = np.meshgrid(X1, Y1)  # Build X and Y of uniform grid
k = 10  # Max number of iterations
coef = 1.5
area_points = BoxPoints()
border_points = BoxPoints()
area_points, border_points = check_box(X, Y, N, L1, L2, d, exact_eval, coef, k)  # Calculate workspace area and border coordinates
area_points_def, border_points_def = check_box(X, Y, N, L1, L2, d, classical_krav_eval, coef, k)  # Calculate workspace area and border coordinates
plot_workspace(L1, L2, d, area_points, border_points)  # Plotting
plot_workspace(L1, L2, d, area_points_def, border_points_def)