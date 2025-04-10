-- TEST
module DailyTwo where

-- Q1: every4th -- 
-- type: list type (same for input and output)
-- parameters: list of elements
-- recursive function that adds every 4th element to new list
-- return: list only consisting of every 4th element of the input list
every4th :: [a] -> [a] 
every4th [] = [] -- if empty list, return empty list
every4th (_:_:_:d:es) = d : every4th es -- skips first three, then adds fourth to list and recursively calls the function
-- every4th (_:_:_:d) = d
every4th (_) = [] 

-- Q2: tupleDotProduct -- 
-- type: Num 
-- parameters: two lists of numbers
-- recursive function that adds terms of products from two lists to create a dot product
-- return: dot product of lists of numbers a and b
tupleDotProduct :: Num a => [a] -> [a] -> a 
tupleDotProduct [] [] = 0 -- if empty, 0
tupleDotProduct (a:as) (b:bs) = a*b + tupleDotProduct as bs
-- tupleDotProduct (a)(b) = a*b

-- Q3: appendToEach -- 
-- type: String 
-- parameters: String, list of Strings
-- recursive function that appends the given string to every string in the list
-- return: list of strings that has appended the string 
appendToEach :: String -> [String] -> [String]
appendToEach _ [] = []
appendToEach string (a:as) = (a ++ string) : appendToEach string as
appendToEach _ [a] = [a]


-- Q4: toSetList -- 
-- type: Eq  
-- parameters: list of items
-- recursive function with helper to remove repeat elements from list
-- return: list with no repeated elements (set)
toSetList :: Eq a => [a] -> [a]
toSetList [] = [] 
toSetList (a:as) = if inList a as == True
    then
        toSetList as
    else 
        a : toSetList as

-- Q4: inList (Helper Function) --
-- type: Eq  
-- parameters: element from list and list
-- recursive function to check if item in list 
-- return: true or false if item is in list
inList :: Eq a => a -> [a] -> Bool
inList _ [] = False
inList item (a:as) = if item == a -- if item is same as current element
    then 
        True    
    else 
        inList item as -- check rest of elements