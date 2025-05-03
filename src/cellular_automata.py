from cellular_parser import cellular_parser
import sys
from copy import deepcopy

from utils import letter_from_color

def assert_type(val, t):
    '''
        Checks if `val` is of type `t` and throws a (catchable) `ValueError` if not.
    '''
    if val != None and not isinstance(val, t):
        found = str(type(val)).split("'")[1] ; expected = str(t).split("'")[1]
        raise ValueError(f'Wrong type ! Found : {val} of type {found} instead of {expected}.')

class State:
    '''
        Represents a cell's state.  
    '''
    def __init__(self, name: str, color: tuple):
        self.name = name
        self.color = color
    
class Cell:
    '''
        Glorified 2-uplet (current: State, next: State)
    '''
    def __init__(self, state: str):
        assert_type(state, str)
        self._current_state = state
        self._next_state = None

    def update(self):
        '''
            Sets current state as next state.
            Returns true if state has changed.
        '''

        if self._next_state == None:
            raise ValueError('Tried to update a Cell with no next state.')
        else:
            has_changed = self._current_state != self._next_state

            self._current_state = self._next_state
            self._next_state = None

            return has_changed

    def get_current_state(self):
        return self._current_state

    def set_next_state(self, state):
        assert_type(state, str)

        self._next_state = state


class Direction:
    '''
        A C style enumeration.
        TODO: Change to `bool` values and check if
              it doesn't break anything (it will)
    '''
    Left  = 0
    Right = 1

class LinkedListNode:
    '''
        <b>Double<b>LinkedListNode was too long to type
    '''
    def __init__(self, left, right, value):
        assert_type(left, LinkedListNode)
        assert_type(right, LinkedListNode)
        # No assert type on `value` so that this type
        # can be used genericly

        self._left = left
        self._right = right
        self._value = value

    def get_towards(self, d):
        assert_type(d, int)

        match d:
            case Direction.Left:
                return self._left
            case Direction.Right:
                return self._right

    def set_towards(self, d, v):
        assert_type(d, int)
        assert_type(v, LinkedListNode)

        match d:
            case Direction.Left:
                self._left = v
            case Direction.Right:
                self._right = v

    def get_value(self):
        return self._value


class Config:
    '''
        Encapsulate a cellular automaton's tape with references
        to its leftmost and rightmost nodes so that any push
        operation is O(1).
        TODO: Make attributes private
    '''

    def __init__(self, first):
        assert_type(first, str)

        self.leftmost: LinkedListNode = LinkedListNode(None, None, Cell(first))
        self.rightmost: LinkedListNode = self.leftmost
        self.length: int = 1

        
    def push_front(self, current_state, next_state = None):
        '''
            Pushes the left end in O(1)
        '''
        assert_type(current_state, str)
        assert_type(next_state, str)

        self.leftmost.set_towards(Direction.Left, LinkedListNode(None, self.leftmost, Cell(current_state)))
        self.leftmost = self.leftmost.get_towards(Direction.Left) # type: ignore
        self.leftmost.get_value().set_next_state(next_state)

        self.length += 1

    def push_back(self, current_state, next_state = None):
        '''
            Pushes the right end in O(1).
        '''
        assert_type(current_state, str)
        assert_type(next_state, str)

        self.rightmost.set_towards(Direction.Right, LinkedListNode(self.rightmost, None, Cell(current_state)))
        self.rightmost = self.rightmost.get_towards(Direction.Right) # type: ignore
        self.rightmost.get_value().set_next_state(next_state)

        self.length += 1

    def pop_front(self):
        self.leftmost = self.leftmost.get_towards(Direction.Right) # type: ignore
        self.leftmost.set_towards(Direction.Left, None)

        self.length -= 1

    def pop_back(self):
        self.rightmost = self.rightmost.get_towards(Direction.Left) # type: ignore
        self.rightmost.set_towards(Direction.Right, None)

        self.length -= 1

    def __repr__(self):
        '''
            Nice formatting
        '''
        current = self.leftmost
        to_return = "|"
        while current != None:
            to_return += f" {(current.get_value().get_current_state())} |"
            current = current.get_towards(Direction.Right)

        return to_return

    def __len__(self):
        return self.length

