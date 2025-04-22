module DailyFive where 

import Data.Char


-- Q1 --
-- type: [(Integer,Integer)], [Integer]
-- parameters: list of pairs of integers
-- function that multiplies each pair of integers in the list and returns a list of the products
-- return: result of multiplying each pair of integers in the list (integer list)
multPairs :: [(Integer,Integer)] -> [Integer]
multPairs [] = []
multPairs list = map (\(x,y) -> x * y) list

-- Q2 --
-- type: [Integer], [(Integer,Integer)]
-- parameters: list of integers
-- function that takes a list of integers and returns a list of tuples containing the integer and its square
-- return: list of tuples containing the integer and its square
squareList :: [Integer] -> [(Integer,Integer)]
squareList [] = []
squareList list = map (\ x -> (x, x * x)) list

-- Q3 --
-- type: [String], [Bool]
-- parameters: list of strings
-- function that checks if the first character of each string in the list is lowercase
-- return: list of booleans indicating if the first character of each string is lowercase
findLowercase :: [String] -> [Bool]
findLowercase [] = []
findLowercase list = map (\x -> isLower (head x)) list