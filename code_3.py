import os
import random
import math
from os import listdir
from os.path import isfile, join
import pygame

pygame.init()
pygame.display.set_caption("Platformer")


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


window = pygame.display.set_mode((WIDTH,HEIGHT))

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(dir1,dir2, width, height, direction = False):
    path = join("assets",dir1,dir2)
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

def get_block(size):
    path = join("assets","Terrain","Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size,size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0,126, size, size)
    surface.blit(image, (0,0), rect)
    return pygame.transform.scale2x(surface)


class Player(pygame.sprite.Sprite):
    COLOR = (255,0,0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters","NinjaFrog", 32, 32, True)
    ANIMATION_DELAY  = 1

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x,y,width,height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.lives = 10000000000000000000000000000
        self.game_over = False
        self.score = 0
    
    def make_point(self):
        self.score += 1
        if self.score >= 10:
            self.lives += 1
            self.score = 0

    def make_hit(self):
        self.hit = True
        self.hit_count = 0
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0
        

    def move(self,dx,dy):
        self.rect.x += dx
        self.rect.y += dy
    
    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0
    
    def loop(self, fps):
        self.y_vel += min(1,(self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel,self.y_vel)
        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit" 
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"
        
        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft = (self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x, offset_y):
        lives_text = font.render(f"Lives: {self.lives}", True, (0, 0, 0))
        win.blit(lives_text, (5, 5))  # 5 pixels padding from the top-left corner    
        win.blit(self.sprite,(self.rect.x - offset_x,self.rect.y - offset_y))
        

class Enemy(pygame.sprite.Sprite):
    COLOR = (255,0,0)
    GRAVITY = 1
    ANIMATION_DELAY  = 1

    def __init__(self, x, y, width, height,name=None):
        super().__init__()
        self.rect = pygame.Rect(x,y,width,height)
        self.sprites = load_sprite_sheets("MainCharacters","MaskDude", 32, 32, True)
        self.name = 'enemy'
        self.x_vel = -5
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        #self.fall_count = 0
        #self.jump_count = 0
        self.hit = False
        self.hit_count = 0

    def make_hit(self):
        self.hit = True
        self.hit_count = 0

    
    def move(self,dx,dy):
        self.rect.x += dx
        self.rect.y += dy
    
    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0
    
    def loop(self, fps):
        self.move(self.x_vel,self.y_vel)
        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps:
            self.hit = False
            self.hit_count = 0
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1
        
    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
            self.x_vel *= -1

        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"
        
        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.sprites[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft = (self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x, offset_y):    
        win.blit(self.sprite,(self.rect.x - offset_x,self.rect.y - offset_y))



class Fruits(pygame.sprite.Sprite):
    COLOR = (255,0,0)
    GRAVITY = 1
    ANIMATION_DELAY  = 1

    def __init__(self, x, y, width, height,fruit_name):
        super().__init__()
        self.rect = pygame.Rect(x,y,width,height)
        self.sprites = load_sprite_sheets("Items","Fruits", 32, 32,False)
        self.name = fruit_name
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        #self.fall_count = 0
        #self.jump_count = 0
        self.hit = False
        self.hit_count = 0

    def make_hit(self):
        self.hit = True
        self.hit_count = 0

    
    def move(self,dx,dy):
        self.rect.x += dx
        self.rect.y += dy
    
    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0
    
    def loop(self, fps):
        self.move(self.x_vel,self.y_vel)
        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps:
            self.hit = False
            self.hit_count = 0
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1
        
    def update_sprite(self):
        sprite_sheet = self.name
        sprite_sheet_name = sprite_sheet# + "_" + self.direction
        sprites = self.sprites[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft = (self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x, offset_y):    
        win.blit(self.sprite,(self.rect.x - offset_x,self.rect.y - offset_y))



class Object(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x, offset_y):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y,size, size)
        block = get_block(size)
        self.image.blit(block, (0,0))
        self.mask = pygame.mask.from_surface(self.image) 

class EndCheckPoint(Object):
    def __init__(self,x,y,width,height):
        super().__init__(x,y,width,height,"End")
        self.endpoint = load_sprite_sheets("Items","Checkpoints\End",width,height)
        self.image = self.endpoint["End (Idle)"][0]
        self.mask = pygame.mask.from_surface(self.image)
                

class Fire(Object):
    ANIMATION_DELAY = 3
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheets("Traps","Fire", width, height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        self.rect = self.image.get_rect(topleft = (self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)
        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

class Saw(Object):
    ANIMATION_DELAY = 3
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "saw")
        self.saw = load_sprite_sheets("Traps","Saw", width, height)
        self.image = self.saw["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.saw[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        self.rect = self.image.get_rect(topleft = (self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)
        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0



'''
class Fruits(Object):
    ANIMATION_DELAY = 2
    def __init__(self, x, y, width, height,fruit_name):
        super().__init__(x, y, width, height, fruit_name)
        #self.fruit = load_sprite_sheets("Items",f'Fruits\{fruit_name}', width, height)
        self.fruit = load_sprite_sheets("Items",'Fruits', width, height)
        self.image = self.fruit[fruit_name][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = fruit_name

    def collected(self):
        #self.fruit = load_sprite_sheets("Fruits","Collected", self.width, self.height)
        self.animation_name = "Collected"

    def loop(self):
        sprites = self.fruit[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0
        self.rect = self.image.get_rect(topleft = (self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count += 1

    def draw(self, win, offset_x, offset_y):
        # Get the non-transparent bounding box of the sprite
        non_transparent_rect = self.image.get_bounding_rect()

        # Draw the sprite on the screen considering the offset and non-transparent bounding box
        win.blit(self.image.subsurface(non_transparent_rect), (self.rect.x - offset_x, self.rect.y - offset_y + non_transparent_rect.y))
'''

def get_background(name):
    image = pygame.image.load(join("assets","Background",name))
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
        if obj and obj.name in ("Apple","Banana","Cherries","Kiwi","Melon","Orange","Pinapple","Strawberry"):
            player.make_point()
            obj.collected()


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
    #enemy.x_vel = 0
    collide_left = collide_enemy(enemy, objects, -PLAYER_VEL * 2)
    collide_right = collide_enemy(enemy, objects, PLAYER_VEL * 2)
    if collide_left:
        enemy.move_right(5)
    if collide_right:   
        enemy.move_left(5)
    #to_check  = [collide_left, collide_right]
    #for  obj in  to_check:
    #    if obj and (obj.name == "fire" or obj and obj.name == "saw"):
    #        player.make_hit()

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

def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Green.png")
    block_size = 96

    player  = Player(100, 100, 50, 50)
       
    enemies_position = [(1.25,1),(-13,18),(-14,18),(-20,18),(-21,18),(-24,18),(-25,18),(-26,18)]
    enemies = [Enemy(block_size * i[0],HEIGHT - block_size*i[1] - 64,50,50) for i in enemies_position]

    floor_position = [(1,-3,0,3),(13,1,0,1),(18,-3,0,-1),(23,-3,0,-2),(23,-2,2,-1)]
    floors = [[Block(i * block_size,HEIGHT - block_size * j[0], block_size) for i in range((WIDTH * j[1] + j[2] *  block_size)// block_size, WIDTH * j[3] // block_size)] for j in floor_position]

    block_columns_positions = {3:(1,4),7:(2,5),11:(0,3),13:(-1,2),17:(2,5),19:(-2,1),23:(-3,0),29:(-4,-1),-3:(1,4),-7:(2,5),-11:(0,3),-13:(-1,2),-17:(2,5),-19:(-2,1),-23:(-3,0),-29:(-4,-1)}
    block_columns = [[Block(block_size * k,i * block_size, block_size) for i in range(v[0],v[1])] for k,v in block_columns_positions.items()]
    
    float_blocks_positions = [(7,11),(0,2),(4,3),(6,7),(9,9),(1,6),(11,14),(7,17),(-7,11),(-4,3),(-6,7),(-9,9),(-1,6),(-11,14),(-7,17),(-12,19),(-18,19),(-32,19),(-24,19),(7,19),(-21,21),(-22,24),(-32,24),(-19,24),(-12,24)]
    float_blocks = [Block(block_size * l[0], HEIGHT - block_size * l[1], block_size) for l in float_blocks_positions]
    
    fire_position_adjusted = 16 + block_size//2
    fires = [Fire(float_blocks[i].rect.x + fire_position_adjusted, float_blocks[i].rect.y - fire_position_adjusted, 16, 32) for i in range(0,16,2)]
    
    saws = [Saw(-90, HEIGHT - block_size  - 80, 38, 38),
            Saw(floors[0][4].rect.x, floors[0][4].rect.y - block_size + 8, 38, 38)]
    end_point = EndCheckPoint(floors[0][8].rect.x, floors[0][8].rect.y - block_size - 24, 64,64)
    
    fruits = [Fruits(40, HEIGHT - block_size * 3, 22, 38,"Melon")]
    
    for fire in fires:
        fire.on()
    for saw in saws:
        saw.on()
    
    block_columns = [block for sublist in block_columns for block in sublist]
    floors = [floor for sublist in floors for floor in sublist]

    objects = [*floors,*float_blocks , *fires, *block_columns,end_point,*saws,*fruits]

    offset_x = 0
    offset_y = 0
    scroll_area_width = 200
    scroll_area_height = 200

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump() 

        player.loop(FPS)        
        for fire in fires:
            fire.loop()
        for saw in saws:
            saw.loop()    
        for enemy in enemies:
            enemy.loop(FPS)
            handle_move_enemy(enemy, objects)
        for fruit in fruits:
            fruit.loop()

        handle_move(player, objects, enemies)
        draw(window, background, bg_image, player, objects, enemies, offset_x, offset_y)

        if ((player.rect.right - offset_x  >= WIDTH - scroll_area_width) and player.x_vel > 0) or ((player.rect.left - offset_x  <= WIDTH - scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

        if ((player.rect.top - offset_y  >= HEIGHT - scroll_area_height) and player.y_vel > 0) or ((player.rect.bottom - offset_y  <= HEIGHT - scroll_area_height) and player.y_vel < 0):
            offset_y += player.y_vel

        if player.game_over:
            draw_message_box(window, player)
            pygame.display.update()

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
    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
