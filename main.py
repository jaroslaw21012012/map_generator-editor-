import sys, pygame, time, os
import ctypes, easygui
from pygame.locals import *
from constants import *
from models import Menu, Map, Button, Input

pygame.init()
clock = pygame.time.Clock()
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)



tiles_images = os.listdir(PATH_TILES)

tiles = [pygame.image.load(os.path.join(PATH_TILES, tile)) for tile in tiles_images]
menu = Menu(display, tiles)


opened_menu = True

layer_font = pygame.font.SysFont('Arial', 16)
common_text = {
    1: "BOTTOM LAYER",
    0: "TOP LAYER"
}

mouse = False

x_pos, y_pos = 0, 0
mode = MENU

btn_new = Button("Create new map", pygame.Rect(300, 300, 200, 50), BLACK, PATH_FONT, 30)
btn_continue = Button("Open old map", pygame.Rect(300, 400, 200, 50), BLACK, PATH_FONT, 30)
btn_create = Button("CREATE MAP", pygame.rect.Rect(525, 350, 170, 50), BLACK, PATH_FONT, 30)

input_width = Input(pygame.Rect(150, 300, 200, 50), BLACK, BG_MENU_BTN, "Enter count of blocks for width:", PATH_FONT, 30, 14)
input_height = Input(pygame.Rect(150, 400, 200, 50), BLACK, BG_MENU_BTN, "Enter count of blocks for height:", PATH_FONT, 30, 14)

value_width = '50'
value_height = '50'
swipe = 0

board = Map(display)

while True:
    display.fill(WHITE)
    if mode == MENU:
        display.fill(BG_MENU)
        btn_new.draw(display, BG_MENU_BTN)
        btn_continue.draw(display, BG_MENU_BTN)
    elif mode == SETTINGS:
        display.fill(BG_MENU)
        input_width.draw(display, board.width)
        input_height.draw(display, board.height)
        btn_create.draw(display, BG_MENU_BTN)
    elif mode == EDITOR:
        board.draw(tiles)
        pygame.draw.rect(display, RED, (12, 500, 85, 85), border_radius=5)
        display.blit(pygame.transform.scale(tiles[board.choosed_tile], (64, 64)), pygame.Rect(25, 510, 64, 64))
        if opened_menu:

            menu.draw(swipe)
        layer_text_surface = layer_font.render(f"Choosed Layer: {common_text.get(board.choosed_layer)}", True, BLACK)
        display.blit(layer_text_surface, (100, 570))
    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if mode == EDITOR:
                if event.key == K_RIGHT:
                    board.choosed_layer = 1
                elif event.key == K_LEFT:
                    board.choosed_layer = 0
                elif event.key == K_1:
                    board.export_map()
                elif event.key == K_SPACE:
                    opened_menu = True
                elif event.key == K_ESCAPE:
                    opened_menu = False
            elif mode == SETTINGS:
                if event.key == K_BACKSPACE:
                    if input_width.active:
                        if len(value_width) > 1:
                            value_width = value_width[:-1]
                        elif len(value_width) == 1:
                            value_width = "0"
                    elif input_height.active:
                        if len(value_height) > 1:
                            value_height = value_height[:-1]
                        elif len(value_height) == 1:
                            value_height = "0"
                if event.key == K_1:
                    if input_width.active:
                        value_width += "1"
                    elif input_height.active:
                        value_height += "1"
                elif event.key == K_2:
                    if input_width.active:
                        value_width += "2"
                    elif input_height.active:
                        value_height += "2"
                elif event.key == K_3:
                    if input_width.active:
                        value_width += "3"
                    elif input_height.active:
                        value_height += "3"
                elif event.key == K_4:
                    if input_width.active:
                        value_width += "4"
                    elif input_height.active:
                        value_height += "4"
                elif event.key == K_5:
                    if input_width.active:
                        value_width += "5"
                    elif input_height.active:
                        value_height += "5"
                elif event.key == K_6:
                    if input_width.active:
                        value_width += "6"
                    elif input_height.active:
                        value_height += "6"
                elif event.key == K_7:
                    if input_width.active:
                        value_width += "7"
                    elif input_height.active:
                        value_height += "7"
                elif event.key == K_8:
                    if input_width.active:
                        value_width += "8"
                    elif input_height.active:
                        value_height += "8"
                elif event.key == K_9:
                    if input_width.active:
                        value_width += "9"
                    elif input_height.active:
                        value_height += "9"
                elif event.key == K_0:
                    if input_width.active:
                        value_width += "0"
                    elif input_height.active:
                        value_height += "0"
                if mode == SETTINGS and int(value_width) > 299:
                    value_width = "299"
                elif mode == SETTINGS and int(value_height) > 299:
                    value_height = "299"
                board.height = int(value_height)
                board.width = int(value_width)
        if event.type == MOUSEMOTION:
            x_pos, y_pos = event.pos
        if event.type == MOUSEBUTTONDOWN and event.type != MOUSEWHEEL:
            if opened_menu and mode == EDITOR:
                rect = pygame.Rect(x_pos, y_pos, 1, 1)
                index = rect.collidelist(menu.invisible_rects)
                if index != -1:
                    if index + 19 * swipe < len(tiles):
                        board.choosed_tile = index + 19 * swipe
                        opened_menu = False
                    break
            if not opened_menu and mode == EDITOR:
                mouse = True
                if pygame.Rect(25, 510, 64, 64).collidepoint(x_pos, y_pos):
                    mouse = False
                    opened_menu = True
            if mode == MENU and btn_continue.is_pressed(x_pos, y_pos):
                board.import_board()
                value_height = str(board.height)
                value_width = str(board.width)
                mode = EDITOR
            elif mode == MENU and btn_new.is_pressed(x_pos, y_pos):
                mode = SETTINGS
            if mode == SETTINGS and input_width.is_pressed(x_pos, y_pos):
                input_width.active = True
                input_height.active = False
            elif mode == SETTINGS and input_height.is_pressed(x_pos, y_pos):
                input_width.active = False
                input_height.active = True
            if mode == SETTINGS and btn_create.is_pressed(x_pos, y_pos):
                if int(value_width) > 4 and int(value_height) > 4:
                    input_width.active = False
                    input_height.active = False
                    board.width = int(value_width)
                    board.height = int(value_height)
                    board.create_new_board(board.path_map)
                    board.create_new_board(board.path_layer)
                    board.import_board()
                    mode = EDITOR
                else:
                    value_width = "5"
                    value_height = "5"
                    ctypes.windll.user32.MessageBoxW(0, "Minimum size is 5x5!", "WARNING!!!", 0x0 | 0x30)
        elif event.type == MOUSEBUTTONUP:
            mouse = False
    keys = pygame.key.get_pressed()
    board.move(keys)
    if keys[K_DOWN]:
        swipe += 1
        if swipe >= (len(tiles) // 19) - 13:
            swipe = (len(tiles) // 19) - 13
    elif keys[K_UP]:
        swipe -= 1
        if swipe < 0:
            swipe = 0
    if mouse and not opened_menu and mode == EDITOR:
        board.update_tile(x_pos, y_pos)


    pygame.display.update()
    clock.tick(FPS)
    print(clock.get_fps())

# 17 FPS при карте 299x299, 406 строк в коде (22.09.24)