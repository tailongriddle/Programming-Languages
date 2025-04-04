# Assignment 2 Starter Code

This assignment has two parts. Be sure to read through all of the assignment document before you start. 
If you are strategic about how you write your Part 1 code, you can reuse a lot of it in Part 2.

**Note:** The experiments in Part 2 can take a while to run. Be sure to give yourself plenty of time.


## Robby's World (Part 2)

In this part, you will implement a genetic algorithm to evolve control strategies for Robby the Robot, as described in Chapter 9 of Complexity: A Guided Tour by
Melanie Mitchell (available in the assignment folder on Canvas), A control strategy will be represented as a string
of characters that code for the following robot actions:

- 0 = MoveNorth
- 1 = MoveSouth
- 2 = MoveEast
- 3 = MoveWest
- 4 = StayPut
- 5 = PickUpCan
- 6 = MoveRandom

Robby’s reward is increased when Robby picks up a soda can, and decreased if Robby hits a wall. The job of your
GA is to evolve a good control strategy that maximizes Robby’s average cumulative reward as it collects empty soda
cans for 200 time steps.

Your GA will maintain a population of genomes representing control strategies. Each genome will be a 243-character
string specifying the action that Robby should take for every possible situation it might find itself in. Robby’s
”situation” will be encoded as a 5-character percept string specifying what Robby currently sees in their immediate
vicinity. For example, the string ’WECWC’ means there is a wall to the north, an empty grid cell to the south, a
soda can to the east, another wall to the west, and a soda can in Robby’s own grid cell.

Each percept string corresponds to a unique code number in the range 0-242, which indicates the (0-based) index
number of the situation, for more details on this check out page 132 in the chapter noted above. We will use mainly
use the percept codes in our problem rather than the strings. (e.g. If the percept code is 240, Robby will perform
the action described by the 240th gene of the genome)

For example, if the genome were all 0’s, in any given situation the Robot would move north.

We will use rank selection (described more in your assignment document), single point crossover, and mutation which will be characterized
as randomly replacing one or more characters in the string.

A list of Robby's World Commands and what they do can be found in the assignment docment 