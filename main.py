import sys, pygame, time, os
from pygame.locals import *
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
clock = pygame.time.Clock()

display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RPG GAME")

#COLOR
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

player_image = pygame.image.load(os.path.join("assets/Player/Idle/Down/player_0.png"))
player_rect = player_image.get_rect()
player_rect.left = 180
player_rect.top = 140

player_direction = "down"
player_run = False
player_index_frame = 0


def load_anim_frames():
    frames = {
        "run": {
            'left': [],
            'right': [],
            'up': [],
            'down': []
        },
        "idle": {
            'left': [],
            'right': [],
            'up': [],
            'down': []
        }
    }
    run_left = os.listdir("assets/Player/Run/Right")
    for image in run_left:
        path = os.path.join("assets/Player/Run/Right", image)
        img = pygame.image.load(path)
        frames['run']['left'].append(img)
    run_right = os.listdir("assets/Player/Run/Left")
    for image in run_right:
        path = os.path.join("assets/Player/Run/Left", image)
        img = pygame.image.load(path)
        frames['run']['right'].append(img)
    run_up = os.listdir("assets/Player/Run/Up")
    for image in run_up:
        path = os.path.join("assets/Player/Run/Up", image)
        img = pygame.image.load(path)
        frames['run']['up'].append(img)
    run_down = os.listdir("assets/Player/Run/Down")
    for image in run_down:
        path = os.path.join("assets/Player/Run/Down", image)
        img = pygame.image.load(path)
        frames['run']['down'].append(img)
    idle_left = os.listdir("assets/Player/Idle/Right")
    for image in idle_left:
        path = os.path.join("assets/Player/Idle/Right", image)
        img = pygame.image.load(path)
        frames['idle']['left'].append(img)
    idle_right = os.listdir("assets/Player/Idle/Left")
    for image in idle_right:
        path = os.path.join("assets/Player/Idle/Left", image)
        img = pygame.image.load(path)
        frames['idle']['right'].append(img)
    idle_up = os.listdir("assets/Player/Idle/up")
    for image in idle_up:
        path = os.path.join("assets/Player/Idle/up", image)
        img = pygame.image.load(path)
        frames['idle']['up'].append(img)
    idle_down = os.listdir("assets/Player/Idle/down")
    for image in idle_down:
        path = os.path.join("assets/Player/Idle/down", image)
        img = pygame.image.load(path)
        frames['idle']['down'].append(img)

    return frames


player_frames = load_anim_frames()

while True:
    display.fill(WHITE)
    display.blit(player_image, player_rect)

    # CHANGE ANIMATION FRAMES
    if player_run:
        player_image = player_frames["run"][player_direction][player_index_frame]
    else:
        player_image = player_frames["idle"][player_direction][player_index_frame]
    player_index_frame += 1
    if player_index_frame == 6:
        player_index_frame = 0

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            player_run = True
            if event.key == K_s:
                player_direction = "down"
            elif event.key == K_w:
                player_direction = "up"
            elif event.key == K_a:
                player_direction = "left"
            elif event.key == K_d:
                player_direction = "right"
        if event.type == KEYUP:
            player_run = False

    pygame.display.update()
    clock.tick(FPS)

