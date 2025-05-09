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
    def __init__(self):
        self.image = pygame.image.load("assets/carrot2.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60,60))
        # self.x = x
        # self.y = y
        # self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.rect = self.image.get_rect(bottomleft=BASE_COORDS)
        self.x = self.rect.x
        self.y = self.rect.y
        self.speed = 1
        self.health = 5
        self.damage = 1

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
        enemy.take_damage(self.damage)

    def is_blocked_by_enemy(self, enemies):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                return True
        return False
    

    def is_blocked_by_base(self, base):

        return self.rect.colliderect(base.rect)


class Base:
    def __init__(self, on_destroy=None):
        self.image = pygame.image.load("assets/base.png")
        self.image = pygame.transform.scale(self.image, BASE_IMG_DIMENSION)
        self.rect = self.image.get_rect(bottomleft=BASE_COORDS)
        self.health = 1000
        self.on_destroy = on_destroy   # Store callback function for when base gets destroy



    def draw(self, surface):
        surface.blit(self.image, self.rect)
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"Base HP: {self.health}", True, (0,0,0))
        surface.blit(health_text, (self.rect.x -50, self.rect.y -20))

    def take_damage(self, damage):
        self.health -= damage
        print(f"Base health: {self.health}")
        if self.health <= 0 and self.on_destroy:
            self.on_destroy()   # Call the callback function when base is destroyed
            



class Enemy: 
    def __init__(self):  
        self.image = pygame.image.load("assets/enemy.png")
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect(bottomright=ENEMY_BASE_COORDS)
        self.x = self.rect.x
        self.y = self.rect.y
        self.health = 15
        self.speed = 1
        self.damage = 1

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
        vege.take_damage(self.damage)  # Deal damage to the vege


        
class EnemyBase:
    def __init__(self, on_destroy=None):
        self.image = pygame.image.load("assets/enemy_base.png")
        self.image = pygame.transform.scale(self.image, BASE_IMG_DIMENSION)
        self.rect = self.image.get_rect(bottomright=ENEMY_BASE_COORDS)
        self.health = 1000
        self.on_destroy = on_destroy  # Store callback function for when base gets destroy


    def draw(self, surface):
        surface.blit(self.image, self.rect)
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"Base HP: {self.health}", True, (0,0,0))
        surface.blit(health_text, (self.rect.x -50, self.rect.y -20))

    def take_damage(self, amount):
        self.health -= amount
        print(f"Enemy base health: {self.health}")
        if self.health <= 0 and self.on_destroy:
            self.on_destroy()           # Call the callback function when enemy base is destroyed
            


def return_alive(entities):
    alive_entities = []
    for entity in entities:
        if entity.health > 0:
            alive_entities.append(entity)
    
    return  alive_entities
