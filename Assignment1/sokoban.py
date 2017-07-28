"""Sokoban routines.

    A) Class SokobanState

    A specializion of the StateSpace Class that is tailored to the game of Sokoban.

    B) class Direction

    An encoding of the directions of movement that are possible for robots in Sokoban.

    Code also contains a list of 40 Sokoban problems for the purpose of testing.
"""

from search import *

class SokobanState(StateSpace):

    def __init__(self, action, gval, parent, width, height, robot, boxes, storage, obstacles,
                 restrictions=None, box_colours=None, storage_colours=None):
        """
        Create a new Sokoban state.

        @param width: The room's X dimension (excluding walls).
        @param height: The room's Y dimension (excluding walls).
        @param robot: A tuple of the robot's location.
        @param boxes: A dictionary where the keys are the coordinates of each box, and the values are the index of that box's restriction.
        @param storage: A dictionary where the keys are the coordinates of each storage point, and the values are the index of that storage point.
        @param obstacles: A frozenset of all the impassable obstacles.
        @param restrictions: A tuple of frozensets of valid storage coordinates for each box. None means that all storage locations are valid.
        @param box_colours: A mapping from each box to the colour to use with the visualizer.
        @param storage_colours: A mapping from each storage location to the colour to use with the visualizer.
        """
        StateSpace.__init__(self, action, gval, parent)
        self.width = width
        self.height = height
        self.robot = robot
        self.boxes = boxes
        self.storage = storage
        self.obstacles = obstacles
        self.restrictions = restrictions
        self.box_colours = box_colours
        self.storage_colours = storage_colours

    def successors(self):
        """
        Generate all the actions that can be performed from this state, and the states those actions will create.        
        """
        successors = []
        transition_cost = 1

        for direction in (UP, RIGHT, DOWN, LEFT):
            new_location = direction.move(self.robot)
            
            if new_location[0] < 0 or new_location[0] >= self.width:
                continue
            if new_location[1] < 0 or new_location[1] >= self.height:
                continue
            if new_location in self.obstacles:
                continue
            
            new_boxes = dict(self.boxes)

            if new_location in self.boxes:
                new_box_location = direction.move(new_location)
                
                if new_box_location[0] < 0 or new_box_location[0] >= self.width:
                    continue
                if new_box_location[1] < 0 or new_box_location[1] >= self.height:
                    continue
                if new_box_location in self.obstacles:
                    continue
                if new_box_location in new_boxes:
                    continue
                
                index = new_boxes.pop(new_location)
                new_boxes[new_box_location] = index
            
            new_robot = tuple(new_location)

            new_state = SokobanState(action=direction.name, gval=self.gval + transition_cost, parent=self,
                                     width=self.width, height=self.height, robot=new_robot,
                                     boxes=new_boxes, storage=self.storage, obstacles=self.obstacles,
                                     restrictions=self.restrictions, box_colours=self.box_colours,
                                     storage_colours=self.storage_colours)
            successors.append(new_state)

        return successors

    def hashable_state(self):
        """
        Return a data item that can be used as a dictionary key to UNIQUELY represent a state.
        """
        return hash((self.robot, frozenset(self.boxes.items())))

    def state_string(self):
        """
        Return a string representation of a state that can be printed to stdout.

        disable_terminal_colouring turns off terminal colouring for terminals
        that do not support ansi characters
        """
        disable_terminal_colouring = False
        fg_colours = {
            'red': '\033[31m',
            'cyan': '\033[36m',
            'blue': '\033[34m',
            'green': '\033[32m',
            'magenta': '\033[35m',
            'yellow': '\033[33m',
            'normal': '\033[0m'
        }
        bg_colours = {
            'red': '\033[41m',
            'cyan': '\033[46m',
            'blue': '\033[44m',
            'green': '\033[42m',
            'magenta': '\033[45m',
            'yellow': '\033[43m',
            'normal': '\033[0m'
        }
        map = []
        for y in range(0, self.height):
            row = []
            for x in range(0, self.width):
                row += [' ']
            map += [row]
        if self.storage_colours:
            if disable_terminal_colouring:
                for storage_point in self.storage:
                    map[storage_point[1]][storage_point[0]] = self.storage_colours[self.storage[storage_point]][0:1].upper()
            else:
                for storage_point in self.storage:
                    map[storage_point[1]][storage_point[0]] = bg_colours[self.storage_colours[self.storage[storage_point]]] + '.' + bg_colours['normal']
        else:
            for (i, storage_point) in enumerate(self.storage):
                map[storage_point[1]][storage_point[0]] = '.'
        for obstacle in self.obstacles:
            map[obstacle[1]][obstacle[0]] = '#'
        map[self.robot[1]][self.robot[0]] = '?'
        if self.box_colours:
            if disable_terminal_colouring:
                for box in self.boxes:
                    if box in self.storage:
                        if self.restrictions is None or box in self.restrictions[self.boxes[box]]:
                            map[box[1]][box[0]] = '$'
                        else:
                            map[box[1]][box[0]] = 'x'
                    else:
                        map[box[1]][box[0]] = self.box_colours[self.boxes[box]][0:1].lower()
            else:
                for box in self.boxes:
                    if box in self.storage:
                        if self.restrictions is None or box in self.restrictions[self.boxes[box]]:
                            map[box[1]][box[0]] = bg_colours[self.storage_colours[self.storage[box]]] + fg_colours[self.box_colours[self.boxes[box]]] + '$' + bg_colours['normal']
                        else:
                            map[box[1]][box[0]] = bg_colours[self.storage_colours[self.storage[box]]] + fg_colours[self.box_colours[self.boxes[box]]] + 'x' + bg_colours['normal']
                    else:
                        map[box[1]][box[0]] = fg_colours[self.box_colours[self.boxes[box]]] + '*' + fg_colours['normal']
        else:
            for box in self.boxes:
                if box in self.storage:
                    if self.restrictions is None or box in self.restrictions[self.boxes[box]]:
                        map[box[1]][box[0]] = '$'
                    else:
                        map[box[1]][box[0]] = 'x'
                else:
                    map[box[1]][box[0]] = '*'

        for y in range(0, self.height):
            map[y] = ['#'] + map[y]
            map[y] = map[y] + ['#']
        map = ['#' * (self.width + 2)] + map
        map = map + ['#' * (self.width + 2)]

        s = ''
        for row in map:
            for char in row:
                s += char
            s += '\n'

        return s        

    def print_state(self):
        """
        Print the string representation of the state. ASCII art FTW!
        """        
        print("ACTION was " + self.action)      
        print(self.state_string())


