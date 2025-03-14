def assert_type(val, t):
    '''
        Checks if `val` is of type `t` and throws a (catchable) `ValueError` if not.
    '''
    if val != None and not isinstance(val, t):
        found = str(type(val)).split("'")[1] ; expected = str(t).split("'")[1]
        raise ValueError(f'Wrong type ! Found : {val} of type {found} instead of {expected}.')

class State:
    '''
        Simple C style enumeration for code readability.
    '''
    Dead  = False
    Alive = True

class Cell:
    '''
        Glorified 2-uplet (current: State, next: State)
    '''
    def __init__(self, state):
        assert_type(state, bool)

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
        assert_type(state, bool)

        self._next_state = state


class Direction:
    '''
        Another C style enumeration.
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
        assert_type(first, bool)

        self.leftmost = LinkedListNode(None, None, Cell(first))
        self.rightmost = self.leftmost

    def push_back(self, current_state, next_state = None):
        '''
            Pushes the right end in O(1).
        '''
        assert_type(current_state, bool)
        assert_type(next_state, bool)

        self.rightmost.set_towards(Direction.Right, LinkedListNode(self.rightmost, None, Cell(current_state)))
        self.rightmost = self.rightmost.get_towards(Direction.Right)
        self.rightmost.get_value().set_next_state(next_state)

    def push_front(self, current_state, next_state = None):
        '''
            Pushes the left end in O(1)
        '''
        assert_type(current_state, bool)
        assert_type(next_state, bool)

        self.leftmost.set_towards(Direction.Left, LinkedListNode(None, self.leftmost, Cell(current_state)))
        self.leftmost = self.leftmost.get_towards(Direction.Left)
        self.leftmost.get_value().set_next_state(next_state)

    def __repr__(self):
        '''
            Nice formatting
        '''
        current = self.leftmost
        to_return = "|"
        while current != None:
            to_return += f" {int(current.get_value().get_current_state())} |"
            current = current.get_towards(Direction.Right)

        return to_return

class CellularAutomaton:
    '''
        Contains the rules to be applied as an 8 bit long array.
        This ensures that the user defines each and every transition
        and that their is one and only one transition per boolean 3-uplet.
    '''

    def __init__(self, rules):
        if len(rules) != 8:
            raise ValueError('Expected 8 rules.')
        else:
            for r in rules:
                assert_type(r, bool)
            self._rules = rules

    def encode_state_bits(left_bit, middle_bit, right_bit):
        '''
            Takes 3 booleans and transform them into an integer.
        '''
        assert_type(left_bit, bool)
        assert_type(middle_bit, bool)
        assert_type(right_bit, bool)

        return (left_bit << 2) + (middle_bit << 1) + (right_bit << 0)

    def step(self, config):
        '''
            Updates `config` with the set of rules `self._rules`
        '''

        assert_type(config, Config)

        # Check if we should enlarge the tape by its left end
        left_bit   = False
        middle_bit = False
        right_bit = config.leftmost.get_value().get_current_state()

        code = CellularAutomaton.encode_state_bits(left_bit, middle_bit, right_bit)

        if self._rules[code] == True:
            config.push_front(State.Dead, State.Alive)

        # Iterating over the whole list left to right and updating next states
        current = config.leftmost
        last = None
        while current != None:
            # (`next` seems no be a python keyword but this is how this variable should be named)
            nex = current.get_towards(Direction.Right)

            # Getting surroundings code
            left_bit = last != None and last.get_value().get_current_state()
            middle_bit = current.get_value().get_current_state()
            right_bit = nex != None and nex.get_value().get_current_state()

            code = CellularAutomaton.encode_state_bits(left_bit, middle_bit, right_bit)

            current.get_value().set_next_state(self._rules[code])

            # Moving forward
            last = current
            current = current.get_towards(Direction.Right)

        # Check if we should enlarge the list by its right end
        left_bit = last.get_value().get_current_state()
        middle_bit = False
        right_bit = False

        code = CellularAutomaton.encode_state_bits(left_bit, middle_bit, right_bit)

        if self._rules[code] == True:
            config.push_back(State.Dead, State.Alive)
        
        # Iterating over the tape right to left and committing changes
        current = config.rightmost
        while current != None:
            current.get_value().update()

            # Moving backwards
            config.leftmost = current
            current = current.get_towards(Direction.Left)

