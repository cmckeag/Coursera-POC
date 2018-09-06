"""
Student portion of Zombie Apocalypse mini-project

Requires the poc provided modules to actually run, so the code won't work.
But the logic for the grid and breadth first search is accurate.
"""

import random
#import poc_grid
#import poc_queue
#import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        Was already implemented
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
        self._human_list = []
        self._zombie_list = []
        
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
        for item in self._zombie_list:
            yield item

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row,col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for item in self._human_list:
            yield item
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        visited = poc_grid.Grid(self.get_grid_height(), self.get_grid_width())
        dummy_value = self.get_grid_height() * self.get_grid_width()
        dfield = [[dummy_value for dummy_col in range(self._grid_width)] 
                       for dummy_row in range(self._grid_height)]
        boundary = poc_queue.Queue()
        gen = None
        if entity_type == HUMAN:
            gen = self.humans()
        elif entity_type == ZOMBIE:
            gen = self.zombies()
        for item in gen:
            boundary.enqueue(item)
            visited.set_full(item[0], item[1])
            dfield[item[0]][item[1]] = 0
        while len(boundary) > 0:
            current_cell = boundary.dequeue()
            for neighbor in self.four_neighbors(current_cell[0], current_cell[1]):
                if visited.is_empty(neighbor[0], neighbor[1]):
                    visited.set_full(neighbor[0], neighbor[1])
                    if self.is_empty(neighbor[0], neighbor[1]):
                        boundary.enqueue(neighbor)
                        dfield[neighbor[0]][neighbor[1]] = dfield[current_cell[0]][current_cell[1]] + 1
        return dfield
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        new_human_list = []
        for pos in self.humans():
            spaces_and_values = {}
            current_value = zombie_distance_field[pos[0]][pos[1]]
            if pos[1] > 0 and self.is_empty(pos[0], pos[1]-1):
                spaces_and_values[(pos[0], pos[1]-1)] = zombie_distance_field[pos[0]][pos[1]-1]
            if pos[0] > 0 and self.is_empty(pos[0]-1, pos[1]):
                spaces_and_values[(pos[0]-1, pos[1])] = zombie_distance_field[pos[0]-1][pos[1]]
            if pos[1] < self.get_grid_width() - 1 and self.is_empty(pos[0], pos[1]+1):
                spaces_and_values[(pos[0], pos[1]+1)] = zombie_distance_field[pos[0]][pos[1]+1]
            if pos[0] < self.get_grid_height() - 1 and self.is_empty(pos[0]+1, pos[1]):
                spaces_and_values[(pos[0]+1, pos[1])] = zombie_distance_field[pos[0]+1][pos[1]]
            if pos[1] > 0 and pos[0] > 0 and self.is_empty(pos[0]-1, pos[1]-1):
                spaces_and_values[(pos[0]-1, pos[1]-1)] = zombie_distance_field[pos[0]-1][pos[1]-1]
            if pos[1] > 0 and pos[0] < self.get_grid_height() - 1 and self.is_empty(pos[0]+1, pos[1]-1):
                spaces_and_values[(pos[0]+1, pos[1]-1)] = zombie_distance_field[pos[0]+1][pos[1]-1]
            if pos[1] < self.get_grid_width() - 1 and pos[0] > 0 and self.is_empty(pos[0]-1, pos[1]+1):
                spaces_and_values[(pos[0]-1, pos[1]+1)] = zombie_distance_field[pos[0]-1][pos[1]+1]
            if pos[1] < self.get_grid_width() - 1 and pos[0] < self.get_grid_height() - 1 and self.is_empty(pos[0]+1, pos[1]+1):
                spaces_and_values[(pos[0]+1, pos[1]+1)] = zombie_distance_field[pos[0]+1][pos[1]+1]
            if not spaces_and_values.values():
                new_human_list.append(pos)
                continue
            max_dist = max(spaces_and_values.values())
            potential_spaces = [key for key in spaces_and_values.keys() if spaces_and_values[key] == max_dist]
            if potential_spaces and max_dist > current_value:
                new_human_list.append(potential_spaces[random.randint(0, len(potential_spaces) - 1)])
            else:
                new_human_list.append(pos)
        self._human_list = new_human_list
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        new_zombie_list = []
        for pos in self.zombies():
            spaces_and_values = {}
            current_value = human_distance_field[pos[0]][pos[1]]
            if pos[1] > 0 and self.is_empty(pos[0], pos[1]-1):
                spaces_and_values[(pos[0], pos[1]-1)] = human_distance_field[pos[0]][pos[1]-1]
            if pos[0] > 0 and self.is_empty(pos[0]-1, pos[1]):
                spaces_and_values[(pos[0]-1, pos[1])] = human_distance_field[pos[0]-1][pos[1]]
            if pos[1] < self.get_grid_width() - 1 and self.is_empty(pos[0], pos[1]+1):
                spaces_and_values[(pos[0], pos[1]+1)] = human_distance_field[pos[0]][pos[1]+1]
            if pos[0] < self.get_grid_height() - 1 and self.is_empty(pos[0]+1, pos[1]):
                spaces_and_values[(pos[0]+1, pos[1])] = human_distance_field[pos[0]+1][pos[1]]
            if not spaces_and_values.values():
                new_zombie_list.append(pos)
                continue
            min_dist = min(spaces_and_values.values())
            potential_spaces = [key for key in spaces_and_values.keys() if spaces_and_values[key] == min_dist]
            if potential_spaces and min_dist < current_value:
                new_zombie_list.append(potential_spaces[random.randint(0, len(potential_spaces) - 1)])
            else:
                new_zombie_list.append(pos)
        self._zombie_list = new_zombie_list

# Start up gui for simulation

#poc_zombie_gui.run_gui(Apocalypse(30, 40))
