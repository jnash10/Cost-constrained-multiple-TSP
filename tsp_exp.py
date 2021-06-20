import numpy as np

import matplotlib.pyplot as plt

from python_tsp.exact import solve_tsp_dynamic_programming

distance_matrix = np.array([[ 0, 51, 27, 26, 25, 42, 20, 51, 20, 42],
 [51,  0, 24, 31, 41, 21, 34,  0, 58, 31],
 [27, 24,  0, 13, 23, 20, 13, 24, 36, 26],
 [26, 31, 13,  0, 33, 33,  5, 31, 41, 39],
 [25, 41, 23, 33,  0, 23, 29, 41, 18, 19],
 [42, 21, 20, 33, 23,  0, 33, 21, 41, 10],
 [20, 34, 13,  5, 29, 33,  0, 34, 36, 38],
 [51,  0, 24, 31, 41, 21, 34,  0, 58, 31],
 [20, 58, 36, 41, 18, 41, 36, 58,  0, 37],
 [42, 31, 26, 39, 19, 10, 38, 31, 37,  0]]
)

coords = [(0, 24), (45, 49), (24, 37), (14, 46), (23, 14), (42, 28), (11, 41), (45, 49), (7, 5), (42, 18)]


permutation, distance = solve_tsp_dynamic_programming(distance_matrix)

print(distance)
print(permutation)
per_x = []
per_y = [] 
per = []

for point in permutation:
    per_x.append(coords[point][0])
    per_y.append(coords[point][1])
    per.append(coords[point])

plt.scatter(per_x,per_y)
plt.plot(per_x, per_y)
title = str("length of route is "+ str(distance))
plt.title(title)
plt.show()