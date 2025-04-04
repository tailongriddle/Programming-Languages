



x = "SUPPLY"
y = "DEMAND"
 
def merge(x, y, toAdd=""):
    if not x:
        print(toAdd + y)
        return [toAdd + y]
    if not y:
        print(toAdd + x)
        return [toAdd + x]
    
    
    return merge(x[1:], y, toAdd + x[0]) + merge(x, y[1:], toAdd + y[0])

x = "STRING"
y = "SWORDS"
result = merge(x, y)
print(result)
print(len(result))