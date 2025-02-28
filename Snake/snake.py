

# Board Constants
CORNER          = "+"
NOTHING         = " "
SIDEBORDER      = "|"
SNAKE           = "#"
TOPBOTTOMBORDER = "-"

# Direction Constants
UP      = (1,0)
DOWN    = (-1,0)
LEFT    = (0,-1)
RIGHT   = (0,1)



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

class Apple:
    def __init__(self):
        pass



class Game:
    def __init__(self,height, width):
        self.height = height
        self.width  = width

        self.snake = Snake([(0,0), (1,0), (2,0), (3,0)], UP)


    def board_matrix(self):
        # return a matrix


        board = []
        for i in range(self.height):
            newRow = []
            for j in range(self.width):
                newRow.append(None)
            board.append(newRow)


        return board


    def render(self):
        matrix = self.board_matrix()



        # print matrix     
        print(CORNER + (TOPBOTTOMBORDER * self.width) + CORNER) # Top border

        for i in range(self.height):
            row_render = ""

            row_render += SIDEBORDER
            for j in range(self.width):
                if (i,j) in self.snake.body:
                    row_render += SNAKE
                elif matrix[i][j] == None:
                    row_render += NOTHING
            row_render += SIDEBORDER

            print(row_render)

        print(CORNER + (TOPBOTTOMBORDER * self.width) + CORNER) # Bottom border


        return





game = Game(10,20)
game.render()
