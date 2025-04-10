
module DailyTwoSpec where

import Test.Hspec
import DailyTwo

main :: IO ()
main = hspec spec

spec :: Spec
spec = do
  describe "every4th" $ do -- EVERY4TH -- 
    context "every4th _" $
      it "should be []" $
        (every4th ([] :: [Integer])) `shouldBe` []
    context "every4th [1]" $ --TEST WITH ONE
      it "should be [1]" $
        (every4th [1]) `shouldBe` []

    context "every4th [1,2]" $ --TEST WITH TWO
      it "should be [1,2]" $
        (every4th [1,2]) `shouldBe` []

    context "every4th [1,2,3,4]" $ -- BASIC TEST (FOUR)
      it "should be [4]" $
        (every4th [1,2,3,4]) `shouldBe` [4]

    context "every4th [1,2,3,4,5]" $ -- TEST WITH FIVE
      it "should be [4]" $
        (every4th [1,2,3,4,5]) `shouldBe` [4]

    context "every4th [1,2,3,4,5,6,7,8]" $ --TEST WITH EIGHT
      it "should be [4,8]" $
        (every4th [1,2,3,4,5,6,7,8]) `shouldBe` [4,8]

-- TUPLE -- 
  describe "tupleDotProduct" $ do 
    context "tupleDotProduct [1,2] [2,3]" $ -- TEST TWO NUMS (8)
      it "should be 8" $
        (tupleDotProduct [1,2] [2,3]) `shouldBe` 8

    context "tupleDotProduct [1,2,2,3] [1,2,2,1]" $ -- TEST FOUR NUMS (12)
      it "should be 12" $
        (tupleDotProduct [1,2,2,3] [1,2,2,1]) `shouldBe` 12

    context "tupleDotProduct [1.0,2.0] [1.0,2.0]" $ -- TEST FLOAT
      it "should be 5.0" $
        (tupleDotProduct [1.0,2.0] [1.0,2.0]) `shouldBe` 5.0

    context "tupleDotProduct [] []" $ -- TEST EMPTY LISTS
      it "should be 0" $
        (tupleDotProduct [] []) `shouldBe` 0

-- toSetList -- 
  describe "toSetList" $ do 
    context "toSetList [5,1,2,3,3,4,5,5]" $ -- ORIGINAL EXAMPLE
      it "should be [1,2,3,4,5]" $
        (toSetList [5,1,2,3,3,4,5,5] ) `shouldBe` [1,2,3,4,5]

    context "toSetList []" $ -- TEST EMPTY
      it "should be []" $
        (toSetList ([] :: [Integer])) `shouldBe` ([] :: [Integer])
   
    context "toSetList [1,1]" $ -- TEST 1,1 RETURN 1
      it "should be [1]" $ 
        (toSetList [1,1]) `shouldBe` [1]

-- appendToEach --
  describe "appendToEach" $ do
    context "appendToEach \"oo\" [\"meow\",\"meeeow\",\"mrrow\"]" $ -- FIRST TEST
      it "should be [\"meowoo\",\"meeeowoo\",\"mrrowoo\"]" $
        (appendToEach "oo" ["meow", "meeeow", "mrrow"]) `shouldBe` ["meowoo", "meeeowoo", "mrrowoo"]

    context "appendToEach \"\" []" $ -- ALL EMPTY TEST
      it "should be []" $
        (appendToEach "" []) `shouldBe` ([] :: [String])

    context "appendToEach \"\" [\"meow\",\"mew\"]" $ -- STRING EMPTY TEST
      it "should be [\"meow\",\"mew\"]" $
        (appendToEach "" ["meow", "mew"]) `shouldBe` ["meow", "mew"]

    context "appendToEach \"meow\" []" $ -- LIST EMPTY TEST
      it "should be []" $
        (appendToEach "meow" []) `shouldBe` ([] :: [String])