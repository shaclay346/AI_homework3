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
    else:
        for i in range(6):
            current_state += [i] * params['n'] ** 2

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
    # initialize all the data structures we will need
    cnt = 0
    solution = ""
    pq = PriorityQueue()
    visited = []
    costToState = {
    }
    backpointers = {}
    flag = True

    # condition to check if cube is already solved
    if(cost('', state) == 0):
        solution = ""
        print("got here")
        flag = False

    # save state, current path and total cost
    pq.put((0, state, ""))
    costToState[""] = 0
    # create string of all possible actions, lower case are CW
    # upper case are CCW
    actions = "udlrbfUDLRFB"

    while(not pq.empty() or flag == False):
        # while qlueue is not empty get from the front of the queue
        curr = pq.get()
        cnt += 1

        # using temp varaibles to make it easier to access data from tuple
        currCost = curr[0]
        currState = curr[1]
        currPath = curr[2]

        # if we find a goal return the path
        if((cost('', currState) == 0) and currPath != ""):
            # goal state found
            print("GOAL found")
            solution = currPath
            break

        for i in actions:
            # go through each action call simulate on the current state plus that one move, then get the new state back
            # do the if else stuff and put it in pq, everytime you pop from the pq add that state
            # in the pq save state and then node(path) and maybe the length of it too
            # paths might be how many things came out of pq
            newPath = currPath + i

            result = simulate(currState, i)

            newCost = cost(newPath, result)
            #newCost = betterCost(newPath, result)

            if(newPath not in visited):
                pq.put((newCost, result, newPath))
                backpointers[newPath] = currPath
                visited.append(newPath)
                costToState[newPath] = newCost
            elif(newPath in costToState.keys()):
                if(costToState[newPath] > newCost):
                    pq.put((newCost, result, newPath))
                    backpointers[newPath] = currPath
                    costToState[newPath] = newCost

    print(f'searched {cnt} paths')
    print('solution:', solution)


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
    # loop through current state of cube
    for i in range(len(state)):
        # add all squares from this side to a list
        side.append(state[i])
        counter += 1
        # once we have looped 9 times we have gone over the whole side
        if(counter % 9 == 0):
            # get the middle color for this side
            middle = side[4]
            # count how many cubes are a different color on this side
            for j in range(len(side)):
                if(side[j] != middle):
                    numDifferent += 1
            side = []
    # divide total number incorrect by 6
    h = numDifferent / 6

    return g + h


def betterCost(node, state):
    # this was a heuristic I thought would be better
    # which was just counting totla number of incorrect #squares
    # it didn't work super well, and the better heuristic in our pdf
    # would take too long to implement. I tried :/
    side = []
    counter = 0
    numDifferent = 0
    for i in range(len(state)):
        side.append(state[i])
        counter += 1
        if(counter % 9 == 0):
            middle = side[4]
            for j in range(len(side)):
                if(side[j] != middle):
                    numDifferent += 1
            side = []

    print(numDifferent + len(node))
    return numDifferent + len(node)


def simulate(state, node):
    '''Simulate rotating the cube from an input state to determine resulting state. 
    Node is a sequence of rotations.'''
    s = state.copy()
    # ***ENTER CODE HERE***  (4 lines)

    # loop through node
    for i in range(len(node)):
        # if its lower case call rotate with CW movement
        if(node[i].islower()):
            rotate(s, node
                   [i].upper())
        # if its upper case call rotate with counter clockwise movement
        else:
            rotate(s, node[i], 'CCW')

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
