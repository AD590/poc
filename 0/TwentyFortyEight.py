"""
Clone of 2048 game.
"""

import poc_2048_gui
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
    Helper function that merges a single row or column in 2048
    """
    result = []
    addable = False
    for index in range(len(line)):
        if line[index] == 0:
            continue
        if not addable:
            result.append(line[index])
            addable = True
            continue
        if result[-1] == line[index] and addable:
            result[-1] *= 2
            addable = False
            continue
        result.append(line[index])
    fills = [0] * (len(line) - len(result))
    result.extend(fills)

    return result

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        
        up_initial = []
        down_initial = []
        left_initial = []
        right_initial = []
        for col in range(grid_width):
            up_initial.append((0,col))
            down_initial.append((grid_height - 1 , col))
        for row in range(grid_height):
            left_initial.append((row, 0))
            right_initial.append((row, grid_width - 1))
        
        self._initial_tiles = {UP : up_initial, DOWN : down_initial,
                               LEFT : left_initial, RIGHT : right_initial}
        print self._initial_tiles
        self.reset()
    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        line = [0] * self.get_grid_width()
        index = 0
        self._grid = []
        while index < self.get_grid_height():
            self._grid.append(list(line))
            index += 1
    
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        result = 'The Grid is:\n'
        for line in self._grid:
            for element in line:
                result += (str(element) + '\t') 
            result += '\n'
        return result

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width
                            
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        for initial_tile in self._initial_tiles[direction]:
            row = initial_tile[0]
            col = initial_tile[1]
            line = []
            while row < self._grid_height and row >= 0 and col < self._grid_width and col >= 0:
                line.append(self.get_tile(row, col))
                row += OFFSETS[direction][0]
                col += OFFSETS[direction][1]
            result = merge(line)
            row = initial_tile[0]
            col = initial_tile[1]
            index = 0
            while row < self._grid_height and row >= 0 and col < self._grid_width and col >= 0:
                self.set_tile(row,col,result[index])
                index += 1
                row += OFFSETS[direction][0]
                col += OFFSETS[direction][1]
        
        self.new_tile()
            
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        empty_squares = []
        for row in range(len(self._grid)):
            for col in range(len(self._grid[row])):
                if self._grid[row][col] == 0:
                    empty_squares.append((row,col))
        if len(empty_squares) != 0:
            selected_square = empty_squares[int(len(empty_squares) * random.random())]
            random_number = 2
            if (random.random() < 0.1):
                random_number = 4
            self._grid[selected_square[0]][selected_square[1]] = random_number
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """        
        self._grid[row][col] = value
    

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """        
        # replace with your code
        return self._grid[row][col]

poc_2048_gui.run_gui(TwentyFortyEight(4, 4))