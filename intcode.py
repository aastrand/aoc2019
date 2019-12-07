import sys


class NotInitializedException(Exception):
    pass


class IntCodeRunner:

    def __init__(self, program, input_values):
        self._program = program
        self._input_values = input_values
        self._input_seq = 0
        self._output_value = None
        self._pc = 0

        self._opcode_table = {}
        self._opcode_table[1] = self.add
        self._opcode_table[2] = self.mul
        self._opcode_table[3] = self.store
        self._opcode_table[4] = self.output
        self._opcode_table[5] = self.jump_if_true
        self._opcode_table[6] = self.jump_if_false
        self._opcode_table[7] = self.less_than
        self._opcode_table[8] = self.equals
        self._opcode_table[99] = self.halt

    def load(self, addr, mode):
        if mode == 0:
            return self._program[self._program[addr]]
        elif mode == 1:
            return self._program[addr]
        else:
            import pdb; pdb.set_trace();
            print("unknown parameter mode: %d" % mode)
            sys.exit(1)

    def add(self, p1m, p2m):
        self._program[self._program[self._pc+3]] = self.load(self._pc+1, p1m) + self.load(self._pc+2, p2m)
        self._pc += 4
        return 0

    def mul(self, p1m, p2m):
        self._program[self._program[self._pc+3]] = self.load(self._pc+1, p1m) * self.load(self._pc+2, p2m)
        self._pc += 4
        return 0

    def halt(self, *c):
        return -1

    def error(self, *c):
        print("unexpected opcode %d, exiting" % self._program[self._pc])
        return -1

    def output(self, p1m, *c):
        self._output_value = self.load(self._pc+1, p1m)
        self._pc += 2
        return 0

    def store(self, *c):
        self._program[self._program[self._pc+1]] = self._input_values[self._input_seq]
        self._input_seq += 1
        self._input_seq = min(self._input_seq, len(self._input_values)-1)
        self._pc += 2
        return 0

    def jump_if_true(self, p1m, p2m):
        if self.load(self._pc+1, p1m) != 0:
            self._pc = self.load(self._pc+2, p2m)
        else:
            self._pc += 3
        return 0

    def jump_if_false(self, p1m, p2m):
        if self.load(self._pc+1, p1m) == 0:
            self._pc = self.load(self._pc+2, p2m)
        else:
            self._pc += 3
        return 0

    def less_than(self, p1m, p2m):
        val = 0
        if self.load(self._pc+1, p1m) < \
            self.load(self._pc+2, p2m):
            val = 1

        self._program[self._program[self._pc+3]] = val
        self._pc += 4
        return 0

    def equals(self, p1m, p2m):
        val = 0
        if self.load(self._pc+1, p1m) == \
            self.load(self._pc+2, p2m):
            val = 1

        self._program[self._program[self._pc+3]] = val
        self._pc += 4
        return 0

    def output_value(self):
        if self._output_value is not None:
            return self._output_value
        else:
            raise NotInitializedException("no output value written by program")

    def run(self, pump_mode=False):
        while (True):
            opcode, p1m, p2m = decode_instruction(self._program[self._pc])
            instr = self._opcode_table.get(opcode, self.error)
            ret = instr(p1m, p2m)

            if (opcode == 4 and pump_mode):
                return opcode

            if (ret == -1):
                return opcode


def decode_instruction(opcode):
    digits = []
    if opcode > 100:
        while len(digits) < 4:
            digits.insert(0, int(opcode % 10))
            opcode = opcode / 10
    else:
        digits = [0, 0, 0, opcode]

    return digits[3], digits[1], digits[0]


def create_runner(input_file, *input_values):
    program = []
    for l in open(input_file, 'r'):
        program.extend(l.strip().split(','))

    # Clean
    for i, c in enumerate(program):
        program[i] = int(c)

    return IntCodeRunner(program, list(input_values))
