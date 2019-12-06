#!/usr/bin/env python3

import sys


def main(input):
    dag = parse(input)
    print(count_all_edges(dag))
    you = find_path(dag, 'YOU')
    san = find_path(dag, 'SAN')
    l1, l2 = remove_common_elements_from_end(you, san)
    print(len(l1) + len(l2))


def remove_common_elements_from_end(l1, l2):
    while True:
        if (len(l1) > 0 and len(l2) > 0) and l1[-1] == l2[-1]:
            l1.pop()
            l2.pop()
        else:
            break

    return l1, l2


def find_path(dag, node):
    path = []
    neighbour = dag.get(node)
    while (neighbour is not None):
        path.append(neighbour)
        neighbour = dag.get(neighbour)

    return path


def count_all_edges(dag):
    count = 0
    for key in dag.keys():
        neighbour = dag.get(key)
        while (neighbour is not None):
            count += 1
            neighbour = dag.get(neighbour)

    return count


def parse(input):
    dag = {}
    for l in open(input, 'r'):
        pair = l.split(')')
        if len(pair) == 2:
            dag[pair[1].strip()] = pair[0].strip()

    return dag


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
