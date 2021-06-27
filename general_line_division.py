import random, math, typing
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

# TODO - Check if this square distance function works
# We are using square of distance to reduce computational requirements
def get_square_of_distance_between_points(point1, point2):
    return (point1[0]-point2[0]) ** 2 + (point1[1]-point2[1]) ** 2

class Place(Node):
    place_color = GREY

    def __init__(self, place_position):
        super().__init__(place_position, self.place_color)
        self.place_position = place_position
        sprites_to_blit.add(self)

        self.place_weight = None
        self.calculate_place_weight()

    def set_neighbouring_places(self, first_place_clockwise, first_place_anticlockwise):
        self.first_place_clockwise = first_place_clockwise
        self.first_place_anticlockwise = first_place_anticlockwise

    def calculate_place_weight(self):
        self.place_weight = get_square_of_distance_between_points(self.place_position, hub_position)

SECTOR_COLORS = [VIOLET, INDIGO, BLUE, GREEN, YELLOW, ORANGE, RED]

class Sector:
    
    def __init__(self, first_place: Place, last_place: Place):
        # First place -> Turn anticlockwise -> last place 
        self.first_place = first_place
        self.last_place = last_place

        self.places_in_sector = []  # From first place to last place
        self.init_places_in_sector()

        self.sector_color = SECTOR_COLORS.pop()
        self.color_places_in_sector()

        self.sector_weight = None
        self.calculate_sector_weight()

    def init_places_in_sector(self):
        next_place = self.first_place
        self.places_in_sector.append(next_place)
        while next_place != self.last_place:
            next_place = next_place.first_place_anticlockwise
            self.places_in_sector.append(next_place)

    def color_places_in_sector(self):
        for place in self.places_in_sector:
            place.change_color(self.sector_color)

    def calculate_sector_weight(self):
        # NOTE: When modifiying this function, also modify functions 'add_place' and 'remove_place'
        self.sector_weight = 0

        for place in self.places_in_sector:
            self.sector_weight += place.place_weight

    def add_place(self, place: Place):
        if place in self.places_in_sector:
            raise Exception("Place being added is already in this sector.")

        place_to_clockwise = place.first_place_clockwise
        place_to_anticlockwise = place.first_place_anticlockwise

        if place_to_anticlockwise == self.places_in_sector[0]:
            self.first_place = place
            self.places_in_sector.insert(0, place)

        elif place_to_clockwise  == self.places_in_sector[-1]:
            self.last_place = place
            self.places_in_sector.insert(len(self.places_in_sector), place)

        else:
            raise Exception("Place being added is not neighbouring a place on either end of self.places_in_sector")

        place.change_color(self.sector_color)
        
        self.sector_weight += place.place_weight
    
    def remove_place(self, place: Place):
        if place not in self.places_in_sector:
            raise Exception("Place being removed is not in this sector.")

        if place == self.places_in_sector[0]:
            self.places_in_sector.pop(0)
            self.first_place = self.places_in_sector[0]

        elif place == self.places_in_sector[-1]:
            self.places_in_sector.pop(-1)
            self.last_place = self.places_in_sector[-1]

        else:
            raise Exception("Place being removed is not in either end of self.places_in_sector")

        place.change_color(Place.place_color)

        self.sector_weight -= place.place_weight

class SortedQueue:

    def __init__(self):
        self.queue = []  # Smallest element has index 0
        self.length = 0

    def add_element(self, key, value):
        i = 0
        while i < self.length:
            if self.queue[i][1] > value:
                self.queue.insert(i, (key, value))
                break
            i += 1

        else:
            self.queue.append((key, value))
        
        self.length += 1

    def get_smallest_element(self):
        key, value = self.queue[0]
        return key, value

    def return_queue(self):
        return self.queue

    def return_keys(self):
        return list(map(lambda x: x[0], self.queue))

