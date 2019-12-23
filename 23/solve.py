#!/usr/bin/env python3

import sys
import intcode

from collections import defaultdict, deque


def read_until_empty(runner):
    codes = defaultdict(int)
    packets = []
    packet = []

    while True:
        ec = runner.run()
        if ec == 4:
            codes[5] = 0

            packet.append(runner.output_value())

            if len(packet) == 3:
                packets.append(packet)
                packet = []

        codes[ec] = codes[ec] + 1
        if codes[5] > 6:
            if runner._input_values[runner._input_seq] == -1:
                break

    return packets


def queue_empty(input_q):
    for q in input_q.values():
        if len(q) > 0:
            return False

    return True


def init(f):
    computers = []
    for address in range(50):
        runner = intcode.create_runner(f, address, -1)
        runner.add_breakpoint_opcode(4)
        runner.add_breakpoint_opcode(5)
        computers.append(runner)

    return computers


def network(computers):
    input_q = defaultdict(deque)
    nat = []
    last_y = -1
    first_nat = None
    while True:
        active = not queue_empty(input_q)
        for address in range(50):
            computer = computers[address]

            # send
            for packet in read_until_empty(computer):
                if packet[0] == 255:
                    nat = (packet[1], packet[2])
                    if not first_nat:
                        first_nat = nat
                else:
                    input_q[packet[0]].append((packet[1], packet[2]))
                active = True

            # receive
            inputs = []
            while len(input_q[address]) > 0:
                packet = input_q[address].popleft()
                inputs.append(packet[0])
                inputs.append(packet[1])
                active = True

            inputs.append(-1)
            computer.set_input_values(*inputs)

        if not active and len(nat) > 0:
            if nat[1] == last_y:
                print("the Y value of the first packet sent to address 255:", first_nat[1])
                print("the first Y value delivered by the NAT to the computer at address 0 twice in a row:", nat[1])
                break
            last_y = nat[1]
            input_q[0].append((nat[0], nat[1]))
            nat = []


def main(f):
    computers = init(f)
    network(computers)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
