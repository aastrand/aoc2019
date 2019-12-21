#!/usr/bin/env python3

import intcode
import sys


def ascii(str):
    return [ord(d) for d in str]


def run_springscript(f, code):
    runner = intcode.create_runner(f)
    runner.set_input_values(*ascii(code))

    while True:
        ec = runner.run(True)
        if ec == 99:
            break

        val = runner.output_value()
        if val < 128:
            print(chr(val), end='')
        else:
            print(val)

    print()


def part_one(f):
    code = """NOT A J
NOT C T
AND D T
OR T J
WALK
"""
    run_springscript(f, code)


def part_two(f):
    runner = intcode.create_runner(f)
    code = """NOT A J
NOT C T
AND D T
AND H T
OR T J
NOT B T
AND D T
OR T J
RUN
"""
    run_springscript(f, code)


def main(f):
    part_one(f)
    part_two(f)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
