#!/usr/bin/env python3

import sys


def main(input):
    lines = []
    for l in open(input, 'r'):
        lines.append(l.strip().split(','))

    grid = {}
    min_distance = -1
    min_steps = -1

    for i, line in enumerate(lines):
        cur_x = 0
        cur_y = 0
        cur_steps = 0
        for move in line:
            direction = move[0]
            length = int(move[1:])
            coords = generate_coords(cur_x, cur_y, direction, length)

            for coord in coords:
                # Never check origo
                if coord == (0, 0):
                    continue

                cur_steps += 1

                grid_value = grid.get(coord)
                # Record traces
                if grid_value is None:
                    grid[coord] = (i, cur_steps)
                elif grid_value[0] != i and grid_value[0] != 'X':
                    # Found a real intersection
                    grid[coord] = ('X', cur_steps + grid_value[1])

                    # Calculate distance and steps
                    new_distance = distance(coord)
                    if min_distance == -1 or new_distance < min_distance:
                        min_distance = new_distance

                    if min_steps == -1 or grid[coord][1] < min_steps:
                        min_steps = grid[coord][1]

            cur_x = coords[-1][0]
            cur_y = coords[-1][1]

    print(min_distance)
    print(min_steps)


def distance(coord):
    return abs(coord[0]) + abs(coord[1])


def generate_coords(cur_x, cur_y, direction, length):
    if direction == 'R':
        l = [(x, cur_y) for x in range(cur_x+1, cur_x+length+1)]
    elif direction == 'L':
        l = [(x, cur_y) for x in range(cur_x-length, cur_x)]
        l.reverse()
    elif direction == 'D':
        l = [(cur_x, y) for y in range(cur_y-length, cur_y)]
        l.reverse()
    elif direction == 'U':
        l = [(cur_x, y) for y in range(cur_y+1, cur_y+length+1)]

    return l


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
