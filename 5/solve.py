#!/usr/bin/env python3

import sys


def load(program, addr, mode):
    if mode == 0:
        return program[program[addr]]
    elif mode == 1:
        return program[addr]
    else:
        import pdb; pdb.set_trace();
        print("unknown parameter mode: %d" % mode)
        sys.exit(1)


def add(pc, program, p1m, p2m):
    program[program[pc+3]] = load(program, pc+1, p1m) + load(program, pc+2, p2m)
    return 0


def mul(pc, program, p1m, p2m):
    program[program[pc+3]] = load(program, pc+1, p1m) * load(program, pc+2, p2m)
    return 0


def halt(pc, program, *c):
    print("halting, value at 0: %d" % program[0])
    return -1


def error(pc, program, *c):
    print("unexpected opcode %d, exiting" % program[pc])
    return -1


def output(pc, program, p1m, *c):
    print(load(program, pc+1, p1m))
    return 0


def store(pc, program, *c):
    program[program[pc+1]] = input_value
    return 0


def jump_if_true(pc, program, p1m, p2m):
    if load(program, pc+1, p1m) != 0:
        return load(program, pc+2, p2m)
    return 0


def jump_if_false(pc, program, p1m, p2m):
    if load(program, pc+1, p1m) == 0:
        return load(program, pc+2, p2m)
    return 0


def less_than(pc, program, p1m, p2m):
    val = 0
    if load(program, pc+1, p1m) < load(program, pc+2, p2m):
        val = 1

    program[program[pc+3]] = val
    return 0


def equals(pc, program, p1m, p2m):
    val = 0
    if load(program, pc+1, p1m) == load(program, pc+2, p2m):
        val = 1

    program[program[pc+3]] = val
    return 0


OPCODE_TABLE = {
    1: (add, 4),
    2: (mul, 4),
    3: (store, 2),
    4: (output, 2),
    5: (jump_if_true, 3),
    6: (jump_if_false, 3),
    7: (less_than, 4),
    8: (equals, 4),
    99: (halt, 0)
}


input_value = 1


def test():
    test_decode_instruction()


def test_decode_instruction():
    assert (1, 0, 1) == decode_instruction(1001)
    assert (1, 1, 0) == decode_instruction(101)
    assert (2, 0, 0) == decode_instruction(2)
    assert (99, 0, 0) == decode_instruction(99)


def main(input, value):
    test()
    program = parse(input)
    global input_value
    input_value = int(value)

    run(program)


def run(program):
    pc = 0
    while (True):
        opcode, p1m, p2m = decode_instruction(program[pc])
        instr, instr_length = OPCODE_TABLE.get(opcode, (error, 0))
        ret = instr(pc, program, p1m, p2m)

        if (ret == -1):
            break

        if ret > 0:
            pc = ret
        else:
            pc += instr_length


def decode_instruction(opcode):
    digits = []
    if opcode > 100:
        while len(digits) < 4:
            digits.insert(0, int(opcode % 10))
            opcode = opcode / 10
    else:
        digits = [0, 0, 0, opcode]

    return digits[3], digits[1], digits[0]


def parse(input):
    program = []
    for l in open(input, 'r'):
        program.extend(l.strip().split(','))

    # Clean
    for i, c in enumerate(program):
        program[i] = int(c)

    return program


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))
