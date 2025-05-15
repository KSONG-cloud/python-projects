import json
import pygame
import random
import sys


from units import Base, EnemyBase, return_alive, WIDTH, HEIGHT, BASE_COORDS

from level_manager import LevelManager

from unit_factory import create_veggie, create_enemy, get_unit_image_path




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


## Create UI buttons
### Load images from config files
def  load_unit_button_images(unit_names):
    images = {}
    for name in unit_names:
        img_path = get_unit_image_path(name)
        img = pygame.image.load(img_path).convert_alpha()
        img = pygame.transform.scale(img, (40, 40))
        images[name] = img
    return images

### Create buttons
def create_ui_buttons(unit_names, rows=2, cols=5, btn_w=60, btn_h=60, gap=10):
    buttons = []
    margin_w = (WIDTH - 5 * btn_w)// 2
    margin_h = (HEIGHT - BASE_COORDS[1] - 2 * btn_h) // 2
    for idx, name in enumerate(unit_names):
        row = idx // cols
        col = idx % cols
        x = margin_w + col * (btn_w + gap)
        y = BASE_COORDS[1] + margin_h + row * (btn_h + gap)
        rect = pygame.Rect(x,y,btn_w, btn_h)
        buttons.append((rect, name))

    return buttons



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

    UNIT_NAMES = ["Carrot", "Broccoli", "Tomato", "Lettuce", "Eggplant", "Corn", "Onion", "Pepper", "Cabbage", "Zucchini"]
    unit_button_images = load_unit_button_images(UNIT_NAMES)
    ui_buttons = create_ui_buttons(UNIT_NAMES)


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

    pause_button_rect = pygame.Rect(1100, 540, 80, 40)

    while game_state['running']:
        # Control FPS
        clock.tick(FPS)
        current_time = pygame.time.get_ticks() - game_state['level_manager'].level_start_time

        
        

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state['running'] = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button_rect.collidepoint(event.pos):
                    if game_state["state"] == "playing":
                        game_state["state"] = "paused"
                    elif game_state["state"] == "paused":
                        game_state["state"] = "playing"
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
                if game_state['state'] == 'playing':
                    for rect, name in ui_buttons:
                        if rect.collidepoint(event.pos):
                            if len(game_state["veggies"]) < MAX_VEGGIES:
                                new_unit = create_veggie(name)
                                game_state["veggies"].append(new_unit)
                            else:
                                message = font.render("Max number of veggies spawned!", True, (255, 0, 0))

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
        # screen.blit(background_img, (0,0))          # Draw background
        screen.blit(background_img, (0, 0), area=pygame.Rect(0, 0, WIDTH, BASE_COORDS[1] + 10))
        ui_bg_rect = pygame.Rect(0, BASE_COORDS[1] + 10, WIDTH, HEIGHT - BASE_COORDS[1]-10)
        pygame.draw.rect(screen, (0, 0, 0), ui_bg_rect)
        game_state['base'].draw(screen)
        game_state['enemy_base'].draw(screen)

        # Draw buttons
        for rect, name in ui_buttons:
            pygame.draw.rect(screen, (255, 255, 255), rect)              # white fill
            pygame.draw.rect(screen, (0, 0, 0), rect, width=2)           # black border
            image = unit_button_images[name]
            img_rect = image.get_rect(center=rect.center)
            screen.blit(image, img_rect)
        
        ### Pause button
        pygame.draw.rect(screen, (200, 200, 200), pause_button_rect, border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0), pause_button_rect, 2, border_radius=8)

        pause_font = pygame.font.Font(None, 24)
        label = "Pause" if game_state["state"] == "playing" else "Resume"
        pause_text = pause_font.render(label, True, (0, 0, 0))
        pause_text_rect = pause_text.get_rect(center=pause_button_rect.center)
        screen.blit(pause_text, pause_text_rect)

        # Updating the game
        if game_state["state"] == "playing":
            # Spawning the vegetables!!
            for vege in game_state["veggies"]:
                targets = game_state["enemies"] + [game_state['enemy_base']]
                vege.move(targets)
                
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

                # Enemies Attack !!!!
                enemy.attack(targets=targets, current_time=current_time)



        # Return alive entities
        game_state["veggies"] = return_alive(game_state["veggies"])
        game_state["enemies"] = return_alive(game_state["enemies"])

        # Drawing the veggies and enemies
        for vege in game_state["veggies"]:
            vege.draw(screen)

        for enemy in game_state["enemies"]:
            enemy.draw(screen)



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
        if game_state['state'] in ["win", "gameover", "paused"]:
            blurred = blur_screen(screen.copy(), WIDTH, HEIGHT)
            screen.blit(blurred, (0,0))
            
            # Win message
            if game_state['state'] == "win":
                buttons = [("Next Level", "next"), ("Close", "quit")]
                label = "You win!"
                button_rects = draw_popup(screen, label, buttons, WIDTH, HEIGHT)
            
            # Paused message
            elif game_state["state"] == "paused":
                pause_msg = font.render("Paused", True, (255, 255, 255))
                pause_msg_rect = pause_msg.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(pause_msg, pause_msg_rect)

            # Gameover message
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