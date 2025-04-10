import random

# define invalid pairs
invalidPairs = {(1, 1), (1, 5), (2, 4), (3, 6), (4, 2), (4, 4), (5, 1), (5, 5)}

# generates random dice roll
def roll_dice():
    return (random.randint(1, 6), random.randint(1, 6))

def simulate_rolls(num_simulations):
    successNum = 0

    for _ in range(num_simulations):
        red_die_values = set()
        green_die_values = set()
        valid_rolls = True

        for _ in range(6):
            roll = roll_dice()
            if roll in invalidPairs:
                valid_rolls = False
                break
            red_die_values.add(roll[0])
            green_die_values.add(roll[1])

        if valid_rolls and len(red_die_values) == 6 and len(green_die_values) == 6:
            successNum += 1

    return successNum / num_simulations

# run simulation 
num_simulations = 10000
probability = simulate_rolls(num_simulations)
print(f"Estimated probability: {probability:.6f}")