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
        self._rel_base = 0

        self._opcode_table = {}
        self._opcode_table[1] = self.add
        self._opcode_table[2] = self.mul
        self._opcode_table[3] = self.input
        self._opcode_table[4] = self.output
        self._opcode_table[5] = self.jump_if_true
        self._opcode_table[6] = self.jump_if_false
        self._opcode_table[7] = self.less_than
        self._opcode_table[8] = self.equals
        self._opcode_table[9] = self.adj_base
        self._opcode_table[99] = self.halt

    def convert_addr(self, addr, mode):
        real_addr = 0
        if mode == 0:
            real_addr = self._program[addr]
        elif mode == 1:
            real_addr = addr
        elif mode == 2:
            real_addr = self._rel_base + self._program[addr]
        else:
            import pdb; pdb.set_trace();
            print("unknown parameter mode: %d" % mode)
            sys.exit(1)

        return real_addr

    def load(self, addr, mode):
        real_addr = self.convert_addr(addr, mode)
        self.check_and_expand(real_addr)
        return self._program[real_addr]

    def store(self, addr, mode, val):
        real_addr = self.convert_addr(addr, mode)
        self.check_and_expand(real_addr)
        self._program[real_addr] = val

    def check_and_expand(self, addr):
        cur_size = len(self._program)
        if addr >= cur_size:
            self._program.extend([0]*(addr + 1 - cur_size ))

    def add(self, p1m, p2m, p3m):
        self.store(self._pc+3, p3m, self.load(self._pc+1, p1m) + self.load(self._pc+2, p2m))
        self._pc += 4
        return 0

    def mul(self, p1m, p2m, p3m):
        self.store(self._pc+3, p3m, self.load(self._pc+1, p1m) * self.load(self._pc+2, p2m))
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

    def input(self, p1m, p2m, p3m):
        self.store(self._pc+1, p1m, self._input_values[self._input_seq])
        self._input_seq += 1
        self._input_seq = min(self._input_seq, len(self._input_values)-1)
        self._pc += 2
        return 0

    def jump_if_true(self, p1m, p2m, *c):
        if self.load(self._pc+1, p1m) != 0:
            self._pc = self.load(self._pc+2, p2m)
        else:
            self._pc += 3
        return 0

    def jump_if_false(self, p1m, p2m, *c):
        if self.load(self._pc+1, p1m) == 0:
            self._pc = self.load(self._pc+2, p2m)
        else:
            self._pc += 3
        return 0

    def less_than(self, p1m, p2m, p3m):
        val = 0
        if self.load(self._pc+1, p1m) < \
            self.load(self._pc+2, p2m):
            val = 1

        self.store(self._pc+3, p3m, val)
        self._pc += 4
        return 0

    def equals(self, p1m, p2m, p3m):
        val = 0
        if self.load(self._pc+1, p1m) == \
            self.load(self._pc+2, p2m):
            val = 1

        self.store(self._pc+3, p3m, val)
        self._pc += 4
        return 0

    def adj_base(self, p1m, *c):
        offset = self.load(self._pc+1, p1m)
        self._rel_base += offset
        self._pc += 2
        return 0

    def output_value(self):
        if self._output_value is not None:
            return self._output_value
        else:
            raise NotInitializedException("no output value written by program")

    def set_input_values(self, *values):
        self._input_values = [v for v in values]

    def run(self, pump_mode=False):
        while (True):
            opcode, params = decode_instruction(self._program[self._pc])
            instr = self._opcode_table.get(opcode, self.error)
            ret = instr(params[0], params[1], params[2])

            if ret == -1 or (opcode == 4 and pump_mode):
                return opcode


def decode_instruction(opcode):
    digits = [int(c) for c in "%s" % opcode]
    digits.reverse()

    if len(digits) > 1:
        if digits[1] != 0:
            opcode = int("%s%s" % (digits[0], digits[1]))
        else:
            opcode = digits[0]
        params = digits[2:]
    else:
        opcode = digits[0]
        params = []

    if len(params) < 3:
        params.extend([0]*(3 - len(params)))

    return opcode, tuple(params)


def create_runner(input_file, *input_values):
    program = []
    for l in open(input_file, 'r'):
        program.extend(l.strip().split(','))

    # Clean
    for i, c in enumerate(program):
        program[i] = int(c)

    return IntCodeRunner(program, list(input_values))
