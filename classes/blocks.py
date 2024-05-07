from classes.object import Object
import pygame
from classes.prep_functions import get_block, load_sprite_sheets
from classes.static_variables import WIDTH, HEIGHT

class Block(Object):
    def __init__(self, x, y, size, block_image_pos):
        super().__init__(x, y,size, size)
        block = get_block(size, block_image_pos)
        self.image.blit(block, (0,0))
        self.mask = pygame.mask.from_surface(self.image) 

class EndCheckPoint(Object):
    def __init__(self,x,y,width,height):
        super().__init__(x,y,width,height,"End")
        self.endpoint = load_sprite_sheets("Items","Checkpoints\End",width,height)
        self.image = self.endpoint["End (Idle)"][0]
        self.mask = pygame.mask.from_surface(self.image)

if __name__ == "__main__":
    Block(Object)
    EndCheckPoint(Object)