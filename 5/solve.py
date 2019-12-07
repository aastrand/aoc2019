#!/usr/bin/env python3

import sys
import intcode


def main(input, value):
    runner = intcode.   create_runner(input, int(value))
    runner.run()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))
