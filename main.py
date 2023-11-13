import pygame
import csv
import settings 
from character import Character
from weapon import Weapon
from items import Item
from world import World

pygame.init()


screen = pygame.display.set_mode((settings.WIDTH,settings.HEIGHT))
pygame.display.set_caption('Jueguito')

clock =  pygame.time.Clock()

#definimos variables del juego
level = 1
screen_scroll = [0, 0]

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

#imagenes salud
heart_empty = scale_img(pygame.image.load("assets/images/items/heart_empty.png").convert_alpha(),settings.ITEM_SCALE)
heart_full = scale_img(pygame.image.load("assets/images/items/heart_full.png").convert_alpha(),settings.ITEM_SCALE)
heart_half = scale_img(pygame.image.load("assets/images/items/heart_half.png").convert_alpha(),settings.ITEM_SCALE)

#imagenes de monedas
coin_images = []
for x in range(4):
    coin_img = scale_img(pygame.image.load(f"assets/images/items/coin_f{x}.png").convert_alpha(), settings.ITEM_SCALE)
    coin_images.append(coin_img)

#imagen pocion
red_potion = scale_img(pygame.image.load("assets/images/items/potion_red.png").convert_alpha(),settings.POTION_SCALE)

item_images = []
item_images.append(coin_images)
item_images.append(red_potion)

#imagenes del arco y flecha
bow_image = scale_img(pygame.image.load("assets/images/weapons/bow.png").convert_alpha(),settings.WEAPON_SCALE)
arrow_image = scale_img(pygame.image.load("assets/images/weapons/arrow.png").convert_alpha(),settings.WEAPON_SCALE)
fireball_image = scale_img(pygame.image.load("assets/images/weapons/fireball.png").convert_alpha(),settings.FIREBALL_SCALE)

#caga imagenes de "baldosas"
tile_list = []
for x in range(settings.TILE_TYPES):
    tile_image = pygame.image.load(f"assets/images/tiles/{x}.png").convert_alpha()
    tile_image = pygame.transform.scale(tile_image, (settings.TILE_SIZE, settings.TILE_SIZE))
    tile_list.append(tile_image)


#carga de sprites de los personajes
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

#funcion para texto
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

#funcion para desplegar informacion en pantalla
def draw_info():
    #panel
    pygame.draw.rect(screen, settings.PANEL, (0, 0, settings.WIDTH, 50))
    pygame.draw.line(screen, settings.WHITE, (0, 50), (settings.WIDTH, 50))
    #dibujar corazones
    half_heart_drawn = False
    for i in range(5):
        if player.health >= ((i+1)*20): # salud = [20,40,60,80,100]
            screen.blit(heart_full,(10 + i * 50, 0))# separaciones = [10,60,110,160,210]
        elif player.health%20 > 0 and half_heart_drawn == False:
            screen.blit(heart_half,(10 + i * 50, 0))
            half_heart_drawn = True
        else:
            screen.blit(heart_empty,(10 + i * 50, 0))
        
    #mostra nivel
    draw_text(f"LEVEL: "+ str(level), font, settings.WHITE, settings.WIDTH/2, 15)

    #mostrar puntaje
    draw_text(f"X{player.score}", font, settings.WHITE, settings.WIDTH - 100, 15)

#funcion para resetear nivel
def reset_level():
    damage_text_group.empty()
    arrow_group.empty()
    item_group.empty()
    fireball_group.empty()

    #crear una lista vacia de baldosas
    #una "rejilla" vacia
    data = []
    for row in range(settings.ROWS):
        r = [-1]*settings.COLS
        data.append(r)

    return data

#clase de texto del daño
class DamageText(pygame.sprite.Sprite):

    def __init__(self,x,y,damage,color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.counter = 0
    
    def update(self):
        #reposicionamos el texto
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]
        # mover el textoo hacia arriba para darle un aspecto copadisimo
        self.rect.y -= 1
        #borra el texto despues de un tiempo
        self.counter += 1
        if self.counter > 30:
            self.kill()

#creando lista vacia de imagenes del nivel
world_data = []
for row in range(settings.ROWS):
    r = [-1] * settings.COLS
    world_data.append(r) # lleno primero con -1 para asignar un espacio vacio

#abrimos el archivo csv
with open(f"levels/level{level}_data.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter = ",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)#se pasan a entero el valor   

world = World()
world.process_data(world_data, tile_list, item_images, mob_animations)

#creacion jugador y enemigos
player = world.player
enemy_list = world.character_list

#dibujando arma
bow = Weapon(bow_image, arrow_image)
#crear grupo de sprites para las flechas y el texto de daño
damage_text_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
fireball_group = pygame.sprite.Group()

score_coin = Item(settings.WIDTH - 120, 23, 0, coin_images, True)
item_group.add(score_coin)

#agrega los item de los datos de nivel
for item in world.item_list:
    item_group.add(item) 

#*Main loop-----------------------------------------
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

    #? ----- actualizaciones
    #actualizar movimiento jugador
    screen_scroll, level_complete = player.move(dx, dy, world.obstacle_tiles, world.exit_tile)
    
    #actualizar todos los objetos
    world.update(screen_scroll)

    #actualizar enemigo
    for enemy in enemy_list:
        fireball = enemy.ai(player, world.obstacle_tiles, screen_scroll, fireball_image)
        if fireball:
            fireball_group.add(fireball)
        if enemy.alive:
            enemy.update()
    #actualizar jugador
    player.update()
    #actualiza flecha
    arrow = bow.update(player)
    if arrow:
        arrow_group.add(arrow)
    for arrow in arrow_group:
        damage, damage_pos = arrow.update(screen_scroll, world.obstacle_tiles, enemy_list) #retorna 2 valores
        if damage:
            damage_text = DamageText(damage_pos.centerx,damage_pos.y,str(damage),settings.RED)
            damage_text_group.add(damage_text)
    
    damage_text_group.update()
    fireball_group.update(screen_scroll, player)
    item_group.update(screen_scroll, player)

    #? ----- dibujados
    #dibujo escenario
    world.draw(screen)

    #dibujar jugador y arma
    for enemy in enemy_list:
        enemy.draw(screen)
    player.draw(screen)
    bow.draw(screen)
    for arrow in arrow_group:
        arrow.draw(screen)
    for fireball in fireball_group:
        fireball.draw(screen)
    damage_text_group.draw(screen)
    item_group.draw(screen)
    draw_info()
    score_coin.draw(screen)

    #chequeamos si el nivel esta completo y cambiamos
    if level_complete == True:
        level += 1
        #borramos la data anterior
        world_data = reset_level()
        #abrimos el nuevo archivo csv
        with open(f"levels/level{level}_data.csv", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter = ",")
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)#se pasan a entero el valor

        world = World()
        world.process_data(world_data, tile_list, item_images, mob_animations) 

    #? eventos--------------------------------------------

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