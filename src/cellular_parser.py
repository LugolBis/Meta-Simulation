
from ast import Eq


class IntRef:
    def __init__(self, value):
        self.value = value
        
    @property
    def v(self): return self.value
    
    def increment(self, offset = 1):
        self.value += offset
    def decrement(self, offset = 1):
        self.value -= offset
    
    def __eq__(self, v: int):
        return self.value == v
    def __lt__(self, v: int):
        return self.value < v
    def __gt__(self, v: int):
        return self.value > v
    def __repr__(self):
        return str(self.value)

def parsing_error_str(cursor: int, expected: str, found: str):
    if found == ' ':
        found = 'space'
    elif found == '\t':
        found = 'indentation'
    elif found == '\n':
        found = 'line break'
    
    return f'Error at byte {cursor}. expected: "{expected}", found: "{found}".'

def skip_empty_lines(source: str, cursor: IntRef):
    while cursor < len(source) and source[cursor.v].isspace():
        cursor.increment()

def number_parser(source: str, cursor: IntRef) -> int:
    '''
        Returns parsed integer contained in any `str`.
        Accepts underscore and spaces in number.
        Raises a `ValueError` if source does not contain
        any number at cursor.
    '''
    parsed = ""
    while cursor < len(source):
        current = source[cursor.v]
        if '0' <= current <= '9':
            parsed += current
        elif current != '_' and current != ' ':
            break
        cursor.increment()
    
    if parsed == "":
        raise ValueError(f'No number at cursor {cursor}.')
    return int(parsed)
    

def tuple_parser(source: str, cursor: IntRef):
    '''
        Parses a tuple of integers.
        blank characters (except line break) ignored.
    '''
    state = 0
    parsed = None
    while cursor < len(source):
        current = source[cursor.v]
        if current != ' ' and current != '\t':
            match state:
                case 0:
                    # Before opening parenthesis
                    if current == '(':
                        parsed = []
                        state = 1
                    else:
                        raise ValueError(parsing_error_str(cursor.v, '(', current))
                case 1:
                    # Value parsing
                    parsed.append(number_parser(source, cursor)) # type: ignore
                    cursor.decrement()
                    state = 2
                case 2:
                    # Making sure separator or closing is here
                    if current == ',':
                        state = 1
                    elif current == ')':
                        break
                    else:
                        raise ValueError(parsing_error_str(cursor.v, 'separator or closed parenthesis', current))
                    
        cursor.increment()
    
    return tuple(parsed) # type: ignore


def name_parser(source: str, cursor: IntRef):
    state = 0
    parsed = ""
    while cursor < len(source):
        current = source[cursor.v]
        match state:
            case 0:
                # Before name
                if current.isalpha():
                    parsed += current
                    state = 1
                elif current != ' ' and current != '\t':
                    raise ValueError(parsing_error_str(cursor.v, 'letter', current))
            case 1:
                if current.isalpha():
                    parsed += current
                else:
                    break
        cursor.increment()
    return parsed

def dummy_name_parser(source: str, cursor: IntRef):
    return (name_parser(source, cursor), None)

def assignation_parser(source: str, cursor: IntRef):
    name = name_parser(source, cursor)
    found_arrow = False
    while cursor < len(source) - 1:
        current = source[cursor.v]
        next = source[cursor.v + 1]
        if current == '<' and next == '-':
            found_arrow = True
            cursor.increment(2)
            break
        elif current != ' ' and current != '\t':
            raise ValueError(parsing_error_str(cursor.v, 'left arrow (<-)', current))
        cursor.increment()
    
    if not found_arrow:
       raise ValueError(parsing_error_str(cursor.v, 'left arrow (<-)', 'end of file')) 
    
    return (name, tuple_parser(source, cursor))
    
def parse_dict(field_function, source: str, cursor: IntRef):
    result = {}
    state = 0
    while cursor < len(source):
        current = source[cursor.v]
        match state:
            case 0:
                line = field_function(source, cursor)
                result[line[0]] = line[1]
                state = 1
            case 1:
                if current == ',':
                    cursor.increment()
                    skip_empty_lines(source, cursor)
                    cursor.decrement()
                    state = 0
                elif current == '\n':
                    break
                elif current != ' ' and current != '\t':
                    raise ValueError(parsing_error_str(cursor.v, 'line break or new line', current))
        cursor.increment()
        
    return result

def subtype_parser(source: str, cursor: IntRef):
    raise NotImplementedError

def transition_parser(source: str, cursor: IntRef):
    raise NotImplementedError

def field_parser(source: str, cursor: IntRef):
    skip_empty_lines(source, cursor)
    
    title = name_parser(source, cursor)
    
    while cursor < len(source):
        current = source[cursor.v]
        if current == ':':
            cursor.increment(2)
            break
        elif current != ' ' and current != '\t':
            raise ValueError(parsing_error_str(cursor.v, ':', current))
        cursor.increment()
    
    data = {}
    match title:
        case "Colors":
            data = parse_dict(assignation_parser,source, cursor)
        case "States":
            data = parse_dict(subtype_parser, source, cursor)
        case "Transitions":
            data = parse_dict(transition_parser, source, cursor)
        case "Initialisation":
            data = parse_dict(dummy_name_parser, source, cursor)
    
    return data

print(field_parser('''
    Colors:
        Extremité <- (0,   0, 0),
        Centre    <- (0, 255, 0)

'''
, IntRef(0)))
