import sys
sys.path.insert(0, '.')  # Add the parent directory to the path
import os
from os import listdir
from os.path import isfile, join
from .static_variables import font,WIDTH,HEIGHT,PLAYER_VEL,MESSAGE_BOX_WIDTH,MESSAGE_BOX_HEIGHT,MESSAGE_BOX_COLOR,BUTTON_WIDTH,BUTTON_HEIGHT,BUTTON_COLOR,BUTTON_TEXT_COLOR
import pygame

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(dir1,dir2, width, height, direction = False):
    script_dir = os.path.dirname(os.path.abspath(__file__)).replace("classes",'')
    path = join(script_dir,"assets",dir1,dir2)
    images = [f for f in listdir(path) if isfile(join(path,f))]

    all_sprites = {}
    
    for image in images:
        sprite_sheet = pygame.image.load(join(path,image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width,height),pygame.SRCALPHA,32)
            rect  =pygame.Rect(i * width, 0 , width, height)
            surface.blit(sprite_sheet, (0,0), rect)
            sprites.append(pygame.transform.scale2x(surface))
        
        if direction:
            all_sprites[image.replace(".png","") + "_right"] = sprites
            all_sprites[image.replace(".png","") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png","")] = sprites

    return all_sprites

def get_block(size,block_image_pos):
    #Blocks that will be the floor, columns and floating blocks on the whole game phase
    script_dir = os.path.dirname(os.path.abspath(__file__)).replace("classes",'')
    path = join(script_dir,"assets","Terrain","Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size,size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(block_image_pos[0],block_image_pos[1], size, size) #0 and 126
    surface.blit(image, (0,0), rect)
    return pygame.transform.scale2x(surface)


def get_background(name):
    script_dir = os.path.dirname(os.path.abspath(__file__)).replace("classes",'')
    image = pygame.image.load(join(script_dir,"assets","Background",name))
    _, _, width, height =  image.get_rect()
    tiles = []
    for i in range(WIDTH//width + 1):
        for j in range(HEIGHT//height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles,image


def draw(window, background, bg_image, player, objects, enemies, offset_x, offset_y):
    for tile in background:
        window.blit(bg_image,tile)

    for obj in objects:
        obj.draw(window, offset_x, offset_y)

    for enm in enemies:
        enm.draw(window, offset_x, offset_y)

    player.draw(window, offset_x, offset_y)
        
    pygame.display.update()

def handle_vertical_collision(player,objects,dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom    
                player.hit_head()
            collided_objects.append(obj)
    return collided_objects

def collide(player, objects, dx,enemies):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break
    for enemy in enemies:
        if pygame.sprite.collide_mask(player,enemy):
            collided_object = enemy
            break

    player.move(-dx, 0)
    player.update()
    return collided_object

def handle_move(player, objects, enemies):
    keys = pygame.key.get_pressed()
    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 2,enemies)
    collide_right = collide(player, objects, PLAYER_VEL * 2,enemies)
    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check  = [collide_left, collide_right, *vertical_collide]
    for  obj in  to_check:
        if obj and (obj.name == "fire" or obj and obj.name == "saw" or obj.name == 'enemy'):
            player.make_hit()
        if obj and obj.name in ("Apple","Bananas","Cherries","Kiwi","Melon","Orange","Pineapple","Strawberry"):
            player.make_point()
            obj.collect()
        if obj and obj.name == "End":
            player.next_phase()    


def collide_enemy(enemy, objects, dx):
    enemy.move(dx, 0)
    enemy.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(enemy, obj):
            collided_object = obj
            break

    enemy.move(-dx, 0)
    enemy.update()
    return collided_object

def handle_move_enemy(enemy, objects):
    collide_left = collide_enemy(enemy, objects, -PLAYER_VEL * 2)
    collide_right = collide_enemy(enemy, objects, PLAYER_VEL * 2)
    if collide_left:
        enemy.move_right(5)
    if collide_right:   
        enemy.move_left(5)

def draw_message_box(window, player):
    pygame.draw.rect(window, MESSAGE_BOX_COLOR, (WIDTH // 2 - MESSAGE_BOX_WIDTH // 2, HEIGHT // 2 - MESSAGE_BOX_HEIGHT // 2, MESSAGE_BOX_WIDTH, MESSAGE_BOX_HEIGHT))

    continue_button_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - BUTTON_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT)
    quit_button_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT)

    pygame.draw.rect(window, BUTTON_COLOR, continue_button_rect)
    pygame.draw.rect(window, BUTTON_COLOR, quit_button_rect)

    continue_text = font.render("Continue", True, BUTTON_TEXT_COLOR)
    quit_text = font.render("Quit", True, BUTTON_TEXT_COLOR)
    lives_text = font.render(f"Lives: {player.lives}", True, (0, 0, 0))

    window.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT // 2 - BUTTON_HEIGHT // 2 + BUTTON_HEIGHT // 4))
    window.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + BUTTON_HEIGHT + BUTTON_HEIGHT // 4))
    window.blit(lives_text, (5, 5))  # Display lives on the top-left corner with padding

def reset_game(player):
    # Reset player position, velocity, and other relevant attributes
    player.rect = pygame.Rect(100, 100, 50, 50)
    player.x_vel = 0
    player.y_vel = 0
    player.mask = None
    player.direction = "left"
    player.animation_count = 0
    player.fall_count = 0
    player.jump_count = 0
    player.hit = False
    player.hit_count = 0
    player.lives = 10
    player.game_over = False

    # Reset the game screen position to its initial state
    offset_x = 0
    offset_y = 0
    return offset_x, offset_y

if __name__ == "__main__":
    reset_game()
    flip()
    load_sprite_sheets()
    get_block()
    get_background()
    draw()
    handle_vertical_collision()
    collide()
    handle_move()
    collide_enemy()
    handle_move_enemy()
    draw_message_box()
    reset_game()    
