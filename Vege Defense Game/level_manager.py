import pygame
from time import time
from random import randint
from units import Apple, Banana, Orange, Grape, Pineapple, Mango, Watermelon, Strawberry, Cherry, Coconut, Lemon


level_data = {
            # 1: [
            #     {"time": 2000, "enemy": Apple},
            #     {"time": 5000, "enemy": Orange},
            #     {"time": 10000, "enemy": Pineapple},
            #     {"time": 15000, "enemy": Apple},
            # ],
            # 2: [
            #     {"time": 2000, "enemy": Orange},
            #     {"time": 5000, "enemy": Pineapple},
            #     {"time": 8000, "enemy": Apple},
            #     {"time": 12000, "enemy": Pineapple},
            # ]
            1: [
                (Apple, 2000),   # Spawn Apple enemy at 2000 ms
                (Banana, 4000),  # Spawn Banana enemy at 4000 ms
                (Cherry, 6000),  # Spawn Cherry enemy at 6000 ms
            ],
            2: [
                (Pineapple, 3000),
                (Grape, 5000),
                (Lemon, 7000),
            ],
            3: [
                (Lemon, 1000),
                (Mango, 3000),
                (Orange, 5000),
                (Pineapple, 7000),
            ],
        }



class LevelManager:
    def __init__(self, level):
        self.level_data = level_data[level].copy()
        self.level_start_time = pygame.time.get_ticks()

    # Handles enemy spawning based on current time
    def update(self, current_time):
        if not self.level_data:
            return []

        events = []
        for enemy_class, spawn_time in self.level_data:
            if current_time - self.level_start_time >= spawn_time:
                events.append((enemy_class, spawn_time))
                

        # Remove enemies that have been spawned
        enemies_to_spawn = []
        for enemy_class, spawn_time in events:
            self.level_data.remove((enemy_class, spawn_time))
            enemy = enemy_class()
            enemies_to_spawn.append(enemy)

        return enemies_to_spawn



