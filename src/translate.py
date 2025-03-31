import sys

def translate_turing_machine(script_path:str, save_path:str):
    BUFFER = {} # key : StateName_READ, value : a tuple that contains the FUTUR_STATE, WRITE, MOVEMENT values
    TM_ALPHABET = set() # Store the symbols used by the Cellular Automaton
    with open (script_path,"r") as fs:
        init_state = fs.readline().strip()
        finals = fs.readline().strip().split(",") # Unused finals state
        input_word = fs.readline().strip().split(",")

        for line in fs:
            line = line.strip()
            if line != "":
                try:
                    current_state, read, futur_state, write, move = line.strip().split(",")
                    TM_ALPHABET.add(read) ; TM_ALPHABET.add(write)
                    if current_state in BUFFER.keys():
                        BUFFER[f"{current_state}{read}"] = (futur_state,write,move)
                    else:
                        BUFFER[f"{current_state}{read}"] = (futur_state,write,move)
                except Exception as error:
                    raise error

    # Store the alphabet of the CellularAutomaton -> {TM_Transitions U {*}} x TM_Alphabet
    CA_ALPHABET = set() 
    for state in BUFFER.keys():
        for letter in TM_ALPHABET:
            CA_ALPHABET.add(f"{state}")
            CA_ALPHABET.add(f"*{letter}")

    print(CA_ALPHABET)

    # TRANSITIONS store the transitions of the CellularAutomaton in this format : key : (CELL_Left, cell_middle, CELL_Right), value: New_CELL
    TRANSITIONS = dict()
    cell_without_state = {letter for letter in CA_ALPHABET if letter[0]=="*"} # Store all the cell alphabet that hasn't got transitions
    for state, transition in BUFFER.items():
        futur_state, write, move = transition
        match move:
            case "-":
                for cell_left in cell_without_state:
                    for cell_right in cell_without_state:
                        TRANSITIONS[(cell_left,state,cell_right)] = f"{futur_state}{write}"
            case ">":
                for cell_left in cell_without_state:
                    for cell_right in cell_without_state:
                        TRANSITIONS[(cell_left,state,cell_right)] = f"*{write}"
                for current_cell in cell_without_state:
                    for cell_right in cell_without_state:
                        TRANSITIONS[(state,current_cell,cell_right)] = f"{futur_state}{current_cell[1:]}"
            case "<":
                for cell_left in cell_without_state:
                    for cell_right in cell_without_state:
                        TRANSITIONS[(cell_left,state,cell_right)] = f"*{write}"
                for current_cell in cell_without_state:
                    for cell_left in cell_without_state:
                        TRANSITIONS[(cell_left,current_cell,state)] = f"{futur_state}{current_cell[1:]}"
            case default:
                print(f"Inconsistent symbol for movement : '{move}'")
    
    # Complete with the transitions where anything change
    for cell_left in CA_ALPHABET:
        for cell_middle in CA_ALPHABET:
            for cell_right in CA_ALPHABET:
                if (cell_left, cell_middle, cell_right) not in TRANSITIONS.keys():
                    TRANSITIONS[(cell_left, cell_middle, cell_right)] = cell_middle

    # Store the Colors of each state
    COLORS = set() 
    for index, value in enumerate(CA_ALPHABET):
        R,G,B = generate_color(index)
        COLORS.add((value,R,G,B))
    
    with open(save_path,"w")  as fd:
        CONTENT = ""
        
        CONTENT += "Colors:\n"
        for color in COLORS:
            CONTENT += f"   Color{color[0]} <- {color[1],color[2],color[3]},\n"
        CONTENT = CONTENT[:-2] + '\n' # Deleting last comma

        CONTENT += "\nStates:\n"
        for state in CA_ALPHABET:
            CONTENT += f"   {state}(Color{state}),\n"
        CONTENT = CONTENT[:-2] + '\n' # Deleting last comma

        CONTENT += "\nTransitions:\n"
        for cells, new_cell in TRANSITIONS.items():
            cell_left, cell_middle, cell_right = cells
            CONTENT += f"   ({cell_left}, {cell_middle}, {cell_right}) -> {new_cell},\n"
        CONTENT = CONTENT[:-2] + '\n' # Deleting last comma

        CONTENT += f"\nInitialisation:\n   *_, *_, {init_state}{input_word[0]},"
        for word in input_word[1:]:
            CONTENT += f" *{word},"
        CONTENT = CONTENT[:-1] + '\n' # Deleting last comma

        fd.write(CONTENT)
    print("Successfully translate The Turing Machine into a Cellular Automaton.")
    

def generate_color(n:int) -> tuple[int,int,int]:
    n1 = (768-n)%768
    n2 = (n1//256)%256
    return (n2,n2,n1%256)

translate_turing_machine("res/to_translate.tur","res/translated.cel")

