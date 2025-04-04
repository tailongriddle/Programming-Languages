#Student Name: Tai-Long Riddle
#Student ID: 873657426

import pandas as pd
import numpy as np
import scipy
import A0_Utils as A0

## Question 1 - Basics

def add(a, b):
    # See Question 1a
    ## TODO: Define Function
    if type(a) is float and type(b) is int:
        return a + float(b)
    
    if type(b) is float and type(a) is int:
        return float(a) + b
    
    if type(a) is list or type(a) is float or type(a) is str or type(a) is int: 
        if type(b) is list or type(b) is float or type(b) is str or type(b) is int:
            if type(a) is type(b):
                return a + b
            else:
                return str(a) + str(b)
    print ("Error!")
    return None

    ## TODO: comment out "raiseNotDefined()" when you start working on this function
    ##A0.raiseNotDefined()

def calcMyGrade(AssignmentScores, MidtermScores, PracticumScores, ICAScores, Weights):
    # See Question 1b
    ## TODO: Define Function
    weightedAverage = 0.0 #weightedAverage float
    weightedAssignment = ((sum(AssignmentScores) / len(AssignmentScores)) / 100) * Weights[0]
    weightedMidterm = ((sum(MidtermScores) / len(MidtermScores)) / 100) * Weights[1]
    weightedPracticum = ((sum(PracticumScores) / len(PracticumScores)) / 100) * Weights[2]
    weightedICA = ((sum(ICAScores) / len(ICAScores)) / 100) * Weights[3]

    weightedAverage = weightedAssignment + weightedMidterm + weightedPracticum + weightedICA
    #print (weightedAverage)
    return weightedAverage

    ## TODO: comment out "raiseNotDefined()" when you start working on this function
    #A0.raiseNotDefined()


## Question 2 - Classes

class node:
    # See Question 2a
    def __init__(self, key, value) -> object:
        self.value = value
        self.key = key
        self.leftChild = None
        self.rightChild = None

    def getChildren(self):
        return [self.leftChild, self.rightChild]
    
    def getKey(self):
        return self.key
    
    def getValue(self):
        return self.value
    
    def assignLeftChild(self, child):
        self.leftChild = child
    
    def assignRightChild(self, child):
        self.rightChild = child

    def inOrderTraversal(self):
        inOrderNodes = []
        if self.leftChild is not None:
            inOrderNodes += self.leftChild.inOrderTraversal()

        inOrderNodes.append(self.getValue())

        if self.rightChild is not None:
            inOrderNodes += self.rightChild.inOrderTraversal()

        return inOrderNodes 

        #A0.raiseNotDefined()

class queue:
    # See Question 2b
    def __init__(self) -> object:
        self.list = []

    def push(self, value):
        self.list.append(value)

    def pop(self):
        if len(self.list) != 0:
            return self.list.pop(0)
        else:
            return None #empty queue return none
    
    def checkSize(self):
        return len(self.list) 
        
    #A0.raiseNotDefined()


## Question 3 - Libraries
def generateMatrix(numRows, numcolumns, minVal, maxVal):
    # See Question 3ai
    ## TODO: Define Function
    arr = np.zeros((numRows, numcolumns), dtype=float)

    for i in range(numRows):
        for j in range(numcolumns):
            arr[i,j] = np.random.randint(minVal,maxVal)

    return arr
    ## TODO: comment out "raiseNotDefined()" when you start working on this function
    #A0.raiseNotDefined()

def multiplyMat(m1, m2):
    # See Question 3a_ii
    ## TODO: Define Function

    # shape tuples
    m1_rows, m1_cols = m1.shape 
    m2_rows, m2_cols = m2.shape

    multarr = np.zeros((m1_rows, m2_cols))

    if m1_cols == m2_rows: #matrix mult flips
        for i in range (m1_rows):
            for j in range(m2_cols):
                for k in range (m1_cols):
                    multarr[i,j] += m1[i,k] * m2[k,j]
        return multarr      
    else:
        print("Incompatible Matrices")
        return None

    ## TODO: comment out "raiseNotDefined()" when you start working on this function
    #A0.raiseNotDefined()

def statsTuple(a, b):
    # See Question 3b
    ## TODO: Define Function
    # shape tuples
    try:
        if len(a) != len(b):
            print("not same length")
            return None

        aSum = sum(a)
        aMean = sum(a)/len(a)
        aMin = min(a)
        aMax = max(a)
        
        bSum = sum(b)
        bMean = sum(b)/len(b)
        bMin = min(b)
        bMax = max(b)

        pearsonCorr, pearsonPValue = scipy.stats.pearsonr(a,b)
        spearmanCorr, spearmanPValue = scipy.stats.spearmanr(a,b)

        return (aSum, aMean, aMin, aMax, bSum, bMean, bMin, bMax, round(pearsonCorr,2), round(spearmanCorr,2))    

    except Exception as e:
        print(f"Error: {e}") # "f" format method to include error messages
        return None

    ## TODO: comment out "raiseNotDefined()" when you start working on this function
    #A0.raiseNotDefined()

def pandas_func(fileName):
    # See Question 3c
    ## TODO: Define Function
    df = pd.read_csv(fileName, delimiter='\t') #read filename into dataframe
    ListOfMeans = [];
    ListOfColumnNames = [];
        

    for column in df:
        if pd.api.types.is_numeric_dtype(df[column]):
            ListOfMeans.append(round(df[column].mean(),2))
        else:
            ListOfColumnNames.append(column)
    
    return ListOfMeans, ListOfColumnNames

    ## TODO: comment out "raiseNotDefined()" when you start working on this function
    #A0.raiseNotDefined()