import pygame
import math

class Weapon():
    def __init__(self,image, arrow_image):
        self.original_image = image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image,self.angle)
        self.arrow_image = arrow_image
        self.rect = self.image.get_rect()
    
    def update(self, player):
        arrow = None #se declara aunque no tenga nada para que el return no de error

        self.rect.center = player.rect.center

        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.centerx    
        y_dist = -(pos[1] - self.rect.centery)
        self.angle = math.degrees(math.atan2(y_dist, x_dist))

        #Cuando recibe la orden de disparar crea una flecha
        if pygame.mouse.get_pressed()[0]:
            arrow = Arrow(self.arrow_image,self.rect.centerx,self.rect.centery,self.angle)
        return arrow

    def draw(self,surface):
        self.image = pygame.transform.rotate(self.original_image,self.angle)
        center_rect = ((self.rect.centerx - int(self.image.get_width()/2)),(self.rect.centery - int(self.image.get_height()/2))) 
        
        surface.blit(self.image,center_rect)

class Arrow(pygame.sprite.Sprite):
    def __init__(self,image,x,y,angle):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = image
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image,self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
    
    def draw(self,surface):
        center_surface = ((self.rect.centerx - int(self.image.get_width()/2)),(self.rect.centery - int(self.image.get_height()/2))) 
        
        surface.blit(self.image,center_surface)