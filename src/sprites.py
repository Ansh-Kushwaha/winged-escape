import pygame, time
from settings import *
from random import choice, randint

class BG(pygame.sprite.Sprite):
    def __init__(self, group, scale_factor, bg):
        super().__init__(group)
        self.bg_image = bg

        full_width = self.bg_image.get_width() * scale_factor
        full_height = self.bg_image.get_height() * scale_factor
        full_sized_image = pygame.transform.scale(self.bg_image, (full_width, full_height))

        self.image = pygame.Surface((full_width * 2, full_height))
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

        # mask
        self.mask = pygame.mask.from_surface(self.image)

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

        # mask
        self.mask = pygame.mask.from_surface(self.image)

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
        self.direction = -4

    def animate(self, delT):
        self.frame_index += 5 * delT
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

    def rotate(self):
        rotated_birdy = pygame.transform.rotozoom(self.image, -self.direction * 8, 1)
        self.image = rotated_birdy
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, delT):
        self.gravity(delT)
        self.animate(delT)
        self.rotate()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, group, scale_factor, flipped, x, y, idx):
        super().__init__(group)
        self.pipe_gap = 100

        pipe = pygame.image.load(f'../graphics/pipes/o{idx}.png').convert_alpha()

        # image
        self.image = pygame.transform.scale(pipe, pygame.math.Vector2(pipe.get_size()) * scale_factor)
        if flipped:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(midbottom=(x, 0 + y + self.pipe_gap))
            self.pos = pygame.math.Vector2(self.rect.topleft)
        else:
            self.rect = self.image.get_rect(midbottom=(x, WINDOW_HEIGHT + y))
            self.pos = pygame.math.Vector2(self.rect.topleft)
        
        # mask
        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self, delT):
        self.pos.x -= 320 * delT # 320 or 160
        self.rect.x = round(self.pos.x)

        # kill
        if self.rect.right <= -40:
            self.kill()

