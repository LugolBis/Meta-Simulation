import sys
import random
from turing_machine import parser_tm_script
from utils import letter_from_color, color_from_letter

def translate_turing_machine(script_path:str, save_path:str):
    buffer = {} # key : StateName_READ, value : a tuple that contains the FUTUR_STATE, WRITE, MOVEMENT values
    tm_alphabet = set() # Store the symbols used by the Cellular Automaton
    with open (script_path,"r") as fs:
        init_state = parser_tm_script(fs)
        finals = parser_tm_script(fs).split(",") # Unused finals state
        input_word = parser_tm_script(fs).split(",")

        for line in fs:
            line = line.strip()
            if line != "" and not line.startswith("//"):
                try:
                    current_state, read, futur_state, write, move = line.strip().split(",")
                    tm_alphabet.add(read) ; tm_alphabet.add(write)
                    buffer[f"{current_state}{read}"] = (futur_state,write,move)

                    reject = f"{futur_state}{read}"
                    if reject not in buffer.keys():
                        buffer[reject] = (reject,"","-")
                except Exception as error:
                    print(f"Error line :\n'{line}'\n")
                    raise error

    # Store the alphabet of the CellularAutomaton -> {TM_transitions U {*}} x tm_alphabet
    ca_alphabet = set()

    # Generate the CA alphabet based on the finals states and the TM alphabet
    for state in finals:
        for letter in tm_alphabet:
            ca_alphabet.add(f"{state}{letter}")
            ca_alphabet.add(f"{init_state}{letter}")

    # Adding already formatted states stored in the buffer
    for state in buffer.keys():
        ca_alphabet.add(state)

    # Adding empty state for each letter in the TM alphabet
    for letter in tm_alphabet:
        ca_alphabet.add(f"*{letter}")

    # transitions store the transitions of the CellularAutomaton in this format : key : (CELL_Left, cell_middle, CELL_Right), value: New_CELL
    transitions = dict()
    cell_without_state = {letter for letter in ca_alphabet if letter[0]=="*"} # Store all the cell alphabet that hasn't got transitions
    for state, transition in buffer.items():
        futur_state, write, move = transition
        match move:
            case "-":
                for cell_left in cell_without_state:
                    for cell_right in cell_without_state:
                        transitions[(cell_left,state,cell_right)] = f"{futur_state}{write}"
            case ">":
                for cell_left in cell_without_state:
                    for cell_right in cell_without_state:
                        transitions[(cell_left,state,cell_right)] = f"*{write}"
                for current_cell in cell_without_state:
                    for cell_right in cell_without_state:
                        transitions[(state,current_cell,cell_right)] = f"{futur_state}{current_cell[1:]}"
            case "<":
                for cell_left in cell_without_state:
                    for cell_right in cell_without_state:
                        transitions[(cell_left,state,cell_right)] = f"*{write}"
                for current_cell in cell_without_state:
                    for cell_left in cell_without_state:
                        transitions[(cell_left,current_cell,state)] = f"{futur_state}{current_cell[1:]}"
            case default:
                print(f"Inconsistent symbol for movement : '{move}'")

    # Store the colors of each state
    colors = set() 
    generated = []
    for index, value in enumerate(ca_alphabet):

        r, g, b = color_from_letter(value[-1])

        colors.add((value, r, g, b))
    
    with open(save_path,"w")  as fd:
        content = ""
        
        content += "Colors:\n"
        for color in colors:
            content += f"   Color{color[0]} <- {color[1],color[2],color[3]},\n"
        content = content[:-2] + '\n' # Deleting last comma

        content += "\nStates:\n"
        for state in ca_alphabet:
            content += f"   {state}(Color{state}),\n"
        content = content[:-2] + '\n' # Deleting last comma

        content += "\nTransitions:\n"
        for cells, new_cell in transitions.items():
            cell_left, cell_middle, cell_right = cells
            content += f"   ({cell_left}, {cell_middle}, {cell_right}) -> {new_cell},\n"
        content = content[:-2] + '\n' # Deleting last comma

        content += f"\nInitialisation:\n   *_, *_, {init_state}{input_word[0]},"
        for word in input_word[1:]:
            content += f" *{word},"
        content += f' *_, *_\n'

        fd.write(content)
    print("Successfully translate The Turing Machine into a Cellular Automaton.")
    

def generate_color(n:int) -> tuple[int,int,int]:
    '''
        Expects an 8-bit n.
    '''

    transpositions = [
        [0, 1, 2, 3, 4, 5, 6, 7],
        [7, 6, 5, 4, 3, 2, 1, 0],
        [4, 3, 2, 1, 0, 7, 6, 5]
    ]

    # Apply transpositions
    result = []
    for trans in transpositions:
        composante = 0
        old_index = 0
        for new_index in trans:
            composante = composante | (nth_bit(n, old_index) << new_index)
            old_index += 1
        result.append(composante)

    return tuple(result)

def nth_bit(x: int, n: int) -> int:
    return (x >> n)%2


if __name__ == "__main__":

    args = sys.argv[1:]
    if len(args)>0:
        translate_turing_machine(args[0],"res/translated.cel")
    else:
        translate_turing_machine("res/binary_add.tur","res/translated.cel")