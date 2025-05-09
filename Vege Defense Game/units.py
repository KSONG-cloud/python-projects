import pygame
import sys



# Class for a unit in the game
class Vegetable:
    def __init__(self,x,y):
        self.image = pygame.image.load("assets/carrot2.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60,60))
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.speed = 1
        self.health = 5
        self.damage = 10

    def move(self):
        global enemies

        if not self.is_blocked_by_enemy(enemies) and not self.is_blocked_by_base():
            self.x += self.speed
            self.rect.x += self.speed
        
            

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"HP: {self.health}", True, (0,255, 0))
        screen.blit(health_text, (self.rect.x, self.rect.y - 20))


    def check_collision(self, enemy):
        # Check for collision with an enemy
        if self.rect.colliderect(enemy.rect):
            self.attack(enemy)
    
    def take_damage(self):
        self.health -= 1  # Reduce health when the veggie is attacked
        if self.health <= 0:
            self.kill()  # Remove veggie if health is 0

    def kill(self):
        global veggies  # Declare veggies as global
        veggies.remove(self)  # Remove the veggie from the list
    
    def attack(self, enemy):
        enemy.take_damage()

    def is_blocked_by_enemy(self, enemies):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                return True
        return False
    

    def is_blocked_by_base(self):
        if self.x + self.rect.width >= WIDTH - 10 - enemy_base_img.get_width() + 1:
            return True
        else:
            return False

class Base:
    def __init__(self):
        self.image = pygame.image.load("assets/enemy_base.png")
        self.image = pygame.transform.scale(enemy_base_img, (100,100))
        self.rect = self.image.get_rect(bottomright=(WIDTH - 10, HEIGHT-120 + self.image.get_height()))
        self.health = 1000


    def draw(self, surface):
        surface.blit(self.image, self.rect)
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"Base HP: {self.health}", True, (0,0,0))
        surface.blit(health_text, (self.rect.x -50, self.rect.y -20))

    def take_damage(self, amount):
        self.health -= amount
        print(f"Enemy base health: {self.health}")
        if self.health <= 0:
            print("You win!")
            pygame.quit()
            sys.exit()



class Enemy: 
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("assets/enemy.png")
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
        self.health = 15
        self.speed = 1

    def move(self):
        global veggies
        if not self.is_blocked_by_enemy(veggies) and not self.is_blocked_by_base():
            self.x -= self.speed
            self.rect.x -= self.speed
        


    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"HP: {self.health}", True, (255, 0, 0))
        screen.blit(health_text, (self.rect.x, self.rect.y - 20))


    def check_collision(self, enemy):
        # Check for collision with an enemy
        if self.rect.colliderect(enemy.rect):
            self.attack(enemy)
    

    def is_blocked_by_enemy(self, enemies):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                return True
        return False

    def is_blocked_by_base(self):
        if self.x  <= 10 + base_img.get_width() - 1:
            return True
        else:
            return False

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()         # Remove enemy if health is 0


    def kill(self):
        global enemies
        enemies.remove(self)
        

    def attack(self, vege):
        vege.take_damage()  # Deal damage to the vege


        
class EnemyBase:
    def __init__(self):
        self.image = pygame.image.load("assets/enemy_base.png")
        self.image = pygame.transform.scale(enemy_base_img, (100,100))
        self.rect = self.image.get_rect(bottomright=(WIDTH - 10, HEIGHT-120 + self.image.get_height()))
        self.health = 1000


    def draw(self, surface):
        surface.blit(self.image, self.rect)
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"Base HP: {self.health}", True, (0,0,0))
        surface.blit(health_text, (self.rect.x -50, self.rect.y -20))

    def take_damage(self, amount):
        self.health -= amount
        print(f"Enemy base health: {self.health}")
        if self.health <= 0:
            print("You win!")
            
