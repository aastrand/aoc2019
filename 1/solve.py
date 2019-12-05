#!/usr/bin/env python3

from math import floor
import sys


def main(input):
    sum = 0
    additional_sum = 0

    for l in open(input, 'r'):
        fuel = fuel_cost(l)
        sum += fuel

        additional_sum += recursive_additional_fuel(fuel)

    print(sum)
    print(sum + additional_sum)


def fuel_cost(mass):
    cost = floor(int(mass) / 3) - 2
    return cost if cost > 0 else 0


def recursive_additional_fuel(base_fuel):
    cost = fuel_cost(base_fuel)
    sum = 0

    while (cost > 0):
        sum += cost
        cost = fuel_cost(cost)

    return sum


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
