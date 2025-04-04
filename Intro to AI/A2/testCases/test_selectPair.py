import pytest
from GAinspector import *
from part1 import*
def test_selectPair_1():
    pop1 = ["1111101100", "0000000100", "1000110010", "0010011011", "1001110000"]
    assert inspect_selectPair(selectPair, pop1, 1) == 1

def test_selectPair_2():
    pop2 = ["1011011111", "0001011010", "1010110001", "1001110100", "1100001100"]
    assert inspect_selectPair(selectPair, pop2, 2 ) == 1

def test_selectPair_3():
    pop3 = ["11111111111", "11110110110", "10101100000", "10000101000", "11101111111", "00000000000"]
    assert inspect_selectPair(selectPair, pop3, 3) == 1

def test_selectPair_4():
    pop4 = ["0011111011000", "1001101110101", "0000110100110", "0010011111101", "1111011111001",
            "0001000011110", "0111000110010", "1110011100001", "1011110010010", "0010111100111",
            "0001110110111", "1100111011100", "0001000101000", "1001111001010", "0100101111100"]
    assert inspect_selectPair(selectPair, pop4,4) == 1
