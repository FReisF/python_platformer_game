import sys
sys.path.insert(0, '.')  # Add the parent directory to the path
from .static_variables import *

phase_before = 'phase_3.py'  # Update if starting from a different phase
phase_after = 'phase_5.py'  # Update if there's a subsequent phase

# Customize the following variables for your new phase:

background_type = "Blue.png"  # Change background image

block_image_location = [0, 126]  # Modify block appearance if needed

enemy_name = "PinkMan"  # Introduce a new enemy type

enemies_position = [(5, 1), (15, 5), (-10, 10)]  # Adjust enemy placements

floor_position = [(1, -3, 0, 5), (7, 2, 0, 3)]  # Modify floor layout

block_columns_positions = [(3, 1, 4), (10, 3, 6)]  # Adjust column placements

float_blocks_positions = [(5, 8), (8, 12), (-5, 6)]  # Modify floating block positions

fruits_positions = [(20, 3, "Apple"), (-20, 7, "Bananas")]  # Change fruit types and locations

saws_positions = [(10, HEIGHT - block_size - 80)]  # Adjust saw placements

end_checkpoint_positions = [block_size * float_blocks_positions[-1][0], HEIGHT - block_size * float_blocks_positions[-1][1]] 