import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type, animation_list, dummy_coin = False):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type #0:moneda 1:pocion
        self.animation_list = animation_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.dummy_coin = dummy_coin

    def update(self, screen_scroll, player, coin_fx, heal_fx):
        
        #reposicionamos en base el scroll de pantalla
        if self.dummy_coin == False:
            self.rect.x += screen_scroll[0]
            self.rect.y += screen_scroll[1]
        
        #chequear si el item colisiona con el personaje
        if self.rect.colliderect(player.rect):
            if self.item_type == 0:
                player.score += 1
                coin_fx.play()
            elif self.item_type == 1:
                player.health += 10
                heal_fx.play()
                if player.health > 100:
                    player.health = 100
            self.kill()


        #ritmo animacion
        animation_cooldown = 150
        #actualizar imagen
        self.image = self.animation_list[self.frame_index]
        #chequear si paso el tiempo desde la ultima imagen
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #resetear  los frames
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0
    
    def draw(self,surface):
        surface.blit(self.image, self.rect)