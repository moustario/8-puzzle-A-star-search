# Puzzle

Solving 8-puzzle using A* search
by Antoine Muresan

## Run

### Depedencies

To install depedencies, execute de the following command in the directory.
> python -m pip install -r requirements.txt

### Config file
You must have a file ending in the `.start` extension. 
In it the file the starting puzzle must be specified this way.

    3 | 1 | 2
    4 | 7 | 5
    6 | 8 |  

The name of the file must be the same as the one specified inside the `game_name` variable inside the program.

### running the script
You can them run the program with the following command.

> python puzzle.py
 
### Output

You can find the solution and generated tree in the corresponding `.log` file.

For example `game.log` for a game using `game.start`


## How the script works

The `main()` function is the most important in the program.

It follows this pattern

1. Initialize the script with the given parameters
2. A while loop :
    1. Check if no fringe can be expanded
        1. End the script with no solution
    2. Choose the best fringe according to the A star strategy, in this case this is done by sorting the fringes by f score and then selecting the first one
    3. Updating the puzzle
    4. Updating the tree
    5. Updating the fringes
    6. Calling f on the fringes
    7. dumping current state of the game to the log file
    8. Checking for goal stat
        1. Find the solution
        3. Display the solution on the terminal and the log file
        2. End script 

## Result of the two prescribed runs

You can find result of both runs in the `.log` files.