import random
from time import sleep

ALIVE = "#"
DEAD  = " "
SIDE_OF_BOARD = "-"


NEWLINE = "\n"

# Create a board of zeroes with specified height and width
def dead_state(height, width):
    board = []
    for i in range(height):
        newRow = []
        for j in range(width):
            newRow.append(0)
        board.append(newRow)

    return board

def random_state(height, width):
    # Build the board with dead_state
    state = dead_state(height,width)


    # Randomise each element of 'state'

    for i in range(height):
        for j in range(width):
            random_number = random.random()
            if random_number >= 0.95:
                state[i][j] = 1
            # Since we initialised to 0, this is technically not needed.
            else:
                state[i][j] = 0

    return state


# To render row by row
def renderRow(row):
    renderedRow = ""
    for state in row:
        if state == 1:
            renderedRow += ALIVE
        else:
            renderedRow += DEAD
    return renderedRow

# This is to render the state from random_state
def render(state):
    renderedState = ""

    # Top of board
    renderedState += (SIDE_OF_BOARD * len(state[0])) + NEWLINE

    for row in state:
        renderedState += renderRow(row) + NEWLINE
    
    # Bottom of board
    renderedState += (SIDE_OF_BOARD * len(state[0]))

    return renderedState




# Calculate the next board state according to the Game of Life
def next_board_state(state):
    
    height = len(state)
    width  = len(state[0])

    next_state = dead_state(height,width)

    for i in range(height):
        for j in range(width):


            neighbour_count = 0

            left  = max(j-1,0)
            right = min(j+2,width)

            # Check top
            if i - 1 >= 0:
                neighbour_count += sum(state[i-1][left: right])

            # Check mid
            if left == j-1:
                neighbour_count += state[i][left] 
            if right == j+2:    
                neighbour_count += state[i][right - 1]

            # Check bottom
            if i + 1 <= height - 1:
                neighbour_count += sum(state[i+1][left:right])
            
            # Game of Life rules
            
            if state[i][j] == 1:
                # If live population with 0 or 1 neighbour --> become dead (Underpopulation)
                # Since it is initialised to 0, technically this is not needed... 
                if neighbour_count <= 1:
                    next_state[i][j] = 0
                # If live population with 2 or 3 neighbours --> stay alive (Just right)   
                elif  neighbour_count <= 3:
                    next_state[i][j] = 1
                # If live population with more than 3 neighbours --> become dead (Overpopulation)
                elif neighbour_count > 3:
                    next_state[i][j] = 0
            # if it is a dead cell with exactly 3 neighbours, it becomes alive (Reproduction)
            elif neighbour_count == 3:
                next_state[i][j] = 1
            
        
    return next_state




if __name__ == "__main__":
    # initialise a random starting state
    height = 10
    width = 10

    # state = random_state(height,width)

    state = [
        [1,0,1,0,1,0,1,1,0,1,0,1],
        [1,1,0,1,0,1,1,1,0,1,0,1],
        [1,0,1,1,1,1,0,0,0,1,0,1],
        [1,0,1,1,1,1,0,0,1,1,0,0],
        [1,0,1,1,1,1,0,0,1,1,0,0],
        [1,0,1,1,1,1,0,0,1,1,0,0],
        [1,0,1,1,1,1,0,0,1,1,0,0],
        [1,0,1,1,1,1,0,0,1,1,0,0],
        [1,0,1,1,1,1,0,0,1,1,0,0],
        [1,0,1,1,1,1,0,0,1,1,0,0],
        [0,0,0,0,0,1,1,1,1,1,0,0]

    ]

    # Print initial state
    print(render(state))


    # The infinite loop
    while True:
        state = next_board_state(state)
        print(render(state))
        sleep(0.1)

