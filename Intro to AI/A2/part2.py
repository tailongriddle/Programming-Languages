import robby
import numpy as np
from utils import *
import random
POSSIBLE_ACTIONS = ["MoveNorth", "MoveSouth", "MoveEast", "MoveWest", "StayPut", "PickUpCan", "MoveRandom"]
rw = robby.World(10, 10)
rw.graphicsOff()

def sortByFitness(genomes):
    tuples = [(fitness(g), g) for g in genomes]
    tuples.sort()
    sortedFitnessValues = [f for (f, g) in tuples]
    sortedGenomes = [g for (f, g) in tuples]
    return sortedGenomes, sortedFitnessValues


def randomGenome(length):
    """
    :param length:
    :return: string, random integers between 0 and 6 inclusive
    """

    """Your Code Here"""
    
    bitString = "" # initialize bitString
    for _ in range(length): # for each in length...
        bitString += str(np.random.randint(7)) # generate 0 or 1
    return bitString # return bitString



def makePopulation(size, length):
    """
    :param size - of population:
    :param length - of genome
    :return: list of length size containing genomes of length length
    """


    """Your Code Here"""
    population = [] # initialize population length
    for _ in range(size): # for each in size...
        population.append(randomGenome(length)) #append new random genome to population
        
    return population # return population

def fitness(genome, steps=200, init=0.50):
    """

    :param genome: to test
    :param steps: number of steps in the cleaning session
    :param init: amount of cans
    :return:
    """
    if type(genome) is not str or len(genome) != 243:
        raise Exception("strategy is not a string of length 243")
    for char in genome:
        if char not in "0123456":
            raise Exception("strategy contains a bad character: '%s'" % char)
    if type(steps) is not int or steps < 1:
        raise Exception("steps must be an integer > 0")
    if type(init) is str:
        # init is a config file
        rw.load(init)
    elif type(init) in [int, float] and 0 <= init <= 1:
        # init is a can density
        rw.goto(0, 0)
        rw.distributeCans(init)
    else:
        raise Exception("invalid initial configuration")

    #()

def fitness(genome):
    """
    :param population:
    :return: a pair of values: the average fitness of the population as a whole and the fitness of the best individual
    in the population.
    """
    actions = ['MoveNorth', 'MoveSouth', 'MoveEast', 'MoveWest', 'StayPut', 'PickUpCan', 'MoveRandom']
    total = 0 # initialize total
    for _ in range(25): # for each in rnage 25...
        rw = robby.World(10, 10) # initialize world
        rw.graphicsOff()  #`turn off graphics`
        for _ in range(200):  # for each in range 200...
            percept_code = rw.getPerceptCode() # get percept code
            if percept_code < len(genome):
                action = actions[int(genome[percept_code])] # get action from genome
                total += rw.performAction(action) # perform action and add to total
    return total / 25 # return average
    

def crossover(genome1, genome2):
    """
    :param genome1:
    :param genome2:
    :return: two new genomes produced by crossing over the given genomes at a random crossover point.
    """
    crossover_point = np.random.randint(1, len(genome1))
    
    new_genome1 = ""
    new_genome2 = ""
    
    for bit in genome2[0:crossover_point]: # for bit in genome2 from 0 to crossover_point...
        new_genome1 += bit # add bit to new_genome1

    for bit in genome1[crossover_point:len(genome1)]: # for bit in genome1 from crossover_point to length...
        new_genome1 += bit # add bit to new_genome1
    
    for bit in genome1[0:crossover_point]: # for bit in genome1 from 0 to crossover_point...
        new_genome2 += bit # add bit to new_genome2
        
    for bit in genome2[crossover_point:len(genome2)]: # for bit in genome2 from crossover_point to length...
        new_genome2 += bit # add bit to new_genome2

    # print("TEST: ")
    # print("CROSS:", crossover_point)
    # print("GENOME1:", new_genome1)
    # print("GENOME2:", new_genome2)


    return new_genome1, new_genome2



