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

    def move(self):
        global enemies

        if not self.is_blocked_by_enemy(enemies):
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




class Enemy: 
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("assets/enemy.png")
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
        self.health = 15
        self.speed = 1

    def move(self):
        global veggies
        if not self.is_blocked_by_enemy(veggies):
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


    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()         # Remove enemy if health is 0


    def kill(self):
        global enemies
        enemies.remove(self)
        

    def attack(self, vege):
        vege.take_damage()  # Deal damage to the vege
        





## Game Setup

# Initialise Pygame
pygame.init()


# Constants for window size
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Cat Defense Game")

# Constants related to Game 
MAX_VEGGIES = 5

# Font for text rendering
font = pygame.font.SysFont("Arial", 30)

# Load images
background_img = pygame.image.load("assets/background.png")
base_img = pygame.image.load("assets/base.png")

veggies = [Vegetable(100, HEIGHT-120)]

enemies = [Enemy(400, HEIGHT - 120), Enemy(600, HEIGHT - 120)]


# Resize (if needed) to match window size
background_img = pygame.transform.scale(background_img, (WIDTH,HEIGHT))
base_img = pygame.transform.scale(base_img, (100,100))

# Set up clock for FPS control
clock = pygame.time.Clock()
FPS = 60


# Main game loop
running = True
message = None
while running:
    # Control FPS
    clock.tick(FPS)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:     # Spacebar is pressed
                if len(veggies) < MAX_VEGGIES:
                    veggies.append(Vegetable(100, HEIGHT-120))
                else:
                    # Create a message when max limit has been reached
                    message = font.render("Max number of veggies spawned!", True, (255,0,0)) # The boolean value is for anti-aliasing. Anti-aliasing is a computer graphics technique that reduces jagged edges in images, especially in curves and diagonal lines, by blending pixels to create a smoother appearance.

    # Draw background and base
    screen.blit(background_img, (0,0))          # Draw background
    screen.blit(base_img, (10, HEIGHT - 120))   # Draw base near bottom left

    # Spawning the vegetables!!
    for vege in veggies:
        vege.move()
        vege.draw(screen)

        # Check for collisions between veggie and enemies
        for enemy in enemies: 
            vege.check_collision(enemy)

    for enemy in enemies:
        enemy.move()
        enemy.draw(screen)
        for vege in veggies:
            enemy.check_collision(vege)

    # Max veggies spawned message
    if message:
        # Get the width and height of the message
        message_width = message.get_width()
        message_height = message.get_height()

        # Center the text on the screen
        x_pos = (WIDTH - message_width) // 2
        y_pos = (HEIGHT - message_height) // 2

        # Blit the message (rendered text) at the calculated position
        screen.blit(message, (x_pos, y_pos))

    # Update screen
    pygame.display.flip()


# Quit Pygame
pygame.quit()
sys.exit()

