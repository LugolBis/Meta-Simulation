from cellular_parser import cellular_parser


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
    def __init__(self, state):
        assert_type(state, str)
        self._current_state = state
        self._next_state = None

    def update(self):
        if self._next_state == None:
            raise ValueError('Tried to update a Cell with no next state.')
        else:
            self._current_state = self._next_state
            self._next_state = None

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

    def push_back(self, current_state, next_state = None):
        '''
            Pushes the right end in O(1).
        '''
        assert_type(current_state, str)
        assert_type(next_state, str)

        self.rightmost.set_towards(Direction.Right, LinkedListNode(self.rightmost, None, Cell(current_state)))
        self.rightmost = self.rightmost.get_towards(Direction.Right) # type: ignore
        self.rightmost.get_value().set_next_state(next_state)

    
    def push_front(self, current_state, next_state = None):
        '''
            Pushes the left end in O(1)
        '''
        assert_type(current_state, str)
        assert_type(next_state, str)

        self.leftmost.set_towards(Direction.Left, LinkedListNode(None, self.leftmost, Cell(current_state)))
        self.leftmost = self.leftmost.get_towards(Direction.Left) # type: ignore
        self.leftmost.get_value().set_next_state(next_state)

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


def check_missing_field_error(fields: dict, expected: list, source: str):
    for e in expected:
        if not e in fields.keys():
            raise ValueError(f'Error in file "{source}" : Missing field "{e}".')

class CellularAutomaton:
    def __init__(self):
        pass


def load_cellular_from_file(path: str):
    parsed = {}
    with open(path) as stream:
        parsed = cellular_parser(stream.read())
    print(parsed)

    check_missing_field_error(parsed, ['Colors', 'States', 'Transitions', 'Initialisation'], path)

    config = Config(parsed['Initialisation'][0]);
    for cell in parsed['Initialisation'][1:]:
        config.push_back(cell)


    return config
 
   

if __name__ == '__main__':
    test = load_cellular_from_file('res/elargissement.cel')
    print(test)
