import numpy as np
from mpmath import iv
import interval as ival
from check_box import check_box
from plot_workspace_area import plot_workspace
from box_class import BoxPoints
from kravchik_operator import get_krav_func

krav_transform = get_krav_func()


def classical_krav_eval(u1, u2, l1, l2, d, p=10):
    """
    Check the cell u with classical Krawczyk operator if it is inside of the workspace area,
    outside or on the border
    :param u1: the X coordinates of cell u
    :param u2: the Y coordinates of cell u
    :param n: number of nodes of uniform grid
    :param l1: the lowest range of 2-RPR rod
    :param l2: the highest range of 2-RPR rod
    :param d: the distance between rods
    :param p: the max number of iterations
    :return: the string 'inside', 'outside' or 'border'
    """
    v1 = ival.Interval([l1, l2])  # Interval form of X-coordinate for box v
    v2 = ival.Interval([l1, l2])  # Interval form of Y-coordinate for box v
    for k in range(p):
        v1mid = v1.mid()
        v2mid = v2.mid()
        v_krav = krav_transform(u1, u2, v1, v2, v1mid, v2mid, d)  # Calculate Kravchik evaluation for u1, u2
        if (v_krav[0][0].isIn(v1)) and (v_krav[1][0].isIn(v2)):  # Compare Kravchik evaluation with v
            return 'inside'  # if it is inside previous interval, then it's inside the workspace area
        if k == p - 1:
            return 'border'  # if we achieve max of the iterations, then it's border
        try:
            v1.intersec(v_krav[0][0])  # if our evalution not fully inside, then intersect it and repeat
            v2.intersec(v_krav[1][0])
        except:                        # if there is no intersection, then the cell is outside
            return 'outside'


def boundary_krav_eval(u1, u2, l1, l2, d, p=10):  # алгоритм с усиленной проверкой по 4 стороным
    """
    Check the cell u with boundary Krawczyk operator if it is inside of the workspace area,
    outside or on the border
    :param u1: the X coordinates of cell u
    :param u2: the Y coordinates of cell u
    :param l1: the lowest range of 2-RPR rod
    :param l2: the highest range of 2-RPR rod
    :param d: the distance between rods
    :param p: the max number of iterations
    :return: the string 'inside', 'outside' or 'border'
    """
    check = True
    # 4 bounds of the checking box v
    v1_border = [ival.Interval([l1, l2]), ival.Interval([l2, l2]), ival.Interval([l1, l2]), ival.Interval([l1, l1])]
    v2_border = [ival.Interval([l1, l1]), ival.Interval([l1, l2]), ival.Interval([l2, l2]), ival.Interval([l1, l2])]
    for s in range(4):  # Check all 4 boxes
        v1 = v1_border[s]
        v2 = v2_border[s]
        for k in range(p):
            v1mid = v1.mid()
            v2mid = v2.mid()
            v1_bor = ival.Interval([l1, l2])
            v2_bor = ival.Interval([l1, l2])
            v_krav = krav_transform(u1, u2, v1, v2, v1mid, v2mid, d) # Calculate Kravchik evaluation for u1, u2
            if (v_krav[0][0].isIn(v1_bor)) and (v_krav[1][0].isIn(v2_bor)): # Compare Kravchik evaluation with v
                check = True
                if p == 3 and check:  # if it is inside all 4 boundaries, then it's inside the workspace area
                    return 'inside'
            else:
                check = False
            if k == p - 1:
                return 'border'  # if we achieve max of the iterations, then it's border
            try:
                v1_bor.intersec(A[0][0])  # if our evalution not fully inside, then intersect it and repeat
                v2_bor.intersec(A[1][0])
                v1 = v1_bor
                v2 = v2_bor
            except:
                return 'outside'  # if there is no intersection, then the cell is outside


d = 6
L1 = 3  # Lower range of row
L2 = 15  # Upper range of row
N = 20  # The number of nodes on uniform grid
l1 = -L2  # Left and lower border of uniform grid
l2 = L2  # Right and upper border of uniform grid
X1 = np.linspace(l1, l2, N)
Y1 = np.linspace(l1, l2, N)
X, Y = np.meshgrid(X1, Y1)  # Build X and Y of uniform grid
k = 10  # Max number of iterations
area_points = BoxPoints()
border_points = BoxPoints()
area_points, border_points = check_box(X, Y, N, L1, L2, d, classical_krav_eval, k)  # Calculate workspace area and border coordinates
area_points_bound, border_points_bound = check_box(X, Y, N, L1, L2, d, boundary_krav_eval, k)  # Calculate workspace area and border coordinates
plot_workspace(L1, L2, d, area_points, border_points)  # Plotting
plot_workspace(L1, L2, d, area_points_bound, border_points_bound)