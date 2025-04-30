# Meta-Simulation

## Objective

This project aims at simulating two models of calculation. It currently supports ***Turing Machines*** and unidimensionnal ***Cellular Automata***.
To do so, we used the Object Oriented capabilities of Python and implemented two custom language parsers, one for each calculation model. We then
were able to implement an algorithm to translate a turing machine into a cellular automaton.

## Getting started
- Clone the repository :
    ```BashScript
    $ git clone https://github.com/LugolBis/Meta-Simulation.git
    ```
- Run the following command (in the folder of the repository) :
    ```
    $ make
    ```
- This will create a python virtual environment, build the latex report and make a demonstration of our program.
- You will find the pdf latex document in the root of the project.
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
Cellular Automata can be expressed by the following context-free grammar :
```
<cellular-automaton> := <colors> '\n' <states> '\n' <transitions> '\n' <initialisation>
<colors>             := 'Colors:\n' <assignations>
<states>             := 'States:\n' <subclassings>
<transitions>        := 'Transitions:\n' <consequences>
<initialisation>     := 'Initialisation:\n' <words>

<assignations>       := <assignation>, <assignations> | <assignation>
<subclassings>       := <subclassing>, <subclassings> | <subclassing>
<consequences>       := <consequence>, <consequences> | <consequence>
<words>              := <identifier>, <words> | <identifier>

<assignation>        := <identifier> '<-' <tuple>
<subclassing>        := <identifier> '(' <identifier> ')
<consequence>        := <tuple> '->' <identifier>
```
<br>

All the following sections are required :
- **Colors** : Assigns an **RGB** color to a name.
- **States** : Declares states and assigns colors.
- **Transitions** : Tuples of 3 States U {Blank} linked with a target State
- **Initialisation** : Initialize the tape with states

> [!WARNING]
> Commas are required between fields but must not appear at the end of a field.

> [!NOTE]
> Indentations are ignored, feel free to format as you want.

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