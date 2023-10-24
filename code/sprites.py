import pygame, time
from settings import *

class BG(pygame.sprite.Sprite):
    def __init__(self, group, scale_factor, bg):
        super().__init__(group)
        bg_image = bg[0]

        # background switch control

        full_width = bg_image.get_width() * scale_factor
        full_height = bg_image.get_height() * scale_factor
        full_sized_image = pygame.transform.scale(bg_image, (full_width, full_height))

        self.image = pygame.Surface((full_width * 3, full_height))
        self.image.blit(full_sized_image, (0, 0))
        self.image.blit(full_sized_image, (full_width, 0))

        self.rect = self.image.get_rect(topleft=(0, 0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, delT):
        self.pos.x -= 240 * delT
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
        self.pos.x -= 360 * delT
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
        self.rect = self.image.get_rect(midleft=(WINDOW_WIDTH / 20, WINDOW_HEIGHT / 2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # movement
        self.g = 10
        self.direction = 0

    def import_frames(self, scale_factor):
        self.frames = []
        for i in range(3):
            # print(f'../graphics/plane/red{i}.png')
            frame = pygame.image.load(f'../graphics/birds/yellow/y{i}.png').convert_alpha()
            scaled_frame = pygame.transform.scale(frame, pygame.Vector2(frame.get_size()) * scale_factor)
            self.frames.append(scaled_frame)
            
    def gravity(self, delT):
        self.direction += self.g * delT
        self.pos.y += self.direction
        self.rect.y = round(self.pos.y)

    def accelerate(self):
        self.direction = -6

    def update(self, delT):
        self.gravity(delT)
        # self.animate(delT)
        # self.rotate(delT)
