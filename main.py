"""Main Module where the game is initialized and run"""
from typing import Any
import pygame
from constants import RED, SCALE, SCREEN_HEIGHT, SCREEN_WIDTH, BG, FPS, PLAYER_SPEED, WEAPON_SCALE
from character import Character
from weapon import Weapon

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon of Darkness")

# create clock for maintaining frame rate
clock = pygame.time.Clock()

# define player movement vars
moving_left = False
moving_right = False
moving_up = False
moving_down = False

# define font
font = pygame.font.Font("assets/fonts/AtariClassic.ttf",20)

# helper func tow scale image
def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w*scale, h*scale))

# load weapon images
bow_image = scale_img(pygame.image.load("assets/images/weapons/bow.png").convert_alpha(), WEAPON_SCALE)
arrow_image = scale_img(pygame.image.load("assets/images/weapons/arrow.png").convert_alpha(), WEAPON_SCALE)


# load character images
mob_animations = []
mob_types = ["elf", "imp", "skeleton", "goblin", "muddy", "tiny_zombie", "big_demon"]
animation_types = ["idle","run"]
for mob in mob_types:
    animation_list = []
    for animation in animation_types:
        # reset temp list of images
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f"assets/images/characters/{mob}/{animation}/{i}.png").convert_alpha()
            img = scale_img(img, SCALE)
            temp_list.append(img)
        animation_list.append(temp_list)
    mob_animations.append(animation_list)

#damage text class
class DamageText(pygame.sprite.Sprite):
    def __init__(self,x,y,damage, color) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage,True,color)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.counter = 0
    def update(self) -> None:
        # move damage text up
        self.rect.y -= 1
        # delete the counter after a few seconds
        self.counter += 1
        if self.counter > 30:
            self.kill()



# create player
player = Character(100,100,100, mob_animations, 0)

# create enemy
enemy = Character(200,300,100, mob_animations,2)

# create weapon
bow = Weapon(bow_image, arrow_image)

# create empty emeny list
enemy_list = []
enemy_list.append(enemy)

# create sprite groups
damage_text_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()

# main game loop
run = True
while run:

    # control frame rate
    clock.tick(FPS)

    screen.fill(BG)
    # calculate player movement
    dx = 0
    dy = 0
    if moving_right:
        dx = PLAYER_SPEED
    if moving_left:
        dx = -PLAYER_SPEED
    if moving_up:
        dy = -PLAYER_SPEED
    if moving_down:
        dy = PLAYER_SPEED
    

    # move player
    player.move(dx,dy)

    # update player
    for enemy in enemy_list:
        enemy.update()
    player.update()
    arrow = bow.update(player)
    if arrow:
        arrow_group.add(arrow)
    for arrow in arrow_group: 
        damage, damage_pos =arrow.update(enemy_list)
        if damage:
            damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), RED)
            damage_text_group.add(damage_text)
    damage_text_group.update()
    
    # draw sprites
    player.draw(screen)
    bow.draw(screen)
    for enemy in enemy_list:
        enemy.draw(screen)
    for arrow in arrow_group:
        arrow.draw(screen)
    damage_text_group.draw(screen)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # take keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_s:
                moving_down = True

                # take keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_s:
                moving_down = False
            
        

    
    pygame.display.update()

pygame.quit()
