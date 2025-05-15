import pygame
import json
from units import Vegetable, Enemy, WIDTH, HEIGHT, BASE_COORDS, ENEMY_BASE_COORDS, BASE_IMG_DIMENSION


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


def get_unit_names():
    return list(UNIT_CONFIG.keys())

def get_unit_image_path(name):
    return UNIT_CONFIG[name]['image_path']

























































































