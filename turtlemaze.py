#!/usr/bin/env python
"""
Visualise maze generation using turtle graphics backend.
"""

from turtle import *

from maze import maze_coords


def setup():
    delay(10)
    screen = getscreen()
    screen.bgcolor('black')
    color('green')
    width(3)

def square(width, height, scale):
    penup()
    goto(0, 0)
    pendown()
    goto(width * scale, 0)
    goto(width * scale, height * scale)
    goto(0, height * scale)
    goto(0, 0)

def main(width, height, scale=5):
    setup()
    square(width, height, scale)
    for x, y in maze_coords(width, height):
        if x == -1 and y == -1:
            penup()
        else:
            goto(x * scale, y * scale)
            pendown()
    raw_input()


if __name__ == '__main__':
    main(width=50, height=50)
