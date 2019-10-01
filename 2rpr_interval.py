import numpy as np
from mpmath import iv
import interval as ival
from check_box import check_box
from plot_workspace_area import plot_workspace
from box_class import BoxPoints

d = 6
L1 = 3  # Lower range of row
L2 = 15  # Upper range of row
N = 50  # The number of nodes on uniform grid
l1 = -L2  # Left and lower border of uniform grid
l2 = L2  # Right and upper border of uniform grid
X1 = np.linspace(l1, l2, N)
Y1 = np.linspace(l1, l2, N)
X, Y = np.meshgrid(X1, Y1)  # Build X and Y of uniform grid
e = 10  # Max number of iterations
area_points = BoxPoints()
border_points = BoxPoints()
area_points, border_points = check_box(X, Y, N, L1, L2, d, e) # Calculate workspace area and border coordinates
plot_workspace(L1, L2, d, area_points, border_points)  # Plotting

"""
### Алгоритм с усилением

area_points_X_l = []
area_points_X_r = []
area_points_Y_l = []
area_points_Y_r = []
border_points_X_l = []
border_points_X_r = []
border_points_Y_l = []
border_points_Y_r = []
for i in range(N-1):
      for j in range(N-1):
        u1 = ival.Interval([X[i, j], X[i, j + 1]])
        u2 = ival.Interval([Y[i, j], Y[i + 1, j]])
        if check_Box_no_Kr(u1, u2) == 0:
          area_points_X_l.append(X[i, j])
          area_points_X_r.append(X[i, j + 1])
          area_points_Y_l.append(Y[i, j])
          area_points_Y_r.append(Y[i+1, j])
        if check_Box(u1, u2) == 0:
          area_points_X_l.append(X[i, j])
          area_points_X_r.append(X[i, j + 1])
          area_points_Y_l.append(Y[i, j])
          area_points_Y_r.append(Y[i+1, j])
        elif check_Box(u1, u2) == 1:
          border_points_X_l.append(X[i, j])
          border_points_X_r.append(X[i, j + 1])
          border_points_Y_l.append(Y[i, j])
          border_points_Y_r.append(Y[i+1, j])
draw_and_compute(L1, L1, L2, L2, d, l1, l2)

### Алгоритм с рекурсивным делением области равномерной сетки

area_points_X_l = []
area_points_X_r = []
area_points_Y_l = []
area_points_Y_r = []
border_points_X_l = []
border_points_X_r = []
border_points_Y_l = []
border_points_Y_r = []

l1 = -L2
l2 = L2
L1x = L1
L1y = L1
L2x = L2
L2y = L2
stop = (l2 - l1)/N# фиксируем длину сторону квадрата u как флаг для остановки
check_Box_branch_and_bounce(L1x, L2x, L1y, L2y)
draw_and_compute(L1, L1, L2, L2, d, l1, l2)
"""