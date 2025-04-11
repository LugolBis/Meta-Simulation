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
<**Initialisation state**> *REQUIRED
<br>
<**Finals state**> *REQUIRED
<br>
<**Word in input**> *REQUIRED
<br>
<**Transitions**>

> [!IMPORTANT]
> The separator choosed is a comma.<br>
> For example you coul have for <**Finals state**> :
> ```
> final_state0,final_state1,final_state2
> ```

> [!NOTE]
> You can put empty line or commented lines everywhere. To declare a comment line use : ```//```

## Requirements :
- Python >= 3.10.x