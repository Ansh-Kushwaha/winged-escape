import pygame
from settings import *

class BG(pygame.sprite.Sprite):
    def __init__(self, group, scale_factor):
        super().__init__(group)
        bg_image = pygame.image.load('../graphics/environment/background.png').convert()

        new_width = bg_image.get_width() * scale_factor
        new_height = bg_image.get_height() * scale_factor
        full_sized_image = pygame.transform.scale(bg_image, (new_width, new_height))

        self.image = pygame.Surface((new_width * 2, new_height))
        self.image.blit(full_sized_image, (0, 0))
        self.image.blit(full_sized_image, (new_width, 0))

        self.rect = self.image.get_rect(topleft = (0, 0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, delT):
        self.pos.x -= 280 * delT
        # looping
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)

class Ground(pygame.sprite.Sprite):
    def __init(self, group, scale_factor):
        super.__init__(group)