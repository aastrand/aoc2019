#!/usr/bin/env python3

import sys
from collections import defaultdict


def handle_image(input_file, width=25, height=6):
    size = width * height
    count = 0
    min_zeros = None
    product = None
    counts = defaultdict(int)
    render = [2] * width * height

    for l in open(input_file, 'r'):
        for digit in l.strip():
            digit = int(digit)

            c = counts[digit]
            counts[digit] = c + 1

            r = render[count]
            if r == 2:
                render[count] = digit

            count += 1

            if count == size:
                if min_zeros is None or counts[0] < min_zeros:
                    min_zeros = counts[0]
                    product = counts[1] * counts[2]

            if count == size:
                count = 0
                counts.clear()


    print(product)
    print_render(render, width, height)


def print_render(render, width, height):
    count = 0
    for n in range(0, width*height):
        print(render[n], end='')
        count += 1
        if (count == width):
            count = 0
            print()
    print()


def test():
    handle_image('small.txt', 2, 2)


def main(input_file):
    test()

    handle_image(input_file)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
