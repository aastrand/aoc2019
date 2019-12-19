#!/usr/bin/env python3

from math import floor
import copy
import intcode
import sys


PIXEL_MAP = {
    0: '.',
    1: '#'
}


def test_pos(f, x, y):
    runner = copy.deepcopy(f)
    runner.set_input_values(x, y)
    ec = runner.run(True)
    return runner.output_value()


def test_beam(f, size, print_grid=True):
    sum = 0
    for y in range(0, size):
        for x in range(0, size):
            out = test_pos(f, x, y)

            if print_grid:
                print(PIXEL_MAP[out], end='')
            sum += out

        if print_grid:
            print()

    print(sum)


def find_first_1(f, y, start=0):
    for x in range(start, y):
        out = test_pos(f, x, y)
        if out == 1:
            return x

    return None


def is_first_x(f, x, y):
    return test_pos(f, x, y) == 1 and test_pos(f, x-1, y) == 0


def is_last_x(f, x, y):
    return test_pos(f, x, y) == 1 and test_pos(f, x+1, y) == 0


def hit(f, x, n, size):
    upper_x = x+size-1
    upper_y = n-size+1
    # is there a a square that perfectly fits here?
    return is_last_x(f, upper_x, upper_y) and is_first_x(f, x, n)  and \
     test_pos(f, upper_x, upper_y-1) == 0 and test_pos(f, x+size, n) == 1 and \
     test_pos(f, x, upper_y) == 1 and test_pos(f, x, n) == 1


def main(f):
    f = intcode.create_runner(f)
    test_beam(f, 50, True)

    # guess starting pos
    y = 1000
    size = 100
    x = 0
    while True:
        x = find_first_1(f, y, x)
        if hit(f, x, y, size):
            print("hit sized square at", x, )
            print(x*10000 + (y-size+1))
            break
        y += 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
