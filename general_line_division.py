from random import randint, seed
#seed("tes1t")
import math

from pygame.draw import line

from pygame_display import *

# In case we want to specify a different window size
window_size = (800, 800)
window_constants_init()

# Yanked code from case_generator.py, with slight modifictaions
# Namely, the first city position is at the center.
# Also, I've made the code more compact, renamed variables and
# made it return only the position of cities
# And it used window_size as the bounding box for generation of nodes
# Oh, and Agam needs to learn PEP-8
def case_gen(number_of_nodes):
    cities_positions = []

    cities_positions.append(window_center)
    number_of_nodes = number_of_nodes - 1

    for i in range(0, number_of_nodes) :
        # Resistricting locations by node_size//2 to ensure all nodes are inside the window
        cities_positions.append((randint(node_size//2, window_size[0] - node_size//2),randint(node_size//2, window_size[1] - node_size//2)))

    return cities_positions

number_of_nodes = 50
cities_positions = case_gen(number_of_nodes)
#print(cities_positions)

nodes = []
nodes.append(Node(cities_positions[0], WHITE))
for city_position in cities_positions[1:]:
    nodes.append(Node(city_position, RED))

sprites_to_blit.add(nodes)

# IMP - Here we assume all lines start from the center of the screen

"""
Below one function is not used anymore, but I'm leaving it here anyway in case I ever need it.
The line from the angle is:
y = ax + b
where slope a = tan(angle)
also, x, y = half_window_width, half_window_height is a solution to th equation

i.e half_window_height = a * half_window_width + b
i.e b = half_window_height - tan(angle) * half-half_window_width

distance of point x1, y1 from line y = ax + b, i.e ax - y + b = 0
d = a*x1 - y1 + b
"""
def get_comparitive_distance(point, angle):
    x1, y1 = point
    a = math.tan(angle)
    b = half_window_height - math.tan(angle) * half_window_width
    d = a * x1 - y1 + b
    return d

def get_point_angle(point):
    x, y = point
    x -= half_window_width
    y = half_window_height - y
    point_angle = math.atan2(y, x)

    return point_angle

"""
To get the angle between line and point, find the angle made by the point with the zero angle line using math.atan2(y, x)

This gives an angle between -pi/2 and pi/2 which is not enough information.

if x value of point is less than half_window_width increase angle by pi/2 

Then subtract that value from angle.
"""
def get_comparative_angle(point, angle):
    point_angle = get_point_angle(point)

    final_result = (angle - point_angle) % (2 * math.pi)

    if final_result > math.pi:
        final_result -= 2 * math.pi

    if final_result < -math.pi:
        final_result += 2 * math.pi
    
    #print(final_result)
    return final_result

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


def get_point_on_either_side_sorted_in_angle_difference(angle):
    sorted_points_clockwise = SortedQueue()
    sorted_points_anticlockwise = SortedQueue()
    #closest_point_positive_angle = (cities_positions[1], get_comparative_angle(cities_positions[1], angle))
    #closest_point_negative_angle = tuple(closest_point_positive_angle)

    for point in cities_positions[1:]:

        angle_from_ray = get_comparative_angle(point, angle)

        """rainbow:
        colour_index = abs(int(angle_from_ray * 7 / math.pi))
        colours = [VIOLET, INDIGO, BLUE, GREEN, YELLOW, ORANGE, RED]
        nodes[cities_positions.index(point)].change_color(colours[colour_index])
        """
        if angle_from_ray > 0:
            sorted_points_clockwise.add_element(point, angle_from_ray)

        elif angle_from_ray < 0:
            sorted_points_anticlockwise.add_element(point, -angle_from_ray)

        else:
            raise Exception("Need to handle when point is on line")

    return sorted_points_clockwise.return_queue(), sorted_points_anticlockwise.return_queue()

def draw_initial_lines(number_of_lines):
    global lines_angle, lines_points_clockwise_sorted, lines_points_anticlockwise_sorted
    lines_angle = []
    lines_points_clockwise_sorted = []
    lines_points_anticlockwise_sorted = []

    angle_shift = 2 * math.pi / number_of_lines
    current_angle = - math.pi
    line_start = window_center

    for line_index in range(number_of_lines):
        sorted_points_clockwise, sorted_points_anticlockwise = get_point_on_either_side_sorted_in_angle_difference(current_angle)
        
        lines_points_clockwise_sorted.append(sorted_points_clockwise)
        lines_points_anticlockwise_sorted.append(sorted_points_anticlockwise)

        first_point_clockwise = sorted_points_clockwise[0][0]
        first_point_anticlockwise = sorted_points_anticlockwise[0][0]

        # Color closest point blue
        nodes[cities_positions.index(first_point_clockwise)].change_color(BLUE)
        nodes[cities_positions.index(first_point_anticlockwise)].change_color(BLUE)

        first_point_clockwise_angle = get_point_angle(first_point_clockwise)
        first_point_anticlockwise_angle = get_point_angle(first_point_anticlockwise)

        #print(first_point_clockwise_angle, first_point_anticlockwise_angle)
        if first_point_clockwise_angle > 0 and first_point_anticlockwise_angle > 0:
            actual_line_angle = (first_point_clockwise_angle + first_point_anticlockwise_angle) / 2

        elif first_point_clockwise_angle < 0 and first_point_anticlockwise_angle < 0:
            actual_line_angle = (first_point_clockwise_angle + first_point_anticlockwise_angle) / 2

        elif abs(first_point_clockwise_angle) > math.pi / 2 and abs(first_point_anticlockwise_angle) > math.pi / 2:
            actual_line_angle = (first_point_clockwise_angle + first_point_anticlockwise_angle) / 2
            if actual_line_angle > 0:
                actual_line_angle += math.pi
            
            elif actual_line_angle <= 0:
                actual_line_angle -= math.pi

        else:
            actual_line_angle = (first_point_clockwise_angle + first_point_anticlockwise_angle) / 2
        
        lines_angle.append(actual_line_angle)

        x = half_window_width * (1 + math.cos(actual_line_angle))
        y = half_window_height * (1 - math.sin(actual_line_angle))
        line_stop = (x, y)
        add_to_lines_to_blit(line_start, line_stop, WHITE)
    
        current_angle += angle_shift        

# DONE - Find the first iteration of lines
# TODO - Find why the line doesn't appear in the middle of closest points when poins have different distances to the hub
# TODO - Iterate over possible line setups

if __name__ == "__main__":

    number_of_lines = int(input("Enter number of lines to draw: "))
    
    draw_initial_lines(number_of_lines)

    pygame_init()

    while True:
        window_loop_iteration()
