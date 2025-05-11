import pygame
import sys

# from main import veggies, enemies, base, enemy_base

# Constants for window size
WIDTH, HEIGHT       = 800, 400

BASE_COORDS         = (10,HEIGHT - 20)                       # Bottom Left
ENEMY_BASE_COORDS   = (WIDTH - 10,HEIGHT - 20)      # Bottom Right
BASE_IMG_DIMENSION  = (100,100)

# Constants for gameplay
BASE_DAMAGE_MULTIPLIER = 10

# Class for a unit in the game
class Vegetable:
    def __init__(self, health, damage, speed, rect, image):
        self.health = health
        self.damage = damage
        self.speed = speed
        self.rect = rect
        self.x = rect.x
        self.y = rect.y
        self.image = image


    def move(self, enemies, enemy_base):
        if not self.is_blocked_by_enemy(enemies) and not self.is_blocked_by_base(enemy_base):
            self.x += self.speed
            self.rect.x += self.speed
            

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"HP: {self.health}", True, (0,255, 0))
        surface.blit(health_text, (self.rect.x, self.rect.y - 20))


    def check_collision(self, enemy):
        # Check for collision with an enemy
        if self.rect.colliderect(enemy.rect):
            self.attack(enemy)
    

    def take_damage(self, damage):
        self.health -= damage  # Reduce health when the veggie is attacked


    def attack(self, enemy):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_delay:
            enemy.take_damage(self.damage)
            self.last_attack_time = current_time


    def is_blocked_by_enemy(self, enemies):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                return True
        return False
    

    def is_blocked_by_base(self, base):
        return self.rect.colliderect(base.rect)


