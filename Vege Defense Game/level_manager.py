import pygame
from time import time
from random import randint


level_data = {
            1: [
                ("Apple", 200),   # Spawn Apple enemy at 200 ms
                ("Banana", 4000),  # Spawn Banana enemy at 4000 ms
                ("Cherry", 6000),  # Spawn Cherry enemy at 6000 ms
            ],
            2: [
                ("Pineapple", 3000),
                ("Grape", 5000),
                ("Lemon", 7000),
            ],
            3: [
                ("Lemon", 1000),
                ("Mango", 3000),
                ("Orange", 5000),
                ("Pineapple", 7000),
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
            if current_time >= spawn_time:
                events.append((enemy_class, spawn_time))
                

        # Remove enemies that have been spawned
        enemies_to_spawn = []
        for enemy_class, spawn_time in events:
            self.level_data.remove((enemy_class, spawn_time))
            enemies_to_spawn.append(enemy_class)

        return enemies_to_spawn



