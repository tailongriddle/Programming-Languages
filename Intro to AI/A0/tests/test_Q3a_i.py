import pytest
import os
from aZero import generateMatrix

def test_1():
    m = generateMatrix(1,1,0,1)
    assert m[0][0] >=0 and m[0][0] <= 1

def test_2():
    m = generateMatrix(1,1,0,1)
    assert len(m) == 1 and len(m[0]) == 1

def test_3():
    m = generateMatrix(1,1,0,1)
    assert isinstance(m[0][0], float) == True

def test_4():
    m = generateMatrix(5,10,0,1)
    assert len(m) == 5 and len(m[0]) == 10

