--TEST
module DailySixSpec where

import Test.Hspec
import DailySix

main :: IO ()
main = hspec spec

spec :: Spec
spec = do
    describe "shorterThan" $ do -- shorterThan -- 
        context "shorterThan _ []" $ -- ALL EMPTY TEST
            it "should be []" $
                (shorterThan 0 ([] :: [String])) `shouldBe` []
        context "shorterThan 3 [\"aaaaaaaa\",\"BB\",\"ccc\"]" $ -- NORMAL
            it "should be [\"ccc\"]" $
                (shorterThan 3 ["aaaaaaaa","BB","ccc"]) `shouldBe` ["BB","ccc"]
        context "shorterThan 0 [\"a\",\"B\",\"c\"]" $ -- ZERO
            it "should be []" $
                (shorterThan 0 ["a","B","c"]) `shouldBe` []
  
    describe "removeMultiples" $ do -- removeMultiples -- 
        context "removeMultiples _ []" $ -- ALL EMPTY TEST
            it "should be []" $
                (removeMultiples 0 ([] :: [Integer])) `shouldBe` []
        context "removeMultiples 3 [1,3,9,10]" $ -- NORMAL
            it "should be [1,10]" $
                (removeMultiples 3 [1,3,9,10]) `shouldBe` [1,10]
        context "removeMultiples 0 [1,3,9,10]" $ -- 1
            it "should be [1,3,9,10]" $
                (removeMultiples 1 [1,3,9,10]) `shouldBe` []

    describe "onlyJust" $ do -- onlyJust -- 
        context "onlyJust []" $ -- ALL EMPTY TEST
            it "should be []" $
                (onlyJust ([] :: [Maybe Integer])) `shouldBe` ([] :: [Maybe Integer])
        context "onlyJust [Nothing, Nothing, Nothing]" $ -- ALL NOTHING
            it "should be []" $
                (onlyJust [Nothing, Nothing, Nothing] :: [Maybe Integer]) `shouldBe` ([] :: [Maybe Integer])
        context "onlyJust [Nothing, Just 1, Just 2]" $ -- MIXED CASE
            it "should be [Just 1, Just 2]" $
                (onlyJust [Nothing, Just 1, Just 2] :: [Maybe Integer]) `shouldBe` [Just 1, Just 2]