def check_missing_field_error(fields: dict, expected: list, source: str):
    for e in expected:
        if not e in fields.keys():
            raise ValueError(f'Error in file "{source}" : Missing field "{e}".')

class TreeNode:
    def __init__(self, name: str):
        self._name     = name 
        self._children = []


    def has_child(self, s: str):
        return s in [c._name for c in self._children]

    def add_child(self, n):
        self._children.append(n)

    def get_child(self, n):
        for c in self._children:
            if c._name == n:
                return c
        return None
    
class IndexTree:
    def __init__(self, index: tuple, dimension: int):
        self._index = index
        self._root = TreeNode('root')
        self._dimension = dimension

    def check_index_valid(self, index: tuple):
          
        if self._dimension != len(index):
            raise ValueError(f'Expected index of size {self._dimension}, found size {len(index)}.')
        for i in index:
            if not i in self._index:
                raise ValueError(f'Index {i} is not in {self._index}.')

    def set(self, index: tuple, value: str):
        self.check_index_valid(index)

        last = None
        current = self._root
        for v in index:
            last = current
            current = current.get_child(v) # type: ignore
            if current == None:
                current = TreeNode(v)
                last.add_child(current)

        current._children.clear()
        current._children.append(TreeNode(value))
            
        
    def get(self, index: tuple):
        self.check_index_valid(index)

        current: TreeNode = self._root
        
        for i in index:
            current = current.get_child(i) # type: ignore
            if current == None:
                return None

        return current._children[0]._name # type: ignore
      
class CellularAutomaton:
    def __init__(self, states: tuple, subtypes: dict, colors: dict):
        self._rules = IndexTree(states, 3)
        self._colors = colors
        self._subtypes = subtypes

    def _apply_rules(self, left: Cell, center: Cell, right: Cell):
        next_state = self._rules.get((left.get_current_state(), center.get_current_state(), right.get_current_state()))
        if next_state != None:
            center.set_next_state(next_state)
        else:
            center.set_next_state(center.get_current_state())

    def _extend_if_necessary(self, edge: tuple, direction: int, config: Config):
        
        self._apply_rules(edge[0], edge[1], edge[2]) # type: ignore
        if edge[1]._next_state != 'Blank':
            # Yes we should !
            match direction:
                case Direction.Left:
                    config.push_front('Blank', edge[1]._next_state)
                case Direction.Right:
                    config.push_back('Blank', edge[1]._next_state)
    def step(self, config: Config, watch = ("None", "None", "None")):
        '''
            Makes a single step in simulation.
            This methode returns a 2-uplet of booleans,
            the first is true if the `watch` transition
            is applied and the second is true if this
            step has changed the configuration.
        '''

        is_watched_transition_applied = False
        changed_config                = False

        # Adding theoritical edge cells

        config.push_front('Blank')
        config.push_back('Blank')
        
        # Let's apply rules on all cells

        current = config.leftmost
        last_node: LinkedListNode = None # type: ignore
        while current != None:

            # Getting last and next state str
            last = 'Blank'
            if last_node != None:
                # We are NOT at the leftmost cell
                last = last_node.get_value().get_current_state()
            next_node = current.get_towards(Direction.Right)
            next = 'Blank'
            if next_node != None:
                # We are NOT at the rightmost cell
                next = next_node.get_value().get_current_state()

            if (last, current.get_value().get_current_state(), next) == watch:
                is_watched_transition_applied = True

            # Applying

            # Inplace modification can only occur in `current`
            self._apply_rules(Cell(last), current.get_value(), Cell(next))

            # Onto the next node !
            last_node = current
            current = current.get_towards(Direction.Right)


        # Updating the cells
        current = config.leftmost
        while current != None:
            if current.get_value().update():
                changed_config = True
            current = current.get_towards(Direction.Right)

        # Deleting edge cells if blank
        if config.leftmost.get_value().get_current_state() == 'Blank':
            config.pop_front()
        if config.rightmost.get_value().get_current_state() == 'Blank':
            config.pop_back()

        return (is_watched_transition_applied, changed_config)
        
