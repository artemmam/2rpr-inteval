import interval as ival
from kravchik_operator import get_krav_func
from box_class import BoxPoints


krav_transform = get_krav_func()
#  TODO: add more description for function check_box


def check_box(x, y, n, l1, l2, d, p = 10):
    """
    Function for checking intervals rectangles on uniform grid to approximate workspace area of 2-RPR robot
    :param x: X-coordinates of elements of uniform grid
    :param y: Y-coordinates of elements of uniform grid
    :param n: number of nodes of uniform grid
    :param l1: the lowest range of 2-RPR rod
    :param l2: the highest range of 2-RPR rod
    :param d: the distance between rods
    :param p: the max number of iterations
    :return: 4 arrays of calculated rectangles: X-coordinates of workspace area, Y-coordinates of workspace area,
             X-coordinates of border of workspace area, Y-coordinates of border of workspace area
    """
    area_points = BoxPoints()
    border_points = BoxPoints()
    for i in range(n - 1):
        for j in range(n - 1):
            u1 = ival.Interval([x[i, j], x[i, j + 1]])  # Interval form of X-coordinate of rectangle of uniform grid
            u2 = ival.Interval([y[i, j], y[i + 1, j]])  # Interval form of Y-coordinate of rectangle of uniform grid
            if classical_krav_eval(u1, u2, n, l1, l2, d, p) == 'inside' or boundary_krav_eval(u1, u2, n, l1, l2, d, p) == 'inside':
                area_points.add_point(u1[0], 'xleft')
                area_points.add_point(u1[1], 'xright')         # inside the workspace area
                area_points.add_point(u2[0], 'yleft')
                area_points.add_point(u2[1], 'yright')
            elif classical_krav_eval(u1, u2, n, l1, l2, d, p) == 'border' or boundary_krav_eval(u1, u2, n, l1, l2, d, p) == 'border':
                border_points.add_point(u1[0], 'xleft')  # if it is inside previous interval, then it's
                border_points.add_point(u1[1], 'xright')  # inside the workspace area
                border_points.add_point(u2[0], 'yleft')
                border_points.add_point(u2[1], 'yright')
    return area_points, border_points

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
"""
def check_Box_branch_and_bounce(L1x, L2x, L1y, L2y):# алгоритм рекурсивного деления исходной области на более мелкие области
  Lx = L2x - L1x
  Ly = L2y - L1y
  if (stop<=Lx) and  (stop<=Ly):
    if Lx == max(Lx, Ly):
      v1_left = ival.Interval([L1x, (L1x + L2x)/2])
      v2_left = ival.Interval([L1y, L2y])
      v1_right = ival.Interval([(L1x + L2x)/2, L2x])
      v2_right = ival.Interval([L1y, L2y])
    else:
      v1_left = ival.Interval([L1x, L2x])
      v2_left = ival.Interval([(L1y + L2y)/2, L2y])
      v1_right = ival.Interval([L1x, L2x])
      v2_right = ival.Interval([L1y, (L1y + L2y)/2])
    for i in range(len(X)-1):
        for j in range(len(Y)-1):
          u1 = ival.Interval([X[i, j], X[i, j + 1]])
          u2 = ival.Interval([Y[i, j], Y[i + 1, j]])
          if (check_Box_custom_v(u1, u2, v1_left, v2_left) == 0) or (check_Box_custom_v(u1, u2, v1_right, v2_right) == 0):
            area_points_X_l.append(u1[0])
            area_points_X_r.append(u1[1])
            area_points_Y_l.append(u2[0])
            area_points_Y_r.append(u2[1])
    check_Box_branch_and_bounce(v1_left[0], v1_left[1], v2_left[0], v2_left[1])
    check_Box_branch_and_bounce(v1_right[0], v1_right[1], v2_right[0], v2_right[1])

def check_Box_custom_v(u1, u2, v1, v2):# базовый алгоритм для рекурсивного алгоритма
  v1_bor = ival.Interval([v1[0], v1[1]])
  v2_bor = ival.Interval([v2[0], v2[1]])
  for k in range(10):
    v1_fou = ival.Interval([L1, L2])
    v2_fou = ival.Interval([L1, L2])
    v1mid = v1_bor.mid()
    v2mid = v2_bor.mid()
    A = Gright_lamb(u1, u2, v1_bor, v2_bor, v1mid, v2mid)
    if (A[0][0].isIn(v1_bor)) and (A[1][0].isIn(v2_bor)):
      return 0
      break
    if k == 9:
      return 1
    try:
      v1_fou.intersec(A[0][0])
      v2_fou.intersec(A[1][0])
      v1_bor = v1_fou
      v2_bor = v2_fou
    except:
      return 2
      break
"""