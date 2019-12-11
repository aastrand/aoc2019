#!/usr/bin/env python3

import sys
import intcode


MOVEMENT_OFFSETS = {
    0: (0, -1), # up
    1: (1, 0),  # right
    2: (0, 1),  # down
    3: (-1, 0)  # left
}


def rotate(orientation, direction):
    orientation += 1 if direction == 1 else -1
    return orientation % 4


def move(pos, direction):
    offset = MOVEMENT_OFFSETS[direction]
    return (pos[0] + offset[0], pos[1] + offset[1])


def paint(runner):
    grid = {}
    pos = (0, 0)
    # 0 = up, 1 = right, 2 = down, 3 = left
    orientation = 0

    while True:
        ec = runner.run(True)

        # 0 means to paint the panel black, and 1 means to paint the panel white.
        color = runner.output_value()
        grid[pos] = color

        ec = runner.run(True)
        if ec == 99:
            break

        # 0 means it should turn left 90 degrees, and 1 means it should turn right 90 degrees.
        direction = runner.output_value()
        orientation = rotate(orientation, direction)

        # move
        pos = move(pos, orientation)

        # read new color
        runner.set_input_values(grid.get(pos, 0))

    return grid


def print_grid(grid):
    color_map = {
        0:  u'\u2591',
        1:  u'\u2593'
    }

    max_x = max_y = min_x = min_y = 0
    for key in grid.keys():
        if key[0] > max_x:
            max_x = key[0]
        if key[0] < min_x:
            min_x = key[0]
        if key[1] > max_y:
            max_y = key[1]
        if key[1] < min_y:
            min_y = key[1]

    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            print(color_map[grid.get((x, y), 0)], end='')
        print()


def test():
    assert 1 == rotate(0, 1)
    assert 2 == rotate(1, 1)
    assert 3 == rotate(2, 1)
    assert 0 == rotate(3, 1)

    assert 3 == rotate(0, 0)
    assert 0 == rotate(1, 0)
    assert 1 == rotate(2, 0)
    assert 2 == rotate(3, 0)

    assert (0, -1) == move((0, 0), 0)
    assert (1, 0) == move((0, 0), 1)
    assert (0, 1) == move((0, 0), 2)
    assert (-1, 0) == move((0, 0), 3)


def main(input):
    test()

    runner = intcode.create_runner(input, 0)
    grid = paint(runner)
    print(len(grid.keys()))

    runner = intcode.create_runner(input, 1)
    grid = paint(runner)
    print_grid(grid)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
