import sys
sys.path.insert(0, '.')  # Add the parent directory to the path
from os import listdir
from os.path import isfile, join
#Import all custom classes, functions and variables
from .prep_functions import *
from .enemy import Enemy
from .fruits import Fruits
from .traps import Saw, Fire
from .blocks import *
from .static_variables import block_size

def multiple_enemies(position_list,enemy_name):
    return [Enemy(block_size * i[0],HEIGHT - block_size*i[1] - 64,50,50,name = enemy_name) for i in position_list]

def create_floor(y,x_start,x_pad,x_end,block_image_pos):
    #Create a single horizontal array of blocks
    return [Block(i * block_size,
                  HEIGHT - block_size * y, 
                  block_size,block_image_pos) for i in range((WIDTH * x_start + x_pad *  block_size)// block_size, WIDTH * x_end // block_size)]

def multiple_floors(position_list,block_image_pos):
    floors = [create_floor(position[0],position[1],position[2],position[3],block_image_pos) for position in position_list] 
    return [floor for sublist in floors for floor in sublist]

def create_column(x,y_start,y_end,block_image_pos):
    #Create a single vertical array of blocks
    return [Block(block_size * x,i * block_size, block_size,block_image_pos) for i in range(y_start,y_end)]

def multiple_columns(position_list,block_image_pos):    
    block_columns = [create_column(position[0],position[1],position[2],block_image_pos) for position in position_list]
    return [block for sublist in block_columns for block in sublist]

def create_float_blocks(position_list,block_image_pos):
    return [Block(block_size * position[0], HEIGHT - block_size * position[1], block_size,block_image_pos) for position in position_list]

def create_fires(position_list,start_float_block,end_float_block,step):
    #Fire position not to stuck the fire in the middle of the floating blocks
    fire_position_adjusted = 16 + block_size//2
    return [Fire(block_size * position_list[i][0] + fire_position_adjusted,HEIGHT - block_size * position_list[i][1] - fire_position_adjusted, 16, 32) for i in range(start_float_block,end_float_block,step)]

def create_saws(position_list):
    return [Saw(position[0], position[1], 38, 38) for position in position_list]

def create_fruits(position_list):
    return [Fruits(position[0], HEIGHT - block_size * position[1], 28, 38,position[2]) for position in position_list] 

def create_end_checkpoints(position_list):
    return EndCheckPoint(position_list[0], position_list[1] - block_size - 24, 64,64)

if __name__ == "__main__":
    create_floor()
    multiple_floors()
    create_column()
    multiple_columns()    
    create_float_blocks()
    create_fires()
    create_fruits()
