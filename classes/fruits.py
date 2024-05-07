import sys
sys.path.insert(0, '.')  # Add the parent directory to the path
from .object import Object
import pygame
from .prep_functions import load_sprite_sheets
from .static_variables import WIDTH, HEIGHT

class Fruits(Object):
    def __init__(self, x, y, width, height, fruit_name):
        super().__init__(x, y, width, height, fruit_name)
        self.sprites = load_sprite_sheets("Items", "Fruits", width, height, False)
        self.name = fruit_name
        self.mask = pygame.mask.from_surface(self.sprites[self.name][0])
        #self.mask = None
        self.collected = False

    def collect(self):
        self.name = "Collected"
        self.update()

    def update(self):
        self.rect = self.sprites[self.name][0].get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprites[self.name][0])

    def draw(self, win, offset_x, offset_y):
        win.blit(self.sprites[self.name][0], (self.rect.x - offset_x, self.rect.y - offset_y))

if __name__ == "__main__":
    Fruits(Object)