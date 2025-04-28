module TriTreeSpec where

import Test.Hspec
import TriTree

main :: IO ()
main = hspec spec

spec :: Spec
spec = do
  describe "search" $ do -- search -- 
    context "search Empty" $ --  EMPTY TEST
      it "should be False" $
        (search 0 (Empty :: TriTree Int)) `shouldBe` False
  
    context "search 1 Leaf 1" $ --  SEARCH LEAF (TRUE)
      it "should be True" $
        (search 1 (Leaf 1 :: TriTree Int)) `shouldBe` True
  
    context "search 1 Leaf 2" $ --  SEARCH LEAF (FALSE)
      it "should be False" $
        (search 1 (Leaf 2)) `shouldBe` False
   
    context "search 1 Node 2 1 Empty Empty Empty" $ --  SEARCH NODE AT NODE (TRUE)
      it "should be True" $
        (search 1 (Node 2 1 Empty Empty Empty)) `shouldBe` True
   
    context "search 1 Node 2 2 Empty Empty Empty" $ --  SEARCH NODE AT NODE (FALSE)
      it "should be False" $
        (search 1 (Node 2 2 Empty Empty Empty)) `shouldBe` False
   
    context "search 1 Node 2 2 (TriTree (Leaf 1)) Empty Empty" $ --  SEARCH NODE AT LEFT TREE (TRUE)
      it "should be True" $
        (search 1 (Node 2 2 (Leaf 1) Empty Empty)) `shouldBe` True
   
    context "search 1 Node 2 2 (TriTree (Leaf 3)) Empty Empty" $ --  SEARCH NODE AT LEFT TREE (FALSE)
      it "should be False" $
        (search 1 (Node 2 2 (Leaf 3) Empty Empty)) `shouldBe` False
   
    context "search 1 Node 2 2 Empty (TriTree (Leaf 1)) Empty" $ --  SEARCH NODE AT CENTER TREE (TRUE)
      it "should be True" $
        (search 1 (Node 2 2 Empty (Leaf 1) Empty)) `shouldBe` True
   
    context "search 1 Node 2 2 Empty (TriTree (Leaf 3)) Empty" $ --  SEARCH NODE AT CENTER TREE (FALSE)
      it "should be False" $
        (search 1 (Node 2 2 Empty (Leaf 3) Empty)) `shouldBe` False
   
    context "search 1 Node 2 2 Empty Empty (TriTree (Leaf 1))" $ --  SEARCH NODE AT RIGHT TREE (TRUE)
      it "should be True" $
        (search 1 (Node 2 2 Empty Empty (Leaf 1))) `shouldBe` True
   
    context "search 1 Node 2 2 Empty Empty (TriTree (Leaf 3))" $ --  SEARCH NODE AT RIGHT TREE (FALSE)
      it "should be False" $
        (search 1 (Node 2 2 Empty Empty (Leaf 3))) `shouldBe` False


  describe "insert" $ do -- insert -- 
    context "insert 1 Empty" $ --  EMPTY TEST
      it "should be Leaf 1" $
        (insert 1 (Empty :: TriTree Int)) `shouldBe` (Leaf 1 :: TriTree Int)

    context "insert 1 Leaf 2" $ -- INSERT INTO LEAF (LEFT)
        it "should be Node 1 2 Empty Empty Empty" $
            (insert 1 (Leaf 2)) `shouldBe` Node 1 2 Empty Empty Empty

    context "insert 3 Leaf 2" $ -- INSERT INTO LEAF (RIGHT)
      it "should be Node 2 3 Empty Empty Empty" $
        (insert 3 (Leaf 2)) `shouldBe` Node 2 3 Empty Empty Empty

    context "insert 3 Node 2 5 Empty Empty Empty" $ -- INSERT INTO CENTER
      it "should be Node 2 5 Empty (Leaf 3) Empty" $
        (insert 3 (Node 2 5 Empty Empty Empty)) `shouldBe` Node 2 5 Empty (Leaf 3) Empty

    context "insert 1 Node 2 5 Empty Empty Empty" $ -- INSERT INTO LEFT
      it "should be Node 2 5 (Leaf 1) Empty Empty" $
        (insert 1 (Node 2 5 Empty Empty Empty)) `shouldBe` Node 2 5 (Leaf 1) Empty Empty

    context "insert 6 Node 2 5 Empty Empty Empty" $ -- INSERT INTO RIGHT
      it "should be Node 2 5 Empty Empty (Leaf 6)" $
        (insert 6 (Node 2 5 Empty Empty Empty)) `shouldBe` Node 2 5 Empty Empty (Leaf 6)

  describe "insertList" $ do -- insertList --
    context "insertList [] Empty" $ -- INSERT EMPTY LIST INTO EMPTY TREE
      it "should be Empty" $
        (insertList ([] :: [Int]) (Empty :: TriTree Int)) `shouldBe` (Empty :: TriTree Int)

    context "insertList [1] Empty" $ -- INSERT SINGLE ELEMENT INTO EMPTY TREE
      it "should be Leaf 1" $
        (insertList [1] Empty) `shouldBe` Leaf 1

    context "insertList [1, 2] Empty" $ -- INSERT TWO ELEMENTS INTO EMPTY TREE
      it "should be Node 1 2 Empty Empty Empty" $
        (insertList [1, 2] Empty) `shouldBe` Node 1 2 Empty Empty Empty

    context "insertList [2, 1] Empty" $ -- INSERT TWO ELEMENTS IN REVERSE ORDER
      it "should be Node 1 2 Empty Empty Empty" $
        (insertList [2, 1] Empty) `shouldBe` Node 1 2 Empty Empty Empty


  describe "identical" $ do -- identical --
    context "identical Empty Empty" $ -- BOTH TREES EMPTY
      it "should be True" $
        (identical (Empty :: TriTree Int) (Empty :: TriTree Int)) `shouldBe` True

    context "identical Empty (Leaf 1)" $ -- ONE TREE EMPTY, ONE LEAF
      it "should be False" $
        (identical Empty (Leaf 1)) `shouldBe` False

    context "identical (Leaf 1) Empty" $ -- ONE TREE EMPTY, ONE LEAF
      it "should be False" $
        (identical (Leaf 1) Empty) `shouldBe` False

    context "identical (Leaf 1) (Leaf 1)" $ -- BOTH TREES SINGLE IDENTICAL LEAF
      it "should be True" $
        (identical (Leaf 1) (Leaf 1)) `shouldBe` True

    context "identical (Leaf 1) (Leaf 2)" $ -- BOTH TREES SINGLE DIFFERENT LEAF
      it "should be False" $
        (identical (Leaf 1) (Leaf 2)) `shouldBe` False

    context "identical (Leaf 1) (Node 1 2 Empty Empty Empty)" $ -- LEAF VS NODE
      it "should be False" $
        (identical (Leaf 1) (Node 1 2 Empty Empty Empty)) `shouldBe` False

    context "identical (Node 1 2 Empty Empty Empty) (Leaf 1)" $ -- NODE VS LEAF
      it "should be False" $
        (identical (Node 1 2 Empty Empty Empty) (Leaf 1)) `shouldBe` False

    context "identical (Node 1 2 Empty Empty Empty) (Node 1 2 Empty Empty Empty)" $ -- IDENTICAL NODES
      it "should be True" $
        (identical (Node 1 2 Empty Empty Empty) (Node 1 2 Empty Empty Empty)) `shouldBe` True

    context "identical (Node 1 2 Empty Empty Empty) (Node 1 3 Empty Empty Empty)" $ -- DIFFERENT NODES
      it "should be False" $
        (identical (Node 1 2 Empty Empty Empty) (Node 1 3 Empty Empty Empty)) `shouldBe` False

    context "identical complex trees" $ -- COMPLEX IDENTICAL TREES
      it "should be True" $
        (identical 
          (Node 1 2 (Leaf 3) Empty (Leaf 4)) 
          (Node 1 2 (Leaf 3) Empty (Leaf 4))) `shouldBe` True

    context "identical complex trees with differences" $ -- COMPLEX DIFFERENT TREES
      it "should be False" $
        (identical 
          (Node 1 2 (Leaf 3) Empty (Leaf 4)) 
          (Node 1 2 (Leaf 5) Empty (Leaf 4))) `shouldBe` False

  describe "treeMap" $ do -- treeMap --
    context "treeMap (+1) Empty" $ -- MAP FUNCTION ON EMPTY TREE
      it "should be Empty" $
        (treeMap (+1) (Empty :: TriTree Int)) `shouldBe` (Empty :: TriTree Int)

    context "treeMap (+1) (Leaf 1)" $ -- MAP FUNCTION ON SINGLE LEAF
      it "should be Leaf 2" $
        (treeMap (+1) (Leaf 1)) `shouldBe` Leaf 2

    context "treeMap (*2) (Node 1 2 Empty Empty Empty)" $ -- MAP FUNCTION ON SIMPLE NODE
      it "should double the values in the Node" $
        (treeMap (*2) (Node 1 2 Empty Empty Empty)) `shouldBe` Node 2 4 Empty Empty Empty

    context "treeMap show (Leaf 1)" $ -- MAP FUNCTION TO CONVERT LEAF VALUE TO STRING
      it "should be Leaf \"1\"" $
        (treeMap show (Leaf 1)) `shouldBe` Leaf "1"

    context "treeMap (*3) complex tree" $ -- MAP FUNCTION ON COMPLEX TREE
      it "should triple all values in the tree" $
        (treeMap (*3) (Node 1 2 (Leaf 3) Empty (Leaf 4))) `shouldBe` Node 3 6 (Leaf 9) Empty (Leaf 12)

    context "treeMap length complex tree" $ -- MAP FUNCTION TO APPLY LENGTH FUNCTION
      it "should map the length of strings in the tree" $
        (treeMap length (Node ("a" :: String) ("abc" :: String) (Leaf ("hello" :: String)) Empty (Leaf ("world" :: String)))) `shouldBe` Node 1 3 (Leaf 5) Empty (Leaf 5)

  describe "treeFoldPreOrder" $ do -- treeFoldPreOrder --
    context "treeFoldPreOrder (+) 0 Empty" $ -- FOLD ON EMPTY TREE
      it "should be 0" $
        (treeFoldPreOrder (+) 0 (Empty :: TriTree Int)) `shouldBe` 0

    context "treeFoldPreOrder (*) 1 (Leaf 2)" $ -- FOLD ON SINGLE LEAF
      it "should be 2" $
        (treeFoldPreOrder (*) 1 (Leaf 2)) `shouldBe` 2

    context "treeFoldPreOrder (+) 0 (Node 1 2 Empty Empty Empty)" $ -- FOLD ON SIMPLE NODE
      it "should sum the values in the Node" $
        (treeFoldPreOrder (+) 0 (Node 1 2 Empty Empty Empty)) `shouldBe` 3

    context "treeFoldPreOrder (*) 1 (Node 2 3 (Leaf 4) Empty (Leaf 5))" $ -- FOLD ON COMPLEX TREE
      it "should multiply all values in the tree" $
        (treeFoldPreOrder (*) 1 (Node 2 3 (Leaf 4) Empty (Leaf 5))) `shouldBe` 120

    context "treeFoldPreOrder (^) 2 (Node 3 2 (Leaf 2) Empty (Leaf 1))" $ -- FOLD WITH EXPONENTIAL FUNCTION
      it "should compute the result of folding with exponentiation" $
        (treeFoldPreOrder (^) 2 (Node 3 2 (Leaf 2) Empty (Leaf 1))) `shouldBe` 4096

    context "treeFoldPreOrder (++) \"\" (Node \"a\" \"b\" (Leaf \"c\") Empty (Leaf \"d\"))" $ -- FOLD WITH STRING CONCATENATION
      it "should concatenate all strings in the tree" $
        (treeFoldPreOrder (++) "" (Node "a" "b" (Leaf "c") Empty (Leaf "d"))) `shouldBe` "abcd"



  describe "treeFoldInOrder" $ do -- treeFoldInOrder --
    context "treeFoldInOrder (+) 0 Empty" $ -- FOLD ON EMPTY TREE
      it "should be 0" $
        (treeFoldInOrder (+) 0 (Empty :: TriTree Int)) `shouldBe` 0

    context "treeFoldInOrder (*) 1 (Leaf 2)" $ -- FOLD ON SINGLE LEAF
      it "should be 2" $
        (treeFoldInOrder (*) 1 (Leaf 2)) `shouldBe` 2

    context "treeFoldInOrder (+) 0 (Node 1 2 Empty Empty Empty)" $ -- FOLD ON SIMPLE NODE
      it "should sum the values in the Node in in-order" $
        (treeFoldInOrder (+) 0 (Node 1 2 Empty Empty Empty)) `shouldBe` 3

    context "treeFoldInOrder (*) 1 (Node 2 3 (Leaf 4) Empty (Leaf 5))" $ -- FOLD ON COMPLEX TREE
      it "should multiply all values in the tree in in-order" $
        (treeFoldInOrder (*) 1 (Node 2 3 (Leaf 4) Empty (Leaf 5))) `shouldBe` 120

    context "treeFoldInOrder (^) 2 (Node 3 2 (Leaf 2) Empty (Leaf 1))" $ -- FOLD WITH EXPONENTIAL FUNCTION
      it "should compute the result of folding with exponentiation in in-order" $
        (treeFoldInOrder (^) 2 (Node 3 2 (Leaf 2) Empty (Leaf 1))) `shouldBe` 4096

    context "treeFoldInOrder (++) \"\" (Node \"a\" \"b\" (Leaf \"c\") Empty (Leaf \"d\"))" $ -- FOLD WITH STRING CONCATENATION
      it "should concatenate all strings in the tree in in-order" $
        (treeFoldInOrder (++) "" (Node "a" "b" (Leaf "c") Empty (Leaf "d"))) `shouldBe` "cabd"



  describe "treeFoldPostOrder" $ do -- treeFoldPostOrder --
    context "treeFoldPostOrder (+) 0 Empty" $ -- FOLD ON EMPTY TREE
      it "should be 0" $
        (treeFoldPostOrder (+) 0 (Empty :: TriTree Int)) `shouldBe` 0

    context "treeFoldPostOrder (*) 1 (Leaf 2)" $ -- FOLD ON SINGLE LEAF
      it "should be 2" $
        (treeFoldPostOrder (*) 1 (Leaf 2)) `shouldBe` 2

    context "treeFoldPostOrder (+) 0 (Node 1 2 Empty Empty Empty)" $ -- FOLD ON SIMPLE NODE
      it "should sum the values in the Node in post-order" $
        (treeFoldPostOrder (+) 0 (Node 1 2 Empty Empty Empty)) `shouldBe` 3

    context "treeFoldPostOrder (*) 1 (Node 2 3 (Leaf 4) Empty (Leaf 5))" $ -- FOLD ON COMPLEX TREE
      it "should multiply all values in the tree in post-order" $
        (treeFoldPostOrder (*) 1 (Node 2 3 (Leaf 4) Empty (Leaf 5))) `shouldBe` 120

    context "treeFoldPostOrder (^) 2 (Node 3 2 (Leaf 2) Empty (Leaf 1))" $ -- FOLD WITH EXPONENTIAL FUNCTION
      it "should compute the result of folding with exponentiation in post-order" $
        (treeFoldPostOrder (^) 2 (Node 3 2 (Leaf 2) Empty (Leaf 1))) `shouldBe` 4096

    context "treeFoldPostOrder (++) \"\" (Node \"a\" \"b\" (Leaf \"c\") Empty (Leaf \"d\"))" $ -- FOLD WITH STRING CONCATENATION
      it "should concatenate all strings in the tree in post-order" $
        (treeFoldPostOrder (++) "" (Node "a" "b" (Leaf "c") Empty (Leaf "d"))) `shouldBe` "cdab"