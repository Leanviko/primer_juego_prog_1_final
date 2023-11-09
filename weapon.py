import random
import pygame
import math
import settings

class Weapon():
    def __init__(self,image, arrow_image):
        self.original_image = image
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image,self.angle)
        self.arrow_image = arrow_image
        self.rect = self.image.get_rect()
        self.fired = False
        self.last_shot = pygame.time.get_ticks()
    
    def update(self, player):
        shoot_cooldown = 350
        arrow = None #se declara aunque no tenga nada para que el return no de error

        self.rect.center = player.rect.center

        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.centerx    
        y_dist = -(pos[1] - self.rect.centery)
        self.angle = math.degrees(math.atan2(y_dist, x_dist))

        #Cuando recibe la orden de disparar crea una flecha
        if pygame.mouse.get_pressed()[0] and self.fired == False and (pygame.time.get_ticks()- self.last_shot > shoot_cooldown):
            arrow = Arrow(self.arrow_image,self.rect.centerx,self.rect.centery,self.angle)
            self.fired = True
            
        if (pygame.time.get_ticks()- self.last_shot > shoot_cooldown or pygame.mouse.get_pressed()[0]==False):
            self.fired = False
            self.last_shot = pygame.time.get_ticks()
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
        self.image = pygame.transform.rotate(self.original_image,self.angle-90)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        #calcular la velocidad vert y hor segun el angulo
        self.dx = math.cos(math.radians(self.angle))*settings.SPEED_ARROW
        self.dy = math.sin(math.radians(self.angle))*settings.SPEED_ARROW*-1
    
    
    def update(self, enemy_list):
        #resetea el daño
        damage = 0
        damage_pos = None

        #cambiar posicion de la flecha segun los diferenciales
        self.rect.x += self.dx
        self.rect.y += self.dy

        #borrar las flechas que salgan de la pantalla
        if self.rect.right < 0 or self.rect.left > settings.WIDTH or self.rect.top < 0 or self.rect.bottom > settings.HEIGHT:
            self.kill()

        #verificamos colision entre flechas y enemigos
        for enemy in enemy_list:
            if enemy.rect.colliderect(self.rect) and enemy.alive:
                damage = 10 + random.randint(-5,5)
                damage_pos = enemy.rect
                enemy.health -= damage
                self.kill()
                break
        
        return damage,damage_pos



    
    def draw(self,surface):
        center_surface = ((self.rect.centerx - int(self.image.get_width()/2)),(self.rect.centery - int(self.image.get_height()/2))) 
        
        surface.blit(self.image,center_surface)