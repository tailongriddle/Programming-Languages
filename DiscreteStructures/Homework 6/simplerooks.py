import random 

def die(invalid, trials):
    everyValue = 0
    validTrials = 0
    
    for _ in range(trials):
        numsRed = []
        numsGreen = [] 
        
        for i in range(6):
            numsRed.append(random.randint(1,6)) # roll red die
            numsGreen.append(random.randint(1,6)) # roll green die
        
        valid = True
        for i in range(6):
            if (numsRed[i], numsGreen[i]) in invalid: #if an ordered pair is in invalid...
                valid = False #...it is invalid
                break
        if valid and sorted(numsRed) == [1, 2, 3, 4, 5, 6] and sorted(numsGreen) == [1, 2, 3, 4, 5, 6]:
            everyValue += 1
        elif valid:
            validTrials += 1
    
    prob = "{:.8f}".format(everyValue / validTrials)
    return prob

invalid = [(1, 1), (1, 5), (2, 4), (3, 6), (4, 2), (4, 4), (5, 1), (5, 5)]

print(die(invalid, 1000000))
