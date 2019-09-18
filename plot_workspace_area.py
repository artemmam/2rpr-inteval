import shapely.geometry as sg
import matplotlib.pyplot as plt
import descartes
from matplotlib.patches import Circle, Rectangle


def plot_workspace(l1, l2, d, points_area_x, points_area_y, points_border_x, points_border_y):
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
        for i in range(len(points_area_x[0])):  # Plot rectangles, which compose workspace area
            rect1 = Rectangle([points_area_x[0][i], points_area_y[0][i]],
                              points_area_x[1][i] - points_area_x[0][i],
                              points_area_y[1][i] - points_area_y[0][i],
                              fill=True, fc='red', color='g', linewidth=1.0, alpha=0.5)
            ax.add_patch(rect1)
        for i in range(len(points_border_x[0])):  # Plot rectangles, which compose the border of workspace area
            rect2 = Rectangle([points_border_x[0][i], points_border_y[0][i]],
                              points_border_x[1][i] - points_border_x[0][i],
                              points_border_x[1][i] - points_border_x[0][i],
                              fill=True, fc='black', color='yellow', linewidth=1.0, alpha=0.5)
            ax.add_patch(rect2)
        plt.show()
    else:
        print('Wrong data')
