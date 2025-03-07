class Symbol:

    def __init__(self, symbol:str="_"):
        assert isinstance(symbol,str), "ERROR : A Symbol take in input of it constructor a str."
        self._sym = symbol

    def set(self,new_value:str):
        self._sym = new_value

    sym = property(lambda x: x._sym,set)

    def __eq__(self, value):
        assert isinstance(value,Symbol), "ERROR : you can't compare a Symbol with an object who's not a Symbol."
        return self._sym == value.sym

    def __repr__(self):
        return f"{self._sym}"

class MoveTo:

    def __init__(self, movement:str=""):
        assert isinstance(movement,str), "ERROR : A MoveTo take in input of it constructor a str."
        match movement.lower():
            case "-" | "stay" : self._move = 0
            case "<" | "left" : self._move = 1
            case ">" | "right" : self._move = 2
            case _ : raise ValueError(f"Invalid movement : '{movement}'")

    def set(self,new_value:int):
        self._move = new_value

    move = property(lambda x: x._move,set)

    def __repr__(self):
        return f"{self._move}"
    
class Transition:

    def __init__(self,read:Symbol,write:Symbol,movement:MoveTo,futur_state:'State'):
        assert isinstance(read,Symbol), f"ERROR : A Transition take in input of it constructor a Symbol object for it's field : read.\nYour input : {read}"
        assert isinstance(write,Symbol), f"ERROR : A Transition take in input of it constructor a Symbol object for it's field : write.\nYour input : {write}"
        assert isinstance(movement,MoveTo), f"ERROR : A Transition take in input of it constructor a MoveTo object for it's field : movement.\nYour input : {movement}"
        assert isinstance(futur_state,State), f"ERROR : A Transition take in input of it constructor an State object for it's field : futur_state.\nYour input : {futur_state}"
        self._read = read
        self._write = write
        self._movement = movement
        self._futur_state = futur_state

    def set_read(self, new_read:Symbol):
        assert isinstance(new_read,Symbol), "ERROR : The read of a 'Transition' need to be a 'Symbol'"
        self._read = new_read

    def set_write(self, new_write:Symbol):
        assert isinstance(new_write,Symbol), "ERROR : The write of a 'Transition' need to be a 'Symbol'"
        self._write = new_write

    def set_movement(self, new_movement:MoveTo):
        assert isinstance(new_movement,MoveTo), "ERROR : The mocement of a 'Transition' need to be a 'MoveTo'"
        self._movement = new_movement

    def set_futur_state(self, new_futur_state:'State'):
        assert isinstance(new_futur_state,State), "ERROR : The futur_state of a 'Transition' need to be a 'int'"
        self._futur_state = new_futur_state

    def from_args(read:str,write:str,movement:str) -> 'Transition':
        """This function create a transition without an empty futur_state."""
        return Transition(Symbol(read), Symbol(write), MoveTo(movement), State([], False))

    read = property(lambda x: x._read,set_read)
    write = property(lambda x: x._write,set_write)
    movement = property(lambda x: x._movement,set_movement)
    futur_state = property(lambda x: x._futur_state,set_futur_state)

    def __repr__(self):
        return f"\nTransition :\nread : {self._read} ; write : {self._write} ;\nmovement : {str(self._movement)} ; futur_state : {id(self._futur_state)}"
    
class State:

    def __init__(self, transitions:list[Transition], final:bool):
        self._transitions = transitions
        self._final = final

    def set_transitions(self, new_transitions:list[Transition]):
        #assert isinstance(new_transitions,list[Transition]), "ERROR : The transitions property of a 'State' need to be a 'list[Transition]' object."
        self._transitions = new_transitions

    def append_transition(self, new_transition:Transition):
        assert isinstance(new_transition,Transition), "ERROR : The transitions property of a 'State' need to be a 'Transition' object."
        self._transitions.append(new_transition)

    def set_final(self, new_final:bool):
        assert isinstance(new_final, bool), "ERROR : The final property of a 'State' need to be a 'bool'."
        self._final = new_final

    def __repr__(self):
        representation = f"state is final : {self._final}"
        for transition in self._transitions : representation += f"\n{transition}"
        return representation

    transitions = property(lambda x: x._transitions,set_transitions)
    final = property(lambda x: x._final,set_final)  

