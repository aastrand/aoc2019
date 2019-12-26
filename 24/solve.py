#!/usr/bin/env python3

import sys
from collections import defaultdict


NEIGHBOUR_OFFSETS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
def offset_pos(pos, offset):
    return (pos[0]+offset[0], pos[1]+offset[1])


def parse(f):
    grid = {}
    y = 0
    for l in open(f, 'r'):
        x = 0
        for d in l.strip():
            grid[(x, y)] = d
            x += 1
        y += 1

    return grid


def evolve(grid):
    new_grid = {}
    for pos, value in grid.items():
        counts = defaultdict(int)
        for offset in NEIGHBOUR_OFFSETS:
            counts[grid.get(offset_pos(pos, offset), '.')] += 1

        if counts['#'] == 1 and value == '#':
            new_grid[pos] = '#'
        elif 0 < counts['#'] < 3 and value == '.':
            new_grid[pos] = '#'
        else:
            new_grid[pos] = '.'

    return new_grid


def print_grid(grid):
    if not grid:
        return

    max_x = max([pos[0] for pos in grid.keys()])
    max_y = max([pos[1] for pos in grid.keys()])
    for y in range(max_y+1):
        for x in range(max_x+1):
            print(grid.get((x, y), '.'), end='')
        print()


def calc_biodiversity(grid, size=5):
    sum = 0
    for y in range(size):
        for x in range(size):
            nth = x + (y*size)
            if grid[(x, y)] == '#':
                sum += pow(2, nth)

    return sum


def test():
    grid = parse('example.txt')
    for i in range(4):
        grid = evolve(grid)

    after = parse('after4.txt')
    assert grid == after

    grid = parse('example2.txt')
    assert 2129920 == calc_biodiversity(grid)


def part1(f):
    grid = parse(f)
    seen = set()
    seen.add(calc_biodiversity(grid))

    while True:
        grid = evolve(grid)
        diversity = calc_biodiversity(grid)
        if diversity in seen:
            print(diversity)
            break
        seen.add(diversity)


# # # # #
# # # # #
# # # # #
# # # # #
# # # # #
INNER_POSITIONS = [(2, 1), (1, 2), (3, 2), (2, 3)]
OUTER_POSITIONS = []
OUTER_TO_INNER = {}
INNER_TO_OUTER = defaultdict(list)
for p in range(5):
    OUTER_POSITIONS.append((p, 0))
    INNER_TO_OUTER[(2, 1)].append((p, 0))

    OUTER_POSITIONS.append((p, 4))
    INNER_TO_OUTER[(2, 3)].append((p, 4))

    OUTER_POSITIONS.append((0, p))
    INNER_TO_OUTER[(1, 2)].append((0, p))

    OUTER_POSITIONS.append((4, p))
    INNER_TO_OUTER[(3, 2)].append((4, p))

for p in range(1, 4):
    OUTER_TO_INNER[(p, 0)] = [(2, 1)]
    OUTER_TO_INNER[(p, 4)] = [(2, 3)]
    OUTER_TO_INNER[(0, p)] = [(1, 2)]
    OUTER_TO_INNER[(4, p)] = [(3, 2)]

#  #  #  #  #
#  #  21 #  #
#  12 #  32 #
#  #  23 #  #
#  #  #  #  #
OUTER_TO_INNER[(0, 0)] = [(2, 1), (1, 2)]
OUTER_TO_INNER[(4, 0)] = [(3, 2), (2, 1)]
OUTER_TO_INNER[(0, 4)] = [(2, 3), (1, 2)]
OUTER_TO_INNER[(4, 4)] = [(3, 2), (2, 3)]


def should_spawn_outer(grid):
    for pos in OUTER_POSITIONS:
        if grid.get(pos) == '#':
            return True

    return False


def should_spawn_inner(grid):
    for pos in INNER_POSITIONS:
        if grid.get(pos) == '#':
            return True

    return False


EMPTY = {}
for y in range(0, 5):
    for x in range(0, 5):
        EMPTY[(x, y)] = '.'
EMPTY[(2,2)] = '?'

def evolve_recursive(grids):
    outer_level = min([k for k in grids.keys()])
    inner_level = max([k for k in grids.keys()])

    if should_spawn_outer(grids[outer_level]):
        outer_level -= 1
        grids[outer_level] = dict(EMPTY)

    if should_spawn_inner(grids[inner_level]):
        inner_level += 1
        grids[inner_level] = dict(EMPTY)

    new_grids = {}
    for level in range(outer_level, inner_level + 1):
        outer = grids.get(level - 1, {})
        grid = grids.get(level)
        inner = grids.get(level + 1, {})

        new_grid = {}
        for pos, value in grid.items():
            if pos == (2, 2):
                new_grid[pos] = '?'
                continue

            counts = defaultdict(int)

            adjecents = set()
            for offset in NEIGHBOUR_OFFSETS:
                n_pos = offset_pos(pos, offset)
                if n_pos == (2, 2):
                    for other_pos in INNER_TO_OUTER[pos]:
                        adjecents.add((level + 1, other_pos))
                elif n_pos[0] < 0 or n_pos[0] > 4 or n_pos[1] < 0 or n_pos[1] > 4:
                    for other_pos in OUTER_TO_INNER[pos]:
                        adjecents.add((level - 1, other_pos))
                else:
                    adjecents.add((level, n_pos))

            for candidate_level, other_pos in adjecents:
                counts[grids.get(candidate_level, {}).get(other_pos, '.')] += 1

            if counts['#'] == 1 and value == '#':
                new_grid[pos] = '#'
            elif 0 < counts['#'] < 3 and value == '.':
                new_grid[pos] = '#'
            else:
                new_grid[pos] = '.'

        new_grids[level] = new_grid

    return new_grids


def print_generations(generations):
    min_level = 0
    max_level = 0
    for generation in generations:
        dmin_level = min([k for k in generation.keys()])
        dmax_level = max([k for k in generation.keys()])
        if dmin_level < min_level:
            min_level = dmin_level
        if dmax_level > max_level:
            max_level = dmax_level

    for level in range(min_level, max_level+1):
        print("level", level)
        for y in range(5):
            for generation in generations:
                grid = generation.get(level)
                for x in range(5):
                    if grid:
                        print(grid[(x, y)], end='')
                    else:
                        print(' ', end='')
                print(' ', end='')
            print()
        print()


def count_bugs(grids):
    sum = 0
    for grid in grids.values():
        for pos, value in grid.items():
            if value == '#':
                sum += 1

    return sum


def part2(f):
    grids = {0: parse(f)}
    generations = [grids]
    for n in range(200):
        grids = evolve_recursive(grids)
        generations.append(grids)
    print(count_bugs(grids))


def main(f):
    test()

    part1(f)
    part2(f)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
