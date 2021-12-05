# MAI-CIR Final Project: Red Light - Green Light
Final Project for the Cognitive Interaction with Robots course (UPC) - Master in Artificial Intelligence

## How to run

## How to generate a State Machine Diagram with Mermaid

You can generate a diagram for your Finite State Machine by running the `draw_states_diagram` script located at the `doc` folder.
It will generate a markdown file containing a mermaid diagram, which you can visualize online at [Mermaid Live Editor](https://mermaid.live).

Example of program execution:

```bash
python3 doc/draw_states_diagram.py --class src.controller.curator_state_machine:CuratorStateMachine
```