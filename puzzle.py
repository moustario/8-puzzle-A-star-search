from anytree import Node, RenderTree, PreOrderIter, AsciiStyle
import copy
import time

tree = None
goal_state = [
    [' ', '1', '2'],
    ['3', '4', '5'],
    ['6', '7', '8'],
]
puzzle = [[-1, -1, -1] for i in range(3)]
game_name = "assig_h_normal"
turn = 1
void = (0, 0)  # i, j
fringe = list()
turn_separator = "-----\n"
inner_separator = "\n"
alt_heuristic = False
existing_states = list()
direction_dir = {
    (0, 1): 'right',
    (0, -1): 'left',
    (1, 0): 'down',
    (-1, 0): 'up'
}
solution = list()
state_generated = 0


def main():
    global fringe, tree, void, puzzle, turn, state_generated
    init()
    count = 0

    start = time.time()
    while(True):
        # if no fringe to expand return failure
        if(len(fringe) == 0):
            print(
                f"no solution found after {count} turns with {state_generated} states generated.")
            end_fail = time.time()
            print(f"Execution time since init : {end_fail-start} seconds.")
            with open(game_name+".log", 'a') as file:
                file.write(f'Generated {state_generated} states.')
                file.write(
                    f'Execution time since init : {end_fail-start} seconds.')
            break

        turn = turn + 1
        # Choose the best fringe according to strategy
        f()
        sorted_fringes = sorted(fringe, key=lambda item: item.f)
        if len(sorted_fringes) == 0:
            break
        else:
            choosen_fringe = sorted_fringes[0]
            choosen_fringe.expanded = True

        # update puzzle
        move_coord = tuple(int(coord)
                           for coord in choosen_fringe.name[1:-1].split(', '))
        # puzzle, void = move_void(copy.deepcopy(puzzle), void, move_coord)
        puzzle = copy.deepcopy(choosen_fringe.state)
        void = move_coord

        # update tree
        update_tree(choosen_fringe)

        # update fringe
        update_fringe()

        # f() update node data
        f()

        count += 1

        dump_state()

        if(goal_state == puzzle):
            end_success = time.time()
            print(
                f"solution found after {count} turns with {state_generated} states generated.")
            find_path(choosen_fringe)
            print(str(solution))
            print(f"Execution time since init : {end_success-start} seconds.")
            with open(game_name+".log", 'a') as file:
                file.write(str(solution))
                file.write(f'Generated {state_generated} states.')
                file.write(
                    f'Execution time since init : {end_success-start} seconds.')
            break


def find_path(node):
    global solution

    solution = find_path_rec(node)

    solution.reverse()


def find_path_rec(node):

    if node.parent == None:
        return []

    par_coord = tuple(int(coord)
                      for coord in node.parent.name[1:-1].split(', '))
    cur_coord = tuple(int(coord)
                      for coord in node.name[1:-1].split(', '))
    dir = (cur_coord[0]-par_coord[0], cur_coord[1]-par_coord[1])
    dir_str = direction_dir[dir]

    return [dir_str] + find_path_rec(node.parent)


def update_tree(choosen_fringe):
    global void, state_generated

    # going through adjacent spot
    adjacents = [(void[0]-1, void[1]), (void[0], void[1]-1),
                 (void[0]+1, void[1]), (void[0], void[1]+1)]
    # clamping values outside puzzle
    for i in range(4):
        adjacents[i] = (max(0, min(adjacents[i][0], 2)),
                        max(0, min(adjacents[i][1], 2)))
    # creating new nodes
    for coord in adjacents:
        if(coord == void):  # avoiding values that were outside the puzzle
            continue
        # TODO : check if the state doesn alreayd exists
        void_coord = tuple(int(coord)
                           for coord in choosen_fringe.name[1:-1].split(', '))
        simulated_puzzle, new_void = move_void(
            copy.deepcopy(choosen_fringe.state), void_coord, coord)
        if(simulated_puzzle in existing_states):
            continue
        node = Node(f"({coord[0]}, {coord[1]})",
                    parent=choosen_fringe, expanded=False, state=list(simulated_puzzle))
        existing_states.append(copy.deepcopy(simulated_puzzle))
        state_generated = state_generated + 1


