#!/usr/bin/env python3

import pickle
import os.path
import sys
from collections import defaultdict


def parse(f):
    grid = {}
    y = 0

    doors = {}
    keys = {}
    positions = []

    for l in open(f, 'r'):
        x = 0
        for c in l.strip():
            pos = (x, y)
            grid[pos] = c

            if c == '@':
                positions.append(pos)
            if 65 <= ord(c) <= 90:
                # door
                doors[c] = pos
            if 97 <= ord(c) <= 122:
                # key
                keys[c] = pos

            x += 1
        y += 1

    return grid, doors, keys, positions


def get_min_dist(Q, dist):
    min = float('inf')
    for v in Q:
        if dist[v] <= min:
            min = dist[v]
            min_node = v
    return min_node


def dijkstra(graph, start, end):
    Q = set()
    dist = {}
    prev = {}

    for pos in graph.keys():
        dist[pos] = float('inf')
        prev[pos] = None
        Q.add(pos)
    dist[start] = 0.0

    while len(Q) > 0:
        u = get_min_dist(Q, dist)
        Q.remove(u)

        for neighbour in graph[u]:
            alt = dist[u] + 1.0
            if alt < dist[neighbour]:
                dist[neighbour] = alt
                prev[neighbour] = u

    path = []
    u = end
    if u in prev or u == start:
        while u:
            path.insert(0, u)
            u = prev.get(u)

    return path, dist


NEIGHBOUR_OFFSETS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
def offset_pos(pos, offset):
    return (pos[0]+offset[0], pos[1]+offset[1])


def keys_and_doors_in_path(keys, door_pos_to_key_pos, path, pos1, pos2):
    path_keys = set()
    path_keys_required = set()
    for pos in path:
        if pos in keys.values() and pos != pos1 and pos != pos2:
            path_keys.add(pos)

        key_pos = door_pos_to_key_pos.get(pos, None)
        if key_pos:
            path_keys_required.add(key_pos)

    return set(path), path_keys, path_keys_required


def precompute_distances(grid, keys, doors):
    graph = defaultdict(set)
    positions = []
    for pos, c in grid.items():
        if c == '#':
            continue
        for offset in NEIGHBOUR_OFFSETS:
            candidate = offset_pos(pos, offset)
            value = grid.get(candidate)
            if value is not None and value != '#':
                graph[pos].add(candidate)
                graph[candidate].add(pos)
            if c == '@':
                positions.append(pos)

    door_pos_to_key_pos = {}
    for door, pos in doors.items():
        door_pos_to_key_pos[pos] = keys[door.lower()]

    distances = {}
    items = list(keys.items())
    for start_pos in positions:
        items.append(('@', start_pos))

    for key1, pos1 in items:
        for key2, pos2 in items:
            if key2 == key1:
                distances[(pos1, pos2)] = (set(), set())
                distances[(pos2, pos1)] = (set(), set())
                continue

            if distances.get((key1, key2)):
                continue

            path, _ = dijkstra(graph, pos1, pos2)
            if len(path) < 2:
                continue

            pos_path, path_keys, path_keys_required = keys_and_doors_in_path(keys, door_pos_to_key_pos, path, pos1, pos2)
            distances[(pos1, pos2)] = (pos_path, path_keys, path_keys_required)
            distances[(pos2, pos1)] = (pos_path, path_keys, path_keys_required)

            for key in path_keys:
                this_path = path[:path.index(key)+1]
                this_path, this_keys, this_keys_required = keys_and_doors_in_path(keys, door_pos_to_key_pos, this_path, pos1, key)
                distances[(pos1, key)] = (this_path, this_keys, this_keys_required)
                distances[(key, pos1)] = (this_path, this_keys, this_keys_required)

    return distances


def reachable(distances, keys, pos, cur_keys):
    reachable = []

    for key, key_pos in keys.items():
        if key_pos == pos or key_pos in cur_keys or (pos, key_pos) not in distances:
            continue

        path, path_keys, path_keys_required = distances[(pos, key_pos)]
        if path_keys_required.issubset(cur_keys) and path_keys.issubset(cur_keys):
            reachable.append((key_pos, key))

    return reachable


def modify_for_part2(grid, start_pos):
    grid = dict(grid)
    positions = []
    # @#@
    # ###
    # @#@
    grid[offset_pos(start_pos, (-1, -1))] = '@'
    positions.append(offset_pos(start_pos, (-1, -1)))
    grid[offset_pos(start_pos, (0, -1))] = '#'
    grid[offset_pos(start_pos, (1, -1))] = '@'
    positions.append(offset_pos(start_pos, (1, -1)))

    grid[offset_pos(start_pos, (-1, 0))] = '#'
    grid[offset_pos(start_pos, (0, 0))] = '#'
    grid[offset_pos(start_pos, (1, 0))] = '#'

    grid[offset_pos(start_pos, (-1, 1))] = '@'
    positions.append(offset_pos(start_pos, (-1, 1)))
    grid[offset_pos(start_pos, (0, 1))] = '#'
    grid[offset_pos(start_pos, (1, 1))] = '@'
    positions.append(offset_pos(start_pos, (1, 1)))

    return grid, positions


SHORTEST_CACHE = {}

