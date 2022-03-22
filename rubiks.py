# rubiks.py
# Solve a 3x3 Rubik's cube using A* search.
import argparse
from graphics import *
import pdb
from queue import PriorityQueue

parser = argparse.ArgumentParser(
    description="Solving a Rubik's Cube with A* Search")
parser.add_argument(
    '-s', '--state', help="text file containing initial state of the cube, encoded as a sequence of integers")


def main(args):
    # Initialize dictionary of parameters
    params = {
        'colors': ["#b71234",
                   "#0046ad",
                   "#ffffff",
                   "#009b48",
                   "#ffd500",
                   "#ff5800"],
        'n': 3,
        'pixels': 45,
        'thickness': 4}

    # Make list to store individual square colors
    # HINT: If the user entered an initial state via command line argument, you
    # should modify this code so that the current_state is *not* the solved
    # cube, but rather the colors of the initial state.
    # ***MODIFY CODE HERE*** (7 lines)
    state = args.state
    current_state = []

    if(state != None):  # change the state
        file = open(state)  # put text in a list
        T1 = list(file.read())

        current_state = list(map(int, T1))
        # print(current_state)
    else:
        for i in range(6):
            current_state += [i] * params['n'] ** 2
        # print(current_state)

    # ***DO NOT MODIFY THE FOLLOWING 2 LINES***
    initial_state = current_state.copy()  # for resetting the cube
    previous_state = current_state.copy()  # for undoing user actions

    # Create GUI
    gui = guisetup(params)
    recolor(gui, current_state, params)  # in case the initial state is mixed

    # Wait for user interaction
    while True:
        key = gui.checkKey()
        if key:
            # print(current_state)
            if key == "Escape":  # quit the program
                break

            elif key == 'p':  # debug the program
                pdb.set_trace()

            elif key == "Ctrl+r":
                # Reset the cube to its initial state
                print('Resetting cube to initial state')
                current_state = initial_state.copy()
                previous_state = initial_state.copy()
                recolor(gui, current_state, params)

            elif key == "Ctrl+z":
                # Undo the last user action
                print('Undoing last user action')
                current_state = previous_state.copy()
                recolor(gui, current_state, params)

            elif key.upper() in 'UDLRBF':
                # Rotate one of the cube faces clockwise
                previous_state = current_state.copy()
                face = key.upper()
                direction = 'CW'
                print("Rotating", face, "face", direction)
                txt = gui.items[-1]
                txt.setText("Rotating " + face + " face " + direction)
                rotate(current_state, face, direction)
                recolor(gui, current_state, params)

            elif key[:6] == 'Shift+' and key[6].upper() in 'UDLRBF':
                # Rotate one of the cube faces counterclockwise
                previous_state = current_state.copy()
                face = key[6].upper()
                direction = 'CCW'
                print("Rotating", face, "face", direction)
                txt = gui.items[-1]
                txt.setText("Rotating " + face + " face " + direction)
                rotate(current_state, face, direction)
                recolor(gui, current_state, params)

            elif key == 's':
                # Solve the cube using A* search
                path = astar(current_state)

            elif key == 'c':
                # Print the current heuristic cost
                print(cost('', current_state))

    gui.close()


def astar(state, verbose=False):
    '''Run A* search on the cube based on its current state.'''
    print('Running A* search...')
    # ***ENTER CODE HERE*** (20-25 lines)
    cnt = 0
    pq = PriorityQueue()
    visited = []
    costToState = {}
    startingState = state
    actions = "UDLRFB"

    # last state -> (state, move to get there like 'L)   this way when we are looping throught
    # backpointers at the end we know the move we took to get there
    backpointers = {}

    # save state, current path and total cost
    pq.put(0, state, '')
    costToState[state] = 0

    while(not pq.empty()):
        curr = pq.get()
        currState = curr[0]
        currPath = curr[1]
        currCost = costToState[curr[0]]

        if(cost(None, state) == 0):
            # goal state found
            break

        for i in actions:
            # go through each action call simulate on the current state plus that one move, then get the new state back
            # do the if else stuff and put it in pq, everytime you pop from the pq add that state
            # in the pq save state and then node(path) and maybe the length of it too
            # paths might be how many things came out of pq
            newPath = currPath + i

            result = simulate(curr[0], i)

            newCost = cost(newPath, result)

            if(result not in visited or costToState[result] > newCost):
                pq.put((newCost, result, newPath))
                backpointers[result] = currState
            elif(costToState[result] != 0 and costToState[result] > newCost):
                pq.put((newCost, result, newPath))
                backpointers[result] = currState

    # I'm thinking I will go through all possible moves and calculate the cost by calling cost() on all of them
    # then I will add all of those to the pq
    # the goal will be the solved cube so after each move the heursitic h(n) is determined so maybe the states with cost are what goes in the PQ
    # and from each state that you dequeue, you add the possible moves with cost for that state to pq

    print(f'searched {cnt} paths')
    print('solution:', '')


