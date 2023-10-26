import pygame, sys, time
from settings import *
from sprites import BG, Ground, Birdy, Obstacle
from random import choice

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Winged Escape')

        # icon
        icon = pygame.image.load('../graphics/icons/icon.png')
        pygame.display.set_icon(icon)

        # backgrounds
        bg = []
        bg.append(pygame.image.load('../graphics/environment/background_day.png').convert())
        bg.append(pygame.image.load('../graphics/environment/background_night.png').convert())

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # scaling
        bg_height = bg[0].get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height

        # day or night
        self.scene = choice((0, 1))

        # sprite setup
        BG(self.all_sprites, self.scale_factor, bg[self.scene])
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
        self.bird = Birdy(self.all_sprites, self.scale_factor * 1.2)

        # event time
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 750)

    def collisions(self):
        if pygame.sprite.spritecollide(self.bird, self.collision_sprites, False):
            pygame.quit()
            sys.exit()
    
    def run(self):
        st_time = time.time()
        # game loop
        while True:
            delT = time.time() - st_time
            st_time = time.time()

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                    self.bird.accelerate()
                if event.type == self.obstacle_timer:
                    Obstacle([self.all_sprites, self.collision_sprites], self.scale_factor, self.scene)
            
            # game logic
            self.display_surface.fill('white')
            self.all_sprites.update(delT)
            self.collisions()
            self.all_sprites.draw(self.display_surface)

            pygame.display.update()
            self.clock.tick(FRAMERATE)



if __name__ == '__main__':
    game = Game()
    game.run()