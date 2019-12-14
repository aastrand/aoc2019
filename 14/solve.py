#!/usr/bin/env python3

import sys
from collections import defaultdict
from math import ceil, floor


def parse(input):
    reaction_map = {}
    for l in open(input, 'r'):
        ingredients, result = l.strip().split('=>')
        amount, chemical = result.strip().split(' ')
        il = []
        for i in ingredients.strip().split(','):
            part = i.strip().split(' ')
            il.append((int(part[0]), part[1]))
        reaction_map[chemical] = (il, int(amount))

    return reaction_map


def sum(fuel_reactions):
    sums = {}
    for pair in fuel_reactions:
        amount = sums.get(pair[1], 0)
        amount += pair[0]
        sums[pair[1]] = amount

    fuel_reactions = []
    for key, value in sums.items():
        fuel_reactions.append((value, key))

    return fuel_reactions


def reduce(reaction_map, fuel_amount=1):
    fuel_reactions = [(fuel_amount * a, c) for a, c in reaction_map['FUEL'][0]]

    waste_map = defaultdict(int)
    while True:
        reduced = []
        for wanted_amount, chem in fuel_reactions:
            if chem not in reaction_map:
                reduced.append((wanted_amount, chem))
                continue
            else:
                if wanted_amount >= waste_map[chem]:
                    wanted_amount -= waste_map[chem]
                    waste_map[chem] = 0

            reactions, produced_amount = reaction_map[chem]
            multiplier = ceil(float(wanted_amount) / float(produced_amount))

            waste = (multiplier * produced_amount) - wanted_amount
            if waste > 0:
                waste_map[chem] += waste

            for reaction_amount, ingredient in reactions:
                new_amount = reaction_amount * multiplier
                had_in_waste = waste_map.get(ingredient, 0)

                if new_amount >= had_in_waste:
                    new_amount -= had_in_waste
                    waste_map[ingredient] = 0
                else:
                    waste_map[ingredient] = had_in_waste - new_amount
                    new_amount = 0

                reduced.append((new_amount, ingredient))

        reduced = sum(reduced)
        if fuel_reactions == reduced:
            break
        else:
            fuel_reactions = reduced

    return fuel_reactions


def find_max(reaction_map):
    ore = 1000000000000
    min = 1
    max = ore
    while min <= max:
        n = floor((max+min)/2)
        new = reduce(reaction_map, n)[0][0]
        if new < ore:
            min = n + 1
        elif new > ore:
            max = n - 1
        else:
            break

    return n


def test():
    reaction_map = parse('first.txt')
    assert 31 == reduce(reaction_map)[0][0]
    reaction_map = parse('second.txt')
    assert 165 == reduce(reaction_map)[0][0]
    reaction_map = parse('third.txt')
    assert 13312 == reduce(reaction_map)[0][0]
    reaction_map = parse('fourth.txt')
    assert 180697 == reduce(reaction_map)[0][0]
    reaction_map = parse('fifth.txt')
    assert 2210736 == reduce(reaction_map)[0][0]

    assert 82892753 == find_max(parse('third.txt'))
    assert 5586022 == find_max(parse('fourth.txt'))
    assert 460664 == find_max(parse('fifth.txt'))


def main(input):
    test()

    reaction_map = parse(input)
    print(reduce(reaction_map))

    print(find_max(reaction_map))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