def find_shortest(distances, keys, positions, have_keys, path):
    best_length, best_positions, best_keys, best_path = SHORTEST_CACHE.get((tuple(positions), frozenset(have_keys)), (-1, list(positions), None, None))
    if best_length > 0:
        return best_length, best_positions, best_keys, best_path

    candidates = [[], [], [], []]
    got_candidates = False
    for i, cur_pos in enumerate(positions):
        candidates[i] = [(pos, key) for pos, key in reachable(distances, keys, cur_pos, have_keys)]
        if candidates[i]:
            got_candidates = True

    if not got_candidates:
        return 0, positions, have_keys, path

    for i in range(len(positions)):
        for pos, key in candidates[i]:
            cur_keys = set(have_keys)
            cur_keys.add(pos)

            cur_positions = list(positions)
            cur_positions[i] = pos

            that_length, that_pos, that_keys, that_path = find_shortest(distances, keys, cur_positions, cur_keys, path)
            length = that_length + len(distances[(positions[i], pos)][0]) - 1
            if best_length == -1 or length <= best_length:
                best_length = length
                best_positions[i] = pos
                best_keys = cur_keys
                best_path = list(that_path)
                best_path.append(best_positions[i])

    SHORTEST_CACHE[(tuple(positions), frozenset(have_keys))] = best_length, best_positions, best_keys, best_path

    return best_length, best_positions, best_keys, best_path


def print_grid(grid):
    max_x = max([pos[0] for pos in grid.keys()])
    max_y = max([pos[1] for pos in grid.keys()])
    for y in range(max_y+1):
        for x in range(max_x+1):
            print(grid[(x, y)], end='')
        print()


def solve(grid, distances, keys, positions):
    best_length, _, _, path = find_shortest(distances, keys, positions, set(), [])
    print(best_length)
    path.reverse()
    for pos in path:
        print(grid[pos], end='')
    print()


def test():
    grid, doors, keys, positions = parse('larger.txt')
    distances = precompute_distances(grid, keys, doors)

    cur_keys = set()
    assert [(keys['a'], 'a')] == reachable(distances, keys, positions[0], cur_keys)
    cur_keys.add(keys['a'])
    assert [(keys['b'], 'b')] == reachable(distances, keys, keys['a'], cur_keys)
    cur_keys.add(keys['b'])
    assert [(keys['c'], 'c')] == reachable(distances, keys, keys['b'], cur_keys)
    cur_keys.add(keys['c'])
    assert [(keys['e'], 'e'), (keys['d'], 'd')] == reachable(distances, keys, keys['c'], cur_keys)
    cur_keys.add(keys['e'])
    assert [(keys['d'], 'd')] == reachable(distances, keys, keys['e'], cur_keys)
    cur_keys.remove(keys['e'])
    cur_keys.add(keys['d'])
    assert [(keys['e'], 'e')] == reachable(distances, keys, keys['d'], cur_keys)
    cur_keys.add(keys['e'])
    assert [(keys['f'], 'f')] == reachable(distances, keys, keys['e'], cur_keys)
    cur_keys.add(keys['f'])
    assert [] == reachable(distances, keys, keys['f'], cur_keys)

    grid, doors, keys, positions = parse('example1.txt')
    distances = precompute_distances(grid, keys, doors)

    cur_keys = set()
    assert [(keys['b'], 'b'), (keys['a'], 'a')] == reachable(distances, keys, positions[0], cur_keys)

    grid, doors, keys, positions = parse('example21.txt')
    grid, positions = modify_for_part2(grid, positions[0])
    distances = precompute_distances(grid, keys, doors)

    cur_keys = set()
    assert [(keys['a'], 'a')] == reachable(distances, keys, positions[0], cur_keys)
    assert [] == reachable(distances, keys, positions[1], cur_keys)
    assert [] == reachable(distances, keys, positions[2], cur_keys)
    assert [] == reachable(distances, keys, positions[3], cur_keys)

    cur_keys.add(keys['a'])
    assert [] == reachable(distances, keys, positions[0], cur_keys)
    assert [] == reachable(distances, keys, positions[1], cur_keys)
    assert [] == reachable(distances, keys, positions[2], cur_keys)
    assert [(keys['b'], 'b')] == reachable(distances, keys, positions[3], cur_keys)

    cur_keys.add(keys['b'])
    assert [] == reachable(distances, keys, positions[0], cur_keys)
    assert [] == reachable(distances, keys, positions[1], cur_keys)
    assert [(keys['c'], 'c')] == reachable(distances, keys, positions[2], cur_keys)
    assert [] == reachable(distances, keys, positions[3], cur_keys)

    cur_keys.add(keys['c'])
    assert [] == reachable(distances, keys, positions[0], cur_keys)
    assert [(keys['d'], 'd')] == reachable(distances, keys, positions[1], cur_keys)
    assert [] == reachable(distances, keys, positions[2], cur_keys)
    assert [] == reachable(distances, keys, positions[3], cur_keys)


def main(f):
    test()

    grid, doors, keys, positions = parse(f)
    if os.path.exists(f+'-distances.pickle'):
        distances = pickle.load(open(f+'-distances.pickle', 'rb'))
    else:
        distances = precompute_distances(grid, keys, doors)
        pickle.dump(distances, open(f+'-distances.pickle', 'wb'))
    solve(grid, distances, keys, positions)

    if len(positions) == 1:
        grid, positions = modify_for_part2(grid, positions[0])
        print_grid(grid)

    if os.path.exists(f+'-distances-part2.pickle'):
        distances = pickle.load(open(f+'-distances-part2.pickle', 'rb'))
    else:
        distances = precompute_distances(grid, keys, doors)
        pickle.dump(distances, open(f+'-distances-part2.pickle', 'wb'))
    SHORTEST_CACHE.clear()
    solve(grid, distances, keys, positions)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
