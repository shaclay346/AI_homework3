# pancakes.py
# Flipping pancakes with greedy best-first search (GBFS).

import argparse
from graphics import *
from matplotlib import cm
import pdb
from queue import PriorityQueue
import random

parser = argparse.ArgumentParser(description="Use greedy best-first search (GBFS) to optimally flip a stack of pancakes")
parser.add_argument('-n', '--num', metavar='pancakes', type=int, help="number of pancakes", default=4)
parser.add_argument('--seed', type=int, help="seed for randomly arranging pancakes initially")


def main(args):
    # Parse inputs
    n = args.num  # number of pancakes
    stack = list(range(n))
    if args.seed is not None:  # randomly shuffle the pancakes initially
        random.shuffle(stack)

    # Make the graphical user interface
    gui = guisetup(stack)

    # Use the graphical user interface
    while True:
        key = gui.checkKey()
        if key:
            if key == "Escape":  # quit the program
                break
            elif key == 'p':  # debug the program
                pdb.set_trace()
            elif key == 's':  # run the search algorithm
                gui.items[-1].setText("Running GBFS...")
                path = gbfs(stack)
            elif key in [str(i) for i in range(1, n + 1)]:  # manually flip some of the pancakes
                flip(gui, stack, int(key))

    gui.close()


def cost(stack):
    '''Compute the cost h(s) for a given stack of pancakes.
    Here, we define cost as the number of pancakes in the wrong position.'''
    # ***MODIFY CODE HERE*** (2 lines)
    h = 0

    return h


def gbfs(stack):
    '''Run greedy best-first search on a stack of pancakes.'''
    print("Running greedy best-first search...")
    # ***MODIFY CODE HERE*** (20-25 lines)
    cnt = 0

    print(f'searched {cnt} paths')
    print('solution:', '')


def guisetup(stack):
    '''Create graphical user interface for a stack of n pancakes.'''
    n = len(stack)  # number of pancakes in the stack
    thickness = 12  # thickness of each pancake, in pixels
    margin = 40
    wid = margin * 2 + 30 * (n + 1)  # each successive pancake gets 30 px wider
    hei = margin * 2 + n * thickness  # top/bottom margins of 40 px + 12 px per pancake
    gui = GraphWin("Pancakes", wid, hei)

    cx = wid / 2  # center of width
    cmap = cm.get_cmap('YlOrBr', n + 1)

    # Draw pancakes
    # ***ENTER CODE HERE*** (10 lines)

    # Add text instructions
    txt = Text(Point(cx, 25), "Press a # to flip pancakes")
    txt._reconfig("anchor", "center")
    txt.setSize(12)
    txt.draw(gui)

    # Return gui object
    return gui


def flip(gui, stack, p):
    '''Flip p pancakes in an ordered stack.'''
    # print("Flipping", p, "pancakes" if p > 1 else "pancake")

    # Get graphics objects from GUI
    obj = gui.items
    pancakes = obj[:-1]
    txt = obj[-1]

    # Update text on GUI
    txt.setText("Flipping " + str(p) + " " +
                ("pancakes" if p > 1 else "pancake"))

    # Move pancakes around in the GUI
    # ***ENTER CODE HERE*** (4 lines)
    # thickness = pancakes[0].config['width']  # may be a helpful variable :)

    # Update the stack (which is separate from the graphics objects)
    # ***ENTER CODE HERE*** (2 lines)

    return stack


def simulate(stack, path):
    '''Simulate the flipping of pancakes to determine the resulting stack.'''
    fakestack = stack.copy()  # make a copy so we don't actually change the real stack
    for action in path:
        try:
            p = int(action)  # how many pancakes are we trying to flip?
            for i in range(1, p // 2 + 1):
                fakestack[-i], fakestack[- (p - i + 1)] = fakestack[-(p - i + 1)], fakestack[-i]
        except:
            print("INVALID ACTION: Check code")

    return fakestack


if __name__ == "__main__":
    main(parser.parse_args())
