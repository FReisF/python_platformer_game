import sys
sys.path.insert(0, '.')  # Add the parent directory to the path
import pygame
import subprocess as sp
from .prep_functions import load_sprite_sheets
from .static_variables import font, WIDTH, HEIGHT

pygame.init()
pygame.display.set_caption("Platformer")

window = pygame.display.set_mode((WIDTH,HEIGHT))

class Player(pygame.sprite.Sprite):
    COLOR = (255,0,0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters","NinjaFrog", 32, 32, True)
    ANIMATION_DELAY  = 1

    def __init__(self, x, y, width, height, pb, pa):
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
        self.phase_before = pb
        self.phase_after = pa
            
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
        points_text = font.render(f"Points: {self.score}", True, (0, 0, 0))
        win.blit(lives_text, (5, 5))  # 5 pixels padding from the top-left corner
        win.blit(points_text, (5, 25))  # 5 pixels padding from the top-left corner    
        win.blit(self.sprite,(self.rect.x - offset_x,self.rect.y - offset_y))

    def next_phase(self):
        pygame.quit()    
        # Start the external Python script
        if self.phase_before == 'phase_4.py':
            sp.Popen.terminate(sp.Popen(['python',self.phase_before]))    
        extProc = sp.Popen(['python', self.phase_after])#'code_3.py'

        # Terminate the current process
        sp.Popen.terminate(sp.Popen(['python',self.phase_before]))#'code_2.py'


if __name__ == "__main__":
    Player(pygame.sprite.Sprite)