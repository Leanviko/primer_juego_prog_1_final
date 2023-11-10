import pygame
import settings
import math



class Character():
    def __init__(self, x, y, health, mob_animations,char_type):
        self.char_type = char_type
        self.score = 0
        self.flip = False
        self.animation_list = mob_animations[self.char_type]
        self.frame_index = 0
        self.action = 0 # 0: parado, 1:correr
        self.update_time = pygame.time.get_ticks()
        self.running = False
        self.health = health 
        self.alive = True

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0,0, settings.TILE_SIZE,settings.TILE_SIZE)
        self.rect.center = (x, y)
    
    def move(self,dx,dy):
        self.running = False
        if dx != 0 or dy != 0:
            self.running = True
        if dx < 0:
            self.flip = True            
        if dx > 0:
            self.flip = False

        #ajuste de velocidad en diagonal
        if dx != 0 and dy != 0:
            dx = dx*(math.sqrt(2)/2)
            dy = dy*(math.sqrt(2)/2)

        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False


        #check que tipo de accion hace el jugador
        if self.running == True:
            self.update_action(1)#run
        else:
            self.update_action(0)#idle

        #ritmo animacion
        animation_cooldown = 70

        #actualiza la imagen
        self.image = self.animation_list[self.action][self.frame_index]
        #chequear el tiempo desde la ultima actualizacion
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #reset de los frames
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
    
    def update_action(self, new_action):
        #chekea si la nueva accion es diferente que al anterior
        if new_action != self.action:
            self.action = new_action
            #reinicia los frames
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        if self.char_type == 0:
            surface.blit(flipped_image,(self.rect.x,self.rect.y-settings.OFFSET*settings.SCALE))
        else:
            surface.blit(flipped_image,self.rect)
        pygame.draw.rect(surface, settings.RED, self.rect, 1)