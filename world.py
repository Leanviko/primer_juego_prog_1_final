import pygame
import settings

class World():
    def __init__(self):
        self.map_tiles = [] # lista principal

    def process_data(self, data, tile_list):
        self.level_length = len(data)
        for y, row in enumerate(data):#los contadores x e y van a ser utiles en la posicion del cuadradito
            for x, tile in enumerate(row): 
                image = tile_list[tile]
                image_rect = image.get_rect()
                image_x = x * settings.TILE_SIZE
                image_y = y * settings.TILE_SIZE
                image_rect.center = (image_x, image_y)
                tile_data = [image, image_rect, image_x, image_y]

                #agregamos la data del "mosaico" el la lista principal
                if tile >=0:
                    self.map_tiles.append(tile_data)
    
    def update(self, screen_scroll):
        #reposisionamos las baldosas con el scroll del movimiento
        #el escenario se mueve alrededor del jugador
        # => tile: tile_data
        for tile in self.map_tiles:
            tile[2] += screen_scroll[0]
            tile[3] += screen_scroll[1]
            tile[1].center = (tile[2], tile[3])

    def draw(self, surface):
        #iteramos en cada tile_data dentro del principal
        for tile in self.map_tiles:
            surface.blit(tile[0],tile[1])