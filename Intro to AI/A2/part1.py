import GAinspector
import numpy as np
from utils import *

def randomGenome(length):
    """
    :param length:
    :return: string, random binary digit
    """
    """Your Code Here"""

    bitString = "" # initialize bitString
    for _ in range(length): # for each in length...
        bitString += str(np.random.randint(2)) # generate 0 or 1
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
    


def fitness(genome):
    """
    :param genome: 
    :return: the fitness value of a genome
    """
    fitness = 0 # initialize fitness
    for bit in genome: # for each bit in the genome string...
        if bit == "1": # if the bit is the string "1"
            fitness += 1 # add one to fitness
            
    return fitness # return fitness


def evaluateFitness(population):
    """
    :param population: 
    :return: a pair of values: the average fitness of the population as a whole and the fitness of the best individual in the population.
    """
    average = 0 # initialize average
    best = 0 # initialize best
    for genome in population: # for each genome in the population...
        average += fitness(genome) # add to total
        if fitness(genome) > best: # if fitness of current genome > best...
            best = fitness(genome) # set best to fitness of current genome
    average = average / len(population) # create average by dividing total by population length
    
    return average, best # return average and best


def crossover(genome1, genome2):
    """
    :param genome1:
    :param genome2:
    :return: two new genomes produced by crossing over the given genomes at a random crossover point.
    """
    # assume genomes are same length?
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
    This function should use weightedChoice, which is available in the Utils File, as a helper function.
    """
    fitness_list = [] # initialize list of fitnesses
    the_population = population.copy() # initialize population
    for genome in the_population: # for each genome in the population...
        fitness_list.append(fitness(genome)) # add fitness of genome
    
    weightedChoice1 = weightedChoice(the_population, fitness_list) # find genome with best fitness
    weightedChoice2 = weightedChoice(the_population, fitness_list) # find second best choice

    return weightedChoice1, weightedChoice2

def runGA(populationSize, crossoverRate, mutationRate, logFile=""):
    """

    :param populationSize: :param crossoverRate: :param mutationRate: :param logFile: :return: xt file in which to
    store the data generated by the GA, for plotting purposes. When the GA terminates, this function should return
    the generation at which the string of all ones was found.is the main GA program, which takes the population size,
    crossover rate (pc), and mutation rate (pm) as parameters. The optional logFile parameter is a string specifying
    the name of a te
    """
    genomeLength = 20 # set genome length
    generation = 1 # initialize generation
    population = makePopulation(populationSize, genomeLength) # create population of random genomes
    
    print("Population size: ", populationSize)
    print("Genome length: ", genomeLength)

    with open(logFile, "w") as f:
        while generation <= 50: # while generation is less than 51
            averageFitness, bestFitness = evaluateFitness(population) # evaluate population
            print(f"Generation {generation}: average fitness {averageFitness:.2f}, best fitness {bestFitness:.2f}")
            f.write(f"{generation} {averageFitness:.2f} {bestFitness:.2f}\n")

            if bestFitness == 20: # if best fitness is 20...
                print(generation) # print generation
                return generation # return that genome
            
            new_population = []
            for _ in range(populationSize // 2): # for each in population size divided by 2...
                genome1, genome2 = selectPair(population) # select pair for crossover
                if np.random.random() < crossoverRate:  # if random number is less than crossover rate...
                    new_genome1, new_genome2 = crossover(genome1, genome2) # crossover
                else:
                    new_genome1, new_genome2 = genome1, genome2 # no crossover
                new_genome1 = mutate(new_genome1, mutationRate) # mutate
                new_genome2 = mutate(new_genome2, mutationRate) # mutate
                
                new_population.append(new_genome1) # add new_genome1 to new_population
                new_population.append(new_genome2) # add new_genome2 to new_population
            
            population = new_population
            generation += 1 # add one to generation

    return None
   
        
        





if __name__ == '__main__':
    #Testing Code
    print("Test Suite")
    GAinspector.inspectFunction(randomGenome)
    GAinspector.inspectFunction(makePopulation)
    GAinspector.inspectFunction(fitness)
    GAinspector.inspectFunction(evaluateFitness)
    
    GAinspector.inspectFunction(crossover)
    GAinspector.inspectFunction(mutate)
    GAinspector.inspectFunction(selectPair)

    runGA(100, 0.7, 0.001, "run1.txt")