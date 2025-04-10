import pytest
import os
from aZero import calcMyGrade

def test_1():
    assert calcMyGrade([100, 100, 100, 100, 100], [100, 100], [100, 100], [100, 100], [10, 20, 30, 40]) == 100

def test_2():
    assert calcMyGrade([0, 0, 0, 0, 0], [0,0], [0, 0], [0, 0], [10, 20, 30, 40]) == 0

def test_3():
    assert calcMyGrade([80, 80, 80, 80, 80], [100, 100], [20, 20], [100, 100], [40, 30, 20, 10]) == 76.0

def test_4():
    assert calcMyGrade([80, 80, 80, 80, 80], [100, 100], [20, 20], [100, 100], [0, 0, 0, 100]) == 100

def test_5():
    assert calcMyGrade([80, 80, 80, 80, 80], [100, 100], [20, 20], [100, 100], [0, 0, 50, 50]) == 60

def test_6():
    assert isinstance(calcMyGrade([80, 80, 80, 80, 80], [100, 100], [20, 20], [100, 100], [0, 0, 50, 50]), float) == True