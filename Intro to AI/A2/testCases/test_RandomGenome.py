import pytest
from GAinspector import *
from part1 import*

def test_randomGenome_1():
    assert inspect_randomGenome(randomGenome, 20) == 1


def test_randomGenome_2():

    assert inspect_randomGenome(randomGenome, 50) == 1