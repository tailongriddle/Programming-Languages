import pytest
import os
from aZero import node

def test_1():
    n1 = node(1,1)
    assert n1.getKey() == 1

def test_2():
    n1 = node(1,5)
    assert n1.getValue() == 5

def test_3():
    n1 = node(1,5)
    n2 = node(2,10)
    n1.assignLeftChild(n2)
    assert n1.getChildren() == [n2, None]

def test_4():
    n1 = node(1,5)
    n2 = node(2,10)
    n1.assignLeftChild(n2)
    l = n1.getChildren()
    assert l[0].getKey() == 2
    assert l[0].getValue() == 10
def test_5():
    n1 = node(1,5)
    n2 = node(2,10)
    n1.assignRightChild(n2)
    assert n1.getChildren() == [None, n2]

def test_6():
    n1 = node(1, 1)
    n2 = node(2, 2)
    n3 = node(3, 3)
    n4 = node(4, 4)
    n5 = node(5, 5)

    n2.assignLeftChild(n1)
    n2.assignRightChild(n3)
    assert n2.inOrderTraversal() == [1,2,3]

def test_7():
    n1 = node(1, 1)
    n2 = node(2, 2)
    n3 = node(3, 3)
    n4 = node(4, 4)
    n5 = node(5, 5)

    n1.assignLeftChild(n4)
    n1.assignRightChild(n5)
    n2.assignLeftChild(n1)
    n2.assignRightChild(n3)
    assert n2.inOrderTraversal() == [4,1,5, 2, 3]


def test_8():
    n1 = node(1, 1)
    n2 = node(2, 2)
    n3 = node(3, 3)
    n4 = node(4, 4)
    n5 = node(5, 5)

    n3.assignLeftChild(n4)
    n3.assignRightChild(n5)
    n2.assignLeftChild(n1)
    n2.assignRightChild(n3)
    assert n2.inOrderTraversal() == [1, 2, 4, 3, 5]