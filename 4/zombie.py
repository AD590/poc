"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
               
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row,col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for cell in self._zombie_list:
            yield (cell[0], cell[1])
        return 

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for cell in self._human_list:
            yield (cell[0], cell[1])
        return
        
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        
        grid_height = self.get_grid_height()
        grid_width = self.get_grid_width()
        visited = poc_grid.Grid(grid_height, grid_width)
        for row in range(grid_height):
            for col in range(grid_width):
                if not self.is_empty(row, col):
                    visited.set_full(row, col)
        distance_field = [[grid_height * grid_width for dummy_col in range(grid_width)] for dummy_row in range(grid_height)]
        boundary  = poc_queue.Queue()
        if entity_type  == 'zombie':
            for cell in self._zombie_list:
                boundary.enqueue(cell)
        elif entity_type == 'human':
            for cell in self._human_list:
                boundary.enqueue(cell)
        for cell in boundary :
            distance_field[cell[0]][cell[1]] = 0
            visited.set_full(cell[0], cell[1])
        while len(boundary) != 0:
            current_cell = boundary.dequeue()
            neighbors = self.four_neighbors(current_cell[0], current_cell[1])
            for neighbor in neighbors:
                if visited.is_empty(neighbor[0], neighbor[1]):
                    visited.set_full(neighbor[0], neighbor[1])
                    boundary.enqueue(neighbor)
                    distance_field[neighbor[0]][neighbor[1]] = min(distance_field[neighbor[0]][neighbor[1]], distance_field[current_cell[0]][current_cell[1]] + 1)
       
        return distance_field
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        human_list = list(self._human_list)
        index = 0
        for cell in human_list:
            all_moves = self.eight_neighbors(cell[0], cell[1])
            all_moves.append(cell)
            max_distance = 0
            max_distance_moves =[]
            for move in all_moves:
                if self.is_empty(move[0], move[1]):
                    if zombie_distance[move[0]][move[1]] > max_distance:
                        max_distance_moves = [move]
                        max_distance = zombie_distance[move[0]][move[1]]
                    elif zombie_distance[move[0]][move[1]] == max_distance:
                        max_distance_moves.append(move)
             
            next_location = random.choice(max_distance_moves)
            self._human_list[index] = next_location
            index += 1
            
    
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        zombie_list = list(self._zombie_list)
        index = 0
        for cell in zombie_list:
            all_moves = self.four_neighbors(cell[0], cell[1])
            all_moves.append(cell)
            min_distance = float('inf')
            min_distance_moves =[]
            for move in all_moves:
                if self.is_empty(move[0], move[1]):
                    if human_distance[move[0]][move[1]] < min_distance:
                        min_distance_moves = [move]
                        min_distance = human_distance[move[0]][move[1]]
                    elif human_distance[move[0]][move[1]] == min_distance:
                        min_distance_moves.append(move)
             
            next_location = random.choice(min_distance_moves)
            self._zombie_list[index] = next_location
            index += 1

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Zombie(30, 40))
