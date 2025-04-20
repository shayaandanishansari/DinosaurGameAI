import pygame

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

GROUND_Y = 550
PLAYER_START_X = 50

GRAVITY = 0.8
JUMP_POWER = -18
JUMP_CUT_FACTOR = 0.5

ANIMATION_SPEED = 100
BIRD_ANIMATION_SPEED = 150

INITIAL_GAME_SPEED = 5
MAX_GAME_SPEED = 15
SPEED_INCREASE_RATE = 0.0005

OBSTACLE_MIN_SPAWN_DELAY_MS = 900
OBSTACLE_MAX_SPAWN_DELAY_MS = 2500
BIRD_FLY_LOW_Y = GROUND_Y - 35
BIRD_FLY_HIGH_Y = GROUND_Y - 120

GROUND_SPEED_FACTOR = 1.0
CLOUD_SPEED_FACTOR = 0.5
CACTUS_SPEED_FACTOR = 1.0
BIRD_SPEED_FACTOR = 1.2

PLAYER_RUN_IMAGES_INDEX = 0
PLAYER_JUMP_IMAGES_INDEX = 1
PLAYER_DUCK_IMAGES_INDEX = 2
PLAYER_AIR_IMAGE_INDEX = 3
PLAYER_DEAD_IMAGE_INDEX = 4
PLAYER_AIR_IMAGE_SCALE_FACTOR = 4

IMAGE_PATHS = {
    "player": [
        ['Assets/dinorun.png', 'Assets/dinorun1.png'],
        ['Assets/dinoJump.png'],
        ['Assets/dinoduck.png', 'Assets/dinoduck2.png'],
        ['Assets/dino.png'],
        ['Assets/dinoDead.png']
    ],
    "bird": [
        'Assets/bird.png', 'Assets/bird2.png' # Corrected key from user example
    ],
    "cactus": [
        'Assets/cactusBig.png',
        'Assets/cactusSmall.png',
        'Assets/cactusSmallMany.png'
    ],
    "ground": [ # Expecting single path in list
        'Assets/ground.png'
    ],
    "cloud": [ # Expecting single path in list
        'Assets/cloud.png'
    ]
}

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)