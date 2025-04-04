import pytest
import os
from aZero import add

def test_addNums():
    assert add(1, 2) == 3

def test_mixedNums():
    assert add(1, 2.5) == 3.5

def test_addStrings():
    assert add("Hello ", "World") == "Hello World"

def test_addLists():
    assert add([1, 2], [3, 4]) == [1, 2, 3, 4]

def test_addStringNum():
    assert add("Hello ", 2) == "Hello 2"

def test_addStringNum_flip():
    assert add(2, "Hello") == "2Hello"

def test_addStringNum_nums():
    assert add("2", "2") == "22"

def test_addTuples():
    assert add((3,4), 2) == None

def test_addTuples_secondTest():
    assert add(2, (2,3)) == None