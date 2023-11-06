import pygame
import settings
import math



class Player():
    def __init__(self,x,y):
        self.rect = pygame.Rect(0,0,40,40)
        self.rect.center = (x,y)
    
    def move(self,dx,dy):

        #ajuste de velocidad en diagonal
        if dx != 0 and dy != 0:
            dx = dx*(math.sqrt(2)/2)
            dy = dy*(math.sqrt(2)/2)

        self.rect.x += dx
        self.rect.y += dy

    def draw(self,surface):
        pygame.draw.rect(surface,settings.RED, self.rect)