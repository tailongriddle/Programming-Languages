import pytest
from GAinspector import *
from part1 import*

def test_crossover_1():
    assert inspect_crossover(crossover, "010101", "100111") == 1

def test_crossover_2():
    assert inspect_crossover(crossover, "0000000", "0000000") == 1

def test_crossover_3():
    assert inspect_crossover(crossover, "1111111", "0000000") == 1

def test_crossover_4():
    assert inspect_crossover(crossover, "111000001", "010110110") == 1

def test_crossover_5():
    assert inspect_crossover(crossover, "10000101110", "00101101011") == 1

