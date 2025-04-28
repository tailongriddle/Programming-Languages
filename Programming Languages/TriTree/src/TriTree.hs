module TriTree where 

-- TYPE FOR ASSIGNMENT
data TriTree a = Empty | 
                 Leaf a | 
                 Node a a (TriTree a) (TriTree a) (TriTree a) 
                 deriving (Eq,Show)


-- SEARCH FUNCTION
-- type: Ord a => a -> TriTree a -> Bool
-- parameters: value to search for, TriTree
-- function that searches for a value in a TriTree
-- return: True if value is found, False if not
search :: (Ord a) => a -> TriTree a -> Bool
search _ Empty = False -- if empty, return false
search toFind (Leaf value) = if value == toFind -- if leaf, check if value at leaf
        then 
            True
        else 
            False
search toFind (Node value1 value2 left center right) = -- if node, check if value at node 
    if value1 == toFind || value2 == toFind 
        then
            True
        else  -- if value not at node, check three trees
            search toFind left || search toFind center || search toFind right

-- INSERT FUNCTION
-- type: Ord a => a -> TriTree a -> TriTree a
-- parameters: value to insert, TriTree
-- function that inserts a value into a TriTree
-- return: TriTree with value inserted
insert :: (Ord a) => a -> TriTree a -> TriTree a
insert toInsert Empty = Leaf toInsert -- inserting into empty tree
insert toInsert (Leaf value) = if toInsert < value -- inserting into existing leaf
    then
        Node toInsert value Empty Empty Empty
    else
        Node value toInsert Empty Empty Empty
insert toInsert (Node value1 value2 left center right) =  -- inserting into node
 if toInsert < value1
        then 
            Node value1 value2 (insert toInsert left) center right
    else if toInsert > value2
        then 
            Node value1 value2 left center (insert toInsert right)
    else
        Node value1 value2 left (insert toInsert center) right


-- INSERT LIST FUNCTION
-- type: Ord a => [a] -> TriTree a -> TriTree a
-- parameters: list of values to insert, TriTree
-- function that inserts a list of values into a TriTree
-- return: TriTree with values inserted
insertList :: (Ord a) => [a] -> TriTree a -> TriTree a 
insertList [] Empty = Empty
insertList [] tree = tree
insertList items tree = foldr insert tree items

-- IDENTICAL FUNCTION
-- type: Ord a => TriTree a -> TriTree a -> Bool
-- parameters: two TriTrees
-- function that checks if two TriTrees are identical
-- return: True if identical, False if not
identical :: (Ord a) => TriTree a -> TriTree a -> Bool
identical Empty Empty = True
identical _ Empty = False
identical Empty _ = False
identical (Leaf value1) (Node value2 value3 left center right) = False
identical (Node value1 value2 left center right) (Leaf value3) = False
identical (Leaf value1) (Leaf value2) = value1 == value2
identical (Node value1 value2 left1 center1 right1) (Node value3 value4 left2 center2 right2) = 
    value1 == value3 && value2 == value4 && identical left1 left2 && identical center1 center2 && identical right1 right2


-- TREE MAP FUNCTION
-- type: (a -> b) -> TriTree a -> TriTree b
-- parameters: function to apply, TriTree
-- function that applies a function to each value in a TriTree
-- return: TriTree with function applied to each value
treeMap :: (a -> b) -> TriTree a -> TriTree b
treeMap function Empty = Empty
treeMap function (Leaf a) = Leaf (function a)
treeMap function (Node value1 value2 left center right) = Node (function value1) (function value2) (treeMap function left) (treeMap function center) (treeMap function right)


--- TREE FOLD PRE ORDER FUNCTION
-- type: (a -> b -> a) -> a -> TriTree b -> a
-- parameters: function to apply, accumulator, TriTree
-- function that folds a TriTree with values first and then three tritrees using a function and an accumulator
-- return: accumulator with function applied to each value in TriTree
treeFoldPreOrder :: (a -> b -> a) -> a -> TriTree b -> a
treeFoldPreOrder function acc Empty = acc
treeFoldPreOrder function acc (Leaf value) = function acc value
treeFoldPreOrder function acc (Node value1 value2 left center right) = 
    let acc1 = function acc value1
        acc2 = function acc1 value2
        acc3 = treeFoldPreOrder function acc2 left
        acc4 = treeFoldPreOrder function acc3 center
    in treeFoldPreOrder function acc4 right


-- TREE FOLD IN ORDER FUNCTION
-- type: (a -> b -> a) -> a -> TriTree b -> a
-- parameters: function to apply, accumulator, TriTree
-- function that folds a TriTree with left tree first, then value1, then center tree, then value2, and finally right tree using a function and an accumulator
-- return: accumulator with function applied to each value in TriTree
treeFoldInOrder :: (a -> b -> a) -> a -> TriTree b -> a
treeFoldInOrder function acc Empty = acc
treeFoldInOrder function acc (Leaf value) = function acc value
treeFoldInOrder function acc (Node value1 value2 left center right) = 
    let acc1 = treeFoldInOrder function acc left
        acc2 = function acc1 value1
        acc3 = treeFoldInOrder function acc2 center
        acc4 = function acc3 value2
    in treeFoldPreOrder function acc4 right




treeFoldPostOrder :: (a -> b -> a) -> a -> TriTree b -> a
treeFoldPostOrder function acc Empty = acc
treeFoldPostOrder function acc (Leaf value) = function acc value
treeFoldPostOrder function acc (Node value1 value2 left center right) = 
    let acc1 = treeFoldPostOrder function acc left
        acc2 = treeFoldPostOrder function acc1 center
        acc3 = treeFoldPostOrder function acc2 right
        acc4 = function acc3 value1
    in function acc4 value2


