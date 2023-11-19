"""Main Module where the game is initialized and run"""
import csv
import pygame
from constants import ITEM_SCALE, PANEL, POTION_SCALE, RED, ROWS, SCALE, SCREEN_HEIGHT, SCREEN_WIDTH, BG, FPS, PLAYER_SPEED, TILE_SIZE, TILE_TYPES, WEAPON_SCALE, WHITE, COLS
from character import Character
from items import Item
from weapon import Weapon
from world import World

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon of Darkness")

# create clock for maintaining frame rate
clock = pygame.time.Clock()

# define game variables
level = 1
screen_scroll = [0,0]

# define player movement vars
moving_left = False
moving_right = False
moving_up = False
moving_down = False

# define font
font = pygame.font.Font("assets/fonts/AtariClassic.ttf",20)

# helper func to scale image
def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w*scale, h*scale))

# load heart images
heart_empty = scale_img(pygame.image.load("assets/images/items/heart_empty.png").convert_alpha(), ITEM_SCALE)
heart_half = scale_img(pygame.image.load("assets/images/items/heart_half.png").convert_alpha(), ITEM_SCALE)
heart_full = scale_img(pygame.image.load("assets/images/items/heart_full.png").convert_alpha(), ITEM_SCALE)

# load coin images
coin_images = []
for x in range(4):
    img = scale_img(pygame.image.load(f"assets/images/items/coin_f{x}.png").convert_alpha(), ITEM_SCALE)
    coin_images.append(img)
# load potion image
red_potion = scale_img(pygame.image.load("assets/images/items/potion_red.png").convert_alpha(), POTION_SCALE)

item_images = []

item_images.append(coin_images)
item_images.append(red_potion)
# load weapon images
bow_image = scale_img(pygame.image.load("assets/images/weapons/bow.png").convert_alpha(), WEAPON_SCALE)
arrow_image = scale_img(pygame.image.load("assets/images/weapons/arrow.png").convert_alpha(), WEAPON_SCALE)

# load tile map images
tile_list = []

for x in range(TILE_TYPES):
    tile_img = pygame.image.load(f"assets/images/tiles/{x}.png").convert_alpha()
    tile_img = pygame.transform.scale(tile_img, (TILE_SIZE, TILE_SIZE))
    tile_list.append(tile_img)

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


# function to output text to screen
def draw_text(text, font, text_col, x,y):
    img = font.render(text, True, text_col)
    screen.blit(img,(x,y))

# create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)
# load in level data and create world

with open(f"levels/level{level}_data.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for x,row in enumerate(reader):
        for y,tile in enumerate(row):
            world_data[x][y] = int(tile)


# init World class
world = World()
world.process_data(world_data,tile_list, item_images)

# function for displaying game info
def draw_info():
    pygame.draw.rect(screen,PANEL, (0,0,SCREEN_WIDTH, 50))
    pygame.draw.line(screen,WHITE, (0,50), (SCREEN_WIDTH, 50))
    # draw lives
    half_heart_drawn = False
    for i in range(5):
        if player.health >= ((i+1) *20):
            screen.blit(heart_full, (10+ i *50, 0 ))
        elif player.health % 20 > 0 and half_heart_drawn is False:
             screen.blit(heart_half, (10+ i *50, 0 ))
             half_heart_drawn = True
        else:
             screen.blit(heart_empty, (10+ i *50, 0 ))
    # draw level
    draw_text(f"Level {str(level)}", font,WHITE,SCREEN_WIDTH /2,15)
    # show score
    draw_text(f"X{player.coins}", font,WHITE,SCREEN_WIDTH-100,15)





#damage text class
class DamageText(pygame.sprite.Sprite):
    def __init__(self,x,y,damage, color) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage,True,color)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.counter = 0
    def update(self) -> None:
        # reposition text based on screen scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]
        # move damage text up
        self.rect.y -= 1
        # delete the counter after a few seconds
        self.counter += 1
        if self.counter > 30:
            self.kill()



# create player
player = Character(400,300,100, mob_animations, 0)

# create enemy
enemy = Character(300,300,100, mob_animations,2)

# create weapon
bow = Weapon(bow_image, arrow_image)

# create empty emeny list
enemy_list = []
enemy_list.append(enemy)

# create sprite groups
damage_text_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()

score_coin = Item(SCREEN_WIDTH-115,23,0,coin_images, dummy_coin=True)
# add items from the level data
for item in world.item_list:
    item_group.add(item)
item_group.add(score_coin)
# 

potion = Item(200,200, 1, [red_potion])
item_group.add(potion)


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
    screen_scroll = player.move(dx,dy)

    # update all objects
    world.update(screen_scroll)
    for enemy in enemy_list:
        enemy.ai(screen_scroll)
        enemy.update()
    player.update()
    arrow = bow.update(player)
    if arrow:
        arrow_group.add(arrow)
    for arrow in arrow_group: 
        damage, damage_pos =arrow.update(screen_scroll,enemy_list)
        if damage:
            damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), RED)
            damage_text_group.add(damage_text)
    damage_text_group.update()
    item_group.update(screen_scroll,player)
    
    ###### draw sprites ######

    # draw world
    world.draw(screen)
    # draw enemies
    for enemy in enemy_list:
        enemy.draw(screen)
    # draw player
    player.draw(screen)
    # draw weapon
    bow.draw(screen)
    # draw arrows
    for arrow in arrow_group:
        arrow.draw(screen)
    damage_text_group.draw(screen)
    item_group.draw(screen)
    draw_info()
    score_coin.draw(screen)

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
