#!/usr/bin/env python3

import numpy as np
import sys
from math import ceil, floor


BASE_PATTERN = [0, 1, 0, -1]


def create_pattern(element, length):
    base = []
    for b in BASE_PATTERN:
        base.extend([b]*element)

    output = []
    for i in range(0, ceil(length / len(base))+1):
        output.extend(base)

    return output[1:length+1]


def process_numpy(signal, matrix, out, temp):
    tmp = np.dot(matrix, signal)
    np.absolute(tmp.A1, out=temp)
    np.mod(temp, 10, out=out)

    return out


def iterate_numpy(signal, n):
    signal = np.array([int(d) for d in signal])
    length = len(signal)
    out = np.array([0] * length)
    temp = np.array([0] * length)

    matrix = [0]*length
    for x in range(0, length):
        matrix[x] = np.array(create_pattern(x+1, length))

    matrix = np.matrix(matrix)

    for i in range(0, n):
        process_numpy(signal, matrix, out, temp)
        signal, out = out, signal

    return ''.join([str(s) for s in signal])


def iterate_sum_from_right(data, n):
    offset = int(data[:7])
    data = list(data) * 10000
    data = data[offset:]

    for n in range(0, n):
        sum = 0
        for x in range(len(data)-1, -1, -1):
            sum += int(data[x])
            sum = sum % 10
            data[x] = sum

    return ''.join([str(d) for d in data[:8]])


def test():
    assert [1, 0, -1, 0] == create_pattern(1, 4)
    assert [0, 1, 1, 0, 0, -1, -1, 0] == create_pattern(2, 8)
    assert [0, 0, 1, 1, 1, 0, 0, 0, -1, -1, -1, 0, 0, 0, 1, 1, 1, 0, 0, 0] == create_pattern(3, 20)

    assert '01029498' == iterate_numpy('12345678', 4)

    assert '24176176' == iterate_numpy('80871224585914546619083218645595', 100)[:8]
    assert '73745418' == iterate_numpy('19617804207202209144916044189917', 100)[:8]
    assert '52432133' == iterate_numpy('69317163492948606335995924319873', 100)[:8]

    assert '84462026' == iterate_sum_from_right('03036732577212944063491565474664', 100)
    assert '78725270' == iterate_sum_from_right('02935109699940807407585447034323', 100)
    assert '53553731' == iterate_sum_from_right('03081770884921959731165446850517', 100)


def main(input):
    test()

    for l in open(input, 'r'):
        signal = l.strip()
    print(iterate_numpy(signal, 100)[:8])

    print(iterate_sum_from_right(signal, 100)[:8])


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
