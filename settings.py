import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

GROUND_Y = 550
PLAYER_START_X = 50

GRAVITY = 0.8
JUMP_POWER = -18
JUMP_CUT_FACTOR = 0.5

ANIMATION_SPEED = 100 # Milliseconds per frame

PLAYER_RUN_IMAGES_INDEX = 0
PLAYER_JUMP_IMAGES_INDEX = 1
PLAYER_DUCK_IMAGES_INDEX = 2
PLAYER_AIR_IMAGE_INDEX = 3
PLAYER_DEAD_IMAGE_INDEX = 4
PLAYER_AIR_IMAGE_SCALE_FACTOR = 4
FAST_FALL_MULTIPLIER = 3

IMAGE_PATHS = {
    "player":[
    ['Assets/dinorun.png', 'Assets/dinorun1.png'],
    ['Assets/dinoJump.png'],
    ['Assets/dinoduck.png', 'Assets/dinoduck2.png'],
    ['Assets/dino.png'],
    ['Assets/dinoDead.png']
    ],

    "bird":[
    'Assets/bird.png', 'Assets/bird2.png'
    ]
}

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)