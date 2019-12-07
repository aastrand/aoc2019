#!/usr/bin/env python3

import itertools
import sys
import intcode


def test():
    assert 43210 == run_sequence("43210.txt", [4,3,2,1,0])
    assert 54321 == run_sequence("54321.txt", [0,1,2,3,4])
    assert 65210 == run_sequence("65210.txt", [1,0,4,3,2])

    assert 139629729 == run_pumped_sequence("139629729.txt", [9,8,7,6,5])
    assert 18216 == run_pumped_sequence("18216.txt", [9,7,8,5,6])


def run_sequence(input_file, sequence):
    last_output = 0
    for phase in sequence:
        runner = intcode.create_runner(input_file, phase, last_output)
        runner.run()
        last_output = runner.output_value()

    return last_output


def run_pumped_sequence(input_file, sequence):
    runners = {}
    last_output = 0
    last_e_output = 0
    while (True):
        for i in range(0, 5):
            runner = runners.get(i)
            if runner is None:
                runner = intcode.create_runner(input_file, sequence[i], last_output)
                runners[i] = runner
            runner._input_values[1] = last_output

            opcode = runner.run(True)
            last_output = runner.output_value()

            if i == 4:
                last_e_output = last_output

            if opcode == 99:
                return last_e_output


def main(input_file):
    test()

    max_signal = -1
    start = [0,1,2,3,4]
    for p in itertools.permutations(start):
        signal = run_sequence(input_file, p)
        if signal > max_signal:
            max_signal = signal

    print(max_signal)

    max_signal = -1
    start = [5,6,7,8,9]
    for p in itertools.permutations(start):
        signal = run_pumped_sequence(input_file, p)
        if signal > max_signal:
            max_signal = signal

    print(max_signal)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
