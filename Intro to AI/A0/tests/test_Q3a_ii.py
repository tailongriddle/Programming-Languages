import numpy as np
import pytest
import os
from aZero import generateMatrix, multiplyMat

def test_1():
    m1 = np.array([[5]])
    m2 = np.array([[10]])
    assert multiplyMat(m1, m2) == [[50]]

def test_2():
    m1 = np.array([[5, 6]])
    m2 = np.array([[10], [20]])
    assert multiplyMat(m1, m2) == [[170]]

def test_3():
    m1 = np.array([[5, 6], [7, 8]])
    m2 = np.array([[10, 20], [30, 40]])
    assert multiplyMat(m1, m2)[0][0] == 230 and multiplyMat(m1,m2)[1][1] == 460

def test_4():
    m1 = np.array([[5,5],[5,5]])
    m2 = np.array([[10]])
    assert multiplyMat(m1, m2) == None
