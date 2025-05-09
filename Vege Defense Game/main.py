import pygame
import sys

from units import Vegetable, Enemy, Base, EnemyBase, return_alive

# Functions

def on_win():
    global game_state
    game_state = "win"

def on_lose():
    global game_state
    game_state = "lose"


















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

veggies = [Vegetable()]
base = Base(on_destroy=on_lose)

enemies = [Enemy(), Enemy()]
enemy_base = EnemyBase(on_destroy=on_win)

# Resize (if needed) to match window size
background_img = pygame.transform.scale(background_img, (WIDTH,HEIGHT))

# Set up clock for FPS control
clock = pygame.time.Clock()
FPS = 60





# Main game loop
running = True
message = None
game_state = "playing"  # or "win" or "lose"
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
                    veggies.append(Vegetable())
                else:
                    # Create a message when max limit has been reached
                    message = font.render("Max number of veggies spawned!", True, (255,0,0)) # The boolean value is for anti-aliasing. Anti-aliasing is a computer graphics technique that reduces jagged edges in images, especially in curves and diagonal lines, by blending pixels to create a smoother appearance.

    # Draw background and base
    screen.blit(background_img, (0,0))          # Draw background
    base.draw(screen)
    enemy_base.draw(screen)
    
    # Spawning the vegetables!!
    for vege in veggies:
        vege.move(enemies, enemy_base)
        vege.draw(screen)

        # Check for collisions between veggie and enemies
        for enemy in enemies: 
            vege.check_collision(enemy)

        # Collision with enemy base
        if vege.rect.colliderect(enemy_base.rect):
            enemy_base.take_damage(vege.damage)

        



    for enemy in enemies:
        enemy.move(veggies, base)
        enemy.draw(screen)

        # Check for collisions between veggie and enemies
        for vege in veggies:
            enemy.check_collision(vege)

        # Collision with our base
        if enemy.rect.colliderect(base.rect):
            base.take_damage(enemy.damage)

    # Return alive entities
    veggies = return_alive(veggies)
    enemies = return_alive(enemies)


    # Max veggies spawned message
    if message and len(veggies) >= MAX_VEGGIES:
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

