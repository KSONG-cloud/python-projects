import pygame
import json
from units import Vegetable, Enemy


# Constants for window size
WIDTH, HEIGHT       = 800, 400

BASE_COORDS         = (10,HEIGHT - 20)                       # Bottom Left
ENEMY_BASE_COORDS   = (WIDTH - 10,HEIGHT - 20)      # Bottom Right
BASE_IMG_DIMENSION  = (100,100)


# Load config files
with open("unit_config.json") as f:
    UNIT_CONFIG = json.load(f)

with open("enemy_config.json") as f:
    ENEMY_CONFIG = json.load(f)


def create_veggie(name):
    config = UNIT_CONFIG[name]
    image = pygame.image.load(config['image_path']).convert_alpha()
    image = pygame.transform.scale(image, (60,60))
    rect = image.get_rect(bottomleft=BASE_COORDS)


    return Vegetable(
        health = config['health'],
        damage = config['damage'],
        speed = config['speed'],
        rect = rect,
        image = image,
        attack_range = config['attack_range'],
        last_attack_time=0,
        attack_delay = config['attack_delay']
    )


def create_enemy(name):
    config = ENEMY_CONFIG[name]
    image = pygame.image.load(config['image_path']).convert_alpha()
    image = pygame.transform.scale(image, (60, 60))
    rect = image.get_rect(bottomright=ENEMY_BASE_COORDS)

    return Enemy(
        health=config["health"],
        damage=config["damage"],
        speed=config["speed"],
        rect=rect,
        image=image,
        attack_range=config['attack_range'],
        last_attack_time=0,
        attack_delay=config["attack_delay"]
    )




























































































