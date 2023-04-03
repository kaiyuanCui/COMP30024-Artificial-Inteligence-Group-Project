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
    # sort by insert order when f values are the same
    insert_order = 0
    generated.put((initial_state.compute_f_value(), insert_order, initial_state))
    while not generated.empty():
        curr_state = generated.get()[-1]

        # for debug
        """
        print("EXPANDING:")
        curr_state.render_board_state()
        print("PARENT:")
        if (curr_state.parent):
            curr_state.parent.render_board_state()
        """
        if curr_state.blue_power == 0:
            return curr_state.get_all_actions() # solution found
        for state in curr_state.generate_children():
            insert_order += 1
            generated.put((state.compute_f_value(), insert_order , state))
        
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
    return board_state(None, input, 0, None)






