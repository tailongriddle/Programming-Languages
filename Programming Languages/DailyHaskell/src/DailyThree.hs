module DailyThree where


-- Q1: removeAllExcept --
-- type: Eq a => a -> [a] -> [a]
-- parameters: character to find, list of characters
-- function that removes all characters from the list except the given character
-- return: list of characters that only contains the given character
removeAllExcept :: Eq a => a -> [a] -> [a] 
removeAllExcept _ [] = [] -- if empty list, return empty list
removeAllExcept given (a:as) = if given == a
    then 
        a : removeAllExcept given as
    else
        removeAllExcept given as



-- Q2: removeChar --
-- type: Eq a => a -> [a] -> [a]
-- parameters: element to find, list of characters
-- function that counts all instances of the given character in the list
-- return: number of instances of that element
countOccurrences :: Eq a => a -> [a] -> Int
countOccurrences _ [] = 0 -- if empty list, return 0
countOccurrences given (a:as) = if given == a
    then 
        1 + countOccurrences given as
    else
        countOccurrences given as

-- Q3: substitute --
-- type: Eq a => a -> a -> [a] -> [a]
-- parameters: element to find, element used to replace, list of elements
-- function that replaces all instances of the given element in the list with another given element
-- return: list of elements with the given element replaced
substitute :: Eq a => a -> a -> [a] -> [a]
substitute _ _ [] = [] -- if empty list, return empty list
substitute toRemove replacement (a:as) = if a == toRemove
    then
        replacement : substitute toRemove replacement as
    else
        a : substitute toRemove replacement as
