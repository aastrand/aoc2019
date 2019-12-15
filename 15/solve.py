#!/usr/bin/env python3

import copy
import intcode
import sys


MOVE_MAP = {
    1: (0, -1),# north
    2: (0, 1), # south
    3: (-1, 0),# west
    4: (1, 0)  # east
}


BACKTRACK_MAP = {
    1: 2,
    2: 1,
    3: 4,
    4: 3
}


OUTPUT_MAP = {
    0: '#',
    1: '.',
    2: 'O'
}


def print_grid(grid, pos=None, clear=False):
    x_min = x_max = y_min = y_max = 0

    for key in grid.keys():
        if x_min > key[0]:
            x_min = key[0]
        if x_max < key[0]:
            x_max = key[0]
        if y_min > key[1]:
            y_min = key[1]
        if y_max < key[1]:
            y_max = key[1]

    if clear:
        print('\033c')
    for y in range(y_min, y_max+1):
        for x in range(x_min, x_max+1):
            if (x, y) == pos:
                print('D', end='')
            else:
                print(grid.get((x, y), ' '), end='')
        print()


def move(pos, i):
    return (pos[0]+MOVE_MAP[i][0], pos[1]+MOVE_MAP[i][1])


def candidate(pos, grid):
    new_i = None
    for d in MOVE_MAP.keys():
        candidate = move(pos, d)
        if candidate not in grid:
            new_i = d
            break

    return new_i


def backtrack(runner, grid, pos, moves):
    while True:
        if not moves:
            return None

        back = moves.pop()
        i = BACKTRACK_MAP[back]
        runner.set_input_values(i)
        runner.run(True)

        pos = move(pos, i)
        new_i = candidate(pos, grid)
        if new_i is not None:
            break

    return pos


def backtrack_explore(runner, grid):
    pos = (0, 0)
    grid[pos] = '.'

    i = 3
    moves = [i]

    o_pos = None
    o_moves = []

    while True:
        runner.set_input_values(i)
        runner.run(True)
        o = runner.output_value()

        new_pos = move(pos, i)
        grid[new_pos] = OUTPUT_MAP[o]

        if o > 0:
            pos = new_pos
            moves.append(i)

        if o == 2:
            o_pos = copy.deepcopy(pos)
            o_moves = copy.deepcopy(moves[:-1])

        i = candidate(pos, grid)
        if i is None:
            pos = backtrack(runner, grid, pos, moves)
            if pos is None:
                break
            i = candidate(pos, grid)

    print_grid(grid, pos)
    print(o_pos, len(o_moves))


def empty_neighbours(pos, grid):
    return filter(lambda pos: grid.get(pos) == '.',
        [move(pos, i) for i in range(1,5)])

def spread(grid):
    minutes = 0
    spreading = True
    while spreading:
        spreading = False
        positions = []
        for pos, val in grid.items():
            if val == 'O':
                for pos in empty_neighbours(pos, grid):
                    positions.append(pos)

        for pos in positions:
            grid[pos] = 'O'
            spreading = True

        if spreading:
            minutes += 1

    print_grid(grid)
    print(minutes)


def main(f):
    runner = intcode.create_runner(f)
    grid = {}

    backtrack_explore(runner, grid)
    spread(grid)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
