from time import sleep
import keyboard
import random

# Board Constants
APPLE               = "O"
CORNER              = "+"
GAMEOVER            = False
GAMEOVER_MESSAGE    = "The snake bit itself. Ouch! Game Over."
GAMESTART           = True
NOTHING             = " "
SIDEBORDER          = "|"
SNAKE               = "#"
SNAKE_HEAD          = "X"
TOPBOTTOMBORDER     = "-"

# Board Dimensions
GAME_HEIGHT = 10
GAME_WIDTH  = 20



# Direction Constants
UP      = (-1,0)
DOWN    = (1,0)
LEFT    = (0,-1)
RIGHT   = (0,1)
OPPOSITE = { UP: DOWN,
             DOWN: UP,
             LEFT: RIGHT,
             RIGHT: LEFT}


# Gamemode Constants
TORUS   = "torus"
KLEIN   = "klein"
RP2     = "rp2"


# Inputs to directions
INPUTS = { "w": UP,     "up": UP,
           "a": LEFT,   "left": LEFT,
           "s": DOWN,   "down": DOWN,
           "d": RIGHT,   "right":RIGHT}





class Snake:
    def __init__(self, init_body, init_direction):
        self.body = init_body
        self.direction = init_direction

    # Add the inputed position to the front of the snake's body and pop off the back
    # so the snake can slither....
    def take_step(self, position):
        self.body = self.body[1:] + [position]

    # Sets the inputed direction as the direction of the snake
    def set_direction(self, direction):
        self.direction = direction

    # Returns the position of the front of the snake's body
    def head(self):
        return self.body[-1]

    # Snake growing from eating an apple
    def grow(self, coordinate):
        self.body = self.body + [coordinate]



class Apple:
    def __init__(self,height,width):
        self.coordinate = self.randomize(height,width)

    def randomize(self,height,width):
        return (int(random.random() * height), int(random.random() * width))
    
    def a_new_apple(self, height, width):
        self.coordinate = self.randomize(height,width)



class Game:
    def __init__(self,height, width, topology=TORUS):
        self.height = height
        self.width  = width

        self.snake = Snake([(0,0), (1,0), (2,0), (3,0), (4,0)], DOWN)

        self.apple = Apple(height, width)

        self.gameState = GAMEOVER

        self.topology = topology


    def board_matrix(self):
        # return a matrix


        board = []
        for i in range(self.height):
            newRow = []
            for j in range(self.width):
                newRow.append(None)
            board.append(newRow)


        return board


    def render(self, matrix):

        print("\n\n\n\n\n")
        # print matrix     
        print(CORNER + (TOPBOTTOMBORDER * self.width) + CORNER) # Top border

        for i in range(self.height):
            row_render = ""

            row_render += SIDEBORDER
            for j in range(self.width):
                # print("HEY",self.snake.body)

                # It's the snake!
                if (i,j) in self.snake.body:
                    if (i,j) == self.snake.head():
                        row_render += SNAKE_HEAD
                    else:
                        row_render += SNAKE
                # If it is the apple
                elif (i,j) == self.apple.coordinate:
                    row_render += APPLE
                # It's not the snake and there is nothing on it
                elif matrix[i][j] == None:
                    row_render += NOTHING
            row_render += SIDEBORDER

            print(row_render)

        print(CORNER + (TOPBOTTOMBORDER * self.width) + CORNER) # Bottom border

        return
    
    # Check if the snake is dead
    def is_snake_dead(self):
        # if the snake overlaps, its dead.
        if len(set(self.snake.body)) < len(self.snake.body):
            self.gameState = GAMEOVER
        return


    


    def newgame(self):

        # New game
        matrix = self.board_matrix()
        self.gameState = GAMESTART

        # functions for changing direction
        def go_up():
            self.snake.set_direction(UP)
            return

        def go_down():
            self.snake.set_direction(DOWN)
            return

        def go_left():
            self.snake.set_direction(LEFT)
            return

        def go_right():
            self.snake.set_direction(RIGHT)
            return

        # keys to change direction
        keyboard.add_hotkey('up', go_up)
        keyboard.add_hotkey('w', go_up)
        keyboard.add_hotkey('down', go_down)
        keyboard.add_hotkey('s', go_down)
        keyboard.add_hotkey('left', go_left)
        keyboard.add_hotkey('a', go_left)
        keyboard.add_hotkey('right', go_right)
        keyboard.add_hotkey('d', go_right)


        while self.gameState:
            # Render board
            self.render(matrix)

            # this is going to make the game go faster the longer the snake is
            snake_length = len(self.snake.body)
            sleep(0.4 - 0.2 * (snake_length/(self.height * self.width)))

            # Take in direction input (Version 2)
            direction_input = self.snake.direction

            
            
            # direction_input = INPUTS[keyboard.read_key()]
            
            

            # Cannot go back on yourself
            if direction_input != OPPOSITE[self.snake.direction]:

                self.snake.set_direction(direction_input)

            next_step = [sum(x) for x in zip(self.snake.head() , self.snake.direction)]

            # Wrap around like a torus
            if next_step[0] >= self.height or next_step[0] <= -1:

                if self.topology == TORUS:
                    next_step[0] = next_step[0] % self.height
                    next_step[1] = next_step[1] % self.width
                elif self.topology == RP2:
                    next_step[0] = (next_step[0]) % self.height
                    next_step[1] = ((next_step[1] + 1) * (-1)) % self.width
                elif self.topology == KLEIN:
                    next_step[0] = (next_step[0]) % self.height
                    next_step[1] = ((next_step[1] + 1) * (-1)) % self.width

            if next_step[1] >= self.width or next_step[1] <= -1:

                if self.topology == TORUS:
                    next_step[0] = next_step[0] % self.height
                    next_step[1] = next_step[1] % self.width
                elif self.topology == RP2:
                    next_step[0] = ((next_step[0] + 1) * (-1)) % self.height
                    next_step[1] = (next_step[1]) % self.width
                elif self.topology == KLEIN:
                    next_step[0] = (next_step[0]) % self.height
                    next_step[1] = (next_step[1]) % self.width

            next_step = tuple(next_step)


            # If next step snake head is on apple, eat apple
            if next_step == self.apple.coordinate:

                # become longer 
                self.snake.grow(next_step)
                # a new apple
                self.apple.a_new_apple(self.height, self.width)

            # Otherwise, just move
            else:

                # Snake move
                self.snake.take_step(next_step)

            # Is snake dead??
            self.is_snake_dead()

            


        self.render(matrix)
        print(GAMEOVER_MESSAGE)
  



game= Game(10,10, RP2)

game.newgame()

