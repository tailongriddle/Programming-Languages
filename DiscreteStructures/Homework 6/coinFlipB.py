import random

def coin(trials):  
    AliceWins = 0 # counter for Alice wins
    BobWins = 0 # counter for Bob wins
    
    for _ in range(trials): # loop for a large trial number
        flipPattern = []# initialize/reset flip pattern to 0
        GameOver = False
        while (GameOver == False): # if flips are same, restart game
            flipPattern.append(random.randint(0,1))
            if len(flipPattern) > 3:
                flipPattern.pop(0)          
            if flipPattern == [0,0,1]:
                AliceWins += 1
                GameOver = True
            elif flipPattern == [0,1,1]:
                 BobWins += 1
                 GameOver = True          
    
    probA = AliceWins/trials # probability Alice wins
    probB = BobWins/trials # probability Bob wins
    return (probA, probB)

# Valid trial
print(coin(1000))