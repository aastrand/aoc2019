#!/usr/bin/env python3

import math
import sys
from collections import defaultdict, deque


IGNORE = set([' ', '\n', None])
NON_PORTALS = set(['.', '#'])
NON_PORTALS.update(list(IGNORE))


NEIGHBOUR_OFFSETS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


START = 'AA'
END = 'ZZ'
SPECIAL_NODES = set([START, END])


def parse(input):
    grid = {}
    y = 0

    for l in open(input, 'r'):
        x = 0
        for c in l:
            if c not in IGNORE:
                grid[(x, y)] = c

            x+= 1
        y += 1

    return grid


def offset_pos(pos, offset):
    return (pos[0]+offset[0], pos[1]+offset[1])


def find_portal_id(pos, grid):
    other_digit_pos = None
    entry = None
    is_outer = False

    max_x = max([pos[0] for pos in grid.keys()])
    max_y = max([pos[1] for pos in grid.keys()])

    for offset in NEIGHBOUR_OFFSETS:
        candidate = offset_pos(pos, offset)
        val = grid.get(candidate)

        if val == '.':
            entry = candidate
        elif val not in NON_PORTALS:
            other_digit_pos = candidate

        if candidate[0] == 0 or candidate[1] == 0 or \
            candidate[0] == max_x or candidate[1] == max_y:
            is_outer = True

    for offset in NEIGHBOUR_OFFSETS:
        candidate = offset_pos(other_digit_pos, offset)
        val = grid.get(candidate)

        if val == '.':
            entry = candidate

        if candidate[0] == 0 or candidate[1] == 0 or \
            candidate[0] == max_x or candidate[1] == max_y:
            is_outer = True

    if pos[1] != other_digit_pos[1]:
        # vertical
        if pos[1] > other_digit_pos[1]:
            pos, other_digit_pos = other_digit_pos, pos
    else:
        # horizontal
        # vertical
        if pos[0] > other_digit_pos[0]:
            pos, other_digit_pos = other_digit_pos, pos

    id = '%s%s' % (grid[pos], grid[other_digit_pos])

    return id, entry, is_outer


def distance(pos1, pos2):
     return math.sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)


def build_graph(grid):
    portal_to_pos = defaultdict(set)
    pos_to_portal = {}

    for pos, c in grid.items():
        if c not in NON_PORTALS:
            id, entry, is_outer = find_portal_id(pos, grid)
            portal_to_pos[id].add(entry)
            pos_to_portal[entry] = (id, is_outer)
            pos_to_portal[pos] = (id, is_outer)

    graph = defaultdict(set)
    for pos, c in grid.items():
        portal_id, is_outer = pos_to_portal.get(pos, (None, False))

        if portal_id:
            portal_and_distances = []
            for portal_pos in portal_to_pos[pos_to_portal[pos][0]]:
                portal_and_distances.append((portal_pos, distance(pos, portal_pos)))

            portal_and_distances.sort(key=lambda x: x[1])
            pos = portal_and_distances[0][0]
            if portal_id not in SPECIAL_NODES:
                graph[pos].add(portal_and_distances[-1][0])
                graph[portal_and_distances[-1][0]].add(pos)

        if portal_id or c == '.':
            for offset in NEIGHBOUR_OFFSETS:
                candidate = offset_pos(pos, offset)
                if grid.get(candidate) == '.':
                    graph[pos].add(candidate)
                    graph[candidate].add(pos)

    return graph, pos_to_portal, {k: list(v) for k, v in portal_to_pos.items()}


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


def get_min_dist(Q, dist):
    min = float('inf')
    for v in Q:
        if dist[v] <= min:
            min = dist[v]
            min_node = v
    return min_node


def recursive_maze_bfs(graph, start, end, pos_to_portal):
    Q = deque()
    visited = set()
    depth = 0
    visited.add((depth, start))
    parent = {}

    Q.append((depth, start))
    while len(Q) > 0:
        depth, v = Q.popleft()

        if (depth, v) == (0, end):
            break

        id, _ = pos_to_portal.get(v, (None, False))

        for neighbour in graph[v]:
            nid, is_outer = pos_to_portal.get(neighbour, (None, False))

            if nid in SPECIAL_NODES and depth > 0:
                continue

            if id and nid and not is_outer and depth == 0:
                continue

            new_depth = depth
            if nid and id and is_outer:
                new_depth += 1
            elif nid and id and not is_outer:
                new_depth -= 1

            if (new_depth, neighbour) not in visited:
                visited.add((new_depth, neighbour))
                parent[(new_depth, neighbour)] = (depth, v)
                Q.append((new_depth, neighbour))

    u = parent[(0, end)]
    path = []
    while u:
        path.insert(0, u)
        u = parent.get(u)

    return path


def main(input):
    grid = parse(input)
    graph, pos_to_portal, portal_to_pos = build_graph(grid)

    start = portal_to_pos['AA'][0]
    end = portal_to_pos['ZZ'][0]
    path, dist = dijkstra(graph, start, end)

    print(int(dist[end]))

    path = recursive_maze_bfs(graph, start, end, pos_to_portal)
    print(len(path))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
