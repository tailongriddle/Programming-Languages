import numpy as np
import pytest
import os
import random
from aZero import pandas_func

def test_1():
    assert pandas_func("ExampleTab.txt")[0][1] == 3.05

def test_2():
    assert pandas_func("ExampleTab.txt")[1][0] == 'class'

def test_3():
    r = [5.67, 3.05, 3.84, 1.24]
    i = random.randint(0,3)
    assert pandas_func("ExampleTab.txt")[0][i] == r[i]
