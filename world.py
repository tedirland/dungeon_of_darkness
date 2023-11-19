from items import Item
from constants import TILE_SIZE


class World():
    def __init__(self) -> None:
        self.map_tiles = []
        self.obstacles_tiles = []
        self.exit_tile = None
        self.item_list = []

    def process_data(self, data, tile_list, item_images):
        self.level_length = len(data)
        # iterate through each value in level data
        for y,row in enumerate(data):
            for x,tile in enumerate(row):
                image = tile_list[tile]
                image_rect = image.get_rect()
                image_x = x * TILE_SIZE
                image_y = y * TILE_SIZE
                image_rect.center = (image_x, image_y)
                tile_data = [image, image_rect, image_x, image_y]

                # draw walls/obstacles
                if tile == 7:
                    self.obstacles_tiles.append(tile_data)
                # draw exit tile
                elif tile == 7:
                    self.exit_tile = tile_data
                if tile == 9:
                    coin = Item(image_x, image_y,0, item_images[0])
                    self.item_list.append(coin)
                    tile_data[0] = tile_list[0]
                



                
                # add image data to main tiles list
                if tile >= 0:
                    self.map_tiles.append(tile_data)
    def draw(self, surface):
        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])

    def update(self, screen_scroll):
        for tile in self.map_tiles:
            tile[2] += screen_scroll[0]
            tile[3] += screen_scroll[1]
            tile[1].center = (tile[2],tile[3])