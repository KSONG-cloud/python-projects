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
    def __init__(self, health, damage, speed, rect, image, attack_range, last_attack_time, attack_delay):
        self.health = health
        self.damage = damage
        self.speed = speed
        self.rect = rect
        self.x = rect.x
        self.y = rect.y
        self.image = image
        self.range = attack_range
        self.last_attack_time = last_attack_time
        self.attack_delay = attack_delay


    def move(self, targets):
        if not self.is_blocked_by_targets(targets):
            self.x += self.speed
            self.rect.x += self.speed
            

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"HP: {self.health}", True, (0,255, 0))
        surface.blit(health_text, (self.rect.x, self.rect.y - 20))
    

    def take_damage(self, damage):
        self.health -= damage  # Reduce health when the veggie is attacked


    def attack(self, targets, current_time):
        # Attack all targets within the attack radius (AoE).
        
        if current_time - self.last_attack_time >= self.attack_delay:
            for target in targets:
                # Check if target is within attack range
                distance = self.calculate_distance(target)
                if distance <= self.range:
                    target.take_damage(self.damage) # Apply damage to target

            self.last_attack_time = current_time

    
    def is_blocked_by_targets(self, targets):
        for target in targets:
            distance = self.calculate_distance(target)
            if distance <= self.range:
                return True
            
        return False


    def calculate_distance(self, target):
        # Calculate distance between self and target
        return target.rect.x - self.x - self.rect.width




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
        if self.health <= 0:
            if self.on_destroy:
                self.on_destroy()      # Call the callback function when base is destroyed


class Enemy: 
    def __init__(self, health, damage, speed, rect, image, attack_range, last_attack_time, attack_delay):  
        self.image = image  
        self.rect = rect
        self.x = self.rect.x
        self.y = self.rect.y
        self.health = health
        self.speed = speed
        self.damage = damage
        self.range = attack_range
        self.last_attack_time = last_attack_time
        self.attack_delay = attack_delay



    def move(self, targets):
        if not self.is_blocked_by_targets(targets):
            self.x -= self.speed
            self.rect.x -= self.speed


    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"HP: {self.health}", True, (255, 0, 0))
        surface.blit(health_text, (self.rect.x, self.rect.y - 20))

    
    def is_blocked_by_targets(self, targets):
        for target in targets:
            distance = self.calculate_distance(target)
            if distance <= self.range:
                return True
            
        return False

    def take_damage(self, damage):
        self.health -= damage 
        

    def attack(self, targets, current_time):
        # Attack all targets within the attack radius (AoE).
        if current_time - self.last_attack_time >= self.attack_delay:
            for target in targets:
                # Check if target is within attack range
                distance = self.calculate_distance(target)
                if distance <= self.range:
                    target.take_damage(self.damage) # Apply damage to target

            self.last_attack_time = current_time


    def calculate_distance(self, target):
        # Calculate distance between self and target
        return self.x - target.rect.x - target.rect.width


        
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
