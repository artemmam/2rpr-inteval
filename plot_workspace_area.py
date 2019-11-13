import shapely.geometry as sg
import matplotlib.pyplot as plt
import descartes
from matplotlib.patches import Circle, Rectangle


import numpy as np
def check_D_1(x, y, a, b, d):  # проверяем лежит ли точка вне малой окр-ти
    """
    Check point if it is outside lower limit of leg (what is the same if these points outside the smallest circles)

    Parameters
    ----------
    x, y : float, the coordinates of points
    x0, y0 : float, the coordinates of the circle's center
    r : float, radius of the circle
    Returns
    -------
    Boolean massive of all points which are outside the smallest circles

    """
    return (((2 * (-(x + d / 2) / (y)) * ((x + d / 2) ** 2 / (2 * y) + y / 2 + (a ** 2 - b ** 2) / (2 * y))) ** 2 -
             4 * (1 + ((x + d / 2) ** 2) / (y ** 2)) * (
                         (((x + d / 2) ** 2) / (2 * y) + y / 2 + (a ** 2 - b ** 2) / (2 * y)) ** 2 - a ** 2)) >= 0)


def check_D_2(x, y, a, b, d):  # проверяем лежит ли точка вне малой окр-ти
    """
    Check points if it is inside the higher limit of leg (what is the same if these points inside the biggest circles)

    Parameters
    ----------
    x, y : float, the coordinates of points
    x0, y0 : float, the coordinates of the circle's center
    r : float, radius of the circle
    Returns
    -------
    Boolean massive of all points which are inside the biggest circles

    return ((x - x0)**2 + (y - y0)**2 <= r**2)

    """
    return (((2 * (-(x - d / 2) / (y)) * (((x - d / 2) ** 2) / (2 * y) + y / 2 + (a ** 2 - b ** 2) / (2 * y))) ** 2 -
             4 * (1 + ((x - d / 2) ** 2) / (y ** 2)) * (
                         (((x - d / 2) ** 2) / (2 * y) + y / 2 + (a ** 2 - b ** 2) / (2 * y)) ** 2 - a ** 2)) >= 0)
def uniform_grid(a, b, d, p, seed=1234):
    """
    Compute the area of DexTar's workspace with Monte Carlo method using uniform grid

    Parameters
    ----------
    l1_l, l2_l : float, the lowest limit of legs
    l1_h, l2_h : float, the highest limit of legs
    d : float, length between legs of the robot
    p : int, amount of points
    seed : int, seed for rng, default = 1234
    Returns
    -------
    area: float , area of 2-RPR robot's workspace
    Xl, Xh : float, X-axis limits for MC rectangle
    Yl, Yh : float, Y-axis limits for MC rectangle

    """
    Xl = -(a + b + d)
    Xh = a + b + d
    Yl = -(a + b + d)
    Yh = a + b + d
    X1 = np.linspace(Xl, Xh, int(np.sqrt(p)))
    Y1 = np.linspace(Yl, Yh, int(np.sqrt(p)))
    X, Y = np.meshgrid(X1, Y1)
    X = X.ravel()
    Y = Y.ravel()
    # print('Стандартное отклоченние',np.std(X), np.std(Y))
    # print('Мат.ожидание',np.mean(X), np.mean(Y))
    #c = 0
    #c = sum((check_D_1(X, Y, a, b, d)) & (check_D_2(X, Y, a, b, d)))
    #area = ((Xh - Xl) * (Yh - Yl) * c / p)
    return X[check_D_1(X, Y, a, b, d) & check_D_2(X, Y, a, b, d)], Y[
        check_D_1(X, Y, a, b, d) & check_D_2(X, Y, a, b, d)], X, Y


