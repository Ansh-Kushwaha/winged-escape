import pygame, time
from settings import *
from random import choice, randint

class BG(pygame.sprite.Sprite):
    def __init__(self, group, scale_factor, bg):
        super().__init__(group)
        self.bg = bg

        # background switch control
        # self.bg_time = 0
        self.bg_index = 0
        self.bg_image = bg[self.bg_index]

        full_width = self.bg_image.get_width() * scale_factor
        full_height = self.bg_image.get_height() * scale_factor
        full_sized_image = pygame.transform.scale(self.bg_image, (full_width, full_height))

        self.image = pygame.Surface((full_width * 3, full_height))
        self.image.blit(full_sized_image, (0, 0))
        self.image.blit(full_sized_image, (full_width, 0))

        self.rect = self.image.get_rect(topleft=(0, 0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, delT):
        self.pos.x -= 60 * delT
        # looping
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)


class Ground(pygame.sprite.Sprite):
    def __init__(self, group, scale_factor):
        super().__init__(group)

        # image
        ground = pygame.image.load('../graphics/environment/ground.png').convert_alpha()
        self.image = pygame.transform.scale(ground, pygame.math.Vector2(ground.get_size()) * scale_factor)

        # position
        self.rect = self.image.get_rect(bottomleft=(0, WINDOW_HEIGHT))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, delT):
        self.pos.x -= 160 * delT
        #looping
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)

class Birdy(pygame.sprite.Sprite):
    def __init__(self, group, scale_factor):
        super().__init__(group)

        # image
        self.import_frames(scale_factor)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        # position
        self.rect = self.image.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # movement
        self.g = 10
        self.direction = 0

    def import_frames(self, scale_factor):
        self.frames = []
        for i in range(3):
            # print(f'../graphics/plane/red{i}.png')
            frame = pygame.image.load(f'../graphics/birds/red/r{i}.png').convert_alpha()
            scaled_frame = pygame.transform.scale(frame, pygame.Vector2(frame.get_size()) * scale_factor)
            self.frames.append(scaled_frame)
            
    def gravity(self, delT):
        self.direction += self.g * delT
        self.pos.y += self.direction
        self.rect.y = round(self.pos.y)

    def accelerate(self):
        self.direction = -4

    def animate(self, delT):
        self.frame_index += 5 * delT
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

    def rotate(self):
        rotated_birdy = pygame.transform.rotozoom(self.image, -self.direction * 8, 1)
        self.image = rotated_birdy

    def update(self, delT):
        self.gravity(delT)
        self.animate(delT)
        self.rotate()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, group, scale_factor):
        super().__init__(group)

        single_obstacle = pygame.image.load(f'../graphics/obstacles/o{choice((1, 2))}.png').convert_alpha()
        self.gap = randint(120, 180)

        obs_height = single_obstacle.get_height() * scale_factor
        obs_width = single_obstacle.get_width() * scale_factor

        scaled_obstacle = pygame.transform.scale(single_obstacle, (obs_width, obs_height))
        flipped_obstacle = pygame.transform.flip(scaled_obstacle, True, True)

        # 

        # image
        self.image = pygame.Surface((obs_width, obs_height * 2 + self.gap), pygame.SRCALPHA)
        self.image.blit(flipped_obstacle, (0, 0))
        self.image.blit(scaled_obstacle, (0, obs_height + self.gap))

        x = WINDOW_WIDTH + randint(30, 70)
        y = WINDOW_HEIGHT + randint(40, 200)
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.pos = pygame.math.Vector2(self.rect.topleft)
            
    def update(self, delT):
        self.pos.x -= 320 * delT # 320 or 160
        self.rect.x = round(self.pos.x)

        # kill
        if self.rect.right <= -40:
            self.kill()
            print('killed')