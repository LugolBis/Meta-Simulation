class Cell:

    def __init__(self, alive:bool=False):
        assert isinstance(alive,bool), "ERROR : alive field of a 'Cell' object need to be a bool."
        self._alive = alive

    def set_alive(self,new_alive:bool):
        assert isinstance(new_alive,bool), "ERROR : alive field of a 'Cell' object need to be a bool."
        self._alive = new_alive

    alive = property(lambda x:x._alive,set_alive)

class Tape:

    def __init__(self, left:'Tape', right:'Tape'):
        self._cell = Cell()
        self._left = left
        self._right = right

    def set_cell(self, new_cell:Cell):
        assert isinstance(new_cell,Cell), "ERROR : The cell of a 'Tape' need to be a 'cell'"
        self._cell = new_cell

    def set_left(self, new_left:'Tape'):
        assert isinstance(new_left,Tape), "ERROR : The left of a 'Tape' need to be a 'Tape'"
        self._left = new_left

    def set_right(self, new_right:'Tape'):
        assert isinstance(new_right,Tape), "ERROR : The right of a 'Tape' need to be a 'Tape'"
        self._right = new_right

    def from_liste(liste:list[bool]) -> 'Tape':
        tape = Tape(None,None)
        if len(liste)>0:
            cell = Cell(liste.pop(0))
            tape.set_cell(cell)
            right_tape = Tape.from_liste(liste)
            right_tape.set_left(tape)
            tape.set_right(right_tape)
            return tape
        else:
            return tape
        
    def get_cells(self):
        current = self.cell
        left = False if self._left == None else self._left.cell
        right = False if self._right == None else self._right.cell
        return tuple(left,current,right)
        
    def repr_left(self):
        if self._left == None : return "None"
        else : return f"|{self._left.repr_left()}|{self._left.cell}"

    def repr_right(self):
        if self._right == None : return "None"
        else : return f"{self._right.cell}|{self._right.repr_right()}|"
        
    def __repr__(self):
        representation = f"{self.repr_left()}| {self._cell} |{self.repr_right()}"
        return representation

    cell = property(lambda x: x._cell,set_cell)
    left = property(lambda x: x._left,set_left)
    right = property(lambda x: x._right,set_right)