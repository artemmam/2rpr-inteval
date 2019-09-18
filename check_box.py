import interval as ival
from kravchik_operator import get_krav_func


krav_transform = get_krav_func()
#  TODO: add more description for function check_box


def check_box(x, y, n, l1, l2, d, e = 10):
    """
    Function for checking intervals rectangles on uniform grid to compare with
    :param x: X-coordinates of elements of uniform grid
    :param y: Y-coordinates of elements of uniform grid
    :param n: number of nodes of uniform grid
    :param l1: the lowest range of 2-RPR rod
    :param l2: the highest range of 2-RPR rod
    :param d: the distance between rods
    :param e: the max number of iterations
    :return: 4 arrays of calculated rectangles: X-coordinates of workspace area, Y-coordinates of workspace area,
             X-coordinates of border of workspace area, Y-coordinates of border of workspace area
    """
    area_points_x_l = []  # Lists of left and right borders of area rectangles for X and Y coordinates
    area_points_x_r = []
    area_points_y_l = []
    area_points_y_r = []
    border_points_x_l = []  # Lists of left and right borders of border rectangles for X and Y coordinates
    border_points_x_r = []
    border_points_y_l = []
    border_points_y_r = []
    for i in range(n - 1):
        for j in range(n - 1):
            u1 = ival.Interval([x[i, j], x[i, j + 1]])  # Interval form of X-coordinate of rectangle of uniform grid
            u2 = ival.Interval([y[i, j], y[i + 1, j]])  # Interval form of Y-coordinate of rectangle of uniform grid
            v1 = ival.Interval([l1, l2])  # Interval form of X-coordinate for box v
            v2 = ival.Interval([l1, l2])  # Interval form of Y-coordinate for box v
            for k in range(e):
                v1mid = v1.mid()
                v2mid = v2.mid()
                v_krav = krav_transform(u1, u2, v1, v2, v1mid, v2mid, d)  # Calculate Kravchik evaluation for u1, u2
                if (v_krav[0][0].isIn(v1)) and (v_krav[1][0].isIn(v2)):  # Compare Kravchik evaluation with v
                    area_points_x_l.append(x[i, j])                 # if it is inside previous interval, than it's
                    area_points_x_r.append(x[i, j + 1])             # inside the workspace area
                    area_points_y_l.append(y[i, j])
                    area_points_y_r.append(y[i + 1, j])
                    break
                if k == e - 1:
                    border_points_x_l.append(x[i, j])       # If we achieve max of the iterations, than it's border
                    border_points_x_r.append(x[i, j + 1])
                    border_points_y_l.append(y[i, j])
                    border_points_y_r.append(y[i + 1, j])
                try:
                    v1.intersec(v_krav[0][0])  # If our evalution not fully inside, than intersect it and repeat
                    v2.intersec(v_krav[1][0])
                except:
                    break                 # if there is no intersection at all, than it's outside of the workspace
    return [area_points_x_l, area_points_x_r], [area_points_y_l, area_points_y_r], [border_points_x_l, border_points_x_r], [border_points_y_l, border_points_y_r]

def check_Box_no_Kr(u1, u2):# алгоритм с усиленной проверкой по 4 стороным
  check = True
  V1_bor = [ival.Interval([L1, L2]), ival.Interval([L2, L2]), ival.Interval([L1, L2]), ival.Interval([L1, L1])]
  V2_bor = [ival.Interval([L1, L1]), ival.Interval([L1, L2]), ival.Interval([L2, L2]), ival.Interval([L1, L2])]
  for p in range(4):
    v1 = V1_bor[p]
    v2 = V2_bor[p]
    for k in range(10):
          v1mid = v1.mid()
          v2mid = v2.mid()
          v1_bor = ival.Interval([L1, L2])
          v2_bor = ival.Interval([L1, L2])
          A = Gright_lamb(u1, u2, v1, v2, v1mid, v2mid)
          if (A[0][0].isIn(v1_bor)) and (A[1][0].isIn(v2_bor)):
            check = True
            if p ==3 and check == True:
              return 0
            break
          else:
            check = False
          try:
            v1_bor.intersec(A[0][0])
            v2_bor.intersec(A[1][0])
            v1 = v1_bor
            v2 = v2_bor
          except:
            break
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