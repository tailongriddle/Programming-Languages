module DailySeven where

-- Q1: findLongest --
-- type: [String] -> String
-- parameters: list of strings
-- function that takes a list of strings and returns the longest string in the list
-- return: longest string in the list
findLongest :: [String] -> String
findLongest [] = ""
findLongest (word : words) = foldl longest word words
  where
    longest a b = if length a >= length b then a else b

-- Q2: anyLarger --
-- type: Integer -> [Integer] -> Bool
-- parameters: integer to check, list of integers
-- function that takes an integer and a list of integers and returns True if any integer in the list is larger than the given integer
-- return: True if any integer in the list is larger than the given integer, False otherwise
anyLarger :: Integer -> [Integer] -> Bool
anyLarger _ [] = False
anyLarger toCheck nums = foldl (\acc x -> acc || x > toCheck) False nums
 
-- Q3: allnames --
-- type: [(String, String)] -> String
-- parameters: list of tuples containing first and last names
-- function that takes a list of tuples containing first and last names and returns a string with all names concatenated
-- return: string with all names concatenated   
allNames :: [(String, String)] -> String
allNames [] = ""
allNames names = foldl (\acc (first, last) -> acc ++ first ++ " " ++ last ++ " ") "" names
