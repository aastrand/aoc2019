#!/usr/bin/env python3

import sys
import intcode
import time


def create_game_grid(runner):
    grid = {}

    while True:
        runner.run(True)
        x = runner.output_value()
        runner.run(True)
        y = runner.output_value()
        e = runner.run(True)
        t = runner.output_value()

        grid[(x, y)] = t

        if e == 99:
            break


    return grid


TILE_MAP = {
    0: ' ',
    1: u'\u2593',
    2: u'\u2591',
    3: '-',
    4: 'O'
}


def grid_dimensions(grid):
    x_max = max([v[0] for v in grid.keys()])
    y_max = max([v[1] for v in grid.keys()])
    return x_max, y_max


def print_grid(grid, x_max, y_max):
    print('\033c')
    for y in range(0, y_max+1):
        for x in range(0, x_max+1):
            print(TILE_MAP.get(grid[(x, y)], 0), end='')
        print()


def run_game(runner, grid, x_max, y_max):
    score = 0
    # Memory address 0 represents the number of quarters that have been inserted; set it to 2 to play for free.
    runner._program[0] = 2

    # If the joystick is in the neutral position, provide 0.
    # If the joystick is tilted to the left, provide -1.
    # If the joystick is tilted to the right, provide 1.
    runner.set_input_values(0)

    ball_pos = None
    paddle_pos = None

    while True:
        runner.run(True)
        x = runner.output_value()
        runner.run(True)
        y = runner.output_value()
        e = runner.run(True)
        t = runner.output_value()

        if (x, y) == (-1, 0):
            score = t
        else:
            grid[(x, y)] = t

        if t == 3:
            ball_pos = (x, y)
        elif t == 4:
            paddle_pos = (x, y)
            print_grid(grid, x_max, y_max)
            print(score)
            time.sleep(0.1)

        if paddle_pos is not None and ball_pos is not None:
            diff = paddle_pos[0] - ball_pos[0]
            runner.set_input_values((diff > 0) - (diff < 0))

        if e == 99:
            break

    print_grid(grid, x_max, y_max)

    return score


def main(input):
    runner = intcode.create_runner(input)
    grid = create_game_grid(runner)
    x_max, y_max = grid_dimensions(grid)
    print_grid(grid, x_max, y_max)

    block_tile_count = 0
    for k in grid.values():
        if k == 2:
            block_tile_count += 1
    print(block_tile_count)

    runner = intcode.create_runner(input)
    score = run_game(runner, grid, x_max, y_max)
    print(score)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
