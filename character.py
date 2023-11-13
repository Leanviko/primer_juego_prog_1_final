import pygame
import settings
import math
import weapon



class Character():
    def __init__(self, x, y, health, mob_animations, char_type, boss, size):
        self.char_type = char_type
        self.boss = boss
        self.score = 0
        self.flip = False
        self.animation_list = mob_animations[self.char_type]
        self.frame_index = 0
        self.action = 0 # 0: parado, 1:correr
        self.update_time = pygame.time.get_ticks()
        self.running = False
        self.health = health 
        self.alive = True

        self.hit = False
        self.last_hit = pygame.time.get_ticks()
        self.stunned = False

        #boos
        self.last_attack = pygame.time.get_ticks()

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0,0, settings.TILE_SIZE * size,settings.TILE_SIZE * size)
        self.rect.center = (x, y)
    
    def move(self,dx,dy, obstacle_tiles):

        screen_scroll = [0, 0]

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
        
        #colisiones con el entorno-----------
        self.rect.x += dx
        for obstacle in obstacle_tiles:
            #chequear colision
            if obstacle[1].colliderect(self.rect):
                #chequea de que lado ocurre la colision
                if dx > 0:
                    self.rect.right = obstacle[1].left
                if dx < 0:
                    self.rect.left = obstacle[1].right
        self.rect.y += dy
        for obstacle in obstacle_tiles:
            #chequear colision
            if obstacle[1].colliderect(self.rect):
                #chequea de que lado ocurre la colision
                if dy > 0:
                    self.rect.bottom = obstacle[1].top
                if dy < 0:
                    self.rect.top = obstacle[1].bottom

        #logica aplicada solo al jugador
        if self.char_type == 0:
            #actualizar scroll en base a la posicion del jugador
            #mover la camara izq y der. Se moverá antes de llegar al borde 
            if self.rect.right > (settings.WIDTH - settings.SCROLL_THRESHOLD):
                screen_scroll[0] = (settings.WIDTH - settings.SCROLL_THRESHOLD) - self.rect.right
                self.rect.right = settings.WIDTH - settings.SCROLL_THRESHOLD
            if self.rect.left < settings.SCROLL_THRESHOLD:
                screen_scroll[0] = settings.SCROLL_THRESHOLD - self.rect.left
                self.rect.left = settings.SCROLL_THRESHOLD
            
            #lo mismo para la camara arriba y abajo.
            if self.rect.bottom > (settings.HEIGHT - settings.SCROLL_THRESHOLD):
                screen_scroll[1] = (settings.HEIGHT - settings.SCROLL_THRESHOLD) - self.rect.bottom
                self.rect.bottom = settings.HEIGHT - settings.SCROLL_THRESHOLD
            if self.rect.top < settings.SCROLL_THRESHOLD:
                screen_scroll[1] = settings.SCROLL_THRESHOLD - self.rect.top
                self.rect.top = settings.SCROLL_THRESHOLD

        return screen_scroll

    #funcion logica solo aplicada a los enemigos
    def ai(self, player, obstacle_tiles, screen_scroll, fireball_image):
        clipped_line = ()
        stun_cooldown = 100
        ai_dx = 0
        ai_dy = 0
        fireball = None

        #reposicion de los modelos en base al scroll de pantalla
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        #linea de vision del enemigo al jugador
        init = (self.rect.centerx, self.rect.centery)
        end = (player.rect.centerx, player.rect.centery)
        line_of_sight = (init, end)

        #chequeamos si la linea de vision obstaculiza con algo
        for obstacle in obstacle_tiles:
            if obstacle[1].clipline(line_of_sight):
                #clipped_line captura la recta entre el enemigo el el obst.
                clipped_line = obstacle[1].clipline(line_of_sight)
        
        #chequeamos las distancia con el jugador con pitagoras
        dist= math.sqrt(((self.rect.centerx - player.rect.centerx)**2)+((self.rect.centery - player.rect.centery)**2))
        
        
        if not clipped_line and dist > settings.RANGE:
            if self.rect.centerx > player.rect.centerx:
                ai_dx = -settings.ENEMY_SPEED
            if self.rect.centerx < player.rect.centerx:
                ai_dx = settings.ENEMY_SPEED
            if self.rect.centery > player.rect.centery:
                ai_dy = -settings.ENEMY_SPEED
            if self.rect.centery < player.rect.centery:
                ai_dy = settings.ENEMY_SPEED

        if self.alive:
            #ataque al jugador
            if self.stunned == False:
                #se moverá hacia el jugador
                self.move(ai_dx, ai_dy, obstacle_tiles) 
                #atacará al jugador
                if dist < settings.ATTACK_RANGE and player.hit == False:
                    player.health -= 10
                    player.hit = True
                    player.last_hit = pygame.time.get_ticks()
                #los jefes disparan bolas de fuego
                fireball_cooldown = 700
                if self.boss:
                    if dist < 500:
                        if pygame.time.get_ticks() - self.last_attack >= fireball_cooldown:
                            fireball = weapon.Fireball(fireball_image,self.rect.centerx, self.rect.centery, player.rect.centerx, player.rect.centery)
                            self.last_attack = pygame.time.get_ticks()

            #chuequeamos si impactó una flecha
            if self.hit == True:
                self.hit = False
                self.last_hit = pygame.time.get_ticks()
                self.stunned = True
                self.running = False
                self.update_action(0) #se quede quieto

            #momento entre impacto y que vuelve a moverse
            if(pygame.time.get_ticks() - self.last_hit > stun_cooldown):
                self.stunned = False
        return fireball

    def update(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False

        hit_cooldown = 1000
        if self.char_type == 0:
            if self.hit == True and (pygame.time.get_ticks() - self.last_hit) > hit_cooldown:
                self.hit = False


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
        