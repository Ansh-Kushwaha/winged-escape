import pygame
from settings import *

class BG(pygame.sprite.Sprite):
    def __init__(self, group, scale_factor):
        super().__init__(group)
        bg_image = pygame.image.load('../graphics/environment/background.png').convert()

        new_width = bg_image.get_width() * scale_factor
        new_height = bg_image.get_height() * scale_factor

        self.image = pygame.transform.scale(bg_image, (new_width, new_height))
        self.rect = self.image.get_rect(topleft = (0, 0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, delT):
        self.pos.x -= 280 * delT

        if self.rect.right <= 0:
            self.pos.x = 0

        self.rect.x = round(self.pos.x)