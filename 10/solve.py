#!/usr/bin/env python3

import numpy
import sys

from collections import defaultdict
from math import atan2, pi


def interpolate(a, b):
    if a == b:
        return [], []

    x = [a[0], b[0]]
    y = [a[1], b[1]]

    return interpolate_inner(x,y), interpolate_inner(y, x)


def interpolate_inner(x, y):
    flipped_x = False
    if x[0] > x[1]:
        x  = [x[1], x[0]]
        flipped_x = True

    if (y[1] - y[0]) == 0:
        x_step = 1
    else:
        x_step = min(1.0, abs((x[1]-x[0]) / (y[1] - y[0])))

    if x_step == 0:
        x_pts = [x[0]] * int(abs(y[1] - y[0]) - 1)
    else:
        x_pts = [float("{0:5f}".format(d)) for d in numpy.arange(x[0]+x_step, x[1], x_step)]
        if x[-1] == x_pts[-1]:
            x_pts = x_pts[:-1]

    if flipped_x:
        x_pts.reverse()

    return x_pts


def is_adjecent(a, b):
    return abs(int(a[0]-b[0])) <= 1 and abs(int(a[1]-b[1])) <= 1


def construct_line_of_sight_map(grid, x_dim, y_dim):
    los_map = defaultdict(set)
    hit_map = {}
    asteroids = []
    for key, value in grid.items():
        if value == '#':
            asteroids.append(key)

    #print("asteroids(%s) = %s" % (len(asteroids), asteroids))

    for a in asteroids:
        for b in asteroids:
            #print("testing %s -> %s" % (a,b))
            if (a == b):
                #print("same, skipping")
                continue

            # memoized
            if hit_map.get((a, b)) is not None:
                #print("already found, skipping")
                continue

            if is_adjecent(a, b):
                #print("%s -> %s: adjecent, adding" % (a, b))
                hit_map[(a, b)] = b
                hit_map[(b, a)] = a
                continue

            x_pts, y_pts = interpolate(a, b)
            for step in range(0, len(x_pts)):
                pos = (x_pts[step], y_pts[step])
                if grid.get(pos) == '#':
                    #print("%s -> %s: hit in %s, adding" % (a, b, pos))
                    hit_map[(a, b)] = pos
                    break
            else:
                #print("nothing between %s and %s, adding" % (a, b))
                hit_map[(a, b)] = b
                hit_map[(b, a)] = a

    for key, value in hit_map.items():
        if key[0] != value:
            los_map[key[0]].add(value)

    return los_map


def find_asteroid_with_most_los(los_map, x_dim, y_dim):
    most_asteroids = -1
    pos = None

    for key, value in los_map.items():
        if len(value) > most_asteroids:
            most_asteroids = len(value)
            pos = key
    for x in range(0, x_dim):
        for y in range(0, y_dim):
            val = los_map.get((x, y), [])
            print("(%s)" % len(val) if len(val) > 0 else '.', end='')
        print()

    return pos, most_asteroids


def angle(a, b):
    return (atan2(b[1] - a[1], b[0] - a[0]) * 180 / pi + 90) % 360


def construct_ordered_angle_pos_list(station_pos, los_set):
    l = []
    for pos in los_set:
        l.append((angle(station_pos, pos), pos))

    l.sort(key=lambda p: p[0])
    return l


def print_grid(grid, x_dim, y_dim, highlights=set()):
    for y in range(0, y_dim):
        for x in range(0, x_dim):
            val = grid[(float(x),float(y))] if (x, y) not in highlights else 'X'
            print(val, end='')
        print()


def test():
    # .#..#
    # .....
    # .....
    assert ([2.0, 3.0], [0.0, 0.0]) == interpolate((1.0, 0.0), (4.0, 0.0))

    # ....#
    # .....
    # .....grid[(float(x),float(y))
    # ....#
    assert ([4.0, 4.0], [1.0, 2.0]) == interpolate((4.0, 0.0), (4.0, 3.0))

    # .#...
    # .....
    # #....
    assert ([0.5], [1.0]) == interpolate((1.0, 0.0), (0.0, 2.0))

    # .....
    # .....
    # ..#..
    # .....
    # ...#.
    assert ([2.5], [3.0]) == interpolate((2.0, 2.0), (3.0, 4.0))

    # .....
    # .....
    # #....
    # .....
    # ...#.
    assert ([1.0, 2.0], [2.666667, 3.333333]) == interpolate((0.0, 2.0), (3.0, 4.0))

    # ....#
    # .....(7.0, 6.0), (4.0, 4.0)
    # #....
    # .....
    # .....
    assert ([1.0, 2.0, 3.0], [1.5, 1.0, 0.5]) == interpolate((0.0, 2.0), (4.0, 0.0))

    # ....#
    # .....
    # .....
    # .....
    # .#...
    assert ([1.75, 2.5, 3.25], [3.0, 2.0, 1.0]) == interpolate((1.0, 4.0), (4.0, 0.0))

    assert(180.0 == angle((0.0, 0.0), (0.0, 1.0))) # down
    assert(90.0 == angle((0.0, 0.0), (1.0, 0.0))) # right
    assert(270.0 == angle((1.0, 0.0), (0.0, 0.0))) # left
    assert(0.0 == angle((0.0, 1.0), (0.0, 0.0))) # up


def main(input):
    grid, x_dim, y_dim = parse(input)

    print_grid(grid, x_dim, y_dim)
    test()

    los_map = construct_line_of_sight_map(grid, x_dim, y_dim)
    station_pos, amount = find_asteroid_with_most_los(los_map, x_dim, y_dim)
    print(station_pos, amount)

    # find all in los_map
    # order by angle
    # remove and count
    # goto #1 with new los_map and count
    # done when los_map empty
    count = 0
    rotating = True
    betted_pos = (-1, -1)
    while rotating:
        ordered_angle_pos_list = construct_ordered_angle_pos_list(station_pos, los_map[(station_pos)])
        for _, pos in ordered_angle_pos_list:
            count += 1
            #print("zapping %s as #%s" % (pos, count))
            if count == 200:
                betted_pos = pos
            grid[pos] = '.'
        los_map = construct_line_of_sight_map(grid, x_dim, y_dim)
        if not los_map:
            rotating = False

    print(int(betted_pos[0] * 100 + betted_pos[1]))


def parse(input):
    grid = {}
    y = 0

    for l in open(input, 'r'):
        x = 0
        for a in l.strip():
            grid[(float(x), float(y))] = a
            x += 1
        x_dim = x
        y += 1
    y_dim = y

    return grid, x_dim, y_dim


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
