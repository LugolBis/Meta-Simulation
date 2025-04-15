# Meta-Simulation

## Objective
This project brings the objective of simulate two specific model of calculation, who are the ***Turing Machine*** and the ***Cellular Automaton***.
The first step was to create classes to modelize these model of calculation and simulate them. The second step was to create a simple algorithm to translate a ***Turing Machine*** into a ***Cellular Automaton*** to perform the same calculs.

## Guetting started
- Clone the repository :
    ```BashScript
    $ git clone 
    ```
- Run the following command (in the folder of the repository) :
    ```
    $ make
    ```
- To create your own ***Turing Machine***/***Cellular Automaton*** scripts check the [Script Format ]() section.

## Script Format
### Turing Machine :
The script format is the following :
<br>

Only the first 3 sections are required :
- **Init state** : The init state.
- **Finals States** : The finals states.
- **The Tape** : The word in input (each letter/symbol need to be separated by a comma)
- **Transitions** : The transitions of the TM (see below for an example).

> [!IMPORTANT]
> The separator choosed is a comma.

> [!NOTE]
> You can put empty line or commented lines everywhere. To declare a comment line use : ```//```.

```
// Init State :
q0
// Finals States :
accept,q3
// Input (here on the alphabet {0,1}*) :
1,1,0,0,1

// Transitions :
q0,0,q1,0,>
q0,1,q2,1,>
q0,_,reject,_,-
q1,0,q3,0,-
q2,1,q2,1,>
q2,0,q3,0,-
```

### Cellular Automaton :
The script format is the following :
<br>

All the following sections are required :
- **Colors** : Identified by name and a tuple of *RGB*
- **States** : Identified by name and linked with a color name
- **Transitions** : Tuples of 3 States U {Blank} linked with another State
- **Initialisation** : Initialize the tape with states

> [!WARNING]
> Commas are very important ! Paid attention to this.

> [!NOTE]
> You can put empty line or commented lines everywhere. To declare a comment line use : ```//```

```
Colors:
    ExempleColor <- (0, 0, 0)

States:
    FirstState (ExempleColor),
    SecondState (ExempleColor)
    
Transitions:
    (Blank, FirstState, SecondState) -> SecondState
    
Initialisation:
    FirstState, SecondState
```

## Requirements :
- Python >= 3.10.x