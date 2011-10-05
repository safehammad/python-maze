#!/usr/bin/env python

"""
Maze generator including recursive and non-recursive variations.
"""


import numpy
from numpy.random import random_integers as rnd
import random


def maze(width, height, recurse=False):
    """Return a generator where each iteration is a full numpy
    array representing the next stage of maze layout.
    """
    # Only odd shapes
    height, width = (height // 2) * 2 + 1, (width // 2) * 2 + 1
    f = maze_non_recurse if not recurse else maze_recurse
    return f(width, height)

def maze_recurse(width, height):
    # Init maze as numpy array (all walls)
    Z = numpy.ones((height, width))

    def carve(y, x):
        Z[y, x] = 0
        yield Z
        # get randomized list of neighbours
        neighbours = [(x + 2, y), (x - 2, y), (x, y + 2), (x, y - 2)]
        random.shuffle(neighbours)
        for nx,ny in neighbours:
            if nx < 0 or ny < 0 or nx >= width or ny >= height:
                continue
            if Z[ny, nx] == 1:
                Z[(y + ny) / 2,(x + nx) / 2] = 0
                for m in carve(ny, nx):
                    yield m

    # choose random internal starting point
    x, y = rnd(0, width // 2 - 1) * 2 + 1, rnd(0, height // 2 - 1) * 2 + 1
    for m in carve(y, x):
        yield m

    # carve exits
    Z[1, 0] = Z[-2, -1] = 0
    yield Z

def maze_non_recurse(width, height):
    # Init maze as numpy array (all walls)
    Z = numpy.ones((height, width))
    stack = []
    # choose random internal starting point
    x, y = rnd(0, width // 2 - 1) * 2 + 1, rnd(0, height // 2 - 1) * 2 + 1
    # get randomized list of neighbours
    n = neighbours(x, y, width, height)
    while True:
        Z[y, x] = 0
        yield Z

        for nx, ny in n:
            if Z[ny, nx] == 1:
                Z[(y + ny) / 2, (x + nx) / 2] = 0
                stack.append((n, (x, y)))
                y, x = ny, nx
                n = neighbours(x, y, width, height)
                break
        else:
            try:
                n, (x, y) = stack.pop()
            except IndexError:
                break

    # carve exits
    Z[1, 0] = Z[-2, -1] = 0
    yield Z

def maze_coords(width, height):
    """Return a generator where each iteration is the x, y coord of
    the next wall (brick?) location.
    """
    # Init maze as numpy array (all walls)
    Z = numpy.ones((height, width))
    stack = []
    # choose random internal starting point
    x, y = rnd(0, width // 2 - 1) * 2 + 1, rnd(0, height // 2 - 1) * 2 + 1
    # get randomized list of neighbours
    n = neighbours(x, y, width, height)
    yield -1, -1
    while True:
        Z[y, x] = 0
        yield (x, y)

        for nx, ny in n:
            if Z[ny, nx] == 1:
                Z[(y + ny) / 2, (x + nx) / 2] = 0
                yield ((x + nx) / 2, (y + ny) / 2)

                stack.append((n, (x, y)))
                y, x = ny, nx
                n = neighbours(x, y, width, height)
                break
        else:
            try:
                n, (x, y) = stack.pop()
                yield (-1, -1)
            except IndexError:
                break

    # carve exits
    Z[1, 0] = Z[-2, -1] = 0

def neighbours(x, y, width, height):
    n = [(x + 2, y), (x - 2, y), (x, y + 2), (x, y - 2)]
    n = filter(lambda v: 0 <= v[0] < height and 0 <= v[1] < height, n)
    random.shuffle(n)
    return iter(n)

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    for m in maze(50, 50):
        pass
    plt.figure(figsize=(10, 5))
    plt.imshow(m, cmap=plt.cm.binary, interpolation='nearest')
    plt.xticks([]), plt.yticks([])
    plt.show()

