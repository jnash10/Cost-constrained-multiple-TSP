import numpy as np

import matplotlib.pyplot as plt

from python_tsp.exact import solve_tsp_dynamic_programming

def tsp_solver(coords, distance_matrix):
    distance_matrix[:, 0]=0


    permutation, distance = solve_tsp_dynamic_programming(distance_matrix)

    #print(distance)
    #print(permutation)
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

    return distance