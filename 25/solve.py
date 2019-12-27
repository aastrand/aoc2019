#!/usr/bin/env python3

import intcode
import re
import sys

from itertools import combinations


SHORTCUTS = {
    'n': 'north',
    's': 'south',
    'e': 'east',
    'w': 'west',
    'g': 'gather',
    'b': 'bruteforce',
    'wsc': 'warp Security Checkpoint'
}


OPPOSITES = {
    'north': 'south',
    'south': 'north',
    'west': 'east',
    'east': 'west'
}


def ascii(str):
    return [ord(d) for d in str]


ROOM_REGEX = r'.*== ([a-zA-Z ]+) ==\n.*'
DOORS_REGEX = r".*Doors here lead:\n(([-a-z ]+\n)+)+.*"
ITEMS_REGEX = r".*Items here:\n(([-a-z ]+\n)+)+.*"
INV_REGEX = r".*Items in your inventory:\n(([-a-z ]+\n)+)+.*"


def read(runner):
    line = []
    while True:
        ec = runner.run(True)
        if ec == 99:
            break

        val = runner.output_value()
        line.append(chr(val))
        if chr(val) == '?':
            break

    return ''.join(line), ec


def gather(runner, doors, items, room, banned_items):
    visited = set()
    q = []
    moves = []
    while True:
        for item in items:
            if item not in banned_items:
                runner.set_input_values(*ascii('take ' + item + '\n'))
                runner, doors, items, inv, room = run(runner, doors, items)

        found_new = False
        for door in doors:
            new_node = (door, room)
            if new_node not in visited:
                q.append(new_node)
                found_new = True

        if not found_new:
            if len(moves) == 0:
                break
            move = OPPOSITES[moves.pop()]
        else:
            node = q.pop()
            move = node[0]
            moves.append(move)

        visited.add((move, room))

        runner.set_input_values(*ascii(move + '\n'))
        runner, doors, items, inv, room = run(runner, doors, items)

    return runner, doors, items, room


def warp(runner, doors, room, destination):
    visited = set()
    q = []
    moves = []
    while True:
        if room == destination:
            break

        found_new = False
        for door in doors:
            new_node = (door, room)
            if new_node not in visited:
                q.append(new_node)
                found_new = True

        if not found_new:
            if len(moves) == 0:
                break
            move = OPPOSITES[moves.pop()]
        else:
            node = q.pop()
            move = node[0]
            moves.append(move)

        visited.add((move, room))

        runner.set_input_values(*ascii(move + '\n'))
        runner, doors, items, inv, room = run(runner, doors, [])

    return runner, doors, items, room


def bruteforce(runner, doors, room, direction):
    runner.set_input_values(*ascii('inv\n'))
    runner, doors, items, inv, _ = run(runner, doors, [])

    for item in inv:
        runner.set_input_values(*ascii('drop ' + item + '\n'))
        runner, doors, items, _, _ = run(runner, doors, [])

    for n in range(1, len(inv) - 1):
        for combo in combinations(inv, n):
            print(combo)
            for item in combo:
                runner.set_input_values(*ascii('take ' + item + '\n'))
                runner, _, _, _, _ = run(runner, [], [])

            runner.set_input_values(*ascii(direction + '\n'))
            runner, doors, items, _, new_room = run(runner, doors, [])

            if new_room != room:
                return runner, doors, items, new_room

            for item in combo:
                runner.set_input_values(*ascii('drop ' + item + '\n'))
                runner, _, _, _, _ = run(runner, [], [])

    return runner, doors, items, room


def try_parse_list(regex, output):
    matches = re.finditer(regex, output, re.MULTILINE)
    l = []
    for m in matches:
        l = [d[2:].strip() for d in m.group(1).split('\n')][:-1]
    return l


def run(runner, doors, items):
    output, ec = read(runner)

    print(output)

    if ec == 99:
        sys.exit(0)

    new_doors = try_parse_list(DOORS_REGEX, output)
    if new_doors:
        doors = new_doors

    items = try_parse_list(ITEMS_REGEX, output)
    inv = try_parse_list(INV_REGEX, output)

    matches = re.finditer(ROOM_REGEX, output, re.MULTILINE)
    room = '?'
    for m in matches:
        room = m.group(1)

    return runner, doors, items, inv, room


def part_one(f):
    runner = intcode.create_runner(f)

    doors = []
    items = []
    moves = []

    banned_items = set(['molten lava', 'infinite loop', 'photons', 'giant electromagnet', 'escape pod'])

    runner, doors, items, inv, room = run(runner, doors, items)
    while True:
        print('room', room)
        print('moves', moves)
        print("$ ", end='')

        str = input()
        str = str.strip()
        str = SHORTCUTS.get(str, str)

        if str == 'gather':
            runner, doors, items, room = gather(runner, doors, items, room, banned_items)
            continue

        if str == 'bruteforce':
            runner, doors, items, room = bruteforce(runner, doors, room, 'south')
            continue

        if str.startswith('warp'):
            destination = str[5:]
            runner, doors, items, room = warp(runner, doors, room, destination)
            continue

        if str in doors and "ejected" not in str:
            if len(moves) > 0 and moves[-1] == OPPOSITES[str]:
                moves.pop()
            else:
                moves.append(str)

        runner.set_input_values(*ascii(str+'\n'))
        runner, doors, items, inv, room = run(runner, doors, items)

    print()


def main(f):
    part_one(f)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
