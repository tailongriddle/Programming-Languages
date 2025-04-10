import pytest
from GAinspector import *
from part1 import*

def test_mutate_1():
    assert inspect_mutate(mutate, "01100100100010100010", 0) == 1

def test_mutate_2():
    assert inspect_mutate(mutate, "11111011110111111111", 1) == 1

def test_mutate_3():
    assert inspect_mutate(mutate, "01001011001011100001", 0.5) == 1

def test_mutate_4():
    assert inspect_mutate(mutate, "01001011001011100001", 0.25) == 1

def test_mutate_5():
    assert inspect_mutate(mutate, "10100111010000101101", 0.001) == 1