def cost(node, state):
    '''Compute the cost g(s)+h(s) for a given set of moves (node) leading to a cube state.

    Let g(s) be the number of moves it took to get to the state.

    Let h(s) be the average number of incorrect square colors on the cube. For h(s)=0, all colors will match the center color of that face, which never moves.
    '''

    # ***MODIFY CODE HERE*** (1 line)
    g = 0
    g = len(node)

    # ***MODIFY CODE HERE*** (7 lines)
    h = 0
    side = []
    counter = 0
    numDifferent = 0
    for i in range(len(state)):
        side.append(unsolved[i])
        counter += 1
        if(counter % 9 == 0):
            middle = side[4]
            for j in range(len(side)):
                if(side[j] != middle):
                    numDifferent += 1
            side = []
            # add the num different to something to store it before we caclculate the avg
    h = numDifferent / 6

    return g + h

# do the for each stuff in this method, feed it the list of all actions


def simulate(state, node):
    '''Simulate rotating the cube from an input state to determine resulting state. 
    Node is a sequence of rotations.'''
    s = state.copy()
    # ***ENTER CODE HERE***  (4 lines)
    for i in range(len(nodes)):
        # call the rotate method to simulate rotating each direction
        # maybe call rotate on both directions CW CCW
        rotate(state, nodes[i])
    for i in range(len(nodes)):
        pass
        # rotate(state, nodes[i], 'CCW')

    #
    return s


def drawface(gui, x0, y0, c, n, w, t):
    '''Draw an individual face of the cube. Requires GraphWin object, starting (x,y) position of the top-left corner of the face, face color, number of squares per row/column, pixel width of each square, and border thickness.'''
    for i in range(n):
        for j in range(n):
            x = x0 + j * w
            y = y0 + i * w
            square = Rectangle(Point(x, y), Point(x + w, y + w))
            square.setFill(c)
            square.setWidth(t)
            square.draw(gui)


def guisetup(params):
    '''Create graphical user interface for Rubik's Cube with n rows and columns.'''

    # Extract relevant parameters
    n = params['n']
    clr = params['colors']
    px = params['pixels']
    t = params['thickness']

    # Draw graphics window
    wid = (4 * n + 2) * px  # +2 for the margin
    hei = (3 * n + 2) * px  # +2 for the margin
    gui = GraphWin("Rubik's Cube", wid, hei)

    # Draw cube faces
    drawface(gui, (n + 1) * px, px, clr[0], n, px, t)  # upper
    drawface(gui, px, (n + 1) * px, clr[1], n, px, t)  # left
    drawface(gui, (n + 1) * px, (n + 1) * px, clr[2], n, px, t)  # front
    drawface(gui, (2 * n + 1) * px, (n + 1) * px, clr[3], n, px, t)  # right
    drawface(gui, (3 * n + 1) * px, (n + 1) * px, clr[4], n, px, t)  # back
    drawface(gui, (n + 1) * px, (2 * n + 1) * px, clr[5], n, px, t)  # down

    # Add text instructions
    txt = Text(Point(15, 20),
               "Press U/D/L/R/B/F to rotate a cube face CW (hold Shift for CCW)")
    txt._reconfig("anchor", "w")
    txt.setSize(12)
    txt.draw(gui)

    # Add text to be used to display user actions
    txt = Text(Point(15, hei - 20), "")
    txt._reconfig("anchor", "w")
    txt.setSize(12)
    txt.setFill("red")
    txt.draw(gui)

    # Return gui object and list of cube square color indices
    return gui


