#!/usr/bin/env python3

from itertools import combinations
from sympy import primefactors
import copy
import sys


def parse(input):
    bodies = []
    for l in open(input, 'r'):
        l = l.strip()[1:-1]
        bodies.append([[int(a.split('=')[1]) for a in l.split(',')], [0, 0, 0]])

    return bodies


def update_velocity(a, b, f, t):
    for axis in range(f, t):
        if a[0][axis] < b[0][axis]:
            a[1][axis] = a[1][axis] + 1
            b[1][axis] = b[1][axis] - 1
        elif  a[0][axis] > b[0][axis]:
            a[1][axis] = a[1][axis] - 1
            b[1][axis] = b[1][axis] + 1


def apply_velocity(a, f=0, t=3):
    for axis in range(f, t):
        a[0][axis] = a[0][axis] + a[1][axis]


def calculate_total_energy(bodies):
    sum = 0
    for b in bodies:
        p1 = 0
        for n in range(0, 3):
            p1 += abs(b[0][n])
        p2 = 0
        for n in range(0, 3):
            p2 += abs(b[1][n])
        sum += p1*p2

    return sum


def print_bodies(bodies, n):
    print("After %s steps:" % n)
    for b in bodies:
        print(b)
    print()


def update_bodies(bodies, combos, f=0, t=3):
    for c in combos:
        update_velocity(bodies[c[0]], bodies[c[1]], f, t)

    for b in bodies:
        apply_velocity(b, f, t)


def compute_lookup_table(bodies, axis):
    combos = [c for c in combinations([0,1,2,3], 2)]

    first_pos = [bodies[0][0][axis],  bodies[1][0][axis], bodies[2][0][axis], bodies[3][0][axis]]
    first_vel = [0, 0, 0, 0]

    lookup = [[first_pos, first_vel]]

    step = 0
    while True:
        step += 1
        for c in combos:
            update_velocity(bodies[c[0]], bodies[c[1]], axis, axis+1)

        pos = [bodies[0][0][axis],  bodies[1][0][axis], bodies[2][0][axis], bodies[3][0][axis]]
        vel = [bodies[0][1][axis],  bodies[1][1][axis], bodies[2][1][axis], bodies[3][1][axis]]

        if first_pos == pos and first_vel == vel:
            print_bodies(bodies, step)
            break

        lookup.append([pos, vel])

        for b in bodies:
            apply_velocity(b, axis, axis+1)

    return lookup


def main(input, steps):
    bodies = parse(input)
    steps = int(steps)
    combos = [c for c in combinations([0,1,2,3], 2)]

    print_bodies(bodies, 0)
    for n in range(1, steps+1):
        update_bodies(bodies, combos)

        if n % (steps/10) == 0:
            print_bodies(bodies, n)

    print(calculate_total_energy(bodies))

    bodies = parse(input)
    x = compute_lookup_table(bodies, 0)
    y = compute_lookup_table(bodies, 1)
    z = compute_lookup_table(bodies, 2)

    print(len(x), len(y), len(z))
    factors = set()
    for t in x, y, z:
        for p in primefactors(len(t)):
            factors.add(p)

    step_delta = 1
    for p in factors:
        step_delta *= p

    step = step_delta
    while True:
        xt = x[step % len(x)]
        yt = y[step % len(y)]
        zt = z[step % len(z)]

        if xt == x[0] and yt == y[0] and zt == z[0]:
            print(step)
            break

        step += step_delta


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))
