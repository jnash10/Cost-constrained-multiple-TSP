#given a time constraint T and a set of cities. solve for min no. of trucks required while satisfying constraint


from tsp import tsp_solver
from case_generator import case_gen
import time

coords, distance_matrix = case_gen()
start_time = time.time()

distance = tsp_solver(coords, distance_matrix)

print(distance)

print(time.time()-start_time)

