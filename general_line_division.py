import random
from pygame_display import *

# region constants

window_size = (800, 800)
window_constants_init()

DEBUG = True

# endregion

# region framework

def generate_node_position(number_of_nodes):
    nodes_positions = []

    # 0 index node is the hub
    nodes_positions.append(window_center)
    number_of_nodes = number_of_nodes - 1

    for i in range(0, number_of_nodes) :
        # Resistricting locations by node_size//2 to ensure all nodes are inside the window
        nodes_positions.append((random.randint(node_size//2, window_size[0] - node_size//2), random.randint(node_size//2, window_size[1] - node_size//2)))

    return nodes_positions

class Hub(Node):
    hub_color = WHITE
    def __init__(self, hub_position):
        super().__init__(hub_position, self.hub_color)

        sprites_to_blit.add(self)

class Place(Node):
    place_color = RED

    def __init__(self, place_position):
        super().__init__(place_position, self.place_color)

        sprites_to_blit.add(self)

    def set_neighbouring_places(self, first_place_clockwise, first_place_anticlockwise):
        self.first_place_clockwise = first_place_clockwise
        self.first_place_anticlockwise = first_place_anticlockwise

def initialise():
    if DEBUG:
        number_of_nodes = 50
        number_of_lines = 5
    else:
        number_of_nodes = int(input("Enter number of nodes to generate: "))
        number_of_lines = int(input("Enter number of lines to draw: "))

    node_positions = generate_node_position(number_of_nodes)

    # 0 index node is the hub
    hub_position = node_positions[0]
    hub = Hub(hub_position)

    places = []
    for place_position in node_positions[1:]:
        places.append(Place(place_position))

# endregion

# region mainloop

pygame_init()

if __name__ == "__main__":

    initialise()

    while True:
        window_loop_iteration()

# endregion
