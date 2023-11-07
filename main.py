import pygame
import settings 
from player import Player

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

animation_types = ["idle","run"]
animation_list = []
for animation in animation_types:
    temp_list = []
    for i in range(4):
        image = pygame.image.load(f"assets/images/characters/elf/{animation}/{i}.png").convert_alpha()
        image = scale_img(image,settings.SCALE)
        temp_list.append(image)
    animation_list.append(temp_list)

print(animation_list)
#creando jugador
player = Player(100,100,animation_list)



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

    player.move(dx, dy)
    player.update()
    player.draw(screen)
    print(str(dx),str(dy))
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