import numpy as np
import pytest
import os
from aZero import statsTuple

def test_1():
    assert statsTuple((1,2,3,4), (1,2,3)) == None

def test_2():
    assert statsTuple((1,2,3,4), (1,2,3,4,5)) == None

def test_3():
    assert statsTuple((1,2,3,4), (1,2,3,4)) == (10, 2.5, 1, 4, 10, 2.5, 1, 4, 1.0, 1.0)

def test_4():
    assert statsTuple((1,2,3,4), (4,3,2,1)) == (10, 2.5, 1, 4, 10, 2.5, 1, 4, -1.0, -1.0)

def test_5():
    assert statsTuple((1,2,3,4), (1,1,1,2)) == (10, 2.5, 1, 4, 5, 1.25, 1, 2, 0.77, 0.77)

