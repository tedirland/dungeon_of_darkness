import pygame

class Button():
    def __init__(self,x,y,img) -> None:
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.topleft = (x,y)
    def draw(self, surface):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check for mouse over and clicked condition
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
            action = True

        surface.blit(self.img, self.rect)
        return action