def update_fringe():
    global fringe

    fringe = list(PreOrderIter(
        tree, filter_=lambda node: node.is_leaf and not node.expanded))


def f():
    global fringe, void, tree

    for leaf in fringe:
        leaf.g = g(leaf)
        leaf.h = h(leaf.state)
        leaf.f = leaf.h + leaf.g


def h(state):
    """Heurisitic function

    Returns:
        int: number of misplaced tiles or zero
    """
    if alt_heuristic:
        return 0
    misplaced_tiles = 0
    for i in range(3):
        for j in range(3):
            if(state[i][j] != goal_state[i][j]):
                misplaced_tiles += 1
    return misplaced_tiles


def g(node):
    return depth(node)


def depth(node):
    """Compute a node depth using recursion

    Args:
        node (Node): Starting node

    Returns:
        int: Depth of the node passed as an argument
    """
    if node.parent == None:
        return 0
    return depth(node.parent) + 1


def move_void(puzzle_to_change, void_coord, move_coord):
    global puzzle

    void_i, void_j = void_coord
    move_i, move_j = move_coord

    puzzle_to_change[void_i][void_j], puzzle_to_change[move_i][move_j] = puzzle_to_change[move_i][move_j], puzzle_to_change[void_i][void_j]
    void_coord = move_coord
    return (puzzle_to_change, void_coord)


def dump_state(erase_file=False):
    """Log current state in the log file, this include the puzzle, the tree and fringes.
    """
    global fringe, tree, puzzle, state_generated

    mode = 'w' if erase_file else 'a'
    with open(game_name+".log", mode) as file:
        for line in puzzle:
            line_to_print = ' | '.join(line) + '\n'
            file.write(line_to_print)
        file.write(inner_separator)
        str_tree = str(RenderTree(tree, style=AsciiStyle()))
        file.write(str_tree+"\n")
        file.write(inner_separator)
        file.write("fringes :\n\t" +
                   ',\n\tNode'.join(str(fringe).split(', Node')) + "\n")
        file.write(f'\nGenerated {state_generated} states so far.')
        file.write("\nEnd of turn "+str(turn)+"\n")
        file.write(turn_separator)


def init_puzzle():
    """Load the start state from file
    """
    global void, puzzle, game_name

    with open(game_name+".start") as file:

        line = file.readline().replace('\n', '')
        i = 0
        while(len(line) != 0):
            els = line.split(" | ")
            for indx, el in enumerate(els):
                puzzle[i][indx] = el
                if puzzle[i][indx] == ' ':
                    void = (i, indx)
            line = file.readline().replace('\n', '')
            i = i+1


def init_tree():
    global void, tree, puzzle, state_generated

    # creating root node
    tree = Node(f"({void[0]}, {void[1]})", expanded=True,
                state=copy.deepcopy(puzzle))
    existing_states.append(copy.deepcopy(puzzle))

    # going through adjacent spot
    adjacents = [(void[0]-1, void[1]), (void[0], void[1]-1),
                 (void[0]+1, void[1]), (void[0], void[1]+1)]
    # clamping values outside puzzle
    for i in range(4):
        adjacents[i] = (max(0, min(adjacents[i][0], 2)),
                        max(0, min(adjacents[i][1], 2)))

    for coord in adjacents:
        if(coord == void):  # avoiding values that were outside the puzzle
            continue
        void_coord = tuple(int(coord)
                           for coord in tree.name[1:-1].split(', '))
        simulated_puzzle, new_void = move_void(
            copy.deepcopy(tree.state), void_coord, coord)
        node = Node(f"({coord[0]}, {coord[1]})", parent=tree,
                    expanded=False, state=copy.deepcopy(simulated_puzzle))
        state_generated = state_generated + 1


def init_fringe():
    global fringe, tree

    fringe = list(PreOrderIter(tree, filter_=lambda node: node.is_leaf))


def init():
    init_puzzle()
    init_tree()
    init_fringe()
    dump_state(True)


if __name__ == "__main__":
    main()
