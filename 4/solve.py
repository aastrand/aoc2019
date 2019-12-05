#!/usr/bin/env python3

import sys


def test():
    # Part one
    #assert meets_critera(111111)
    assert not meets_critera(223450)
    assert not meets_critera(123789)

    # Part two
    assert meets_critera(112233)
    assert not meets_critera(123444)
    assert meets_critera(111122)


def main():
    test()

    num = 0
    for n in range(109165, 576723+1):
        if meets_critera(n):
            num += 1

    print(num)


def meets_critera(n):
    str = "%d" % n

    if len(str) != 6:
        return False

    digit_map = {}
    last_digit = -1

    for digit in str:
        id = int(digit)
        if id < last_digit:
            return False
        if last_digit == id:
            count = digit_map.get(id, 1)
            digit_map[id] = count + 1
        last_digit = id

    for value in digit_map.values():
        if value == 2:
            return True

    return False


if __name__ == '__main__':
    sys.exit(main())
