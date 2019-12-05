#!/usr/bin/env python3

from copy import deepcopy
from math import floor
import sys


def add(pc, program):
    program[program[pc+3]] = program[program[pc+1]] + program[program[pc+2]]
    return 0


def mul(pc, program):
    program[program[pc+3]] = program[program[pc+1]] * program[program[pc+2]]
    return 0


def halt(pc, program):
    print("halting, value at 0: %d" % program[0])
    return 1


def error(pc, program):
    print("unexpected opcode %d, exiting" % program[pc])
    return 1


OPCODE_TABLE = {
    1: add,
    2: mul,
    99: halt
}


def main(input):
    original_program = parse(input)

    for noun in range(0, 100):
        for verb in range(0, 100):
            print (noun, verb)
            program = alter(noun, verb, deepcopy(original_program))
            program = run(program)


def alter(noun, verb, program):
    program[1] = noun
    program[2] = verb

    return program


def run(program):
    pc = 0
    while (True):
        opcode = program[pc]
        fun = OPCODE_TABLE.get(opcode, error)
        ret = fun(pc, program)
        if (ret != 0):
            break

        pc += 4

    return program


def parse(input):
    program = []
    for l in open(input, 'r'):
        program.extend(l.strip().split(','))

    # Clean
    for i, c in enumerate(program):
        program[i] = int(c)

    return program


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
