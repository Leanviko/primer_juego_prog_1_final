import pygame
import settings 
from character import Character
from weapon import Weapon

pygame.init()


screen = pygame.display.set_mode((settings.WIDTH,settings.HEIGHT))
pygame.display.set_caption('Jueguito')
clock =  pygame.time.Clock()

# variables de movimiento del jugador
moving_right = False
moving_left = False
moving_up = False
moving_down = False

#definimos fuente
font = pygame.font.Font("assets/fonts/AtariClassic.ttf",20)

#funcion para escalar
def scale_img(image,scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image,(w*scale,h*scale))


#carga de las imagenes del arco
bow_image = scale_img(pygame.image.load("assets/images/weapons/bow.png").convert_alpha(),settings.WEAPON_SCALE)
arrow_image = scale_img(pygame.image.load("assets/images/weapons/arrow.png").convert_alpha(),settings.WEAPON_SCALE)

#carga de sprites
mob_animations = []
mob_types = ["elf","imp","skeleton","goblin","muddy","tiny_zombie","big_demon"]

# lista principal de animaciones[lista de tipo de personaje[lista de animacion de ese personje]]
animation_types = ["idle","run"]# quieto o corriendo
for mob in mob_types:
    animation_list = []
    for animation in animation_types:
        temp_list = []
        for i in range(4):
            image = pygame.image.load(f"assets/images/characters/{mob}/{animation}/{i}.png").convert_alpha()
            image = scale_img(image,settings.SCALE)
            temp_list.append(image)
        animation_list.append(temp_list)
    mob_animations.append(animation_list)

#clase de texto del daño
class DamageText(pygame.sprite.Sprite):
    def __init__(self,x,y,damage,color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.counter = 0
    
    def update(self):
        # mover el textoo hacia arriba para darle un aspecto copadisimo
        self.rect.y -= 1
        #borra el texto despues de un tiempo
        self.counter += 1
        if self.counter > 30:
            self.kill()


#creacion jugador y enemigos
player = Character(100, 100, 100,mob_animations,0)
enemy = Character(100, 300, 100,mob_animations,1)

#dibujando arma
bow = Weapon(bow_image, arrow_image)
#crear grupo de sprites para las flechas y el texto de daño
damage_text_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()



#lista de enemigos
enemy_list = []
enemy_list.append(enemy)

#*Main loop------------------------------------------

run = True
while run:
    clock.tick(settings.FPS)
    screen.fill(settings.BG)

    dx=0
    dy=0
    if moving_right == True:
        dx += settings.SPEED
    if moving_left == True:
        dx -= settings.SPEED
    if moving_up == True:
        dy -= settings.SPEED
    if moving_down == True:
        dy += settings.SPEED

    #actualizar movimiento jugador
    player.move(dx, dy)

    
    #actualizar enemigo
    for enemy in enemy_list:
        enemy.update()
        print(enemy.health)
    #actualizar jugador
    player.update()
    #actualiza flecha
    arrow = bow.update(player)
    
    if arrow:
        arrow_group.add(arrow)
    for arrow in arrow_group:
        damage, damage_pos = arrow.update(enemy_list) #retorna 2 valores
        if damage:
            damage_text = DamageText(damage_pos.centerx,damage_pos.y,str(damage),settings.RED)
            damage_text_group.add(damage_text)
    
    damage_text_group.update()


    #dibujar jugador y arma
    for enemy in enemy_list:
        enemy.draw(screen)
    player.draw(screen)
    bow.draw(screen)
    for arrow in arrow_group:
        arrow.draw(screen)
    damage_text_group.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True 
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_s:
                moving_down = True
            if event.key == pygame.K_w:
                moving_up = True
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_s:
                moving_down = False
            if event.key == pygame.K_w:
                moving_up = False

    pygame.display.update()

pygame.quit()