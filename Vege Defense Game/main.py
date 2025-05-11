import pygame
import sys

from units import Carrot, Enemy, Base, EnemyBase, return_alive

# Functions

## Callback functions for changing game state when either base or enemy base is destroyed
def on_win():
    global game_state
    game_state = "win"

def on_gameover():
    global game_state
    game_state = "gameover"



## Bluring screen
def blur_screen(surface):
    scale = 0.25
    small = pygame.transform.smoothscale(surface,(int(WIDTH * scale), int(HEIGHT * scale)))
    return pygame.transform.smoothscale(small, (WIDTH, HEIGHT))


## Draw Pop up Overlay
def draw_popup(screen, message, buttons):

    # Semi-transparent dark background
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0,0,0,180)) # Last value is alpha
    screen.blit(overlay, (0,0))

    

    # Pop up box
    box_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 100, 300, 200)
    pygame.draw.rect(screen,(255,255,255), box_rect,border_radius=12)
    pygame.draw.rect(screen, (0,0,0),box_rect, width=2, border_radius=12)

    # Message
    font = pygame.font.Font(None, 48)
    text = font.render(message, True, (0,0,0))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
    screen.blit(text, text_rect)


    # Buttons
    button_rects = []
    for i, (label, action) in enumerate(buttons):
        rect = pygame.Rect(WIDTH // 2 - 100 + i * 110, HEIGHT // 2 + 30, 100, 40)
        pygame.draw.rect(screen, (200,200,200), rect, border_radius=8)
        pygame.draw.rect(screen, (0,0,0), rect, 2, border_radius=8)

        btn_font = pygame.font.Font(None, 32)
        btn_text = btn_font.render(label, True, (0,0,0))
        btn_text_rect = btn_text.get_rect(center=rect.center)
        screen.blit(btn_text, btn_text_rect)
        button_rects.append((rect, action))


    return button_rects


# def draw_popup(screen, message, buttons):
#     # Step 1: darken overlay
#     overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
#     overlay.fill((0, 0, 0, 150))  # 150 = semi-transparent black
#     screen.blit(overlay, (0, 0))

#     # Step 2: popup box
#     popup_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 100, 300, 200)
#     pygame.draw.rect(screen, (255, 255, 255), popup_rect)  # white box
#     pygame.draw.rect(screen, (0, 0, 0), popup_rect, 3)     # black border

#     # Step 3: main message
#     font = pygame.font.Font(None, 48)
#     text = font.render(message, True, (0, 0, 0))
#     text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
#     screen.blit(text, text_rect)

#     # Step 4: draw buttons
#     button_rects = []
#     for i, (label, action) in enumerate(buttons):
#         btn_rect = pygame.Rect(WIDTH // 2 - 100 + i * 120, HEIGHT // 2 + 30, 100, 40)
#         pygame.draw.rect(screen, (180, 180, 180), btn_rect)
#         pygame.draw.rect(screen, (0, 0, 0), btn_rect, 2)

#         btn_font = pygame.font.Font(None, 32)
#         btn_text = btn_font.render(label, True, (0, 0, 0))
#         screen.blit(btn_text, btn_text.get_rect(center=btn_rect.center))

#         button_rects.append((btn_rect, action))

#     print(f"[Popup] drew {len(button_rects)} buttons for '{message}'")
#     return button_rects


## Helper functions to deal with in between games
def reset_game(starting_state):
    global  game_state
    veggies = starting_state["veggies"].copy()
    enemies = starting_state["enemies"].copy()
    base = Base(on_destroy=on_gameover)
    enemy_base = EnemyBase(on_destroy=on_win)
    game_state = "playing"


def load_next_level():
    # No next level yet....
    reset_game()







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

starting_state = {"veggies":[Carrot()], "enemies":[Enemy()]}

veggies = starting_state["veggies"].copy()
base = Base(on_destroy=on_gameover)

enemies = starting_state["enemies"].copy()
enemy_base = EnemyBase(on_destroy=on_win)

# enemy_base.on_destroy()


# Resize (if needed) to match window size
background_img = pygame.transform.scale(background_img, (WIDTH,HEIGHT))

# Set up clock for FPS control
clock = pygame.time.Clock()
FPS = 60

# Character to keypad matching
UNIT_KEYS = {
    pygame.K_1: Carrot,
    pygame.K_KP1: Carrot,
}



# Main game loop
running = True
message = None
game_state = "playing"  # or "win" or "gameover"
button_rects = []
while running:
    # Control FPS
    clock.tick(FPS)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rects:
                for rect,action in button_rects:
                    if rect.collidepoint(event.pos):
                        if action == "restart":
                            reset_game()
                        elif action == "next":
                            load_next_level()
                        elif action == "quit":
                            pygame.quit()
                            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in UNIT_KEYS:
                if len(veggies) < MAX_VEGGIES:
                    unit_class = UNIT_KEYS[event.key]
                    new_unit = unit_class()
                    veggies.append(new_unit)
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
        current_time = pygame.time.get_ticks()
        if vege.rect.colliderect(enemy_base.rect):
            if (current_time - vege.last_attack_time >= vege.attack_delay):
                enemy_base.take_damage(vege.damage)
                vege.last_attack_time = current_time

        



    for enemy in enemies:
        enemy.move(veggies, base)
        enemy.draw(screen)

        # Check for collisions between veggie and enemies
        for vege in veggies:
            enemy.check_collision(vege)

        # Collision with our base
        current_time = pygame.time.get_ticks()
        if enemy.rect.colliderect(base.rect):
            if (current_time - enemy.last_attack_time >= enemy.attack_delay):
                base.take_damage(enemy.damage)
                enemy.last_attack_time = current_time

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


    # Game state checking
    if game_state in ["win", "gameover"]:
        blurred = blur_screen(screen.copy())
        screen.blit(blurred, (0,0))
        

        if game_state == "win":
            buttons = [("Next Level", "next"), ("Close", "quit")]
            label = "You win!"
        else:
            buttons = [("Start Again", "restart"), ("Close", "quit")]
            label = "Game Over"

        button_rects = draw_popup(screen, label, buttons)
    # Update screen
    pygame.display.flip()


# Quit Pygame
pygame.quit()
sys.exit()

