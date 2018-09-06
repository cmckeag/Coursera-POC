"""
Clone of 2048 game.

Note: Requires external modules that aren't present. The code won't work, but
the logic is functional for 2048 (I'm pretty sure)
"""

#import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    res = [xxx for xxx in line if xxx > 0]
    for index in range(len(res)-1):
        if res[index] == 0:
            continue
        if res[index] == res[index+1] and res[index] > 0:
            res[index] *= 2
            res[index+1] = 0
    res = [xxx for xxx in res if xxx > 0]
    res += [0] * (len(line) - len(res))
    return res

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._height = grid_height
        self._width = grid_width
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        row = [0]*self._width
        self._board = [row[:] for dummy_ind in range(self._height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        rows = [' '.join(map(str,xxx)) for xxx in self._board]
        
        return ','.join(rows)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        moved = False
        if direction == LEFT or direction == RIGHT:
            for row in range(self._height):
                new_row = None
                if direction == LEFT:
                    new_row = merge(self._board[row])
                    if new_row != self._board[row]:
                        moved = True
                    self._board[row] = new_row
                else:
                    new_row = merge(self._board[row][::-1])
                    if new_row != self._board[row][::-1]:
                        moved = True
                    self._board[row] = new_row[::-1]
                
                
        elif direction == UP or direction == DOWN:
            t_board = [list(zzz) for zzz in zip(*self._board)]
            for row in range(self._width):
                if direction == UP:
                    new_row = merge(t_board[row])
                    if new_row != t_board[row]:
                        moved = True
                    t_board[row] = new_row
                else:
                    new_row = merge(t_board[row][::-1])
                    if new_row != t_board[row][::-1]:
                        moved = True
                    t_board[row] = new_row[::-1]
            self._board = [list(zzz) for zzz in zip(*t_board)]
            
        if moved:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        rows_with_spaces = [ind for ind, row in enumerate(self._board) if 0 in row]
        random_row_index = rows_with_spaces[random.randint(0, len(rows_with_spaces) - 1)]
        random_row = self._board[random_row_index]
        columns_with_spaces = [ind for ind, value in enumerate(random_row) if value is 0]
        random_col_index = columns_with_spaces[random.randint(0, len(columns_with_spaces) - 1)]
        value_determiner = random.randint(1,10)
        if value_determiner == 4:
            self._board[random_row_index][random_col_index] = 4
        else:
            self._board[random_row_index][random_col_index] = 2

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._board[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._board[row][col]