# TODO - See if origin_position works as intended.
def get_point_angle(point, origin_position):
    x, y = point

    #x -= half_window_width
    #y = half_window_height - y
    x -= origin_position[0]
    y = origin_position[1] - y

    point_angle = math.atan2(y, x)

    return point_angle

def get_points_sorted_by_angle_from_positive_x_axis(node_positions):
    origin_position = node_positions[0]

    points_sorted_by_angle_queue = SortedQueue()

    for point in node_positions[1:]:
        angle = get_point_angle(point, origin_position)
        points_sorted_by_angle_queue.add_element(point, angle)

    points_sorted_by_angle = points_sorted_by_angle_queue.return_keys()

    points_sorted_by_angle_index = []
    for point in points_sorted_by_angle:
        points_sorted_by_angle_index.append(node_positions.index(point))

    return points_sorted_by_angle_index

def set_neighbouring_places_for_nodes(places: typing.Iterable[Place], points_sorted_by_angle):
    number_of_nodes = len(places)

    for i, point in enumerate(points_sorted_by_angle):
        first_place_clockwise = places[points_sorted_by_angle[i-1]-1]  # Excluding hub since point considers hub as well
        if i+1 < number_of_nodes:
            first_place_anticlockwise = places[points_sorted_by_angle[i+1]-1]  # Excluding hub since point considers hub as well
        else:
            first_place_anticlockwise = places[points_sorted_by_angle[0]-1]  # Excluding hub since point considers hub as well
        places[point-1].set_neighbouring_places(first_place_clockwise, first_place_anticlockwise)  # Excluding hub since point considers hub as well

def initialise_sectors(places, points_sorted_by_angle_index, number_of_sectors, number_of_nodes):
    sectors = []

    number_of_places_per_sector = number_of_nodes // number_of_sectors

    place_index = 0  # refers to points_sorted_by_angle_index which doesn't include hub

    first_place_index = points_sorted_by_angle_index[place_index]
    place_index += number_of_places_per_sector
    while place_index < number_of_nodes:
        second_place_index = points_sorted_by_angle_index[place_index - 1]
        sectors.append(Sector(places[first_place_index-1], places[second_place_index-1]))
        first_place_index = points_sorted_by_angle_index[place_index]
        place_index += number_of_places_per_sector

    second_place_index = points_sorted_by_angle_index[-1]
    sectors.append(Sector(places[first_place_index-1], places[second_place_index-1]))

    return sectors

def move_place_between_sectors(place_being_moved, original_sector, final_sector):
    original_sector.remove_place(place_being_moved)
    final_sector.add_place(place_being_moved)

def switch_over_one_random_place():
    i = random.randint(1, number_of_sectors-1)
    move_place_between_sectors(sectors[i].first_place, sectors[i], sectors[i-1])

def initialise():
    global number_of_nodes, number_of_sectors, hub_position, sectors

    if DEBUG:
        number_of_nodes = 20
        number_of_sectors = 5
    else:
        number_of_nodes = int(input("Enter number of nodes to generate: "))
        number_of_sectors = int(input("Enter number of lines to draw: "))

    node_positions = generate_node_position(number_of_nodes)

    # 0 index node is the hub. This fact is also used in function get_points_sorted_by_angle_from_positive_x_axis
    hub_position = node_positions[0]
    hub = Hub(hub_position)

    places = []
    for place_position in node_positions[1:]:
        places.append(Place(place_position))

    points_sorted_by_angle_index = get_points_sorted_by_angle_from_positive_x_axis(node_positions)

    set_neighbouring_places_for_nodes(places, points_sorted_by_angle_index)

    sectors = initialise_sectors(places, points_sorted_by_angle_index, number_of_sectors, number_of_nodes)

    # Triggering function switch_over_one_random_place whenever return key is pressed
    # This function will move a random place on either end of a sector into the neighbouring sector
    custom_events_by_key_press[pygame.K_RETURN] = switch_over_one_random_place

# endregion

# region mainloop

pygame_init()

if __name__ == "__main__":

    initialise()

    while True:
        window_loop_iteration()

# endregion
