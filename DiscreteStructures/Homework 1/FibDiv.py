import math



def FibonacciIndex(number):
    term1 = 0
    term2 = 1
    sum = 1
    index = 1
    
    if number == 0:
        return 0, 0
    
    if number == 1:
        return 1, 1
    
    while (sum % number != 0):
        sum = term1 + term2
        term1 = term2
        term2 = sum
        index = index + 1
    
    return sum, index


## main 

print(FibonacciIndex(8))
print(FibonacciIndex(9))
print(FibonacciIndex(10))
print(FibonacciIndex(100))
print(FibonacciIndex(1000))


    