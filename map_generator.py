import sys, pygame, time, os
import ctypes, easygui
from pygame.locals import *
from constants import *

pygame.init()
clock = pygame.time.Clock()
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)


def create_new_map(value_width=50, value_height=50):
    with open("maps/map1.txt", "w") as f:
        row = " ".join(["0" for x in range(value_width)]) + "\n"
        f.write(row)
        for y in range(value_height - 2):
            row = "0 " + " ".join(["1" for x in range(value_width - 2)]) + " 0\n"
            f.write(row)
        row = " ".join(["0" for x in range(value_width)]) + "\n"
        f.write(row)


def create_new_bottom_layer(value_width = 50, value_height = 50):
    with open("maps/layer1.txt", "w") as f:
        row = " ".join(["0" for x in range(value_width)]) + "\n"
        f.write(row)
        for y in range(value_height - 2):
            row = "0 " + " ".join(["-1" for x in range(value_width - 2)]) + " 0\n"
            f.write(row)
        row = " ".join(["0" for x in range(value_width)]) + "\n"
        f.write(row)

def import_map():
    with open("maps/map1.txt", "r") as f:
        rows = []
        lines = f.readlines()
        for line in lines:
            row = line.replace("\n", "").split()
            row = [int(x) for x in row]
            rows.append(row)
        return rows


def import_bottom_layer():
    with open("maps/layer1.txt", "r") as f:
        rows = []
        lines = f.readlines()
        for line in lines:
            row = line.replace("\n", "").split()
            row = [int(x) for x in row]
            rows.append(row)
        return rows


def export_map(g_map):
    with open("maps/map1.txt", "w") as f:
        for row in g_map:
            f.write(" ".join([str(x) for x in row]) + "\n")


def export_bottom_layer(g_map):
    with open("maps/layer1.txt", "w") as f:
        for row in g_map:
            f.write(" ".join([str(x) for x in row]) + "\n")


def import_tiles():
    tiles = []
    tiles_images = os.listdir("assets/Tiles")
    for tile in tiles_images:
        image = os.path.join("assets/Tiles/", tile)
        image = pygame.image.load(image)
        tiles.append(image)
    return tiles


def draw_map(g_map, tiles, move_x, move_y):
    for y in range(len(g_map)):
        for x in range(len(g_map[y])):
            left = move_x + x * 32
            top = move_y + y * 32
            if g_map[y][x] != -1:
                tile = tiles[g_map[y][x]]
                display.blit(tile, pygame.Rect(left, top, 32, 32))


def draw_menu(tiles, procrutka = 0):
    #pygame.draw.rect(display, (242, 194, 126, 128), (30, 30, 740, 540), border_radius=4)

    window_bg = pygame.Surface((740, 540))  # the size of your rect
    window_bg.set_alpha(200)                # alpha level
    window_bg.fill((74, 58, 35))           # this fills the entire surface
    display.blit(window_bg, (30, 30))    # (0,0) are the top-left coordinates

    for i in range(procrutka, 14 + procrutka):
        part_tiles = tiles[i * 19:(i + 1) * 19]
        for x, tile in enumerate(part_tiles):
            left = 52 + x * 32 + x * 5
            top = 52 + (i - procrutka) * 32 + (i - procrutka) * 5
            display.blit(tile, pygame.Rect(left, top, 32, 32))


