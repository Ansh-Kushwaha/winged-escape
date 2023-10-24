import pygame, sys, time
from settings import *
from sprites import BG

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Winged Escape')

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # scaling
        bg_height = pygame.image.load('../graphics/environment/background.png').get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height

        # sprite setup
        BG(self.all_sprites, self.scale_factor)
    
    def run(self):
        st_time = time.time()
        # game loop
        while True:
            delT = time.time() - st_time
            st_time = time.time()

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.exit()
                    sys.exit()
            
            # game logic
            self.display_surface.fill('white')
            self.all_sprites.update(delT)
            self.all_sprites.draw(self.display_surface)

            pygame.display.update()
            self.clock.tick(FRAMERATE)



if __name__ == '__main__':
    game = Game()
    game.run()