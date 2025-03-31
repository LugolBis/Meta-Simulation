

class IntRef:
    def __init__(self, value):
        self.value = value
        
    def get_v(self): return self.value
    def set_v(self, x: int): self.value = x

    v = property(get_v, set_v)

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

def skip_spaces_until(sentinel: str, source: str, cursor: IntRef):
    while cursor < len(source):
        current = source[cursor.v]
        if current == sentinel:
            break
        elif current != ' ' and current != '\t':
            raise ValueError(parsing_error_str(cursor.v, sentinel, current))
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
        raise ValueError(parsing_error_str(cursor.v, 'number', source[cursor.v]))
    return int(parsed)
    

def tuple_parser(source: str, cursor: IntRef):
    '''
        Parses a tuple of integers.
        blank characters (except line break) ignored.
    '''
    state = 0
    parsed: list = None # type: ignore
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
                    to_append = None
                    base_cursor = cursor.v
                    try:
                        to_append = number_parser(source, cursor) # type: ignore
                    except:
                        cursor.v = base_cursor
                        to_append = name_parser(source, cursor)

                    parsed.append(to_append)
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
                if current.isalpha() or current == '*' or current == '_':
                    parsed += current
                    state = 1
                elif current != ' ' and current != '\t':
                    raise ValueError(parsing_error_str(cursor.v, 'letter, "*" or "_"', current))
            case 1:
                if current.isalpha() or current == '*' or current == '_':
                    parsed += current
                else:
                    break
        cursor.increment()
    return parsed

def dummy_name_parser(source: str, cursor: IntRef):
    n = name_parser(source, cursor)
    cursor.decrement()
    return n

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
    
def parse_dict(field_function, source: str, cursor: IntRef, in_fact_list = False):
    result = {}
    if in_fact_list:
        result = []
    state = 0
    while cursor < len(source):
        current = source[cursor.v]
        match state:
            case 0:
                line = field_function(source, cursor)
                if in_fact_list:
                    result.append(line)
                else:
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
    name = name_parser(source, cursor)
    
    skip_spaces_until('(', source, cursor)
    # Cursor on '('
    cursor.increment()
    subtype = name_parser(source, cursor)
    skip_spaces_until(')', source, cursor)

    return (name, subtype) 


def transition_parser(source: str, cursor: IntRef):
    left = tuple_parser(source, cursor)
    cursor.increment()

    skip_spaces_until('-', source, cursor)
    cursor.increment()
    
    if source[cursor.v] != '>':
        raise ValueError(parsing_error_str(cursor.v, '>', source[cursor.v]))
    cursor.increment()

    right = name_parser(source, cursor)
    cursor.decrement()

    return (left, right)


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
            data = parse_dict(dummy_name_parser, source, cursor, True)
    
    return (title, data)

def cellular_parser(source: str):
    cursor = IntRef(0)
    data = {}
    while cursor < len(source):
        field = field_parser(source, cursor)
        print(f"{field[0]} parsed !")
        data[field[0]] = field[1]
    return data

