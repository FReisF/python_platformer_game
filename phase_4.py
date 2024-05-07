import sys
sys.path.insert(0, '..')  # Add the parent directory to the path

from classes.prep_functions import *
from classes.create_functions import *
from classes.player import Player
from classes.static_variables import FPS
from classes.p4_variables import *
import pygame

pygame.init()
pygame.display.set_caption("Platformer")

window = pygame.display.set_mode((WIDTH,HEIGHT))

def main(window):
    #set clock for running pygame
    clock = pygame.time.Clock()
    
    #set background for the phase
    background, bg_image = get_background(background_type)
    
    #create player
    player  = Player(100, 100, 50, 50, phase_before, phase_after)

    #create enemies   
    enemies = multiple_enemies(enemies_position,enemy_name)

    #Create block floors
    floors = multiple_floors(floor_position,block_image_location)

    #create block columns
    block_columns = multiple_columns(block_columns_positions,block_image_location)
    
    #create floating blocks
    float_blocks = create_float_blocks(float_blocks_positions,block_image_location)
    
    #create fires
    fires = create_fires(float_blocks_positions,0,16,2)

    #create saws
    saws = create_saws(saws_positions) 

    #Create end point for the game
    end_point = create_end_checkpoints(end_checkpoint_positions)

    #Create the fruits
    fruits = create_fruits(fruits_positions)

    #Loop through the elements that have some sort of movement (can be on or off)
    for fire in fires:
        fire.on()
    for saw in saws:
        saw.on()

    #Collect all the elements to be shown on screen besides player and enemy
    objects = [*floors,*float_blocks,*fires,*block_columns,end_point,*saws,*fruits]
    
    #Select all elements but fruits as those ones do not have the same hit behavior
    objects_collide = objects[:-1]
    
    #Set the area for the camera effect 
    offset_x = 0
    offset_y = 0
    scroll_area_width = 200
    scroll_area_height = 200

    run = True
    while run:
        clock.tick(FPS)

        #Get keyboard strikes
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump() 

        #Call the loop on each object that has a loop and the respective behavior set on their classes
        player.loop(FPS)        
        for fire in fires:
            fire.loop()
        for saw in saws:
            saw.loop()    
        for enemy in enemies:
            enemy.loop(FPS)
            handle_move_enemy(enemy, objects_collide)
        
        handle_move(player, objects, enemies)
        draw(window, background, bg_image, player, objects, enemies, offset_x, offset_y)

        #Adjust the "camera" position on the screen
        if ((player.rect.right - offset_x  >= WIDTH - scroll_area_width) and player.x_vel > 0) or ((player.rect.left - offset_x  <= WIDTH - scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

        if ((player.rect.top - offset_y  >= HEIGHT - scroll_area_height) and player.y_vel > 0) or ((player.rect.bottom - offset_y  <= HEIGHT - scroll_area_height) and player.y_vel < 0):
            offset_y += player.y_vel

        #Check if game is over and if yes set the end screen 
        if player.game_over:
            draw_message_box(window, player)
            pygame.display.update()

            #If Game is over get the decision between continue or quit game from user.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if (
                        WIDTH // 2 - BUTTON_WIDTH // 2 <= x <= WIDTH // 2 + BUTTON_WIDTH // 2
                        and HEIGHT // 2 - BUTTON_HEIGHT // 2 <= y <= HEIGHT // 2 + BUTTON_HEIGHT // 2
                    ):
                        # Continue button clicked
                        offset_x, offset_y = reset_game(player)
                    elif (
                        WIDTH // 2 - BUTTON_WIDTH // 2 <= x <= WIDTH // 2 + BUTTON_WIDTH // 2
                        and HEIGHT // 2 + BUTTON_HEIGHT <= y <= HEIGHT // 2 + BUTTON_HEIGHT * 2
                    ):
                        # Quit button clicked
                        run = False
    #Quit the whole game
    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
