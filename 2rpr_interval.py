import numpy as np
from mpmath import iv
import interval as ival
from check_box import check_box
from plot_workspace_area import plot_workspace
from box_class import BoxPoints
from kravchik_operator import get_krav_func, get_rec_func

krav_transform = get_krav_func()
rec_func = get_rec_func()

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
        print("\nClassic krav:")
        print("v1 = ", v1)
        print("v2 = ", v2)
        print("krav = ", v_krav)
        print("Boundary krav:")
        rv = boundary_krav_check(u1, u2, v1, v2, l1, l2, d)
        if rv:
            print("rv = ", rv)
        if (v_krav[0][0].isIn(v1)) and (v_krav[1][0].isIn(v2)):  # Compare Kravchik evaluation with v
            return 'inside'  # if it is inside previous interval, then it's inside the workspace area
        elif boundary_krav_check(u1, u2, v1, v2, l1, l2, d):
            print("Ura!")
            return 'inside'
        if k == p - 1:
            return 'border'  # if we achieve max of the iterations, then it's border
        try:
            v1.intersec(v_krav[0][0])  # if our evalution not fully inside, then intersect it and repeat
            v2.intersec(v_krav[1][0])
        except:                        # if there is no intersection, then the cell is outside
            return 'outside'


def boundary_krav_check(u1, u2, v1, v2, l1, l2, d):  # алгоритм с усиленной проверкой по 4 стороным
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
    # return check
    # 4 bounds of the checking box v
    # v1_border = [ival.Interval([l1, l2]), ival.Interval([l2, l2]), ival.Interval([l1, l2]), ival.Interval([l1, l1])]
    # v2_border = [ival.Interval([l1, l1]), ival.Interval([l1, l2]), ival.Interval([l2, l2]), ival.Interval([l1, l2])]
    v1_border = [ival.Interval([v1[0], v1[1]]), ival.Interval([v1[1], v1[1]]), ival.Interval([v1[0], v1[1]]), ival.Interval([v1[0], v1[0]])]
    v2_border = [ival.Interval([v2[0], v2[0]]), ival.Interval([v2[0], v2[1]]), ival.Interval([v2[1], v2[1]]), ival.Interval([v2[0], v2[1]])]
    for s in range(4):  # Check all 4 boxes
        v1mid = v1_border[s].mid()
        v2mid = v2_border[s].mid()
        v_krav = krav_transform(u1, u2, v1_border[s], v2_border[s], v1mid, v2mid, d) # Calculate Kravchik evaluation for u1, u2
        print("v1 = ", v1_border[s])
        print("v2 = ", v2_border[s])
        print("u1 = ", u1)
        print("u2 = ", u2)
        print("v1mid = ", v1mid)
        print("v2mid", v2mid)
        print("v_krav = ", v_krav)
        # print("v1_bor = ", v1_bor)
        # print("v2_bor = ", v2_bor)

        print("rec = ", rec_func(u1, u2, v1_border[s], v2_border[s], v1mid, v2mid, d))

        if not ((v_krav[0][0].isIn(v1_border[s])) and (v_krav[1][0].isIn(v2_border[s]))): # Compare Kravchik evaluation with v
            check = False
            break
    return check


d = 6
L1 = 3  # Lower range of row
L2 = 15  # Upper range of row
N = 2  # The number of nodes on uniform grid
# l1 = -L2  # Left and lower border of uniform grid
# l2 = L2  # Right and upper border of uniform grid
l1 = 1
l2 = 3
X1 = np.linspace(l1, l2, N)
Y1 = np.linspace(l1, l2, N)
X, Y = np.meshgrid(X1, Y1)  # Build X and Y of uniform grid
k = 10  # Max number of iterations
area_points = BoxPoints()
border_points = BoxPoints()
area_points, border_points = check_box(X, Y, N, L1, L2, d, classical_krav_eval, k)  # Calculate workspace area and border coordinates
# area_points_bound, border_points_bound = check_box(X, Y, N, L1, L2, d, boundary_krav_eval, k)  # Calculate workspace area and border coordinates
plot_workspace(L1, L2, d, area_points, border_points)  # Plotting
# plot_workspace(L1, L2, d, area_points_bound, border_points_bound)