def mutate(genome, mutationRate):
    """
    :param genome:
    :param mutationRate:
    :return: a new mutated version of the given genome.
    """
    new_genome = "" # initialize new_genome
    randomIndexList = [] # initialize list of random indexes
    available_indexes = [] # initialize list of available indexes
    
    i = 0 # set i to 0
    while i < len(genome): # while i is less than length of genome string...
        available_indexes.append(i) # append i to list of available indexes
        i+=1 # increment i
        
    num_mutations = int(mutationRate * len(genome)) # calculate the number of mutations based on the mutation rate
    
    for _ in range(num_mutations): # for each mutation...
        randomIndex = random.choice(available_indexes) # set randomindex to a random index in list of available indexes
        available_indexes.remove(randomIndex) # remove that index from available indexes
        randomIndexList.append(randomIndex) # add random index to list of random indexes
        
    for index, bit in enumerate(genome): # for each bit in the genome...
        if index in randomIndexList: # if the index is one of the chosen indexes, flip the bit
            if bit == "1": # if the bit is 1...
                new_genome += "0" # change to 0
            else:
                new_genome += "1" # change to 1
        else: # if not a random chosen index...
            new_genome += bit # add original bit to new_genome
        
    return new_genome # return mutated genome

def selectPair(population):
    """

    :param population:
    :return: two genomes from the given population using fitness-proportionate selection.
    This function should use RankSelection,
    """
    fitnessList = [fitness(genome) for genome in population]  # calculate fitness for each genome
    sorted_indices = np.argsort(fitnessList)  # sort indices of the fitness list
    
    ranks = np.arange(1, len(population) + 1)  # ranks of the genomes
    rankWeights = ranks / np.sum(ranks)  # normalized rank weights

    weightedChoice1 = np.random.choice(population, p=rankWeights)  # select first genome
    weightedChoice2 = np.random.choice(population, p=rankWeights)  # select second genome

    return weightedChoice1, weightedChoice2


def runGA(populationSize, crossoverRate, mutationRate, logFile=""):
    """

    :param populationSize: :param crossoverRate: :param mutationRate: :param logFile: :return: xt file in which to
    store the data generated by the GA, for plotting purposes. When the GA terminates, this function should return
    the generation at which the string of all ones was found.is the main GA program, which takes the population size,
    crossover rate (pc), and mutation rate (pm) as parameters. The optional logFile parameter is a string specifying
    the name of a te
    """
    rw.graphicsOff()

    genomeLength = 20  # set genome length
    generation = 1  # initialize generation
    population = makePopulation(populationSize, genomeLength)  # create population of random genomes
    
    print("Population size: ", populationSize)
    print("Genome length: ", genomeLength)

    with open(logFile, "w") as log:
        while generation <= 300:  # while generation is less than or equal to 300
            fitness_values = [fitness(genome) for genome in population]  # calculate fitness for each genome
            averageFitness = sum(fitness_values) / populationSize  # calculate average fitness
            bestFitness = max(fitness_values)  # calculate best fitness
            bestIndex = fitness_values.index(bestFitness)  # get index of the best fitness
            bestStrategy = population[bestIndex]  # find best strategy

            # Log the results every 10 generations
            if generation % 10 == 0:
                log.write(f"{generation} {averageFitness:.2f} {bestFitness:.2f} {' '.join(map(str, bestStrategy))}\n")
                
            print(f"Generation {generation}: average fitness {averageFitness:.2f}, best fitness {bestFitness:.2f}")

            if bestFitness == genomeLength:  # if best fitness is the max 
                print(f"Best genome in generation: {generation}")
                return generation  # return that genome
            
            new_population = []
            while len(new_population) < populationSize:  # fill new population until it reaches pop size
                genome1, genome2 = selectPair(population)  # select pair for crossover
                if np.random.random() < crossoverRate:  # if random number is less than crossover rate...
                    new_genome1, new_genome2 = crossover(genome1, genome2)  # crossover
                else:
                    new_genome1, new_genome2 = genome1, genome2  # no crossover
                new_genome1 = mutate(new_genome1, mutationRate)  # mutate
                new_genome2 = mutate(new_genome2, mutationRate)  # mutate
                
                new_population.append(new_genome1)  # add new_genome1 to new_population
                new_population.append(new_genome2)  # add new_genome2 to new_population

            population = new_population[:populationSize]  # ensure population size remains constant
            generation += 1  # add one to generation

    return None  # if no optimal genome found within 300 generations
        
        


def test_FitnessFunction():
    f = fitness(rw.strategyM)
    print("Fitness for StrategyM : {0}".format(f))



#test_FitnessFunction()

runGA(100, 1.0, 0.05, "runGA.log")