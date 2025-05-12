module DailyNineSpec where

import Test.Hspec
import DailyNine

main :: IO ()
main = hspec spec

spec :: Spec
spec = do

  describe "onlyNothing" $ do
    context "onlyNothing with an empty list" $
      it "should return True" $
        onlyNothing (\x -> if x > 0 then Just x else Nothing) ([] :: [Int]) `shouldBe` True

    context "onlyNothing with all Nothing results" $
      it "should return True" $
        onlyNothing (\x -> if x > 0 then Just x else Nothing) [-1, -2, -3] `shouldBe` True

    context "onlyNothing with some Just results" $
      it "should return False" $
        onlyNothing (\x -> if x > 0 then Just x else Nothing) [-1, 2, -3] `shouldBe` False

  describe "firstAnswer" $ do
    context "firstAnswer with an empty list" $
      it "should return Nothing" $
        firstAnswer (\x -> if x > 0 then Just x else Nothing) ([] :: [Int]) `shouldBe` Nothing

    context "firstAnswer with the first Just result" $
      it "should return Just 2" $
        firstAnswer (\x -> if x > 0 then Just x else Nothing) [-1, 2, 3] `shouldBe` Just 2

    context "firstAnswer with all Nothing results" $
      it "should return Nothing" $
        firstAnswer (\x -> if x > 0 then Just x else Nothing) [-1, -2, -3] `shouldBe` Nothing

  describe "allAnswers" $ do
    context "allAnswers with an empty list" $
      it "should return Just []" $
        allAnswers (\x -> if x > 0 then Just [x] else Nothing) ([] :: [Int]) `shouldBe` Just []

    context "allAnswers with all Just results" $
      it "should return Just [1, 2, 3]" $
        allAnswers (\x -> if x > 0 then Just [x] else Nothing) [1, 2, 3] `shouldBe` Just [1, 2, 3]

    context "allAnswers with one Nothing result" $
      it "should return Nothing" $
        allAnswers (\x -> if x > 0 then Just [x] else Nothing) [1, -2, 3] `shouldBe` Nothing


