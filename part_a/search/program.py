# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

from .utils import render_board
from .utils import board_state
from queue import PriorityQueue


def search(input: dict[tuple, tuple]) -> list[tuple]:
    """
    This is the entry point for your submission. The input is a dictionary
    of board cell states, where the keys are tuples of (r, q) coordinates, and
    the values are tuples of (p, k) cell states. The output should be a list of 
    actions, where each action is a tuple of (r, q, dr, dq) coordinates.

    See the specification document for more details.
    """
 
    
    generated = PriorityQueue()
    initial_state = get_initial_board_state(input)
    generated.put(initial_state, initial_state.compute_f_value())
    while not generated.empty():
        curr_state = generated.get()
        # for debug
        print("EXPANDING:")
        curr_state.render_board_state()
        if curr_state.blue_power == 0:
            return curr_state.get_all_actions()
        for state in curr_state.generate_children():
            generated.put(state, state.compute_f_value())
        
    # no solution is found, which should not be possible if our algorithm is correct    
    return []

    # The render_board function is useful for debugging -- it will print out a 
    # board state in a human-readable format. Try changing the ansi argument 
    # to True to see a colour-coded version (if your terminal supports it).
    print(render_board(input, ansi=False))

    # Here we're returning "hardcoded" actions for the given test.csv file.
    # Of course, you'll need to replace this with an actual solution...
    return [
        (5, 6, -1, 1),
        (3, 1, 0, 1),
        (3, 2, -1, 1),
        (1, 4, 0, -1),
        (1, 3, 0, -1)
    ]

def get_initial_board_state(input: dict[tuple, tuple]) -> board_state:
    powers = {'r': 0,  'b':0} # powers of red and blue
    for cell_state in input.values():
        powers[cell_state[0]] += cell_state[1]
      


    return board_state(None, powers['b'], powers['r'], input, 0, None)

def spread(current_board: board_state, direction: tuple, coordinate: tuple):
    power = current_board[coordinate]
    for step in range(1, power + 1):
        target_coordinate = coordinate + direction * step
        # accounting for the wrap around of the board
        if target_coordinate[0] >= 7:
            target_coordinate = (target_coordinate[0] - 7, target_coordinate[1])
        if target_coordinate[1] >= 7:
            target_coordinate = (target_coordinate[0], target_coordinate[1] - 7)
        curr_power = (current_board[target_coordinate])[1]
        # if a cell's power exceeds 6, it is removed from the game
        if curr_power == 6:
            current_board.pop(target_coordinate)
        # empty cell
        elif current_board.get(target_coordinate) == None:
            current_board[target_coordinate] = ("r", 1)
        # case where the power of the cell is in a valid range
        else:
            current_board[target_coordinate] = ("r", curr_power + 1)




