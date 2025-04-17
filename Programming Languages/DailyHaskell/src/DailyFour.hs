module DailyFour where


-- Q1: zip3Lists --
-- type: [a] -> [b] -> [c] -> [(a,b,c)]
-- parameters: three lists of any type
-- function that zips three lists together into a list of tuples
-- return: list of tuples containing the elements of the three lists
zip3Lists :: [a] -> [b] -> [c] -> [(a,b,c)]
zip3Lists [] [] [] = []
zip3Lists (a:as) (b:bs) (c:cs) = (a,b,c) : zip3Lists as bs cs


-- Q2: unzipTriples --
-- type: [(a,b,c)] -> ([a],[b],[c])
-- parameters: list of tuples containing three elements
-- function that unzips a list of tuples into three lists
-- return: three lists containing the elements of the tuples
unzipTriples :: [(a,b,c)] -> ([a],[b],[c])
unzipTriples [] = ([], [], [])
unzipTriples ((a,b,c) : xs) = 
    let 
        (as, bs, cs) = unzipTriples xs 
    in
        (a:as, b:bs, c:cs)

-- Q3: mergeSorted3 --
-- type: Ord a => [a] -> [a] -> [a] -> [a]
-- parameters: three sorted lists of any type
-- function that merges three sorted lists into one sorted list
-- return: one sorted list containing the elements of the three lists
mergeSorted3 :: Ord a => [a] -> [a] -> [a] -> [a]
mergeSorted3 [] [] [] = []
mergeSorted3 xs [] [] = xs
mergeSorted3 [] ys [] = ys
mergeSorted3 [] [] zs = zs
mergeSorted3 (a:as) (b:bs) (c:cs) =
    if a <= b && a <= c then
        a : mergeSorted3 as (b:bs) (c:cs)
    else if b <= a && b <= c then
        b : mergeSorted3 (a:as) bs (c:cs)
    else
        c : mergeSorted3 (a:as) (b:bs) cs
mergeSorted3 (a:as) (b:bs) [] =
    if a <= b then
        a : mergeSorted3 as (b:bs) []
    else
        b : mergeSorted3 (a:as) bs []
mergeSorted3 (a:as) [] (c:cs) =
    if a <= c then
        a : mergeSorted3 as [] (c:cs)
    else
        c : mergeSorted3 (a:as) [] cs
mergeSorted3 [] (b:bs) (c:cs) =
    if b <= c then
        b : mergeSorted3 [] bs (c:cs)
    else
        c : mergeSorted3 [] (b:bs) cs

    