def sokoban_goal_state(state):
  """
  Returns True if we have reached a goal state.

  @param state: a sokoban state
  OUTPUT: True (if goal) or False (if not)
  """
  if state.restrictions is None:
    for box in state.boxes:
      if box not in state.storage:
        return False
    return True
  for box in state.boxes:
    if box not in state.restrictions[state.boxes[box]]:
      return False
  return True

def generate_coordinate_rect(x_start, x_finish, y_start, y_finish):
    """
    Generate tuples for coordinates in rectangle (x_start, x_finish) -> (y_start, y_finish)
    """
    coords = []
    for i in range(x_start, x_finish):
        for j in range(y_start, y_finish):
            coords.append((i, j))
    return coords

"""
Sokoban Problem Set, for testing
"""
PROBLEMS = (
    # Sokobanonline lesson problems are from https://www.sokobanonline.com/play/lessons
    # Boxxle problems are from: http://sokoban.info/?2 (any restrictions are our own)
    # Easiest 10
    # Problem 0, Sokobanonline lesson #2-1
    SokobanState("START", 0, None, 4, 4, # dimensions
                 (0, 3), #robot
                 {(1, 2): 0, (1, 1): 1}, #boxes
                 {(2, 1): 0, (2, 2): 1}, #storage
                 frozenset(((0, 0), (1, 0), (3, 3))), #obstacles
                 (frozenset(((2, 1),)), frozenset(((2, 2),))), #restrictions,
                 {0: 'cyan', 1: 'magenta'}, #box colours
                 {0: 'cyan', 1: 'magenta'} #storage colours
                 ),
    # Problem 1, Sokobanonline lesson #2-3
    SokobanState("START", 0, None, 5, 4, # dimensions
             (0, 3), #robot
             {(2, 1): 0, (3, 1): 1}, #boxes
             {(2, 1): 0, (3, 1): 1}, #storage
             frozenset(((0, 0), (4, 0), (2, 3), (3, 3), (4, 3))), #obstacles
             (frozenset(((3, 1),)), frozenset(((2, 1),))), #restrictions,
             {0: 'cyan', 1: 'magenta'}, #box colours
             {1: 'cyan', 0: 'magenta'} #storage colours
             ),
    # Problem 2, Sokobanonline lesson #2-5
    SokobanState("START", 0, None, 6, 4, # dimensions
             (5, 3), #robot
             {(1, 1): 0, (3, 1): 1}, #boxes
             {(2, 0): 0, (2, 2): 1}, #storage
             frozenset(((2, 1), (0, 0), (5, 0), (0, 3), (1, 3), (2, 3), (3, 3))), #obstacles
             (frozenset(((2, 0),)), frozenset(((2, 2),))), #restrictions,
             {0: 'cyan', 1: 'magenta'}, #box colours
             {0: 'cyan', 1: 'magenta'} #storage colours
             ),
    # Problem 3
    SokobanState("START", 0, None, 5, 5, # dimensions
                 (2, 1), # robot
                 {(1, 1): 0, (1, 3): 1, (3, 1): 2, (3, 3): 3}, #boxes
                 {(0, 0): 0, (0, 4): 1, (4, 0): 2, (4, 4): 3}, #storage
                 frozenset(((1, 0), (2, 0), (3, 0), (1, 4), (2, 4), (3, 4))), #obstacles
                 None
                 ),
    # Problem 4
    SokobanState("START", 0, None, 5, 5, # dimensions
                 (4, 0), #robot
                 {(3, 1): 0, (3, 2): 1, (3, 3): 2}, #boxes
                 {(0, 0): 0, (0, 4): 1, (0, 2): 2}, #storage
                 frozenset(((2, 0), (2, 1), (2, 3), (2, 4))), #obstacles
                 (frozenset(((0, 0),)), frozenset(((0, 4),)), frozenset(((0, 2),))), #restrictions
                 {0: 'cyan', 1: 'magenta', 2: 'yellow'},
                 {0: 'cyan', 1: 'magenta', 2: 'yellow'}
                 ),
    # Problem 5, Problem 4 with no hints
    SokobanState("START", 0, None, 5, 5, # dimensions
                 (4, 0), #robot
                 {(3, 1): 0, (3, 2): 1, (3, 3): 2}, #boxes
                 {(0, 0): 0, (0, 2): 1, (0, 4): 2}, #storage
                 frozenset(((2, 0), (2, 1), (2, 3), (2, 4))), #obstacles
                 None #restrictions
                 ),
    # Problem 6
    SokobanState("START", 0, None, 6, 5, # dimensions
        (0, 4), #robot
        {(1, 3): 0, (3, 3): 1}, # boxes
        {(5, 4): 0, (0, 1): 1}, # storages
        frozenset((generate_coordinate_rect(0, 4, 2, 3))), # obstacles
        None, # restrictions
        ),
    # Problem 7, Boxxle 1, problem 2
    SokobanState("Start", 0, None, 8, 7, # dimensions
        (5, 5), # robot
        {(3, 5): 1, (1, 3): 1, (3, 2): 0, (2, 1): 0}, # boxes
        {(0, 0): 1, (1, 0): 1, (0, 1): 0, (1, 1): 0}, # storages
        frozenset(((0, 4), (1, 4), (2, 4), (3, 4), (5, 4), (1, 5), (1, 6), (7, 6), (7, 5),
        (7, 4), (7, 3), (7, 2), (2, 2), (4, 2), (5, 2), (5, 1))), # obstacles
        (frozenset(((0, 1), (1, 1),)), frozenset(((0, 0), (1, 0),))),
        {0: 'cyan', 1: 'magenta'},
        {0: 'cyan', 1: 'magenta'}
        ),
    # Problem 8, Boxxle 1 problem 3
    SokobanState("Start", 0, None, 6, 4, # dimensions
        (1, 0),
        {(1, 1): 0, (2, 1): 0, (3, 2): 0, (4, 1): 0, (5, 2): 0}, # boxes
        {(4, 0): 0, (5, 0): 0, (5, 1): 0, (5, 2): 0, (5, 3): 0}, # storages
        frozenset(((0, 0), (2, 0), (3, 0), (0, 3), (1, 3), (2, 3))), # obstacles
        None
        ),
    # Problem 9, Boxxle 1 problem 4
    SokobanState("Start", 0, None, 6, 6, # dimensions
        (1, 0), # robot
        {(2, 1): 0, (1, 4): 0, (4, 5): 0}, # boxes
        {(0, 3): 0, (0, 4): 0, (0, 5): 0}, # storages
        frozenset(((0, 0), (0, 1), (0, 2), (1, 2), (1, 3), (3, 2), (3, 3), (4, 4),
        (3, 0), (4, 0), (5, 0), (5, 1), (5, 2))), # obstacles
        None
        ),

    # MEDIUM 10
    # Problem 10, Sokobanonline lesson #2-12
    SokobanState("START", 0, None, 6, 4, # dimensions
         (5, 3), #robot
         {(3, 1): 0, (2, 2): 1, (3, 2): 2, (4, 2): 3}, #boxes
         {(0, 0): 0, (2, 0): 1, (1, 0): 2, (1, 1): 3}, #storage
         frozenset((generate_coordinate_rect(4, 6, 0, 1)
                   + generate_coordinate_rect(0, 3, 3, 4))), #obstacles
         (frozenset(((0, 0),)), frozenset(((2, 0),)), frozenset(((1, 0),)), frozenset(((1, 1),))), #restrictions,
         {0: 'cyan', 1: 'magenta', 2: 'yellow', 3: 'red'}, #box colours
         {0: 'cyan', 1: 'magenta', 2: 'yellow', 3: 'red'} #storage colours
         ),
    # Problem 11, Sokobanonline lesson #2-12, less hints
    SokobanState("START", 0, None, 6, 4, # dimensions
         (5, 3), #robot
         {(3, 1): 0, (2, 2): 1, (3, 2): 2, (4, 2): 3}, #boxes
         {(0, 0): 0, (2, 0): 1, (1, 0): 2, (1, 1): 3}, #storage
         frozenset((generate_coordinate_rect(4, 6, 0, 1)
                   + generate_coordinate_rect(0, 3, 3, 4))), #obstacles
         (frozenset(((0, 0),)), frozenset(((2, 0),)), frozenset(((1, 0),)), frozenset(((0, 0), (2, 0), (1, 0), (1, 1),))), #restrictions,
         {0: 'cyan', 1: 'magenta', 2: 'yellow', 3: 'normal'}, #box colours
         {0: 'cyan', 1: 'magenta', 2: 'yellow', 3: 'red'} #storage colours
         ),
    # Problem 12
    SokobanState("START", 0, None, 9, 6, # dimensions
        (0, 0), #robot
        {(4, 3): 0, (6, 4): 1}, # Boxes
        {(1, 3): 0, (1, 5): 1}, # Storages
        frozenset((generate_coordinate_rect(2, 7, 2, 3) + generate_coordinate_rect(2, 3, 2, 6))), # obstacles
        None, #restrictions
        ),
    # Problem 13
    SokobanState("START", 0, None, 10, 7, # dimensions
        (0, 0), #robot
        {(5, 3): 0, (7, 4): 1}, # Boxes
        {(1, 3): 0, (1, 6): 1}, # Storages
        frozenset((generate_coordinate_rect(2, 8, 2, 3) + generate_coordinate_rect(2, 3, 2, 7))), # obstacles
        None, #restrictions
        ),
    # Problem 14
    SokobanState("Start", 0, None, 6, 6, # dimensions
        (5, 5), #robot
        {(3, 2): 0, (3, 3): 1, (3, 4): 2, (4, 3): 3}, # boxes
        {(0, 2): 0, (0, 3): 1, (0, 4): 2, (0, 5): 3}, # storages
        frozenset(((1, 2), (1, 3), (1, 4), (1, 5), (2, 2), (5, 1), (5, 0))), # obstacles
        None, # restrictions
        ),
    # Problem 15
    SokobanState("Start", 0, None, 6, 5, # dimensions
        (1, 4), # robot
        {(4, 4): 0, (1, 2): 1, (4, 0): 3}, # boxes
        {(0, 4): 0, (5, 2): 1, (0, 0): 3}, # storages
        frozenset(), # no obstacles
        None
        ),
    # Problem 16
    SokobanState("Start", 0, None, 7, 6, # dimensions
        (1, 0),
        {(1, 1): 0, (2, 3): 1, (2, 4): 1},
        {(2, 5): 0, (5, 1): 1, (5, 3): 1},
        frozenset(((3, 0), (3, 1), (3, 2), (3, 4), (3, 5),)),
        (frozenset(((2, 5),)), frozenset(((2, 5), (5, 1), (5, 3),))),
        {0: 'cyan', 1: 'normal'},
        {0: 'cyan', 1: 'magenta'}
        ),
    # Problem 17, Boxxle 1, problem 1
    SokobanState("Start", 0, None, 7, 7, # dimensions
        (0, 0), #robot
        {(1, 1): 0, (1, 2): 1, (2, 1): 1}, # boxes
        {(6, 2): 0, (6, 3): 1, (6, 4): 2}, # storages
        frozenset(((0, 3), (0, 4), (0, 5), (0, 6), (1, 3), (1, 4), (3, 0), (3, 1), (3, 2), (3, 3),
        (4, 3), (5, 3), (5, 2), (5, 1), (6, 1), (6, 6), (5, 6), (4, 6), (4, 5), )), # obstacles
        None
        ),
    # Problem 18, Boxxle 1 problem 5
    SokobanState("Start", 0, None, 8, 5, # dimensions
        (1, 2), # robot
        {(1, 1): 0, (3, 2): 0, (5, 3): 0, (6, 2): 0}, # boxes
        {(1, 4): 0, (1, 3): 0, (2, 4): 0, (2, 3): 0}, # storages
        frozenset(((0, 0), (0, 1), (0, 4), (3, 4), (3, 3), (7, 4), (7, 3), (7, 0), (6, 0),
            (2, 1), (3, 1), (4, 1))), # obstacles
        None
        ),
    # Problem 19, Boxxle 1 problem 8
    SokobanState("Start", 0, None, 8, 5, # dimensions
        (7, 2), # robot
        {(2, 2): 0, (3, 1): 0, (3, 3): 0, (4, 2): 0, (5, 3): 0}, # boxes
        {(0, 2): 0, (0, 3): 0, (1, 1): 0, (1, 2): 0, (1, 3): 0}, # storages
        frozenset(((0, 1), (0, 0), (1, 0), (2, 0), (4, 1), (5, 1), (7, 0), (7, 1), (7, 3), (7, 4),
            (0, 4), (1, 4), (2, 4), (3, 4))),
        None
        ),

    # HARD 20
    # Problem 20, Sokobanonline lesson #2-15
    SokobanState("START", 0, None, 8, 6, # dimensions
         (1, 2), #robot
         {(1, 3): 0, (2, 3): 1, (3, 3): 2, (4, 3): 3, (5, 3): 4}, #boxes
         {(7, 0): 0, (7, 1): 1, (7, 2): 2, (7, 3): 3, (7, 4): 4}, #storage
         frozenset((generate_coordinate_rect(0, 7, 0, 2) + [(0, 2), (6, 2), (7, 5)]
         + generate_coordinate_rect(0, 5, 5, 6))), #obstacles
         (frozenset(((7, 0),)), frozenset(((7, 1),)), frozenset(((7, 2),)), frozenset(((7, 3),)), frozenset(((7, 4),))), #restrictions,
         {0: 'cyan', 1: 'magenta', 2: 'yellow', 3: 'red', 4: 'green'}, #box colours
         {0: 'cyan', 1: 'magenta', 2: 'yellow', 3: 'red', 4: 'green'} #storage colours
         ),
    # Problem 21, https://www.sokobanonline.com/play/community/pc46/remodel-3/18907_puzzle-0201-kbr-901
    SokobanState("START", 0, None, 6, 5, # dimensions
         (5, 2), #robot
         {(3, 1): 0, (3, 2): 1, (3, 3): 2, (4, 2): 3}, #boxes
         {(1, 2): 0, (2, 2): 1, (3, 2): 2, (0, 2): 3}, #storage
         frozenset((generate_coordinate_rect(4, 6, 0, 1)
                    + generate_coordinate_rect(3, 6, 4, 5))
                    + [(1, 1), (1, 3)]), #obstacles
         (frozenset(((1, 2),)), frozenset(((2, 2),)), frozenset(((3, 2),)), frozenset(((0, 2),)), frozenset(((7, 4),))), #restrictions,
         {0: 'cyan', 1: 'magenta', 2: 'yellow', 3: 'red', 4: 'green'}, #box colours
         {0: 'cyan', 1: 'magenta', 2: 'yellow', 3: 'red', 4: 'green'} #storage colours
         ),
    # Problem 22
    SokobanState("START", 0, None, 8, 5, # dimensions
        (0, 3), #robot
        {(1, 3): 0, (3, 3): 1, (5, 3): 2}, # boxes
        {(7, 4): 0, (0, 1): 1, (0, 4): 2}, # storages
        frozenset((generate_coordinate_rect(0, 6, 2, 3))), # obstacles
        (frozenset(((7, 4), (0, 1),)), frozenset(((7, 4), (0, 1),)), frozenset(((0, 4),))), # restrictions,
        {0: 'normal', 1: 'normal', 2: 'cyan'},
        {0: 'magenta', 1: 'magenta', 2: 'cyan'}
        ),
    # Problem 23
    SokobanState("START", 0, None, 8, 5, # dimensions
        (0, 3), #robot
        {(1, 3): 0, (3, 3): 1, (5, 3): 2}, # boxes
        {(7, 4): 0, (0, 1): 1, (0, 4): 2}, # storages
        frozenset((generate_coordinate_rect(0, 6, 2, 3))), # obstacles
        None, # restrictions
        ),
    # Problem 24
    SokobanState("Start", 0, None, 10, 6, # dimensions
        (0, 3), #robot
        {(1, 1): 0, (3, 1): 1, (5, 1): 1}, # boxes
        {(7, 1): 0, (9, 5): 1, (8, 5): 1}, # storages
        frozenset((generate_coordinate_rect(0, 8, 0, 1) + generate_coordinate_rect(1, 8, 3, 4))), # obstacles
        (frozenset(((7,1),)), frozenset(((8, 5), (9, 5),))),
        {0: 'cyan', 1: 'magenta'},
        {0: 'cyan', 1: 'magenta'}
        ),
    # Problem 25
    SokobanState("Start", 0, None, 10, 6, # dimensions
        (0, 3), #robot
        {(1, 1): 1, (3, 1): 1, (5, 1): 0}, # boxes
        {(7, 1): 0, (9, 5): 1, (8, 5): 1}, # storages
        frozenset((generate_coordinate_rect(0, 8, 0, 1) + generate_coordinate_rect(1, 8, 3, 4))), # obstacles
        (frozenset(((7,1),)), frozenset(((8, 5), (9, 5),))),
        {0: 'cyan', 1: 'magenta'},
        {0: 'cyan', 1: 'magenta'}
        ),
    # Problem 26
    SokobanState("Start", 0, None, 6, 6, # dimensions
        (5, 5), #robot
        {(3, 2): 0, (3, 4): 1, (4, 3): 2, (3, 3): 3}, # boxes
        {(0, 5): 0, (0, 4): 1, (0, 3): 2, (0, 2): 3}, # storages
        frozenset(((1, 2), (1, 3), (1, 4), (1, 5), (2, 2), (5, 1), (5, 0))), # obstacles
        (frozenset(((0, 5),)), frozenset(((0, 4),)), frozenset(((0, 3),)), frozenset(((0, 2),))), # restrictions
        {0: 'cyan', 1: 'magenta', 2: 'yellow', 3: 'red'},
        {0: 'cyan', 1: 'magenta', 2: 'yellow', 3: 'red'}
        ),
    # Problem 27
    SokobanState("Start", 0, None,6, 5, # dimensions
        (5, 2), # robot
        {(4, 2): 0, (4, 1): 1, (3, 1): 2, (4, 3): 3, (3, 3): 4}, # boxes
        {(0, 0): 0, (0, 1): 1, (0, 2): 2, (1, 3): 3, (1, 4): 4}, # storages
        frozenset(((2, 1), (2, 3), (2, 4), (2, 0),)), # obstacles
        (frozenset(((0, 0),)), frozenset(((0, 1),)),
         frozenset(((0, 2),)), frozenset(((1, 3),)), frozenset(((1, 4),))), # restrictions
        {0: 'magenta', 1: 'yellow', 2: 'red', 3: 'green', 4: 'blue'},
        {0: 'magenta', 1: 'yellow', 2: 'red', 3: 'green', 4: 'blue'}
        ),
    # Problem 28
    SokobanState("Start", 0, None,6, 5, # dimensions
        (5, 2), # robot
        {(3, 1): 1, (4, 1): 1, (4, 2): 1, (4, 3): 1, (3, 3): 1}, # boxes
        {(0, 0): 1, (0, 1): 1, (0, 2): 1, (1, 3): 1, (1, 4): 1}, # storages
        frozenset(((2, 1), (2, 3), (2, 4), (2, 0))), # obstacles
        None
        ),
    # Problem 29
    SokobanState("Start", 0, None,7, 5, # dimensions
        (5, 2), # robot
        {(1, 1): 0, (4, 2): 1, (4, 1): 2, (3, 1): 3, (4, 3): 4, (3, 3): 5}, # boxes
        {(6, 2): 0, (0, 0): 1, (0, 1): 2, (0, 2): 3, (1, 3): 4, (1, 4): 5}, # storages
        frozenset(((2, 1), (2, 3), (2, 4),)), # obstacles
        (frozenset(((6, 2),)), frozenset(((0, 0),)), frozenset(((0, 1),)),
         frozenset(((0, 2),)), frozenset(((1, 3),)), frozenset(((1, 4),))), # restrictions
        {0: 'cyan', 1: 'magenta', 2: 'yellow', 3: 'red', 4: 'green', 5: 'blue'},
        {0: 'cyan', 1: 'magenta', 2: 'yellow', 3: 'red', 4: 'green', 5: 'blue'}
        ),
    # Problem 30
    SokobanState("Start", 0, None,7, 5, # dimensions
        (5, 2), # robot
        {(1, 1): 0, (3, 1): 1, (4, 1): 1, (4, 2): 1, (4, 3): 1, (3, 3): 1}, # boxes
        {(6, 2): 0, (0, 0): 1, (0, 1): 1, (0, 2): 1, (1, 3): 1, (1, 4): 1}, # storages
        frozenset(((2, 1), (2, 3), (2, 4),)), # obstacles
        (frozenset(((6, 2),)), frozenset(((0, 0), (0, 1), (0, 2), (1, 3), (1, 4),))), # restrictions
        {0: 'cyan', 1: 'magenta'},
        {0: 'cyan', 1: 'magenta'}
        ),
    # Problem 31
    SokobanState("Start", 0, None, 6, 6, # dimensions
        (0, 0), # robot
        {(4, 1): 0, (4, 2): 1, (4, 3): 2, (4, 4): 3}, # boxes
        {(0, 2): 0, (0, 3): 1, (1, 3): 2, (0, 5): 3}, # storages
        frozenset(((0, 1), (1, 1), (2, 1), (2, 2), (2, 3))), # obstacles
        None
        ),
    # Problem 32
    SokobanState("Start", 0, None, 5, 5, # dimensions
        (4, 1), # robot
        {(1, 3): 0, (1, 1): 1, (3, 2): 2}, # boxes
        {(0, 1): 0, (4, 2): 1, (0, 3): 2}, # storages
        frozenset(((0, 0), (1, 0), (0, 4), (1, 4))), # obstacles
        (frozenset(((1, 0),)), frozenset(((4, 2),)), frozenset(((0, 3),))), # restrictions
        {0: 'cyan', 1: 'magenta', 2: 'yellow'},
        {0: 'cyan', 1: 'magenta', 2: 'yellow'}
        ),
    # Problem 33
    SokobanState("Start", 0, None, 5, 5, # dimensions
        (2, 2), # robot
        {(1, 1): 0, (1, 2): 0, (1, 3): 0, (3, 1): 1, (3, 2): 1, (3, 3): 1}, # boxes
        {(0, 1): 1, (0, 2): 1, (0, 3): 1, (4, 1): 0, (4, 2): 0, (4, 3): 0}, # storages
        frozenset(), # No obstacles
        (frozenset(((4, 1), (4, 2), (4, 3),)), frozenset(((0, 1), (0, 2), (0, 3)))),
        {0: 'cyan', 1: 'magenta'},
        {0: 'cyan', 1: 'magenta'}
        ),
    # Problem 34
    SokobanState("Start", 0, None, 7, 5, # dimensions
        (6, 2), # robot
        {(3, 2): 0, (5, 2): 1, (3, 3): 1, (3, 1): 2, (4, 3): 2}, # boxes
        {(0, 1): 0, (0, 2): 1, (1, 2): 1, (0, 3): 2, (1, 3): 2}, # storages
        frozenset(((0, 4), (1, 4), (0, 0), (1, 0), (1, 1), (3, 0), (4, 4))), # walls
        (frozenset(((0, 1),)), frozenset(((0, 2), (1, 2))), frozenset(((0, 1), (0, 2), (1, 2), (0, 3), (1, 3)))), # restrictions
        {0: 'cyan', 1: 'magenta', 2: 'normal'},
        {0: 'cyan', 1: 'magenta', 2: 'yellow'}
        ),
    # Problem 35
    SokobanState("Start", 0, None, 7, 5, # dimensions
        (6, 2), # robot
        {(3, 3): 0, (3, 2): 1, (3, 1): 2, (4, 3): 3, (5, 2): 4}, # boxes
        {(0, 3): 0, (1, 3): 1, (0, 2): 2, (1, 2): 3, (0, 1): 4}, # storages
        frozenset(((0, 4), (1, 4), (0, 0), (1, 0), (1, 1), (3, 0), (4, 4))), # walls
        None,
        ),
    # Problem 36, Boxxle 1 problem 6 with simplification
    SokobanState("Start", 0, None, 9, 11, # dimensions
        (7, 0), # robot
        {(3, 5): 0, (3, 7): 1, (5, 7): 2, (5, 5): 3}, # boxes
        {(3, 3): 0, (1, 7): 1, (5, 9): 2, (7, 5): 3}, # storages
        frozenset(((4, 6), (6, 0), (6, 1), (5, 1), (4, 1), (3, 1), (2, 1), (2, 2), (1, 2), (0, 2),
            (0, 8), (0, 9), (0, 10), (6, 10), (7, 10), (8, 10), (8, 3), (8, 4),
            (6, 3), (5, 3), (4, 3), (3, 4), (1, 4), (1, 5), (1, 6), (2, 7), (2, 9),
            (3, 9), (4, 9), (5, 8), (7, 8), (7, 7), (7, 6), (6, 5))), # obstacles
        (frozenset(((3, 3),)), frozenset(((1, 7),)), frozenset(((5, 9),)), frozenset(((7, 5),))),
        {0: 'cyan', 1: 'magenta', 2: 'yellow', 3: 'red'},
        {0: 'cyan', 1: 'magenta', 2: 'yellow', 3: 'red'}
        ),
    # Problem 37, Boxxle 1 problem 7
    SokobanState("Start", 0, None, 8, 6, # dimensions
        (7, 0), # robot
        {(2, 2): 0, (3, 4): 1, (4, 2): 2, (6, 2): 2, (3, 3): 2}, # boxes
        {(0, 5): 0, (1, 5): 1, (2, 5): 2, (3, 5): 2, (4, 5): 2}, # storages
        frozenset(((2, 0), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (0, 4), (7, 5), (7, 4),
            (5, 0), (5, 1), (5, 3), (5, 4), (4, 3))), # obstacles
        (frozenset(((0, 5),)), frozenset(((1, 5),)), frozenset(((2, 5), (3, 5), (4, 5)))),
        {0: 'cyan', 1: 'magenta', 2: 'yellow'},
        {0: 'cyan', 1: 'magenta', 2: 'yellow'}
        ),
    # Problem 38, Boxxle 1 problem 9
    SokobanState("Start", 0, None, 9, 7, # dimensions
        (7, 6), # robot
        {(1, 5): 0, (4, 5): 0, (7, 5): 0, (7, 2): 1, (1, 2): 2, (4, 1): 2}, # boxes
        {(3, 3): 0, (4, 3): 0, (5, 3): 0, (5, 4): 1, (4, 4): 2, (3, 4): 2}, # storages
        frozenset(((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (2, 4), (2, 3), (3, 2), (4, 2), (5, 2),
            (6, 3), (6, 4), (8, 4), (8, 3), (8, 2), (8, 1), (8, 0), (3, 0), (4, 0))), # obstacles
        (frozenset(((3, 3), (4, 3), (5, 3),)), frozenset(((5, 4),)), frozenset(((4, 4), (3, 4),))),
        {0: 'cyan', 1: 'magenta', 2: 'yellow'},
        {0: 'cyan', 1: 'magenta', 2: 'yellow'}
        ),
    # Problem 39, Boxxle 1 problem 9 (no hints)
    SokobanState("Start", 0, None, 9, 7, # dimensions
        (7, 6), # robot
        {(1, 5): 0, (4, 5): 0, (7, 5): 0, (7, 2): 1, (1, 2): 2, (4, 1): 2}, # boxes
        {(3, 3): 0, (4, 3): 0, (5, 3): 0, (5, 4): 1, (4, 4): 2, (3, 4): 2}, # storages
        frozenset(((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (2, 4), (2, 3), (3, 2), (4, 2), (5, 2),
            (6, 3), (6, 4), (8, 4), (8, 3), (8, 2), (8, 1), (8, 0), (3, 0), (4, 0))), # obstacles
        None,
        )
)

"""
Sokoban Directions: encodes directions of movement that are possible for each robot.
"""
class Direction():
    """
    A direction of movement.
    """
    
    def __init__(self, name, delta):
        """
        Creates a new direction.
        @param name: The direction's name.
        @param delta: The coordinate modification needed for moving in the specified direction.
        """
        self.name = name
        self.delta = delta
    
    def __hash__(self):
        """
        The hash method must be implemented for actions to be inserted into sets 
        and dictionaries.
        @return: The hash value of the action.
        """
        return hash(self.name)
    
    def __str__(self):
        """
        @return: The string representation of this object when *str* is called.
        """
        return str(self.name)
    
    def __repr__(self):
        return self.__str__()
    
    def move(self, location):
        """
        @return: Moving from the given location in this direction will result in the returned location.
        """
        return (location[0] + self.delta[0], location[1] + self.delta[1])


#Global Directions
UP = Direction("up", (0, -1))
RIGHT = Direction("right", (1, 0))
DOWN = Direction("down", (0, 1))
LEFT = Direction("left", (-1, 0))



  
