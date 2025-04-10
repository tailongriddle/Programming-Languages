import pytest
from GAinspector import *
from part1 import*

def test_evaluateFitness_1():
    pop1 = ["1000001110", "0101100101", "1000101101", "0001011011", "0101000001"]
    assert inspect_evaluateFitness(evaluateFitness, pop1, 4.4, 5, 1) == 1


def test_evaluateFitness_2():
    pop2 = ["1111101100", "0000000100", "1000110010", "0010011011", "1001110000"]
    assert inspect_evaluateFitness(evaluateFitness, pop2, 4.2, 7, 2) == 1


def test_evaluateFitness_3():
    pop3 = ["1011011111", "0001011010", "1010110001", "1001110100", "1100001100"]
    assert inspect_evaluateFitness(evaluateFitness, pop3, 5.2, 8, 3) == 1


def test_evaluateFitness_4():
    pop4 = ["0011111011000", "1001101110101", "0000110100110", "0010011111101", "1111011111001",
            "0001000011110", "0111000110010", "1110011100001", "1011110010010", "0010111100111",
            "0001110110111", "1100111011100", "0001000101000", "1001111001010", "0100101111100"]
    assert inspect_evaluateFitness(evaluateFitness, pop4, 6.93333333333, 10, 4) == 1





