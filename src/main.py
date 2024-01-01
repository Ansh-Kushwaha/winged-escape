import pygame, sys, time
from settings import *
from sprites import BG, Ground, Birdy, Pipe
from random import choice, randint

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Winged Escape')

        # text
        self.font = pygame.font.Font("../graphics/font/numbers_font.ttf", 40)

        # score
        self.score = 0
        self.best = -1
        
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
        self.pipes = pygame.sprite.Group()

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
        self.pipe_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.pipe_timer, 750)

    def collisions(self):
        if pygame.sprite.spritecollide(self.bird, self.collision_sprites, False):
            pygame.quit()
            sys.exit()

    def calculate_score(self):
        for pipe in self.pipes:
            if pipe.type == 'bottom' and pipe.pos.x < self.bird.pos.x - self.bird.image.get_size()[0]:
                if not pipe.scored:
                    pipe.scored = True
                    self.score += 1

    def display_score(self):
        score_surf = self.font.render(str(self.score), True, 'Black' if self.scene == 0 else 'White')
        score_rect = score_surf.get_rect(midtop=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 10))
        self.display_surface.blit(score_surf, score_rect)
        
    
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
                if event.type == self.pipe_timer:
                    x = WINDOW_WIDTH + randint(30, 70)
                    y = randint(-50, 40) # random increase or decrease
                    Pipe([self.pipes, self.all_sprites, self.collision_sprites], self.scale_factor, False, x, y, self.scene)
                    Pipe([self.pipes, self.all_sprites, self.collision_sprites], self.scale_factor, True, x, y, self.scene)
            
            # game logic
            self.display_surface.fill('white')
            self.all_sprites.update(delT)
            self.collisions()

            # score calculation
            self.calculate_score()

            self.all_sprites.draw(self.display_surface)
            self.display_score()
            pygame.display.update()
            self.clock.tick(FRAMERATE)



if __name__ == '__main__':
    game = Game()
    game.run()