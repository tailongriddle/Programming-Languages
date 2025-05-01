module DailyEightSpec where

import Test.Hspec
import DailyEight

main :: IO ()
main = hspec spec

spec :: Spec
spec = do

  describe "findSmallest" $ do
    context "findSmallest []" $ -- EMPTY LIST
      it "should return Nothing" $
        findSmallest ([] :: [Int]) `shouldBe` Nothing

    context "findSmallest [5]" $ -- SINGLE ELEMENT
      it "should return Just 5" $
        findSmallest [5] `shouldBe` Just 5

    context "findSmallest [3, 1, 4]" $ -- MULTIPLE ELEMENTS
      it "should return Just 1" $
        findSmallest [3, 1, 4] `shouldBe` Just 1

    context "findSmallest [10, 20, 5]" $ -- MULTIPLE ELEMENTS WITH SMALLEST AT THE END
      it "should return Just 5" $
        findSmallest [10, 20, 5] `shouldBe` Just 5

    context "findSmallest [7, 7, 7]" $ -- ALL ELEMENTS EQUAL
      it "should return Just 7" $
        findSmallest [7, 7, 7] `shouldBe` Just 7

    context "findSmallest [100, 50, 200, 25]" $ -- MIXED ELEMENTS
      it "should return Just 25" $
        findSmallest [100, 50, 200, 25] `shouldBe` Just 25





  describe "allTrue" $ do
    context "allTrue []" $ -- EMPTY LIST
      it "should return Nothing" $
        allTrue [] `shouldBe` Nothing

    context "allTrue [True]" $ -- SINGLE TRUE ELEMENT
      it "should return Just True" $
        allTrue [True] `shouldBe` Just True

    context "allTrue [False]" $ -- SINGLE FALSE ELEMENT
      it "should return Just False" $
        allTrue [False] `shouldBe` Just False

    context "allTrue [True, True, True]" $ -- ALL TRUE ELEMENTS
      it "should return Just True" $
        allTrue [True, True, True] `shouldBe` Just True

    context "allTrue [True, False, True]" $ -- MIXED ELEMENTS WITH FALSE
      it "should return Just False" $
        allTrue [True, False, True] `shouldBe` Just False

    context "allTrue [False, True, True]" $ -- FIRST ELEMENT FALSE
      it "should return Just False" $
        allTrue [False, True, True] `shouldBe` Just False

    context "allTrue [True, True, False]" $ -- LAST ELEMENT FALSE
      it "should return Just False" $
        allTrue [True, True, False] `shouldBe` Just False


  describe "countAllVotes" $ do
    context "countAllVotes []" $ -- EMPTY LIST
      it "should return (0, 0, 0)" $
        countAllVotes [] `shouldBe` (0, 0, 0)

    context "countAllVotes [Nothing]" $ -- SINGLE NOTHING
      it "should return (1, 0, 0)" $
        countAllVotes [Nothing] `shouldBe` (1, 0, 0)

    context "countAllVotes [Just True]" $ -- SINGLE TRUE
      it "should return (0, 1, 0)" $
        countAllVotes [Just True] `shouldBe` (0, 1, 0)

    context "countAllVotes [Just False]" $ -- SINGLE FALSE
      it "should return (0, 0, 1)" $
        countAllVotes [Just False] `shouldBe` (0, 0, 1)

    context "countAllVotes [Nothing, Just True, Just False]" $ -- MIXED VALUES
      it "should return (1, 1, 1)" $
        countAllVotes [Nothing, Just True, Just False] `shouldBe` (1, 1, 1)

    context "countAllVotes [Just True, Just True, Nothing, Just False, Nothing]" $ -- COMPLEX MIXED VALUES
      it "should return (2, 2, 1)" $
        countAllVotes [Just True, Just True, Nothing, Just False, Nothing] `shouldBe` (2, 2, 1)

    context "countAllVotes [Nothing, Nothing, Nothing]" $ -- ALL NOTHING
      it "should return (3, 0, 0)" $
        countAllVotes [Nothing, Nothing, Nothing] `shouldBe` (3, 0, 0)

    context "countAllVotes [Just True, Just True, Just True]" $ -- ALL TRUE
      it "should return (0, 3, 0)" $
        countAllVotes [Just True, Just True, Just True] `shouldBe` (0, 3, 0)

    context "countAllVotes [Just False, Just False, Just False]" $ -- ALL FALSE
      it "should return (0, 0, 3)" $
        countAllVotes [Just False, Just False, Just False] `shouldBe` (0, 0, 3)