class Carrot(Vegetable):
    def __init__(self):  
        self.image = pygame.image.load("assets/carrot2.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60,60))
        self.rect = self.image.get_rect(bottomleft=BASE_COORDS)
        self.attack_delay = 500
        self.last_attack_time = 0
        super().__init__(health=5, damage=1, speed=1, rect=self.rect, image=self.image)

class Broccoli(Vegetable):
    def __init__(self):
        self.image = pygame.image.load("assets/broccoli.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect(bottomleft=BASE_COORDS)
        self.attack_delay = 600
        self.last_attack_time = 0
        super().__init__(health=10, damage=2, speed=6, rect=self.rect, image=self.image)


class Tomato(Vegetable):
    def __init__(self):
        self.image = pygame.image.load("assets/tomato.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect(bottomleft=BASE_COORDS)
        self.attack_delay = 400
        self.last_attack_time = 0
        super().__init__(health=4, damage=3, speed=12, rect=self.rect, image=self.image)


class Lettuce(Vegetable):
    def __init__(self):
        self.image = pygame.image.load("assets/lettuce.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect(bottomleft=BASE_COORDS)
        self.attack_delay = 500
        self.last_attack_time = 0
        super().__init__(health=6, damage=1, speed=8, rect=self.rect, image=self.image)


class Eggplant(Vegetable):
    def __init__(self):
        self.image = pygame.image.load("assets/eggplant.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect(bottomleft=BASE_COORDS)
        self.attack_delay = 700
        self.last_attack_time = 0
        super().__init__(health=8, damage=4, speed=5, rect=self.rect, image=self.image)


class Corn(Vegetable):
    def __init__(self):
        self.image = pygame.image.load("assets/corn.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect(bottomleft=BASE_COORDS)
        self.attack_delay = 450
        self.last_attack_time = 0
        super().__init__(health=7, damage=2, speed=9, rect=self.rect, image=self.image)


class Onion(Vegetable):
    def __init__(self):
        self.image = pygame.image.load("assets/onion.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect(bottomleft=BASE_COORDS)
        self.attack_delay = 480
        self.last_attack_time = 0
        super().__init__(health=5, damage=3, speed=7, rect=self.rect, image=self.image)


class Pepper(Vegetable):
    def __init__(self):
        self.image = pygame.image.load("assets/pepper.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect(bottomleft=BASE_COORDS)
        self.attack_delay = 520
        self.last_attack_time = 0
        super().__init__(health=6, damage=2, speed=11, rect=self.rect, image=self.image)


class Cabbage(Vegetable):
    def __init__(self):
        self.image = pygame.image.load("assets/cabbage.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect(bottomleft=BASE_COORDS)
        self.attack_delay = 550
        self.last_attack_time = 0
        super().__init__(health=9, damage=1, speed=6, rect=self.rect, image=self.image)


class Zucchini(Vegetable):
    def __init__(self):
        self.image = pygame.image.load("assets/zucchini.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect(bottomleft=BASE_COORDS)
        self.attack_delay = 470
        self.last_attack_time = 0
        super().__init__(health=6, damage=3, speed=10, rect=self.rect, image=self.image)




class Base:
    def __init__(self, on_destroy=None):
        self.image = pygame.image.load("assets/base.png")
        self.image = pygame.transform.scale(self.image, BASE_IMG_DIMENSION)
        self.rect = self.image.get_rect(bottomleft=BASE_COORDS)
        self.health = 5
        self.on_destroy = on_destroy   # Store callback function for when base gets destroy



    def draw(self, surface):
        surface.blit(self.image, self.rect)
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"Base HP: {self.health}", True, (0,0,0))
        surface.blit(health_text, (self.rect.x -50, self.rect.y -20))

    def take_damage(self, damage):
        self.health -= damage
        print(f"Base health: {self.health}")
        if self.health <= 0:
            if self.on_destroy:
                self.on_destroy()      # Call the callback function when base is destroyed


class Enemy: 
    def __init__(self, health, damage, speed, rect, image):  
        self.image = image  
        self.rect = rect
        self.x = self.rect.x
        self.y = self.rect.y
        self.health = health
        self.speed = speed
        self.damage = damage



    def move(self, enemies, enemy_base):
        if not self.is_blocked_by_enemy(enemies) and not self.is_blocked_by_base(enemy_base):
            self.x -= self.speed
            self.rect.x -= self.speed


    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"HP: {self.health}", True, (255, 0, 0))
        surface.blit(health_text, (self.rect.x, self.rect.y - 20))


    def check_collision(self, enemy):
        # Check for collision with an enemy
        if self.rect.colliderect(enemy.rect):
            self.attack(enemy)
    

    def is_blocked_by_enemy(self, enemies):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                return True
        return False


    def is_blocked_by_base(self, base):
        return self.rect.colliderect(base.rect)
  

    def take_damage(self, damage):
        self.health -= damage 
        

    def attack(self, vege):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_delay:
            vege.take_damage(self.damage)  # Deal damage to the vege
            self.last_attack_time = current_time


class Apple(Enemy):
    def __init__(self):  
        self.image = pygame.image.load("assets/apple.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect(bottomright=ENEMY_BASE_COORDS)
        self.attack_delay = 500
        self.last_attack_time = 0
        super().__init__(health=15, damage=1, speed=10, rect=self.rect, image=self.image)


class Banana(Enemy):
    def __init__(self):  
        self.image = pygame.image.load("assets/banana.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(bottomright=ENEMY_BASE_COORDS)
        self.attack_delay = 600
        self.last_attack_time = 0
        super().__init__(health=10, damage=1, speed=12, rect=self.rect, image=self.image)

class Orange(Enemy):
    def __init__(self):  
        self.image = pygame.image.load("assets/orange.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(bottomright=ENEMY_BASE_COORDS)
        self.attack_delay = 450
        self.last_attack_time = 0
        super().__init__(health=12, damage=2, speed=8, rect=self.rect, image=self.image)

class Grape(Enemy):
    def __init__(self):  
        self.image = pygame.image.load("assets/grape.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(bottomright=ENEMY_BASE_COORDS)
        self.attack_delay = 700
        self.last_attack_time = 0
        super().__init__(health=8, damage=3, speed=6, rect=self.rect, image=self.image)

class Pineapple(Enemy):
    def __init__(self):  
        self.image = pygame.image.load("assets/pineapple.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(bottomright=ENEMY_BASE_COORDS)
        self.attack_delay = 550
        self.last_attack_time = 0
        super().__init__(health=15, damage=2, speed=9, rect=self.rect, image=self.image)

class Mango(Enemy):
    def __init__(self):  
        self.image = pygame.image.load("assets/mango.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(bottomright=ENEMY_BASE_COORDS)
        self.attack_delay = 400
        self.last_attack_time = 0
        super().__init__(health=10, damage=4, speed=7, rect=self.rect, image=self.image)

class Watermelon(Enemy):
    def __init__(self):  
        self.image = pygame.image.load("assets/watermelon.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(bottomright=ENEMY_BASE_COORDS)
        self.attack_delay = 500
        self.last_attack_time = 0
        super().__init__(health=18, damage=1, speed=6, rect=self.rect, image=self.image)

class Strawberry(Enemy):
    def __init__(self):  
        self.image = pygame.image.load("assets/strawberry.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(bottomright=ENEMY_BASE_COORDS)
        self.attack_delay = 650
        self.last_attack_time = 0
        super().__init__(health=7, damage=3, speed=10, rect=self.rect, image=self.image)

class Cherry(Enemy):
    def __init__(self):  
        self.image = pygame.image.load("assets/cherry.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(bottomright=ENEMY_BASE_COORDS)
        self.attack_delay = 600
        self.last_attack_time = 0
        super().__init__(health=9, damage=2, speed=8, rect=self.rect, image=self.image)

class Coconut(Enemy):
    def __init__(self):  
        self.image = pygame.image.load("assets/coconut.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(bottomright=ENEMY_BASE_COORDS)
        self.attack_delay = 550
        self.last_attack_time = 0
        super().__init__(health=16, damage=3, speed=5, rect=self.rect, image=self.image)

class Lemon(Enemy):
    def __init__(self):  
        self.image = pygame.image.load("assets/lemon.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(bottomright=ENEMY_BASE_COORDS)
        self.attack_delay = 500
        self.last_attack_time = 0
        super().__init__(health=11, damage=2, speed=9, rect=self.rect, image=self.image)

        
class EnemyBase:
    def __init__(self, on_destroy=None):
        self.image = pygame.image.load("assets/enemy_base.png")
        self.image = pygame.transform.scale(self.image, BASE_IMG_DIMENSION)
        self.rect = self.image.get_rect(bottomright=ENEMY_BASE_COORDS)
        self.health = 10
        self.on_destroy = on_destroy  # Store callback function for when base gets destroy


    def draw(self, surface):
        surface.blit(self.image, self.rect)
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"Base HP: {self.health}", True, (0,0,0))
        surface.blit(health_text, (self.rect.x -50, self.rect.y -20))


    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            if self.on_destroy:
                self.on_destroy()           # Call the callback function when enemy base is destroyed

                
            

# Function for removing dead entities
def return_alive(entities):
    alive_entities = []
    for entity in entities:
        if entity.health > 0:
            alive_entities.append(entity)
    
    return  alive_entities
