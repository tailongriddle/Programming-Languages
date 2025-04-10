import sys
import subprocess

import matplotlib.pyplot as plt
import numpy as np

plt.rc('font',**{'family':'serif','serif':['Times']}) #change font

## ratio calculator
def ratio(mAcc,fAcc):

    totalAcc = mAcc+fAcc
    maleRatio = float(mAcc/totalAcc)
    femaleRatio = float(fAcc/totalAcc)

    return (maleRatio,femaleRatio)

## DEFINE RATIOS ##
w = 0.3

## Astronomy
mA, fA = ratio(512, 89)

## Biology
mB, fB = ratio(22, 24)

## Law
mL, fL = ratio(138, 131)

## Physics
mP, fP = ratio(353, 17)

## Psychology
mPS, fPS = ratio(120, 202)

## Sociology
mS, fS = ratio(53, 94)

## GRAPH ##

x = ["Astronomy","Biology","Law","Physics","Psychology","Sociology"]
male = [mA, mB, mL, mP, mPS, mS] # male acceptance ratios
female = [fA, fB, fL, fP, fPS, fS] # female acceptance ratios


x_axis = np.arange(len(x)) # creates range of values

#as
plt.bar(x_axis, male, color="#60c47b", width=w) 
plt.bar(x_axis + w, female, color="pink", width=w)

plt.xticks(x_axis, x, fontsize=8)
plt.xlabel("Department", fontsize=10)
plt.ylabel("Ratio of Accepted Students", fontsize=10)

# creates legend and places in upper right
plt.gca().legend(["male","female"],loc='upper right',title="Gender")

# title
plt.title("How do Different Departments Compare for the Gender Makeup of Total Acceptances?", fontsize=12, weight="bold")

# show the graph
plt.show()
