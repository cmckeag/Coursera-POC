"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors


This code solves slider puzzles of any rectangular size.
Unfortunately the external modules are not present so we can't run this with a gui,
but the code is functional.
The solution occurs in the solve_puzzle() method, using all the helper methods in the class.
"""

#import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # Condition 1
        if self.get_number(target_row, target_col) != 0:
            return False
        # Condition 3
        for col_dex in range(target_col+1, self._width):
            if self.get_number(target_row, col_dex) != target_row*self._width + col_dex:
                return False
        # Condition 2:
        for row_dex in range(target_row+1, self._height):
            for col_dex in range(self._width):
                if self.get_number(row_dex, col_dex) != row_dex*self._width + col_dex:
                    return False
        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        
        Pretty sure this could have been done with a few less
        if statements (some redundancy here) but it would still be
        an if-else heavy execution tree either way.
        """
        target_tile = self.current_position(target_row, target_col)
        # Phase 1: Move the 0 tile to the current location of the target tile
        up_moves = ['u'] * (target_row - target_tile[0])
        lateral_moves = []
        if target_tile[1] > target_col:
            lateral_moves = ['r'] * (target_tile[1] - target_col)
        elif target_tile[1] < target_col:
            lateral_moves = ['l'] * (target_col - target_tile[1])
        phase1_moves = up_moves + lateral_moves
        # Phase 2: Depending on the moves we took to get the 0 tile
        # to the target tile, use repositioning moves to get the target
        # tile to its target position.
        # Case: Target tile was directly to the left
        if len(up_moves) == 0:
            res = ''.join(phase1_moves + ['urrdl'] * (len(lateral_moves) - 1))
            for charr in list(res):
                self.update_puzzle(charr)
            return res
        # Case: Target tile was exactly 1 row up:
        if len(up_moves) == 1:
            # Sub-cases: target was to the left/right
            if phase1_moves[-1] == 'r':
                res = ''.join(phase1_moves + ['ulldr'] * (len(lateral_moves) - 1) + ['ullddruld'])
                for charr in list(res):
                    self.update_puzzle(charr)
                return res
            elif phase1_moves[-1] == 'l':
                res = ''.join(phase1_moves + ['urrdl'] * (len(lateral_moves) - 1) + ['druld'])
                for charr in list(res):
                    self.update_puzzle(charr)
                return res
            else:
                res = ''.join(phase1_moves + ['ld'])
                for charr in list(res):
                    self.update_puzzle(charr)
                return res
        # General case: Target was 2 rows up or more, any distance left or right
        else:
            phase2_moves = []
            # Sub-cases: target was to the left/right
            if phase1_moves[-1] == 'r':
                phase2_moves = phase2_moves + ['dllur'] * (len(lateral_moves) - 1) + ['dlu']
            elif phase1_moves[-1] == 'l':
                phase2_moves = phase2_moves + ['drrul'] * (len(lateral_moves) - 1) + ['dru']
            # At this point, the target tile should be above its target position,
            # with the 0 tile directly above it. We just have to move it down
            # by u-1 positions
            phase2_moves = phase2_moves + ['lddru'] * (len(up_moves) - 1) + ['ld']
            # and done
        res = ''.join(phase1_moves + phase2_moves)
        for charr in list(res):
            self.update_puzzle(charr)
        return res

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        target_tile = self.current_position(target_row, 0)
        # Start by moving the 0 tile to the current position of the target tile,
        # by moving up then to the right
        up_moves = ['u'] * (target_row - target_tile[0])
        right_moves = ['r'] * target_tile[1]
        phase1_moves = up_moves + right_moves
        # Now, try to get the target tile up-right of its target position, with the
        # 0 tile to its left
        phase2_moves = []
        if len(up_moves) == 1:
            if len(right_moves) == 0:
                # Easy case
                phase2_moves = ['r'] * (self._width - 1)
                res = ''.join(phase1_moves + phase2_moves)
                for charr in res:
                    self.update_puzzle(charr)
                return res
            if len(right_moves) == 1:
                phase2_moves = phase2_moves + ['l']
            else:
                phase2_moves = phase2_moves + ['ulldr'] * (len(right_moves) - 1) + ['l']
        else:
            if len(right_moves) > 0:
                phase2_moves = phase2_moves + ['dllur'] * (len(right_moves) - 1) + ['dlu']
            phase2_moves = phase2_moves + ['rddlu'] * (len(up_moves) - 2) + ['rdl']
        # Should now have the 0 tile on the left of the target tile.
        # Use the answer from the quiz to put the target tile into place
        res = ''.join(phase1_moves + phase2_moves + ['ruldrdlurdluurddlur'] + (['r'] * (self._width - 2)))
        for charr in list(res):
            self.update_puzzle(charr)
        return res

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self.get_number(0, target_col) != 0:
            return False
        if self.get_number(1, target_col) != self._width + target_col:
            return False
        for col_dex in range(target_col+1, self._width):
            if self.get_number(0, col_dex) != col_dex:
                return False
            if self.get_number(1, col_dex) != self._width + col_dex:
                return False
        for row_dex in range(2, self._height):
            for col_dex in range(self._width):
                if self.get_number(row_dex, col_dex) != row_dex*self._width + col_dex:
                    return False
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self.get_number(1, target_col) != 0:
            return False
        for col_dex in range(target_col+1, self._width):
            if self.get_number(0, col_dex) != col_dex:
                return False
            if self.get_number(1, col_dex) != self._width + col_dex:
                return False
        for row_dex in range(2, self._height):
            for col_dex in range(self._width):
                if self.get_number(row_dex, col_dex) != row_dex*self._width + col_dex:
                    return False
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        self.update_puzzle('l')
        self.update_puzzle('d')
        target_tile = self.current_position(0, target_col)
        if target_tile == (0, target_col):
            return 'ld'
        up_moves = ['u'] * (1 - target_tile[0])
        left_moves = ['l'] * (target_col - 1 - target_tile[1])
        phase1_moves = up_moves + left_moves
        phase2_moves = []
        if len(up_moves) == 0:
            phase2_moves = phase2_moves + ['urrdl'] * (len(left_moves) - 1)
        else:
            if len(left_moves) == 0:
                phase2_moves = phase2_moves + ['ld']
            else:
                phase2_moves = ['drrul'] * (len(left_moves) - 1) + ['druld']
        # Final string taken from the homework quiz
        res = ''.join(phase1_moves + phase2_moves + ['urdlurrdluldrruld'])
        for charr in list(res):
            self.update_puzzle(charr)
        return 'ld' + res

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        target_tile = self.current_position(1, target_col)
        up_moves = ['u'] * (1 - target_tile[0])
        left_moves = ['l'] * (target_col - target_tile[1])
        phase1_moves = up_moves + left_moves
        phase2_moves = []
        if len(up_moves) == 0:
            phase2_moves = phase2_moves + ['urrdl'] * (len(left_moves) - 1) + ['ur']
        else:
            if len(left_moves) == 0:
                self.update_puzzle('u')
                return 'u'
            phase2_moves = phase2_moves + ['drrul'] * (len(left_moves) - 1) + ['dru']
        res = ''.join(phase1_moves + phase2_moves)
        for charr in list(res):
            self.update_puzzle(charr)
        return res

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # Just spam 'rdlu' until it's done
        tile0_position = self.current_position(0,0)
        res = ['u'] * tile0_position[0] + ['l'] * tile0_position[1]
        for charr in res:
            self.update_puzzle(charr)
        while self.get_number(0,1) != 1:
            res = res + ['rdlu']
            for charr in list('rdlu'):
                self.update_puzzle(charr)
        return ''.join(res)

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        if self.lower_row_invariant(0,0):
            return ''
        tile0_position = self.current_position(0,0)
        moves = ['r'] * (self._width - 1 - tile0_position[1]) + ['d'] * (self._height - 1 - tile0_position[0])
        for charr in list(''.join(moves)):
            self.update_puzzle(charr)
        pos_ind = self._width * self._height - 1
        while pos_ind >= (2 * self._width):
            if pos_ind % self._width > 0:
                moves = moves + [self.solve_interior_tile(int(pos_ind / self._width), pos_ind % self._width)]
                pos_ind -= 1
                assert self.lower_row_invariant(int(pos_ind / self._width), pos_ind % self._width)
            else:
                moves = moves + [self.solve_col0_tile(int(pos_ind / self._width))]
                pos_ind -= 1
                assert self.lower_row_invariant(int(pos_ind / self._width), pos_ind % self._width)
        # Now only a 2-by-m puzzle remains
        pos_ind = self._width - 1
        while pos_ind > 1:
            assert self.row1_invariant(pos_ind % self._width)
            moves = moves + [self.solve_row1_tile(pos_ind)]
            assert self.row0_invariant(pos_ind % self._width)
            moves = moves + [self.solve_row0_tile(pos_ind)]
            pos_ind -= 1
        # Now a 2-by-2 should remain
        moves = moves + [self.solve_2x2()]
        return ''.join(moves)

# Start interactive simulation
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))

