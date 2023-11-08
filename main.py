import pygame
import settings 
from character import Character
from weapon import Weapon

pygame.init()


screen = pygame.display.set_mode((settings.WIDTH,settings.HEIGHT))
pygame.display.set_caption('Jueguito')
clock =  pygame.time.Clock()

moving_right = False
moving_left = False
moving_up = False
moving_down = False

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
animation_types = ["idle","run"]
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


#creando jugador
player = Character(100,100,mob_animations,0)
#dibujando arma
bow = Weapon(bow_image, arrow_image)
#crear grupo de sprites para las flechas
arrow_group = pygame.sprite.Group()



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

    #actualizar movimiento
    player.move(dx, dy)

    #actualizar jugador y arma
    player.update()
    arrow = bow.update(player)
    if arrow:
        arrow_group.add(arrow)


    #dibujar jugador y arma
    player.draw(screen)
    bow.draw(screen)
    for arrow in arrow_group:
        arrow.draw(screen)


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