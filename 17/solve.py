#!/usr/bin/env python3

import itertools
import sys
import intcode


NEIGHBOUR_OFFSETS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


TURN_MAP = {
    ('^', (1, 0)): ('R', '>'),
    ('^', (-1, 0)): ('L', '<'),
    ('>', (0, 1)): ('R', 'v'),
    ('>', (0, -1)): ('L', '^'),
    ('v', (1, 0)): ('L', '>'),
    ('v', (-1, 0)): ('R', '<'),
    ('<', (0, 1)): ('L', 'v'),
    ('<', (0, -1)): ('R' '^')
}


ROBOT_VALUES = set(['^', 'v', '<', '>'])


def get_grid(runner):
    x = y = x_max =0
    grid = {}
    while True:
        ec = runner.run(True)
        if ec == 99:
            break

        out = runner.output_value()
        print(chr(out), end='')

        if out == 10:
            x = 0
            y += 1
        else:
            grid[(x, y)] = out
            x += 1

    return grid


def offset_pos(pos, offset):
    return (pos[0]+offset[0], pos[1]+offset[1])


def is_intersection(pos, grid):
    return [35, 35, 35, 35] == [grid.get(offset_pos(pos, offset)) for offset in NEIGHBOUR_OFFSETS]


def get_intersections(grid, x_max=51, y_max=41):
    intersections = []
    for y in range(0, y_max):
        for x in range(0, x_max):
            pos = (x, y)
            value = grid[pos]

            if value == 35 and is_intersection(pos, grid):
                intersections.append(pos)
                print('O', end='')
            else:
                print(chr(value), end='')

        print()

    return intersections


def find_way_to_turn(grid, pos):
    turn = None
    for offset in NEIGHBOUR_OFFSETS:
        candidate = offset_pos(pos, offset)
        if grid.get(candidate) == 35:
            turn = TURN_MAP.get((chr(grid[pos]), offset))
            if turn:
                break

    return turn


def find_turn_offset(grid, pos, value):
    for offset in NEIGHBOUR_OFFSETS:
        if (TURN_MAP.get((value, offset)) is not None) and \
            grid.get(offset_pos(pos, offset)) == 35:
            return offset

    return None


def walk_straight(grid, pos):
    offset = find_turn_offset(grid, pos, chr(grid[pos]))
    while True:
        lookahead = offset_pos(pos, offset)
        if grid.get(lookahead) != 35:
            return pos
        else:
            pos = lookahead

    return None


def get_path(grid):
    path = []
    for pos, value in grid.items():
        if chr(value) in ROBOT_VALUES:
            start_pos = pos
            break

    while True:
        turn = find_way_to_turn(grid, start_pos)
        if not turn:
            break

        path.append(turn[0])
        path.append(turn[0])

        new_pos = walk_straight(grid, start_pos)
        x_diff = start_pos[0] - new_pos[0]
        y_diff = start_pos[1] - new_pos[1]

        length = max(abs(x_diff), abs(y_diff))

        if length > 9:
            val = str(length)
        else:
            val = '0%s' % str(length)

        path.append(val)
        start_pos = new_pos
        grid[start_pos] = ord(turn[1])

    return ''.join(path)


def find_parts(path):
    # all substrings of proper length that appear at least twice
    min_length = 8
    substrings = [path[i: j] for i in range(len(path))
          for j in range(i + 1, len(path) + 1)]
    substrings = [s for s in substrings if ((len(s) % 4 == 0) and (len(s) > 7) and (s[0:2] in ('RR', 'LL')) and len(s) < 21)]

    counts = {}
    for substring in substrings:
        try:
             counts[substring] += 1
        except KeyError:
             counts[substring] = 1

    substrings = []
    for key, value in counts.items():
        if value > 1:
            substrings.append(key)

    # validate combinations of substrings against string
    # must be able to construct complete string of sub-parts
    possible_solutions = []
    for combo in itertools.combinations(substrings, 3):
        copy = str(path)
        parts = []
        while len(copy) > 0:
            for part in combo:
                if copy.find(part) == 0:
                    parts.append(part)
                    copy = copy[len(part):]
                    if len(copy) == 0:
                        possible_solutions.append(parts)
                    break
            else:
                copy = ""

    return possible_solutions[0]


def clean(parts):
    name_to_move = {}
    move_to_name = {}
    names = ['A', 'B', 'C']
    for a in zip(list(set(parts)), names):
        name_to_move[a[1]] = a[0]
        move_to_name[a[0]] = a[1]

    seq = []
    for part in parts:
        seq.append(ord(move_to_name[part]))
        seq.append(ord(','))
    seq.pop()
    seq.append(10)

    for name in names:
        movement = name_to_move[name]
        for instr in [movement[i:i+2] for i in range(0, len(movement), 2)]:
            if instr[0] in ('L', 'R'):
                seq.append(ord(instr[0]))
            else:
                for digit in instr:
                    seq.append(ord(digit))
            seq.append(ord(','))
        seq.pop()
        seq.append(10)

    seq.append(ord('n'))
    seq.append(10)

    return seq


def find_robots(parts, runner):
    runner._program[0] = 2
    runner.set_input_values(*parts)
    ec = runner.run()
    out = runner.output_value()
    print(out)


def test(intersections, grid):
    assert ['RR08RR08', 'RR04RR04RR08', 'LL06LL02', 'RR04RR04RR08', 'RR08RR08', 'LL06LL02'] == find_parts('RR08RR08RR04RR04RR08LL06LL02RR04RR04RR08RR08RR08LL06LL02')[1]

    pos = (26, 0)
    test_grid = dict(grid)

    test_grid[pos] = ord('<')
    assert ('L', 'v') == find_way_to_turn(test_grid, pos)
    test_grid[pos] = ord('>')
    assert ('R', 'v') == find_way_to_turn(test_grid, pos)
    test_grid[pos] = ord('^')
    assert ('R', '>') == find_way_to_turn(test_grid, pos)
    test_grid[pos] = ord('v')
    assert ('L', '>') == find_way_to_turn(test_grid, pos)


def main(input):
    runner = intcode.create_runner(input)

    grid = get_grid(runner)
    intersections = get_intersections(grid)
    print(sum([pos[0]*pos[1] for pos in intersections]))

    # https://docs.google.com/spreadsheets/d/15wLqapfZMMDCPygSJAw0JPA8LX6mrJzCc-aFj2biwJY/edit?folder=0AK2tILtqsQc4Uk9PVA#gid=862776920
    # seq = 'A,B,A,C,B,C,A,C,B,C'
    # A = 'L,8,R,10,L,10'
    # B = 'R,10,L,8,L8,L,10'
    # C = 'L,4,L,6,L8,L8'

    path = get_path(grid)
    parts = find_parts(path)
    runner = intcode.create_runner(input)
    find_robots(clean(parts), runner)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
