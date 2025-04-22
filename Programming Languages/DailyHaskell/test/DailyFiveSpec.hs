--TEST
module DailyFiveSpec where

import Test.Hspec
import DailyFive

main :: IO ()
main = hspec spec

spec :: Spec
spec = do
    describe "multPairs" $ do -- multPairs -- 
        context "multPairs []" $ -- ALL EMPTY TEST
            it "should be []" $
                (multPairs ([] :: [(Integer,Integer)])) `shouldBe` []
        context "multPairs [(1,2),(3,4)]" $ -- NORMAL
            it "should be [2,12]" $
                (multPairs [(1,2),(3,4)]) `shouldBe` [2,12]
        context "multPairs [(0,1),(1,1)]" $ -- ZERO
            it "should be [0,1]" $
                (multPairs [(0,1),(1,1)]) `shouldBe` [0,1]
   
    describe "squareList" $ do -- squareList -- 
        context "squareList []" $ -- ALL EMPTY TEST
            it "should be []" $
                (squareList ([] :: [Integer])) `shouldBe` []
        context "squareList [1,2,3,4)]" $ -- NORMAL
            it "should be [(1,1),(2,4),(3,9),(4,16)]" $
                (squareList [1,2,3,4]) `shouldBe` [(1,1),(2,4),(3,9),(4,16)]
        context "squareList [0,1]" $ -- ZERO
            it "should be [(0,0),(1,1)]" $
                (squareList [0,1]) `shouldBe` [(0,0),(1,1)]

    describe "findLowercase" $ do -- findLowercase -- 
        context "findLowercase []" $ -- ALL EMPTY TEST
            it "should be []" $
                (findLowercase ([] :: [String])) `shouldBe` []
        context "findLowercase [\"a\",\"B\",\"c\"]" $ -- NORMAL
            it "should be [True, False, True]" $
                (findLowercase ["a","B","c"]) `shouldBe` [True, False, True]
