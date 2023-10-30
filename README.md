# Maze Generator
This program generates random mazes using Prim's algorithm. Each time the program is run a new unique maze is generated. Then, there are 2 options to solve the maze; A recursive depth-first search algorithm, and a breadth-first search algorithm. The depth-first algorithm uses recursion to explore every path until it reaches a dead end. Once it reaches a dead end it backtracks and explores a different path. The breadth-first explores every possibility at once. The breadth-first algorithm is artificially slowed to show that it is more computationally expensive.

## Instructions to Run
1. Clone the repository with `git clone git@github.com:aidanGoesch/MazeGenerator.git`

2. Run `cd MazeGenerator` to switch into the repository directory

3. Install the external libraries with `pip install -r requirements.txt`

4. To run the script, use the command `python view.py` in the top level of the repository 
