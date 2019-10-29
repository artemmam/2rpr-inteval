import interval as ival
from kravchik_operator import get_krav_func
from box_class import BoxPoints
#  TODO: add more description for function check_box


def check_box(x, y, n, l1, l2, d, checker, coef, p=10):
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

            if checker(u1, u2, l1, l2, d, coef, p) == 'inside': #or boundary_krav_eval(u1, u2, n, l1, l2, d, p) == 'inside':
                area_points.add_point(u1[0], 'xleft')
                area_points.add_point(u1[1], 'xright')         # inside the workspace area
                area_points.add_point(u2[0], 'yleft')
                area_points.add_point(u2[1], 'yright')
            elif checker(u1, u2, l1, l2, d, coef, p) == 'border': #or boundary_krav_eval(u1, u2, n, l1, l2, d, p) == 'border':
                border_points.add_point(u1[0], 'xleft')  # if it is inside previous interval, then it's
                border_points.add_point(u1[1], 'xright')  # inside the workspace area
                border_points.add_point(u2[0], 'yleft')
                border_points.add_point(u2[1], 'yright')
    return area_points, border_points