import pytest
from GAinspector import *
from part1 import*

def test_makePopulation_1():
    assert inspect_makePopulation(makePopulation, 10, 30) == 1
def test_makePopulation_2():
    assert inspect_makePopulation(makePopulation, 20, 40) == 1


