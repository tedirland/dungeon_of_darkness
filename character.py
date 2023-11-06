import pygame
from constants import RED

class Character():
    def __init__(self,x,y ):
        self.rect = pygame.Rect(0,0,40,40)
        self.rect.center = (x,y)
    
    def draw(self, surface):
        pygame.draw.rect(surface,RED, self.rect)