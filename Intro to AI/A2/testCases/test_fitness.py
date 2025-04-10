import pytest
from GAinspector import *
from part1 import*

def test_fitness_1():
    assert inspect_fitness(fitness, "100110101111010", 9) == 1


def test_fitness_2():

    assert inspect_fitness(fitness, "111111", 6) == 1


def test_fitness_3():

    assert inspect_fitness(fitness, "0000000", 0) == 1


def test_fitness_4():

    assert inspect_fitness(fitness, "0000100000", 1) == 1