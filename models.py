import pygame
from pygame.locals import *
class Map:
    def __init__(self, display, width: int = 50, height: int = 50):
        self.path_map = "maps/map1.txt"
        self.path_layer = "maps/layer1.txt"
        self.width = width
        self.height = height
        self.map = []
        self.layer = []
        self.move_x = 0
        self.move_y = 0
        self.display = display
        self.choosed_layer = 1
        self.choosed_tile = 0

    def create_new_board(self, path):
        with open(path, "w") as f:
            row = " ".join(["0" for x in range(self.width)]) + "\n"
            f.write(row)
            for y in range(self.height - 2):
                row = "0 " + " ".join(["1" for x in range(self.width - 2)]) + " 0\n"
                f.write(row)
            row = " ".join(["0" for x in range(self.width)]) + "\n"
            f.write(row)

    def import_board(self):
        with open(self.path_map, "r") as f:
            rows = []
            lines = f.readlines()
            for line in lines:
                row = line.replace("\n", "").split()
                row = [int(x) for x in row]
                rows.append(row)
            self.map = rows

        with open(self.path_layer, "r") as f:
            rows = []
            lines = f.readlines()
            for line in lines:
                row = line.replace("\n", "").split()
                row = [int(x) for x in row]
                rows.append(row)
            self.layer = rows

    def export_map(self):
        with open(self.path_map, "w") as f:
            for row in self.map:
                f.write(" ".join([str(x) for x in row]) + "\n")

        with open(self.path_layer, "w") as f:
            for row in self.layer:
                f.write(" ".join([str(x) for x in row]) + "\n")

    def draw(self, tiles):
        for y in range(self.height):
            for x in range(self.width):
                left = self.move_x + x * 32
                top = self.move_y + y * 32
                if self.map[y][x] != -1:
                    tile = tiles[self.map[y][x]]
                    self.display.blit(tile, pygame.Rect(left, top, 32, 32))
                if self.layer[y][x] != -1:
                    tile = tiles[self.layer[y][x]]
                    self.display.blit(tile, pygame.Rect(left, top, 32, 32))

    def move(self, keys):
        if keys[K_d]:
            self.move_x -= 32
        elif keys[K_a]:
            self.move_x += 32
        elif keys[K_w]:
            self.move_y += 32
        elif keys[K_s]:
            self.move_y -= 32

    def update_tile(self, x_pos, y_pos):
        x = (x_pos - self.move_x) // 32
        y = (y_pos - self.move_y) // 32
        if 0 <= y <= self.height - 1 and 0 <= x <= self.width - 1:
            if self.choosed_layer == 1:
                self.map[y][x] = self.choosed_tile
            else:
                self.layer[y][x] = self.choosed_tile
class Menu:
    def __init__(self, display, tiles):
        self.window_bg = pygame.Surface((740, 540))  # the size of your rect
        self.window_bg.set_alpha(200)  # alpha level
        self.window_bg.fill((74, 58, 35))  # this fills the entire surface
        self.display = display
        self.tiles = tiles
        self.invisible_rects = self.create_invisible_rects()


    def draw(self, procrutka):
        self.display.blit(self.window_bg, (30, 30))  # (0,0) are the top-left coordinates
        for i in range(procrutka, 14 + procrutka):
            part_tiles = self.tiles[i * 19:(i + 1) * 19]
            for x, tile in enumerate(part_tiles):
                left = 52 + x * 32 + x * 5
                top = 52 + (i - procrutka) * 32 + (i - procrutka) * 5
                self.display.blit(tile, pygame.Rect(left, top, 32, 32))

    def create_invisible_rects(self):
        count_tiles = len(self.tiles)
        tiles = [x for x in range(count_tiles)]
        blocks = []

        for i in range(count_tiles // 19 + 1):
            part_tiles = tiles[i * 19:(i + 1) * 19]
            for x, tile in enumerate(part_tiles):
                left = 52 + x * 32 + x * 5
                top = 52 + i * 32 + i * 5
                blocks.append(pygame.Rect(left, top, 32, 32))
        return blocks