class Tape:

    def __init__(self, left:'Tape', right:'Tape'):
        self._symbol = Symbol()
        self._left = left
        self._right = right

    def set_symbol(self, new_symbol:Symbol):
        assert isinstance(new_symbol,Symbol), "ERROR : The symbol of a 'Tape' need to be a 'Symbol'"
        self._symbol = new_symbol

    def set_left(self, new_left:'Tape'):
        assert isinstance(new_left,Tape), "ERROR : The left of a 'Tape' need to be a 'Tape'"
        self._left = new_left

    def set_right(self, new_right:'Tape'):
        assert isinstance(new_right,Tape), "ERROR : The right of a 'Tape' need to be a 'Tape'"
        self._right = new_right

    def from_liste(liste:list['str']) -> 'Tape':
        tape = Tape(None,None)
        if len(liste)>0:
            symbol = Symbol(liste.pop(0))
            tape.set_symbol(symbol)
            right_tape = Tape.from_liste(liste)
            right_tape.set_left(tape)
            tape.set_right(right_tape)
            return tape
        else:
            return tape
        
    def move_left(self) -> 'Tape':
        if isinstance(self._left, Tape):
            return self._left
        else:
            new_tape = Tape(None,self)
            self.set_left(new_tape)
            return new_tape
        
    def move_right(self) -> 'Tape':
        if isinstance(self._right, Tape):
            return self._right
        else:
            new_tape = Tape(self,None)
            self.set_right(new_tape)
            return new_tape
        
    def repr_left(self):
        if self._left == None : return "None"
        else : return f"|{self._left.repr_left()}|{self._left.symbol}"

    def repr_right(self):
        if self._right == None : return "None"
        else : return f"{self._right.symbol}|{self._right.repr_right()}|"
        
    def __repr__(self):
        representation = f"{self.repr_left()}|> {self._symbol} <|{self.repr_right()}"
        return representation

    symbol = property(lambda x: x._symbol,set_symbol)
    left = property(lambda x: x._left,set_left)
    right = property(lambda x: x._right,set_right)

class Configuration:

    def __init__(self, tape:Tape, current_state:State):
        self._tape = tape
        self._current_state = current_state

    def set_tape(self,new_tape:Tape):
        assert isinstance(new_tape,Tape), "ERROR : The 'Configuration' property 'tape' need to be a 'Tape' object."
        self._tape = new_tape

    def set_current_state(self,new_current_state:State):
        assert isinstance(new_current_state,State), "ERROR : The 'Configuration' property 'current_state' need to be a 'State' object."
        self._current_state = new_current_state

    def update(self) -> bool:
        current_symbol:Symbol = self._tape.symbol
        for transition in self._current_state.transitions:
            if transition.read == current_symbol:
                self._tape.set_symbol(transition.write)
                match transition.movement.move:
                    case 0: pass # When that match 'Stay'
                    case 1: self.set_tape(self._tape.move_left())
                    case 2: self.set_tape(self._tape.move_right())
                    case _: raise ValueError(f"ERROR : inconsistent value in MoveTo object : {transition.movement.move}")
                self.set_current_state(transition.futur_state)
                return True
        return False
    
    def __repr__(self):
        return f"-- Configuration --\nCurrent State : {self._current_state}\n\nTape :\n{self._tape}"

    tape = property(lambda x: x._tape,set_tape)
    current_state = property(lambda x: x._current_state,set_current_state)

class TuringMachine:

    def __init__(self, configuration:Configuration, states:set[State]):
        self._configuration = configuration
        self._states = states
        self._step = 0

    def from_script(path:str) -> 'TuringMachine':
        BUFFER = {} # key : state name, value : (State, []) the list contains the names of the futurs_states
        with open (path,"r") as fs:
            init_state = fs.readline().strip()

            finals = fs.readline().strip().split(",")
            for final_state in finals:
                BUFFER[final_state] = (State([],True),[])
            
            tape = Tape.from_liste(fs.readline().strip().split(","))

            for line in fs:
                line = line.strip()
                if line != "":
                    try:
                        current_state, read, futur_state, write, move = line.strip().split(",")
                        if current_state in BUFFER.keys():
                            BUFFER[current_state][0].append_transition(Transition.from_args(read,write,move))
                            BUFFER[current_state][1].append(futur_state)
                        else:
                            BUFFER[current_state] = (State([Transition.from_args(read,write,move)], False), [futur_state])
                    except Exception as error:
                        raise error
            
        for key, value in BUFFER.items():
            new_transitions = value[0].transitions
            for index, futur_state in enumerate(value[1]):
                if futur_state in BUFFER.keys():
                    new_transitions[index].set_futur_state(BUFFER[futur_state][0])
            BUFFER[key][0].set_transitions(new_transitions)
            
        return TuringMachine(Configuration(tape,BUFFER[init_state][0]),set())

    def set_configuration(self, new_configuration:Configuration):
        assert isinstance(new_configuration,Configuration), "ERROR : The 'TuringMachine' property 'configuration' need to be a 'Configuration' object."
        self._configuration = new_configuration

    def set_states(self, new_states:set[State]):
        assert isinstance(new_states,set[State]), "ERROR : The 'TuringMachine' property 'configuration' need to be a 'Dict[int, State]' object."
        self._states = new_states

    def set_step(self, new_step:int):
        assert isinstance(new_step,int), "ERROR : The 'TuringMachine' property 'step' need to be an 'int' object."
        self._step = new_step

    def check_final(self) -> bool:
        return self._configuration.current_state.final

    def run(self) -> bool:
        active = True
        while active:
            active = self._configuration.update()
        return self.check_final()

    def run_with_limit(self,limit:int) -> bool:
        active = True
        while active and self._step<limit:
            active = self._configuration.update()
            self._step += 1
        return self.check_final()

    def __repr__(self):
        return f"TuringMachine -- at step : {self._step}\n{self._configuration}"

    configuration = property(lambda x: x._configuration,set_configuration)
    states = property(lambda x: x._states,set_states)
    step = property(lambda x: x._step,set_step)

if __name__ == '__main__':
    mt = TuringMachine.from_script("/home/lugolbis/Bureau/UVSQ/L3_Info/S6/IN620/IN620/res/test.txt")
    mt.run()
    print("\n\n")
    print(mt)