def load_cellular_from_file(path: str):
    parsed = {}
    with open(path) as stream:
        parsed = cellular_parser(stream.read())

    check_missing_field_error(parsed, ['Colors', 'States', 'Transitions', 'Initialisation'], path)

    config = Config(parsed['Initialisation'][0]);
    for cell in parsed['Initialisation'][1:]:
        config.push_back(cell)

    parsed['Colors']['Blank'] = (255, 255, 255)

    automaton = CellularAutomaton(tuple(list(parsed['States'].keys()) + ['Blank']), parsed['States'], parsed['Colors'])

    for transition in parsed['Transitions']:
        automaton._rules.set(transition, parsed['Transitions'][transition])        

    return (automaton, config)


class StopRule:
    def __init__(self, max_step = -1, last_transition = ("None", "None", "None"), stop_when_still = False):
        self.max_step = max_step
        self.last_transition = last_transition
        self.stop_when_still = stop_when_still

def simulate_automaton(automaton: CellularAutomaton, config: Config, stop_rule: StopRule):
    '''
        This function implements the question 5.
    '''

    steps = 0
    while True:        
        # Simulation automaton
        (last_transition_applied, changed) = automaton.step(config, watch = stop_rule.last_transition)
        steps += 1
        
        print(f'Step {steps} :\n\t{config}\n')

        # Stopping simulation if either of stop_rule's limitations are reached
        if last_transition_applied:
            print("Stopped because automaton applied end transition.")
            break;
        if stop_rule.stop_when_still and not changed:
            print("Stopped because config did not change.")
            break
        if stop_rule.max_step == steps:
            print("Stopped after simulating max_step.")
            break

'''
# Testing question 5
(automaton, config) = load_cellular_from_file('res/palindrome.cel')
simulate_automaton(automaton, config, StopRule(stop_when_still = True))
'''

if __name__ == '__main__':
    import pygame
    
    args = sys.argv[1:]
    loaded = ""
    if len(args)>0:
        loaded = args[0]
    else:
        loaded = 'res/elargissement.cel'

    (automaton, config) = load_cellular_from_file(loaded)

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.SysFont('Arial', 16)
    clock = pygame.time.Clock()
    running = True
    compteur = 0
    result = ""

    while running or result!="":

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                result=""

        screen.fill("white")

        current = config.leftmost
        i = 0
        while current != None:
            
            screen.blit(font.render(f"Cellular automaton : {loaded}", True, (0, 0, 0)), dest=(10, 10))

            # Drawing a cell
            try:
                # Tries to draw as letter
                letter = letter_from_color(automaton._colors[automaton._subtypes[current.get_value().get_current_state()]])
                pygame.draw.rect(
                    screen,
                    "black",
                    (400 + (i - len(config)/2) * 20, 300, 20, 20),
                    1
                )
                screen.blit(
                    font.render(letter, True, (0, 0, 0)),
                    dest = (405 + (i - len(config)/2) * 20, 300, 0, 0)
                )
            except:
                # Not a letter matching magic value state
                pygame.draw.rect(
                    screen,
                    automaton._colors[automaton._subtypes[current.get_value().get_current_state()]],
                    (400 + (i - len(config)/2) * 20, 300, 20, 20)
                )
            
            current = current.get_towards(Direction.Right)
            i += 1
        
        pygame.display.flip()

        clock.tick(60)
        
        # Making the automaton step every 25 frames
        compteur = (compteur + 1)%25
        if compteur == 0:
            automaton.step(config)
