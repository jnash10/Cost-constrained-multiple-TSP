from random import randint
import numpy as np

from pygame_display import *

window_size = (800, 800)

pygame_init()

# Yanked code from case_generator.py, with slight modifictaions
# Namely, the first city position is at the center.
# Also, I've made the code more compact, renamed variables and
# made it return only the position of cities
# And it used window_size as the bounding box for generation of nodes
# Oh, and Agam needs to learn PEP-8
def case_gen(number_of_nodes):
    cities_positions = []

    cities_positions.append((window_size[0]//2, window_size[1]//2))
    number_of_nodes = number_of_nodes - 1

    for i in range(0, number_of_nodes) :
        # Resistricting locations by node_size//2 to ensure all nodes are inside the window
        cities_positions.append((randint(node_size//2, window_size[0] - node_size//2),randint(node_size//2, window_size[1] - node_size//2)))

    return cities_positions

number_of_nodes = 17
cities_positions = case_gen(number_of_nodes)
print(cities_positions)

nodes = []
nodes.append(Node(cities_positions[0], WHITE))
for city_position in cities_positions[1:]:
    nodes.append(Node(city_position, RED))

sprites_to_blit.add(nodes)

# TODO - Get the actual algorithm working

while True:
    window_loop_iteration()
