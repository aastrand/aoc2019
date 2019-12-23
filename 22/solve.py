#!/usr/bin/env python3

import re
import sys


def deal_reference(deck):
    deck.reverse()
    return deck


def inc_reference(deck, inc):
    inc = int(inc)
    new = [-1]*len(deck)

    pos = 0
    for n in range(0, len(deck)):
        new[pos] = deck[n]
        pos += inc
        pos = pos % len(deck)

    return new


def cut_reference(deck, n):
    n = int(n)
    if n < 0:
        n = len(deck) + n

    part1 = deck[:n]
    part2 = deck[n:]
    part2.extend(part1)

    return part2


def deal(length, i):
    return length - i - 1


def inc(length, i, n):
    return int(n)*i % length


def cut(length, i, n):
    n = int(n)
    if n < 0:
        n = length + n

    return ((length - n) + i) % length


OP_REGEX = {
    '^deal with increment ([-0-9]+)$': inc,
    '^deal into new stack$': deal,
    '^cut ([-0-9]+)$': cut
}


def parse(input):
    ops = []

    for l in open(input, 'r'):
        for regex, f in OP_REGEX.items():
            match = re.match(regex, l.strip())
            if match:
                ops.append((f, match.groups()))

    return ops


def test():
    # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    assert 6  == deal(10, 3)

    # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # [0, 7, 4, 1, 8, 5, 2, 9, 6, 3]
    assert 0 == inc(10, 0, 3)
    assert 3 == inc(10, 1, 3)
    assert 6 == inc(10, 2, 3)
    assert 9 == inc(10, 3, 3)
    assert 2 == inc(10, 4, 3)

    length = 10007
    deck = [n for n in range(length)]
    offset = 32
    dealt = inc_reference(deck, offset)
    for i, val in enumerate(dealt):
        pos = inc(length, i, offset)
        assert deck[i] == dealt[pos]

    # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # [5, 6, 7, 8, 9, 0, 1, 2, 3, 4]
    assert 5 == cut(10, 0, 5)
    assert 8 == cut(10, 3, 5)
    assert 4 == cut(10, 9, 5)

    length = 10007
    deck = [n for n in range(length)]
    offset = 512
    dealt = cut_reference(deck, offset)
    for i, val in enumerate(dealt):
        pos = cut(length, i, offset)
        assert deck[i] == dealt[pos]


    # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    assert 9 == deal(10, 0)
    assert 6 == deal(10, 3)
    assert 1 == deal(10, 8)

    length = 10007
    deck = [n for n in range(length)]
    dealt = deal_reference([n for n in range(length)])
    for i, val in enumerate(dealt):
        pos = deal(length, i)
        assert deck[i] == dealt[pos]


def track(ops, length, i):
    for f, args in ops:
        i = f(length, i, *args)

    return i


def part1(input):
    ops = parse(input)
    print(track(ops, 10007, 2019))


def deal_reverse(length, _, a, b):
    return -a % length, (length - 1 - b) % length


def inc_reverse(length, i, a, b):
    return (a * i % length), (b * i % length)


def cut_reverse(length, i, a, b):
    return a, (b - i) % length


OP_REGEX_REVERSE = {
    '^deal with increment ([-0-9]+)$': inc_reverse,
    '^deal into new stack$': deal_reverse,
    '^cut ([-0-9]+)$': cut_reverse
}


def part2(input):
    pos = 2020
    length = 119315717514047
    shuffles = 101741582076661

    # "ends up in position 2020" => we need to reverse the shuffle
    # treat a shuffle as a linear function: new_pos = a*pos + b
    a, b = 1, 0
    for l in open(input, 'r'):
        for regex, f in OP_REGEX_REVERSE.items():
            match = re.match(regex, l.strip())
            if match:
                i = match.groups()[0] if match.groups() else 0
                a, b = f(length, int(i), a, b)
                break

    # now, to repeat a trillion times, we steal some math from reddit
    # https://www.reddit.com/r/adventofcode/comments/ee0rqi/2019_day_22_solutions/fbtugcu?utm_source=share&utm_medium=web2x
    r = (b * pow(1 - a, length - 2, length)) % length
    print(((pos - r) * pow(a, shuffles * (length - 2), length) + r) % length)


def main(input):
    test()

    part1(input)

    part2(input)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
