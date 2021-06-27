from python_tsp.exact import solve_tsp_dynamic_programming
import math

def get_distance_matrix_from_points(points):
    dist = lambda p1, p2: math.sqrt(((p1-p2)**2).sum())
    dist = points[0][0]-points[0][0]
    distance_matrix = [[dist(p1, p2) for p2 in points] for p1 in points]
    return distance_matrix

def solve(points):
    distance_matrix = get_distance_matrix_from_points(points)
    permutation, distance = solve_tsp_dynamic_programming(distance_matrix)

    return permutation, distance

print(get_distance_matrix_from_points([(1,1), (2,2), (3,3)]))
