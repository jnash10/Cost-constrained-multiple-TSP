import pygame, random

# region pygame initialisation

CAPTION = "Simulation"

window_size = (800, 800)
window_width, window_height = window_size
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
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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

# endregion

# region mainloop

def window_loop_iteration():
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            pygame.quit()
            quit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                pygame.quit()
                quit()
    
    window_surface.fill(BLACK)
    sprites_to_blit.update()
    sprites_to_blit.draw(window_surface)
    pygame.display.update()

    # Comment out below code if actual algorithm appears slow since we dont want to limit the speed of MTSP algorithm.
    # The below line ensures FPS_LIMIT(current value of 60) iterations per second.
    clock.tick(FPS_LIMIT)  

# endregion
