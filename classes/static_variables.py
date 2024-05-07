import pygame
pygame.init()
font = pygame.font.Font(None, 24)  # None means default system font, 12 is the font size
WIDTH, HEIGHT  = 1000, 600
FPS = 100
PLAYER_VEL = 15
MESSAGE_BOX_WIDTH = 300
MESSAGE_BOX_HEIGHT = 100
MESSAGE_BOX_COLOR = (200, 200, 200)
BUTTON_WIDTH = 80
BUTTON_HEIGHT = 30
BUTTON_COLOR = (100, 100, 100)
BUTTON_TEXT_COLOR = (255, 255, 255)

block_size = 96

'''
background_type = "Green.png"

block_image_location = [0,126]


enemy_name = "MaskDude"

enemies_position = [(1.25,1),(-13,18),(-14,18),(-20,18),
                        (-21,18),(-24,18),(-25,18),(-26,18)]

floor_position = [(1,-3,0,3),(13,1,0,1),(18,-3,0,-1),
                      (23,-3,0,-2),(23,-2,2,-1)]

block_columns_positions = [(3,1,4),(7,2,5),(11,0,3),(13,-1,2),(17,2,5),
                               (19,-2,1),(23,-3,0),(29,-4,-1),(-3,1,4),(-7,2,5),
                               (-11,0,3),(-13,-1,2),(-17,2,5),(-19,-2,1),
                               (-23,-3,0),(-29,-4,-1)]

float_blocks_positions = [(7,11),(0,2),(4,3),(6,7),(9,9),(1,6),(11,14),
                              (7,17),(-7,11),(-4,3),(-6,7),(-9,9),(-1,6),(-11,14),
                              (-7,17),(-12,19),(-18,19),(-32,19),(-24,19),(7,19),
                              (-21,21),(-22,24),(-32,24),(-19,24),(-12,24)]

fruits_positions = [(40,3,"Apple"),
                        (-40,3,"Bananas"),
                        (block_size * -7,12,"Cherries"),
                        (WIDTH * -2  - block_size * 8,25,"Kiwi"),
                        (WIDTH * -2  - block_size * 5,25,"Melon"),
                        (WIDTH * -2  - block_size * 2,25,"Orange"),
                        (WIDTH * -2  + block_size * 3,25,"Pineapple"),
                        (WIDTH * -2  + block_size * 5,25,"Strawberry"),
                        (WIDTH * -2  + block_size * 7,25,"Melon")]

saws_positions = [(-90, HEIGHT - block_size  - 80),
                  (floor_position[0][1], floor_position[0][0] - block_size + 8)]

end_checkpoint_positions = [block_size * float_blocks_positions[-1][0], HEIGHT - block_size * float_blocks_positions[-1][1]]
'''