import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from character import Character

pygame.init()

# declare constants



screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon of Darkness")

# create player

player = Character(100,100)


# main game loop
run = True
while run:
    
    player.draw(screen)
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()

pygame.quit()
