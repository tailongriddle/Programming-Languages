module DailySix where

-- Q1 --
-- type: Int, [String]
-- parameters: an integer and a list of strings
-- function that takes an integer and a list of strings and returns a list of strings that are shorter than or equal to the given integer
-- return: list of strings that are shorter than or equal to the given integer
shorterThan :: Int -> [String] -> [String]
shorterThan _ [] = []
shorterThan num list = filter (\x -> length x <= num) list 

-- Q2 --
-- type: Integer, [Integer]
-- parameters: an integer and a list of integers
-- function that takes an integer and a list of integers and returns a list of integers that are not multiples of the given integer
-- return: list of integers that are not multiples of the given integer
removeMultiples :: Integer -> [Integer] -> [Integer]
removeMultiples _ [] = []
removeMultiples num list = filter (\x -> x `mod` num /= 0) list

-- Q3 --
-- type: [Maybe a]
-- parameters: a list of Maybe values
-- function that takes a list of Maybe values and returns a list of Just values
-- return: list of Just values
onlyJust :: Eq a => [Maybe a] -> [Maybe a]
onlyJust [] = []
onlyJust list = filter (\x -> x /= Nothing) list 