def rotate(state, face, direction='CW'):
    '''Rotate the cube face in a given direction.'''
    if face == 'U':
        src = [9, 10, 11, 18, 19, 20, 27, 28, 29,
               36, 37, 38, 0, 1, 2, 5, 8, 7, 6, 3]
        if direction == 'CW':
            dst = [36, 37, 38, 9, 10, 11, 18, 19, 20,
                   27, 28, 29, 2, 5, 8, 7, 6, 3, 0, 1]
        elif direction == 'CCW':
            dst = [18, 19, 20, 27, 28, 29, 36, 37,
                   38, 9, 10, 11, 6, 3, 0, 1, 2, 5, 8, 7]

    elif face == 'D':
        src = [45, 46, 47, 50, 53, 52, 51, 48, 15, 16,
               17, 24, 25, 26, 33, 34, 35, 42, 43, 44]
        if direction == 'CW':
            dst = [47, 50, 53, 52, 51, 48, 45, 46, 24, 25,
                   26, 33, 34, 35, 42, 43, 44, 15, 16, 17]
        elif direction == 'CCW':
            dst = [51, 48, 45, 46, 47, 50, 53, 52, 42, 43,
                   44, 15, 16, 17, 24, 25, 26, 33, 34, 35]

    elif face == 'L':
        src = [0, 3, 6, 18, 21, 24, 45, 48, 51, 38,
               41, 44, 9, 10, 11, 12, 14, 15, 16, 17]
        if direction == 'CW':
            dst = [18, 21, 24, 45, 48, 51, 44, 41, 38,
                   6, 3, 0, 11, 14, 17, 10, 16, 9, 12, 15]
        elif direction == 'CCW':
            dst = [44, 41, 38, 0, 3, 6, 18, 21, 24, 51,
                   48, 45, 15, 12, 9, 16, 10, 17, 14, 11]

    elif face == 'R':
        src = [2, 5, 8, 20, 23, 26, 47, 50, 53, 36,
               39, 42, 27, 28, 29, 30, 32, 33, 34, 35]
        if direction == 'CW':
            dst = [42, 39, 36, 2, 5, 8, 20, 23, 26, 53,
                   50, 47, 29, 32, 35, 28, 34, 27, 30, 33]
        elif direction == 'CCW':
            dst = [20, 23, 26, 47, 50, 53, 42, 39, 36,
                   8, 5, 2, 33, 30, 27, 34, 28, 35, 32, 29]

    elif face == 'B':
        src = [36, 37, 38, 41, 44, 43, 42, 39, 2,
               1, 0, 9, 12, 15, 51, 52, 53, 35, 32, 29]
        if direction == 'CW':
            dst = [38, 41, 44, 43, 42, 39, 36, 37, 9,
                   12, 15, 51, 52, 53, 35, 32, 29, 2, 1, 0]
        elif direction == 'CCW':
            dst = [42, 39, 36, 37, 38, 41, 44, 43, 35,
                   32, 29, 2, 1, 0, 9, 12, 15, 51, 52, 53]

    elif face == 'F':
        src = [18, 19, 20, 23, 26, 25, 24, 21, 6, 7,
               8, 27, 30, 33, 47, 46, 45, 17, 14, 11]
        if direction == 'CW':
            dst = [20, 23, 26, 25, 24, 21, 18, 19, 27,
                   30, 33, 47, 46, 45, 17, 14, 11, 6, 7, 8]
        elif direction == 'CCW':
            dst = [24, 21, 18, 19, 20, 23, 26, 25, 17,
                   14, 11, 6, 7, 8, 27, 30, 33, 47, 46, 45]

    temp = state.copy()
    for i, j in zip(src, dst):
        state[j] = temp[i]


def recolor(gui, state, params):
    '''Recolor the cube in the GUI.'''

    # Get graphics objects from GUI
    obj = gui.items
    squares = obj[:-1]

    # Extract relevant parameters
    n = params['n']
    c = params['colors']

    # Update colors
    for i in range(len(state)):
        squares[i].setFill(c[state[i]])


if __name__ == '__main__':
    main(parser.parse_args())
