import json
import pygame
import random
import sys


from units import Base, EnemyBase, return_alive

from level_manager import LevelManager

from unit_factory import create_veggie, create_enemy



# Functions

## Bluring screen
def blur_screen(surface, width, height):
    scale = 0.25
    small = pygame.transform.smoothscale(surface,(int(width * scale), int(height * scale)))
    return pygame.transform.smoothscale(small, (width, height))


## Draw Pop up Overlay
def draw_popup(screen, message, buttons, width, height):

    # Semi-transparent dark background
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0,0,0,180)) # Last value is alpha
    screen.blit(overlay, (0,0))

    # Pop up box
    box_rect = pygame.Rect(width // 2 - 150, height // 2 - 100, 310, 200)
    pygame.draw.rect(screen,(255,255,255), box_rect,border_radius=12)
    pygame.draw.rect(screen, (0,0,0),box_rect, width=2, border_radius=12)

    # Message
    font = pygame.font.Font(None, 48)
    text = font.render(message, True, (0,0,0))
    text_rect = text.get_rect(center=(width // 2, height // 2 - 40))
    screen.blit(text, text_rect)

    # Buttons
    button_rects = []
    for i, (label, action) in enumerate(buttons):
        rect = pygame.Rect(width // 2 - 130 + i * 140, height // 2 + 30, 130, 40)
        pygame.draw.rect(screen, (200,200,200), rect, border_radius=8)
        pygame.draw.rect(screen, (0,0,0), rect, 2, border_radius=8)

        btn_font = pygame.font.Font(None, 32)
        btn_text = btn_font.render(label, True, (0,0,0))
        btn_text_rect = btn_text.get_rect(center=rect.center)
        screen.blit(btn_text, btn_text_rect)
        button_rects.append((rect, action))

    return button_rects


## Reset game
def reset_game(state, on_gameover, on_win):
    state["veggies"] = []
    state["enemies"] = []
    state['base'] = Base(on_destroy=on_gameover)
    state['enemy_base'] = EnemyBase(on_destroy=on_win)
    state['level_manager'] = LevelManager(level=state['current_level'])
    state["state"] = "playing"
    state["running"] = True
    return   


def load_next_level(state, on_gameover, on_win):
    if state['current_level'] < 3:
        state['current_level'] += 1
    reset_game(state, on_gameover, on_win)
    return


def main():
    # Game Setup

    ## Initialise Pygame
    pygame.init()

    ## Constants for window size
    WIDTH, HEIGHT = 800, 400
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Vege Defense Game")

    ## Constants related to Game 
    MAX_VEGGIES = 50

    ## Font for text rendering
    font = pygame.font.SysFont("Arial", 30)

    ## Load images
    background_img = pygame.image.load("assets/background.png")

    ## Resize (if needed) to match window size
    background_img = pygame.transform.scale(background_img, (WIDTH,HEIGHT))

    ## Set up clock for FPS control
    clock = pygame.time.Clock()
    FPS = 60

    ## Character to keypad matching

    UNIT_KEYS = {
        pygame.K_1: "Carrot",   pygame.K_KP1: "Carrot",
        pygame.K_2: "Broccoli",   pygame.K_KP2: "Broccoli",
        pygame.K_3: "Tomato",     pygame.K_KP3: "Tomato",
        pygame.K_4: "Lettuce",    pygame.K_KP4: "Lettuce",
        pygame.K_5: "Eggplant",   pygame.K_KP5: "Eggplant",
        pygame.K_6: "Corn",       pygame.K_KP6: "Corn",
        pygame.K_7: "Onion",      pygame.K_KP7: "Onion",
        pygame.K_8: "Pepper",     pygame.K_KP8: "Pepper",
        pygame.K_9: "Cabbage",    pygame.K_KP9: "Cabbage",
        pygame.K_0: "Zucchini",   pygame.K_KP0: "Zucchini"

    }


    # Main game loop

    ## Game state
    game_state = {
        "state": "playing" ,         # or "win" or "gameover"
        "veggies": [] ,
        "enemies" : [],
        'base': None,
        'enemy_base': None,
        'level_manager': None,
        "current_level": 1,
        "running": True
        }  
    
    ## Callback functions for changing game state when either base or enemy base is destroyed
    def on_win():
        game_state["state"] = "win"
        return

    def on_gameover():
        game_state["state"] = "gameover"
        return

    # Define base and enemy_base after callback functions are defined
    game_state['base'] = Base(on_destroy=on_gameover)
    game_state['enemy_base'] = EnemyBase(on_destroy=on_win)
    game_state["level_manager"] = LevelManager(level=game_state['current_level'])

    # level_manager = LevelManager(level=game_state['current_level'])
    
    message = None
    
    button_rects = []

    while game_state['running']:
        # Control FPS
        clock.tick(FPS)
        current_time = pygame.time.get_ticks() - game_state['level_manager'].level_start_time
        

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state['running'] = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rects:
                    for rect,action in button_rects:
                        if rect.collidepoint(event.pos):
                            if action == "restart":
                                reset_game(state=game_state, on_gameover=on_gameover, on_win=on_win)
                                current_time = pygame.time.get_ticks() - game_state['level_manager'].level_start_time  
                            elif action == "next":
                                load_next_level(state=game_state, on_gameover=on_gameover, on_win=on_win)
                                current_time = pygame.time.get_ticks() - game_state['level_manager'].level_start_time
                            elif action == "quit":
                                pygame.quit()
                                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key in UNIT_KEYS:
                    if len(game_state["veggies"]) < MAX_VEGGIES:
                        unit_name = UNIT_KEYS[event.key]
                        new_unit = create_veggie(unit_name)
                        game_state["veggies"].append(new_unit)
                    else:
                        # Create a message when max limit has been reached
                        message = font.render("Max number of veggies spawned!", True, (255,0,0)) # The boolean value is for anti-aliasing. Anti-aliasing is a computer graphics technique that reduces jagged edges in images, especially in curves and diagonal lines, by blending pixels to create a smoother appearance.

        # Draw background and base
        screen.blit(background_img, (0,0))          # Draw background
        game_state['base'].draw(screen)
        game_state['enemy_base'].draw(screen)
        
        # Spawning the vegetables!!
        for vege in game_state["veggies"]:
            targets = game_state["enemies"] + [game_state['enemy_base']]
            vege.move(targets)
            vege.draw(screen)
            
            # Veggies Attack !!!!
            vege.attack(targets=targets, current_time=current_time)


        # Spawning Enemies!!!
        enemies_to_spawn = game_state['level_manager'].update(current_time=current_time)
        
        for enemy in enemies_to_spawn:
            print(enemy, "is spawned at time", current_time)
            new_enemy = create_enemy(enemy)
            game_state["enemies"].append(new_enemy)


        for enemy in game_state["enemies"]:
            targets = game_state["veggies"] + [game_state['base']]
            enemy.move(targets)
            enemy.draw(screen)

            # Enemies Attack !!!!
            enemy.attack(targets=targets, current_time=current_time)



        # Return alive entities
        game_state["veggies"] = return_alive(game_state["veggies"])
        game_state["enemies"] = return_alive(game_state["enemies"])


        # Max veggies spawned message
        if message and len(game_state["veggies"]) >= MAX_VEGGIES:
            # Get the width and height of the message
            message_width = message.get_width()
            message_height = message.get_height()

            # Center the text on the screen
            x_pos = (WIDTH - message_width) // 2
            y_pos = (HEIGHT - message_height) // 2

            # Blit the message (rendered text) at the calculated position
            screen.blit(message, (x_pos, y_pos))


        # Game state checking
        if game_state['state'] in ["win", "gameover"]:
            blurred = blur_screen(screen.copy(), WIDTH, HEIGHT)
            screen.blit(blurred, (0,0))
            

            if game_state['state'] == "win":
                buttons = [("Next Level", "next"), ("Close", "quit")]
                label = "You win!"
            else:
                buttons = [("Start Again", "restart"), ("Close", "quit")]
                label = "Game Over"

            button_rects = draw_popup(screen, label, buttons, WIDTH, HEIGHT)
        
        # Update screen
        pygame.display.flip()


    # Quit Pygame
    pygame.quit()
    sys.exit()

    


if __name__ == "__main__":
    main()