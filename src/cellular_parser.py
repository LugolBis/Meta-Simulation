'''
    Automate    -> Transitions Mot '\n'? Eof
    Transitions -> (Etat'\n')⁸
    Mot         -> Etat | Etat','Mot
    Etat        -> 'Mort' | 'Vivant'
'''

from cellular_automata import CellularAutomaton, Config

class Token:
    Unknown = 0
    State = 1
    BreakLine = 2
    Separator = 3
    EndOfFile = 4
    def __init__(self, text):
        self.text = text
        if text == '\n':
            self.value = Token.BreakLine
        elif text == ',':
            self.value = Token.Separator
        elif text == 'Vivant' or text == 'Mort':
            self.value = Token.State
        elif text == "":
            self.value = Token.Unknown
        elif text == "\0":
            self.value = Token.EndOfFile
        else:
            raise ValueError(f'Unknown text : {text}')

    def __repr__(self):
        if self.text == '\n':
            return 'LineBreak'
        elif self.text == ',':
            return 'Separator'
        elif self.text == '\0':
            return 'EOF'
        else:
            return self.text

class ParserState:
    Transitions = 0
    LetterOfWord = 1
    NextLetter = 2
    Done = 3


def tokenize(source):
    tokens = []
    multiline_comment_level = 0 
    in_simple_comment = False
    max_token_length = 6
    window = "\0\0"

    i = 0
    l = len(source)
    while i < l:
        if source[i] != ' ':
            window = window[1] + source[i]
            if multiline_comment_level != 0:
                if window == '*/':
                    multiline_comment_level -= 1
                elif window == '/*':
                    multiline_comment_level += 1
            elif in_simple_comment:
                if source[i] == '\n':
                    in_simple_comment = False
                    tokens.append(Token(source[i]))
            else:
                new_token = Token("")
                j = i
                m = j + max_token_length
                buffer = ""
                found_comment = False
                while j < m:
                    buffer += source[j]
                    if buffer == '/*':
                        multiline_comment_level = 1
                        found_comment = True
                        break
                    elif buffer == '//':
                        in_simple_comment = True
                        found_comment = True
                        break
                    else:
                        try:
                            new_token = Token(buffer)
                        except:
                            pass
                    j += 1
                
                if not found_comment:
                    if new_token.value == Token.Unknown:
                        raise ValueError(f'Unknown token : {buffer}')
                    else:
                        i += len(new_token.text) - 1
                        tokens.append(new_token)
                else:
                    i += 1

        i += 1


    tokens.append(Token('\0'))

    return tokens

def parse(tokens):
    state = ParserState.Transitions
    transitions = []
    init_word = []

    i = 0
    while i < len(tokens):
        token = tokens[i]
        if (i==0 and token.value == Token.BreakLine) or (i > 0 and token.value == Token.BreakLine and tokens[i-1].value == Token.BreakLine):
            i += 1
            continue

        match state:
            case ParserState.Transitions:
                if token.value == Token.State:
                    transitions.append(token.text == "Vivant")
                    if len(transitions) == 8:
                        state = ParserState.LetterOfWord
                    if i+1 >= len(tokens) or tokens[i+1].value != Token.BreakLine:
                        raise ValueError(f'Expected line break, found "{tokens[i+1].text}".')
                    else:
                        i += 1
                else:
                    raise ValueError(f'Unexpected token while parsing transitions : "{token}". Expected "Vivant" or "Mort".')
            case ParserState.LetterOfWord:
                if token.value == Token.State:
                    init_word.append(token.text == 'Vivant')
                    state = ParserState.NextLetter
                else:
                    raise ValueError(f'Unexpected token while parsing initial word : "{token}". Expected "Vivant" or "Mort".')
            case ParserState.NextLetter:
                if token.value == Token.Separator:
                    state = ParserState.LetterOfWord
                elif token.value == Token.EndOfFile or token.value == Token.BreakLine:
                    state = ParserState.Done
                else:
                    raise ValueError(f'Unexpected token while parsing initial word: "{token}". Expected ",", line break or EOF.')
            case ParserState.Done:
                if token.value != Token.BreakLine and token.value != Token.EndOfFile:
                    raise ValueError(f'Tokens after EOF : "{token}".')

        i += 1

    automaton = CellularAutomaton(transitions)
    config = Config(init_word[0])
    for i in range(1, len(init_word)):
        config.push_back(init_word[i])

    return (automaton, config)
