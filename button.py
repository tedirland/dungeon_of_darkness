import pygame

class Button():
    def __init__(self,x,y,img) -> None:
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.topleft = (x,y)
    def draw(self, surface):
        action = False
        surface.blit(self.img, self.rect)
        return action