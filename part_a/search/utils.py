# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion
import math


MAX_CELL_POWER = 6
SIDE_WIDTH = 7
# (dr, dq) must be one of: (0, 1), (−1, 1), (−1, 0), (0, −1), (1, −1), or, (1, 0)
VALID_DIRECTIONS = [(0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1), (1, 0)]
RED_CELL = "r"
BLUE_CELL = "b"


def apply_ansi(str, bold=True, color=None):
    """
    Wraps a string with ANSI control codes to enable basic terminal-based
    formatting on that string. Note: Not all terminals will be compatible!

    Arguments:

    str -- String to apply ANSI control codes to
    bold -- True if you want the text to be rendered bold
    color -- Colour of the text. Currently only red/"r" and blue/"b" are
        supported, but this can easily be extended if desired...

    """
    bold_code = "\033[1m" if bold else ""
    color_code = ""
    if color == "r":
        color_code = "\033[31m"
    if color == "b":
        color_code = "\033[34m"
    return f"{bold_code}{color_code}{str}\033[0m"

def render_board(board: dict[tuple, tuple], ansi=False) -> str:
    """
    Visualise the Infexion hex board via a multiline ASCII string.
    The layout corresponds to the axial coordinate system as described in the
    game specification document.
    
    Example:

        >>> board = {
        ...     (5, 6): ("r", 2),
        ...     (1, 0): ("b", 2),
        ...     (1, 1): ("b", 1),
        ...     (3, 2): ("b", 1),
        ...     (1, 3): ("b", 3),
        ... }
        >>> print_board(board, ansi=False)

                                ..     
                            ..      ..     
                        ..      ..      ..     
                    ..      ..      ..      ..     
                ..      ..      ..      ..      ..     
            b2      ..      b1      ..      ..      ..     
        ..      b1      ..      ..      ..      ..      ..     
            ..      ..      ..      ..      ..      r2     
                ..      b3      ..      ..      ..     
                    ..      ..      ..      ..     
                        ..      ..      ..     
                            ..      ..     
                                ..     
    """
    dim = 7
    output = ""
    for row in range(dim * 2 - 1):
        output += "    " * abs((dim - 1) - row)
        for col in range(dim - abs(row - (dim - 1))):
            # Map row, col to r, q
            r = max((dim - 1) - row, 0) + col
            q = max(row - (dim - 1), 0) + col
            if (r, q) in board:
                color, power = board[(r, q)]
                text = f"{color}{power}".center(4)
                if ansi:
                    output += apply_ansi(text, color=color, bold=False)
                else:
                    output += text
            else:
                output += " .. "
            output += "    "
        output += "\n"
    return output


class board_state:

    # i am not sure if this is correct, but i attempted to start with the creation of the board_state class - Bryant
    # i think this should work, apparently in python we can't overload the constructor, so i made a function to handle the initial state - Kevin
    def __init__(self, parent, board:dict[tuple, tuple], g_value: int, action_taken:tuple):
        self.parent = parent
        self.board = board
        self.g_value = g_value
        self.action_taken = action_taken

        powers = {RED_CELL: 0,  BLUE_CELL:0} # powers of red and blue
        for cell_state in board.values():
            powers[cell_state[0]] += cell_state[1]
        self.blue_power = powers[BLUE_CELL]
        self.red_power = powers[RED_CELL]
        # for debug
        # print("NEW BOARD STATE:")
        # self.render_board_state()

    def render_board_state(self):
        print("================================\n")
        print("blue power: " + str(self.blue_power))
        print("red power: " + str(self.red_power))
        print("g value: " + str(self.g_value))
        print("action taken: " + str(self.action_taken))
        print("f value: " + str(self.compute_f_value()))
        print(render_board(self.board))
        print("================================\n")

    def get_blue_cells(self):
        blue_cells = []
        for coords, cell in self.board.items(): 
            if cell[0] == "b":
                blue_cells.append(coords)
        return blue_cells


    def compute_f_value(self):
        # using the number of blue cells and the heuristic, however this might not be admissable
        counts = self.count_cells()
        return self.g_value + self.least_total_cost()
    
    # spread in every possible directions and get the resulting board states
    def generate_children(self): 
        children = []
        for coordinates, cell in self.board.items():
            if cell[0] == RED_CELL:
                for direction in VALID_DIRECTIONS:
                    board_copy = dict(self.board)
                    self.spread(board_copy, direction, coordinates)
                    children.append(board_state(self, board_copy, self.g_value+1, coordinates + direction))
        return children


    
    def get_all_actions(self):
        # trace back to root node and find all actions taken
        actions = []
        curr_node = self
        while(curr_node.parent):
            actions.insert(0, curr_node.action_taken)
            curr_node = curr_node.parent
        return actions


    # i moved the function here so that generate_children can call it - Kevin
    def spread(self, current_board: dict[tuple, tuple], direction: tuple, coordinate: tuple):
        power = current_board[coordinate][1]
        # remove the cell to spread from
        current_board.pop(coordinate)
        for step in range(1, power + 1):
            target_coordinate = (coordinate[0] + direction[0] * step, coordinate[1] + direction[1] * step)
            # accounting for the wrap around of the board
            if target_coordinate[0] >= SIDE_WIDTH:
                target_coordinate = (target_coordinate[0] - SIDE_WIDTH, target_coordinate[1])
            if target_coordinate[1] >= SIDE_WIDTH:
                target_coordinate = (target_coordinate[0], target_coordinate[1] - SIDE_WIDTH)

            # handle when target_coordinate is empty
            if target_coordinate not in current_board.keys():
                curr_power = 0
            else:
                curr_power = (current_board[target_coordinate])[1] 
            # if a cell's power exceeds 6, it is removed from the game
            if curr_power == MAX_CELL_POWER:
                current_board.pop(target_coordinate)
            # case where the power of the cell is in a valid range
            else:
                current_board[target_coordinate] = ("r", curr_power + 1)

        
      
    def count_cells(self) -> dict[str, int]:
        counts = {RED_CELL: 0, BLUE_CELL: 0}
        for cell in self.board.values():
            counts[cell[0]] += 1

        return counts
    
    def least_cost_from_cell(self, from_x: int, from_y: int, cell: tuple, power: int):
        x_diff = abs(from_x - cell[0])
        y_diff = abs(from_y - cell[1])
        min_distance = min(x_diff, y_diff) + abs(x_diff - y_diff)
        return max(0, min_distance - power) + 1

    
    def least_total_cost(self):
        # this is slower than summing up the costs to each blue cell, but should be admissable?
        least_costs = {} #  key: coords of the cell from which the least cost is achieved; value: cost
        for blue_cell in self.get_blue_cells():  # we can store blue cells as an attribute to further improve time complexity
            least_cost = float('inf') # initialise with very big number
            from_cell = None
            for coords, red_cell in self.board.items():
                if red_cell[0] == 'r':
                    cost = self.least_cost_from_cell(coords[0], coords[1], blue_cell, red_cell[1])
                    if cost < least_cost:
                        least_cost = cost
                        from_cell = coords
            # can be ignored if there is already a larger least cost from this cell          
            if from_cell in least_costs.keys() and least_cost < least_costs[from_cell]:
                continue
                
            least_costs[from_cell] = least_cost
        

        return sum(least_costs.values())
