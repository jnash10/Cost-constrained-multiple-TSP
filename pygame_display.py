import pygame, random

# region pygame initialisation

def window_constants_init():
    global window_width, window_height, window_center, half_window_width, half_window_height
    window_width, window_height = window_size
    window_center = window_width // 2, window_height // 2
    half_window_width = window_width // 2
    half_window_height = window_height // 2

CAPTION = "Simulation"

window_size = (800, 800)
window_constants_init()

def pygame_init():
    global window_surface, clock, FPS_LIMIT, FONT
    pygame.init()
    window_surface = pygame.display.set_mode(window_size)  
    pygame.display.set_caption(CAPTION)
    clock = pygame.time.Clock()
    FPS_LIMIT = 60

    FONT = pygame.font.Font(None, 30)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 127, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
INDIGO = (75, 0, 130)
VIOLET = (148, 0, 211)
# endregion

# region sprites

sprites_to_blit = pygame.sprite.Group()

class FPS_label(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def update(self):
        self.image = FONT.render(str(int(clock.get_fps())), True, WHITE)
        self.rect = self.image.get_rect(bottomright = window_size)

sprites_to_blit.add(FPS_label())

node_size = 15

class Node(pygame.sprite.Sprite):

    def __init__(self, node_position, node_color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((node_size, node_size))
        pygame.draw.circle(self.image, node_color, (node_size//2, node_size//2), node_size//2)
        self.position = node_position
        self.rect = self.image.get_rect(center = self.position)

    def change_color(self, node_color):
        pygame.draw.circle(self.image, node_color, (node_size//2, node_size//2), node_size//2)

lines_to_blit = []  # Add (line_start, line_stop, line_color) tuples here

def add_to_lines_to_blit(line_start, line_stop, line_color = WHITE):
    lines_to_blit.append((line_start, line_stop, line_color))

def remove_lines_to_blit():
    lines_to_blit = []

def draw_lines():
    for line_start, line_stop, line_color in lines_to_blit:
        pygame.draw.line(window_surface, line_color, line_start, line_stop)

# endregion

# region mainloop

update_required = True

def window_loop_iteration():
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            pygame.quit()
            quit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                pygame.quit()
                quit()
    
    if update_required:
        window_surface.fill(BLACK)
        sprites_to_blit.update()
        sprites_to_blit.draw(window_surface)
        draw_lines()
        pygame.display.update()

    # Comment out below code if actual algorithm appears slow since we dont want to limit the speed of MTSP algorithm.
    # The below line ensures FPS_LIMIT(current value of 60) iterations per second.
    clock.tick(FPS_LIMIT)  

# endregion