def plot_workspace(l1, l2, d, area_points, border_points):
    """
    Function for plotting workspace area of 2-RPR robot with approximation on uniform grid
    :param l1: the lowest range of 2-RPR rod
    :param l2: the highest range of 2-RPR rod
    :param d:  the distance between rods
    :param points_area_x:  the array of X-coordinates of area points
    :param points_area_y:  the array of Y-coordinates of area points
    :param points_border_x:  the array of X-coordinates of border points
    :param points_border_y:  the array of Y-coordinates of border points
    :return:
    """
    left_border = -l2  # Left border of rectangle which we use to build uniform grid
    right_border = l2  # Right border of rectangle which we use to build uniform grid
    if l1 < l2:
        l1 += 1e-10
        fig, ax = plt.subplots(figsize=(8, 8))
        x_min, y_min, x_max, y_max = left_border - 1, left_border - 1, right_border + 1, right_border + 1
        ax.set_xlim([x_min, x_max])
        ax.set_ylim([y_min, y_max])
        a = sg.Point(0,0).buffer(l1)  # Init circles with shapely
        b = sg.Point(0,0).buffer(l2)
        c = sg.Point(d,0).buffer(l1)
        e = sg.Point(d,0).buffer(l2)
        ab = b.difference(a)  # Calculate rings as a difference of bigger circle and smaller circle for each rod
        cd = e.difference(c)
        middle = ab.intersection(cd)  # Calculates final area of robot workspace as intersection of two rings
        circle1 = Circle((0, 0), radius=l1, fill=False, color='r')  # Init circles with matplotlib for plot
        circle2 = Circle((0, 0), radius=l2, fill=False, color='r')
        circle3 = Circle((d, 0), radius=l1, fill=False, color='b')
        circle4 = Circle((d, 0), radius=l2, fill=False, color='b')
        rect1 = Rectangle([left_border, left_border],
                          abs(left_border) + abs(right_border),  # Init rectangle in which uniform grid is built
                          abs(left_border) + abs(right_border), fill=False, color='g', linewidth=2.0)
        ax.add_patch(descartes.PolygonPatch(middle, fc='b', ec='k', alpha=0.2))  # Adding patches to plot
        ax.add_patch(circle1)
        ax.add_patch(circle2)
        ax.add_patch(circle3)
        ax.add_patch(circle4)
        ax.add_patch(rect1)
        ax.axes.set_aspect('equal')
        for i in range(len(area_points.get_points('xleft'))):  # Plot rectangles, which compose workspace area
            rect1 = Rectangle([area_points.get_points('xleft')[i], area_points.get_points('yleft')[i]],
                              area_points.get_points('xright')[i] - area_points.get_points('xleft')[i],
                              area_points.get_points('yright')[i] - area_points.get_points('yleft')[i],
                              fill=True, fc='red', color='g', linewidth=1.0, alpha=0.5)
            ax.add_patch(rect1)
        for i in range(len(border_points.get_points('xleft'))):  # Plot rectangles, which compose the border of workspace area
            rect2 = Rectangle([border_points.get_points('xleft')[i], border_points.get_points('yleft')[i]],
                              border_points.get_points('xright')[i] - border_points.get_points('xleft')[i],
                              border_points.get_points('yright')[i] - border_points.get_points('yleft')[i],
                              fill=True, fc='black', color='yellow', linewidth=1.0, alpha=0.5)
            ax.add_patch(rect2)
        plt.show()
    else:
        print('Wrong data')


def uni_plotter(area_points, border_points, L2, a = 0, b = 0, d = 0):
    left_border = -L2  # Left border of rectangle which we use to build uniform grid
    right_border = L2
    fig, ax = plt.subplots(figsize=(8, 8))
    x_min, y_min, x_max, y_max = left_border - 1, left_border - 1, right_border + 1, right_border + 1
    ax.set_xlim([x_min, x_max])
    ax.set_ylim([y_min, y_max])
    rect1 = Rectangle([left_border, left_border], 2*right_border, 2*right_border, fill=False, color='g',
                      linewidth=2.0)
    if a>0:
        X_uni, Y_uni, X1_uni, Y1_uni = uniform_grid(a, b, d, 100000)
        ax.scatter(X_uni, Y_uni)
    ax.add_patch(rect1)
    ax.axes.set_aspect('equal')
    for i in range(len(area_points.get_points('xleft'))):  # Plot rectangles, which compose workspace area
        rect1 = Rectangle([area_points.get_points('xleft')[i], area_points.get_points('yleft')[i]],
                          area_points.get_points('xright')[i] - area_points.get_points('xleft')[i],
                          area_points.get_points('yright')[i] - area_points.get_points('yleft')[i],
                          fill=True, fc='red', color='g', linewidth=1.0, alpha=0.5)
        ax.add_patch(rect1)
    for i in range(
            len(border_points.get_points('xleft'))):  # Plot rectangles, which compose the border of workspace area
        rect2 = Rectangle([border_points.get_points('xleft')[i], border_points.get_points('yleft')[i]],
                          border_points.get_points('xright')[i] - border_points.get_points('xleft')[i],
                          border_points.get_points('yright')[i] - border_points.get_points('yleft')[i],
                          fill=True, fc='black', color='yellow', linewidth=1.0, alpha=0.5)
        ax.add_patch(rect2)
    plt.show()
