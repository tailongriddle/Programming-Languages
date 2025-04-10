import random

def coin(trials,p):
    
    outcomes = [0,1] # heads [0] or tails [1]
    weights = [p,1-p] # probabilities for heads and tails
    if (p < 0 or p > 1):
        print("IMPOSSIBLE PROBABILITY")
        return (0,0)
    if (p == 0 or p == 1):
        print("GAME WILL CONTINUE FOREVER; NEITHER WINS")
        return (0,0)
    
    AliceWins = 0 # counter for Alice wins
    BobWins = 0 # counter for Bob wins
    for _ in range(trials): # loop for a large trial number
        flip1 = 0 # initialize/reset flip1 to 0
        flip2 = 0 #i initialize/reset flip2 to 0
        while (flip1==flip2): # if flips are same, restart game
            flip1 = random.choices(outcomes,weights,k=1) # first flip
            flip2 = random.choices(outcomes,weights,k=1) # second flip
            
            if flip1[0] == 0 and flip2[0] == 1: # HT, condition Alice wins
                AliceWins += 1
            elif flip1[0] == 1 and flip2[0] == 0: # TH, condition Bob wins
                BobWins += 1
    
    probA = AliceWins/trials # probability Alice wins
    probB = BobWins/trials # probability Bob wins
    return (probA, probB)

# Valid trial
print(coin(100000,0.5))
# Invalid trials
print(coin(100000,-1))
print(coin(100000,2))

# Forever trials
print(coin(100000,0))
print(coin(100000,1))