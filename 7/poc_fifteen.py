"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

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
        Updates the puzzle state based on the provided move string`
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
        if self._grid[target_row][target_col] != 0:
            return False
        for col in range(target_col + 1, self._width):
            if self._grid[target_row][col] != target_row * self._width + col:
                return False
        for row in range(target_row + 1, self._height):
            for col in range(self._width):
                if self._grid[row][col] != row * self._width + col:
                    return False
        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        ret = ''
        assert self.lower_row_invariant(target_row, target_col), 'not ready for solve_interior_tile(' + str(target_row) + ',' + str(target_col) + ')\n' + self.__str__() 
        position = self.current_position(target_row, target_col)
        if position[0] == target_row:
            ret += 'l' * (target_col - position[1])
            ret += 'urrdl' * (target_col - position[1] - 1)
            self.update_puzzle(ret)
            return ret
        elif position[1] == target_col:
            ret += 'u' * (target_row -position[0])
            ret += 'lddru' * (target_row - position[0] - 1)
            ret += 'ld'
            self.update_puzzle(ret)
            return ret
        elif position [0] == 0:
            ret += 'u' * (target_row - position[0])
            if position[1] < target_col:
                ret += 'l' * (target_col - position[1])
                ret += 'drrul' * (target_col - position[1] - 1)
                ret += 'dr'
            if position[1] > target_col:
                ret += 'r' * (position[1] - target_col)
                ret += 'dl'
                ret += 'lurdl' * (position[1] - target_col -1)
            ret += 'uld'
            ret +=  'druld'* (target_row - position[0]-1)
            self.update_puzzle(ret)
            return ret
        else :
            ret += 'u' * (target_row - position[0])
            if position[1] < target_col:
                ret += 'l' * (target_col - position[1])
                ret += 'urrdl' * (target_col - position[1] - 1)
            else:
                ret += 'r' * (position[1] - target_col - 1)
                ret += 'rulld' * (position[1] - target_col)
            ret += 'druld' * (target_row - position[0])
            self.update_puzzle(ret)
            return ret


    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, 0), 'not ready for solve_col0_tile'
        ret = ''
        position = self.current_position(target_row, 0)
        if position[0] == target_row - 1 and position[1] == 0:
            ret += 'u'
        elif position[0] == target_row -1 and position[1] == 1:
            ret += 'uurdldruuldrdlu'
        else:
            ret += 'r'
            if position[1] == 0:
                ret += 'u' * (target_row - position[0] - 1)
                ret += 'lu'
                ret += 'rddlu' * (target_row - position[0] - 1)
            if position[1] == 1:
                ret += 'u' * (target_row - position[0] - 1)
                ret += 'lurdlu'
                ret += 'rddlu' * (target_row - position[0] - 1)
            else:
                ret += 'u' * (target_row - position[0])
                ret += 'r' * (position[1] - 1)
                if position[0] == 0:
                    ret += 'dllur' * (position[1] - 1)
                else:
                    ret += 'ulldr' * (position[1] - 1)
                ret += 'dlu'
                ret += 'rddlu' * (target_row - position[0] -1)
        ret += 'r' * (self._width - 1)
        self.update_puzzle(ret)
        return ret 
        
        

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self._grid[0][target_col] != 0 :
            return False
        if self._grid[1][target_col] != self._width + target_col:
            return False
        for col in range(target_col + 1, self._width):
            for row in range(2):
                if self._grid[row][col] != self._width * row + col:
                    return False
        for row in range(2, self._height):
            for col in range(self._width):
                if self._grid[row][col] != self._width * row + col:
                    return False
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self._grid[1][target_col] != 0 :
            return False
        for col in range(target_col + 1, self._width):
            for row in range(2):
                if self._grid[row][col] != self._width * row + col :
                    return False
        for row in range(2, self._height):
            for col in range(self._width):
                if self._grid[row][col] != self._width * row + col:
                    return False
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col), 'Not ready for row0_invariant'
        position = self.current_position(0, target_col)
        if position == (0, target_col - 1):
            ret = 'ld'
        elif position == (1, target_col - 1):
            ret = 'ldlurrdluldrruld'
        else:
            ret = 'd'
            ret += 'l' * (target_col - position[1] - 1)
            if position[0] == 1:
                ret += 'uldruld'
            if position[0] == 0:
                ret += 'uld'
            ret += 'rruld' * (target_col - position[1] -1)
        self.update_puzzle(ret)
        return ret

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col), 'Not ready for row1_invariant'
        position = self.current_position(1, target_col)       
        if position[1] == target_col:
            self.update_puzzle('u')
            return 'u'
        ret = 'l' * (target_col - position[1])
        if position[0] == 0:
            ret += 'urdlur'
        if position [0] == 1:
            ret += 'ur'
        ret += 'rdlur' * (target_col - position[1] -1)
        self.update_puzzle(ret)
        return ret
    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        assert self.row1_invariant(1), 'Error!!'
        ret = 'ul'
        tmp = self.clone()
        tmp.update_puzzle(ret)
        for dummy in range(2):
            if tmp.row0_invariant(0):
                break
            tmp.update_puzzle('drul')
            ret += 'drul'
        self.update_puzzle(ret)
        return ret

    def start(self):
        """
        return a solution to move tile(0) to the start point
        """
        position = self.current_position(0,0)
        ret = 'r' * (self._width - position[1] - 1)
        ret += 'd' * (self._height - position[0] - 1)
        self.update_puzzle(ret)
        return ret
        
    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        tmp = self.clone()
        ret = tmp.start()
        for row in range(tmp.get_height() -1 , 1, -1):
            for col in range(tmp.get_width() -1, 0, -1):
                ret += tmp.solve_interior_tile(row, col)
            ret += tmp.solve_col0_tile(row)
        for col in range(self.get_width() -1, 1, -1):
            ret += tmp.solve_row1_tile(col)
            ret += tmp.solve_row0_tile(col)
        ret += tmp.solve_2x2()
        self.update_puzzle(ret)
        return ret

poc_fifteen_gui.FifteenGUI(Puzzle(3,3))

"""
class Test(poc_fifteen_gui.FifteenGUI):

    def __init__(self, puzzle, directions):
        poc_fifteen_gui.FifteenGUI.__init__(self, puzzle)
        self._frame.add_button('STEP', self.step, 100)
        self._directions = directions
        
    def step(self):
        if len(self._directions) == 0:
            print 'No move'
            return
        try:
            self._puzzle.update_puzzle(self._directions[0])
            self._directions = self._directions[1:]
        except:
            print "invalid move:", self._directions[0]
    
puz = Puzzle(4,4,[[1,1,1,1],[1,8,1,1],[10,1,0,11],[12,13,14,15]])
direction = puz.solve_interior_tile(2,2)
print direction
test = Test(puz, direction)
"""