def create_invisible_tiles():
    count_tiles = len(os.listdir("assets/Tiles"))
    tiles = [x for x in range(count_tiles)]
    blocks = []

    for i in range(count_tiles // 19 + 1):
        part_tiles = tiles[i * 19:(i + 1) * 19]
        for x, tile in enumerate(part_tiles):
            left = 52 + x * 32 + x * 5
            top = 52 + i * 32 + i * 5
            blocks.append(pygame.Rect(left, top, 32, 32))
    return blocks










#create_new_bottom_layer()

g_map = import_map()
layer = import_bottom_layer()
tiles = import_tiles()
move_x = 0
move_y = 0

invisible_tiles = create_invisible_tiles()
mouse_pos = pygame.mouse.get_pos()
choosed_tile = 0
choosed_layer = 1
opened_menu = True

#layer_text
layer_font = pygame.font.SysFont('Arial', 16)
common_text = {
    0: "BOTTOM LAYER",
    1: "TOP LAYER"
}

mouse = False

x_pos, y_pos = 0, 0
mode = MENU
#font and buttons
btn_font = pygame.font.Font('fonts/Accuratist.otf', 30)
btn_new = pygame.Rect(300, 300, 200, 50)
btn_new_text = btn_font.render("Create new map", True, BLACK)
btn_new_text_rect = btn_new_text.get_rect()
btn_new_text_rect.center = btn_new.center
btn_continue = pygame.Rect(300, 400, 200, 50)
btn_continue_text = btn_font.render("Open old map", True, BLACK)
btn_continue_text_rect = btn_continue_text.get_rect()
btn_continue_text_rect.center = btn_continue.center



input_font = pygame.font.Font('fonts/Accuratist.otf', 30)
label_font = pygame.font.Font('fonts/Accuratist.otf', 14)
def draw_input_width(value_width):
    input_width = pygame.Rect(150, 300, 200, 50)
    input_width_text = btn_font.render(f"{value_width}", True, BLACK)
    input_width_text_rect = input_width_text.get_rect()
    input_width_text_rect.center = input_width.center
    pygame.draw.rect(display, BG_MENU_BTN, input_width, border_radius=5)
    display.blit(input_width_text, input_width_text_rect)
    label_width = label_font.render("Enter count of blocks for width:", True, BLACK)
    label_width_rect = label_width.get_rect()
    label_width_rect.top = input_width.top - 20
    label_width_rect.left = input_width.left + 5
    display.blit(label_width, label_width_rect)

def draw_input_height(value_height):
    input_height = pygame.Rect(150, 400, 200, 50)
    input_height_text = btn_font.render(f"{value_height}", True, BLACK)
    input_height_text_rect = input_height_text.get_rect()
    input_height_text_rect.center = input_height.center
    label_height = label_font.render("Enter count of blocks for height:", True, BLACK)
    label_height_rect = label_height.get_rect()
    label_height_rect.top = input_height.top - 20
    label_height_rect.left = input_height.left + 5
    pygame.draw.rect(display, BG_MENU_BTN, input_height, border_radius=5)
    display.blit(input_height_text, input_height_text_rect)
    display.blit(label_height, label_height_rect)
input_height_invisible = pygame.Rect(150, 400, 200, 50)
input_width_invisible = pygame.Rect(150, 300, 200, 50)



active_input_width = True
active_input_height = False
value_width = '50'
value_height = '50'

swipe = 0


btn_create = pygame.rect.Rect(525, 350, 170, 50)
btn_create_text = btn_font.render(f"CREATE MAP", True, BLACK)
btn_create_text_rect = btn_create_text.get_rect()
btn_create_text_rect.center = btn_create.center






while True:
    display.fill(WHITE)
    if mode == MENU:
        display.fill(BG_MENU)
        pygame.draw.rect(display, BG_MENU_BTN, btn_new, border_radius=5)
        display.blit(btn_new_text, btn_new_text_rect)
        pygame.draw.rect(display, BG_MENU_BTN, btn_continue, border_radius=5)
        display.blit(btn_continue_text, btn_continue_text_rect)
    elif mode == SETTINGS:
        display.fill(BG_MENU)
        draw_input_width(int(value_width))
        draw_input_height(int(value_height))
        pygame.draw.rect(display, BG_MENU_BTN, btn_create, border_radius=10)
        display.blit(btn_create_text, btn_create_text_rect)
    elif mode == EDITOR:
        draw_map(layer, tiles, move_x, move_y)
        draw_map(g_map, tiles, move_x, move_y)
        pygame.draw.rect(display, RED, (12, 500, 85, 85), border_radius=5)
        display.blit(pygame.transform.scale(tiles[choosed_tile], (64, 64)), pygame.Rect(25, 510, 64, 64))
        if opened_menu:
            draw_menu(tiles, swipe)
        layer_text_surface = layer_font.render(f"Choosed Layer: {common_text.get(choosed_layer)}", True, BLACK)
        display.blit(layer_text_surface, (100, 570))
    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if mode == EDITOR:
                if event.key == K_RIGHT:
                    choosed_layer = 1
                elif event.key == K_LEFT:
                    choosed_layer = 0
                elif event.key == K_2:
                    export_map(g_map)
                    export_bottom_layer(layer)
                elif event.key == K_SPACE:
                    opened_menu = True
                elif event.key == K_ESCAPE:
                    opened_menu = False
            elif mode == SETTINGS:
                if event.key == K_BACKSPACE:
                    if active_input_width:
                        if len(value_width) > 1:
                            value_width = value_width[:-1]
                        elif len(value_width) == 1:
                            value_width = "0"
                    elif active_input_height:
                        if len(value_height) > 1:
                            value_height = value_height[:-1]
                        elif len(value_height) == 1:
                            value_height = "0"
                if event.key == K_1:
                    if active_input_width:
                        value_width += "1"
                    elif active_input_height:
                        value_height += "1"
                elif event.key == K_2:
                    if active_input_width:
                        value_width += "2"
                    elif active_input_height:
                        value_height += "2"
                elif event.key == K_3:
                    if active_input_width:
                        value_width += "3"
                    elif active_input_height:
                        value_height += "3"
                elif event.key == K_4:
                    if active_input_width:
                        value_width += "4"
                    elif active_input_height:
                        value_height += "4"
                elif event.key == K_5:
                    if active_input_width:
                        value_width += "5"
                    elif active_input_height:
                        value_height += "5"
                elif event.key == K_6:
                    if active_input_width:
                        value_width += "6"
                    elif active_input_height:
                        value_height += "6"
                elif event.key == K_7:
                    if active_input_width:
                        value_width += "7"
                    elif active_input_height:
                        value_height += "7"
                elif event.key == K_8:
                    if active_input_width:
                        value_width += "8"
                    elif active_input_height:
                        value_height += "8"
                elif event.key == K_9:
                    if active_input_width:
                        value_width += "9"
                    elif active_input_height:
                        value_height += "9"
                elif event.key == K_0:
                    if active_input_width:
                        value_width += "0"
                    elif active_input_height:
                        value_height += "0"
                if mode == SETTINGS and int(value_width) > 299:
                    value_width = "299"
                elif mode == SETTINGS and int(value_height) > 299:
                    value_height = "299"
        if event.type == MOUSEMOTION:
            x_pos, y_pos = event.pos
        if event.type == MOUSEBUTTONDOWN and event.type != MOUSEWHEEL:
            if opened_menu and mode == EDITOR:
                rect = pygame.Rect(x_pos, y_pos, 1, 1)
                index = rect.collidelist(invisible_tiles)
                if index != -1:
                    if index + 19 * swipe < len(tiles):
                        choosed_tile = index + 19 * swipe
                        opened_menu = False
                    break
            if not opened_menu and mode == EDITOR:
                mouse = True
                if pygame.Rect(25, 510, 64, 64).collidepoint(x_pos, y_pos):
                    mouse = False
                    opened_menu = True
            if mode == MENU and btn_continue.collidepoint(x_pos, y_pos):
                g_map = import_map()
                value_height = str(len(g_map))
                value_width = str(len(g_map[0]))
                layer = import_bottom_layer()
                mode = EDITOR
            elif mode == MENU and btn_new.collidepoint(x_pos, y_pos):
                mode = SETTINGS
            if mode == SETTINGS and input_width_invisible.collidepoint(x_pos, y_pos):
                active_input_width = True
                active_input_height = False
            elif mode == SETTINGS and input_height_invisible.collidepoint(x_pos, y_pos):
                active_input_width = False
                active_input_height = True
            if mode == SETTINGS and btn_create.collidepoint(x_pos, y_pos):
                if int(value_width) > 4 and int(value_height) > 4:
                    active_input_width = False
                    active_input_height = False
                    create_new_map(int(value_width), int(value_height))
                    create_new_bottom_layer(int(value_width), int(value_height))
                    g_map = import_map()
                    layer = import_bottom_layer()
                    mode = EDITOR
                else:
                    value_width = "5"
                    value_height = "5"
                    ctypes.windll.user32.MessageBoxW(0, "Minimum size is 5x5!", "WARNING!!!", 0x0 | 0x30)
                    #easygui.msgbox("Lorem ipsum", "title", "okay")
        elif event.type == MOUSEBUTTONUP:
            mouse = False
    keys = pygame.key.get_pressed()
    if keys[K_d]:
        move_x -= 32
    elif keys[K_a]:
        move_x += 32
    elif keys[K_w]:
        move_y += 32
    elif keys[K_s]:
        move_y -= 32
    if keys[K_DOWN]:
        swipe += 1
        if swipe >= (len(tiles) // 19) - 13:
            swipe = (len(tiles) // 19) - 13
    elif keys[K_UP]:
        swipe -= 1
        if swipe < 0:
            swipe = 0
    if mouse and not opened_menu and mode == EDITOR:
        x = int((x_pos - move_x) / 32)
        y = int((y_pos - move_y) / 32)
        if 0 <= y <= int(value_height) - 1 and 0 <= x <= int(value_width) - 1:
            if choosed_layer == 1:
                g_map[y][x] = choosed_tile
            else:
                layer[y][x] = choosed_tile



    pygame.display.update()
    clock.tick(FPS)
    print(clock.get_fps())

# 17 FPS при карте 299x299, 406 строк в коде (22.09.24)