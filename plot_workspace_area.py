import shapely.geometry as sg
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

def plot_workspace(l1, l2, d, points_area, points_border):
    left_border = -l2
    right_border = l2
    Ax=[]
    Ay=[]
    if (l1<l2):
        l1+=1e-10
        fig, ax = plt.subplots(figsize=(8, 8))
        x_min, y_min, x_max, y_max = left_border - 1, left_border - 1, right_border + 1, right_border + 1
        ax.set_xlim([x_min, x_max])
        ax.set_ylim([y_min, y_max])
        a = sg.Point(0,0).buffer(l1)# circles init with shpaely
        b = sg.Point(0,0).buffer(l2)
        c = sg.Point(d,0).buffer(l1)
        e = sg.Point(d,0).buffer(l2)
        ab=b.difference(a)# plot ring from l1 and l2
        cd=e.difference(c)
        middle = ab.intersection(cd)
        circle1 = Circle((0, 0), radius=l1_l, fill=False, color='r')# circles init with matplotlib
        circle2 = Circle((0, 0), radius=l1_h, fill=False, color='r')
        circle3 = Circle((d, 0), radius=l2_l, fill=False, color='b')
        circle4 = Circle((d, 0), radius=l2_h, fill=False, color='b')
        rect1=Rectangle([left_border, left_border], abs(left_border) + abs(right_border), abs(left_border) + abs(right_border), fill=False, color='g', linewidth=2.0)
        ax.add_patch(descartes.PolygonPatch(middle, fc='b', ec='k', alpha=0.2))# adding patches to plot
        ax.add_patch(circle1)
        ax.add_patch(circle2)
        ax.add_patch(circle3)
        ax.add_patch(circle4)
        ax.add_patch(rect1)
       # ax.grid()
        ax.axes.set_aspect('equal')
        for i in range(len(area_points_X_l)):
            rect1 = Rectangle([area_points_X_l[i], area_points_Y_l[i]], area_points_X_r[i] - area_points_X_l[i],
                            area_points_Y_r[i] - area_points_Y_l[i], fill=True, fc='red', color='g', linewidth=1.0, alpha=0.5)
            ax.add_patch(rect1)
        for i in range(len(border_points_X_l)):
            rect2 = Rectangle([border_points_X_l[i], border_points_Y_l[i]], border_points_X_r[i] - border_points_X_l[i],
                            border_points_Y_r[i] - border_points_Y_l[i], fill=True, fc='black', color='yellow', linewidth=1.0, alpha=0.5)
            ax.add_patch(rect2)
    else:
        print('Wrong data')