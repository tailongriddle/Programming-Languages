module DailyEight where


-- Q1 --
-- type: [a] -> [Maybe a]
-- parameters: list of elements
-- function that takes a list and returns a list with the first and last elements swapped
-- return: list with the first and last elements swapped
findSmallest :: (Ord a) => [a] -> Maybe a
findSmallest [] = Nothing
findSmallest [num] = Just num
findSmallest (num:num2:nums) = 
    findSmallest ((if num < num2 then num else num2) : nums)


-- Q2 --
-- type: [Bool] -> Maybe Bool]
-- parameters: list of booleans
-- function that takes a list of booleans and returns True if all elements are True, False otherwise
-- return: True if all elements are True, False otherwise
allTrue :: [Bool] -> Maybe Bool
allTrue [] = Nothing
allTrue [num] = Just num
allTrue (num:nums) = if num == False
    then Just False
    else allTrue nums

-- Q3 --
-- type: [Bool] -> Maybe Bool
-- parameters: list of booleans
-- function that takes a list of booleans and returns number of Nothing, True, and False values
-- return: number of Nothing, True, and False values
countAllVotes :: [Maybe Bool] -> (Integer, Integer, Integer)
countAllVotes [] = (0,0,0)
countAllVotes (Nothing : votes) =
    let (n, t, f) = countAllVotes votes
    in (n + 1, t, f)
countAllVotes (Just True : votes) =
    let (n, t, f) = countAllVotes votes
    in (n, t + 1, f)
countAllVotes (Just False : votes) =
    let (n, t, f) = countAllVotes votes
    in (n, t, f + 1)