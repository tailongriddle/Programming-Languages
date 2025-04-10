import pytest
import os
from aZero import queue

def test_1():
    q = queue()
    q.push(1)
    q.push(2)
    q.push(3)
    assert q.checkSize() == 3

def test_2():
    q = queue()
    q.push(1)
    q.push(2)
    q.push(3)
    q.pop()
    assert q.checkSize() == 2

def test_3():
    q = queue()
    q.push(1)
    q.push(2)
    q.push(3)
    q.pop()
    q.pop()
    assert q.checkSize() == 1

def test_4():
    q = queue()
    q.push(1)
    q.push(2)
    q.push(3)
    q.pop()
    q.pop()
    q.pop()
    assert q.checkSize() == 0

def test_5():
    q = queue()
    q.push(1)
    q.push(2)
    q.push(3)
    q.pop()
    q.pop()
    q.pop()
    q.pop()
    assert q.checkSize() == 0

def test_6():
    q = queue()
    q.push(1)
    q.push(2)
    q.push(3)
    q.pop()
    q.pop()
    assert q.pop() == 3

def test_7():
    q = queue()
    q.push(1)
    q.push(2)
    q.push(3)
    q.pop()
    q.pop()
    q.pop()
    q.pop()
    q.push(4)
    assert q.pop() == 4