import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, BG, FPS, PLAYER_SPEED
from character import Character

pygame.init()

# declare constants



screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon of Darkness")

# create clock for maintaining frame rate

clock = pygame.time.Clock()

# define player movement vars
moving_left = False
moving_right = False
moving_up = False
moving_down = False

player_image = pygame.image.load("assets/images/characters/elf/idle/0.png").convert_alpha()

# create player
player = Character(100,100, player_image)


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
    
    player.draw(screen)
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
