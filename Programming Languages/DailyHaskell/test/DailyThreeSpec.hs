--TEST
module DailyThreeSpec where

import Test.Hspec
import DailyThree

main :: IO ()
main = hspec spec

spec :: Spec
spec = do
    describe "removeAllExcept" $ do -- removeAllExcept -- 
        context "removeAllExcept \"\" []" $ -- BOTH EMPTY TEST
            it "should be []" $
                (removeAllExcept "" []) `shouldBe` []
        context "removeAllExcept 'a' \"\"" $ -- TEST WITH ONE
            it "should be []" $
                (removeAllExcept 'a' "") `shouldBe` []
        context "removeAllExcept 'a' \"book\"" $ -- NOTHING TO REMOVE
            it "should be []" $
                (removeAllExcept 'a' "book") `shouldBe` []
        context "removeAllExcept 'a' \"aaaa\"" $ -- ALL CHARACTERS MATCH
            it "should be [a,a,a,a]" $
                (removeAllExcept 'a' "aaaa") `shouldBe` ['a','a','a','a']
        context "removeAllExcept 1 [1,2,3,4]" $ -- TEST WITH NUMBERS
            it "should be [1]" $
                (removeAllExcept 1 [1,2,3,4]) `shouldBe` [1]

    describe "countOccurences" $ do -- countOccurences -- 
        context "countOccurences \"\" []" $ -- BOTH EMPTY TEST
            it "should be 0" $
                (countOccurrences "" []) `shouldBe` 0
        context "countOccurences 'a' \"\"" $ -- TEST WITH NONE
            it "should be 0" $
                (countOccurrences 'a' "") `shouldBe` 0
        context "countOccurences 'a' \"aaaa\"" $ -- ALL CHARACTERS MATCH
            it "should be 4" $
                (countOccurrences 'a' "aaaa") `shouldBe` 4
        context "countOccurences 1 [1,1,3,4]" $ -- TEST WITH NUMBERS
            it "should be 2" $
                (countOccurrences 1 [1,1,3,4]) `shouldBe` 2
        context "countOccurences 2 [1,1,3,4]" $ -- TEST WITH NUMBERS
            it "should be 0" $
                (countOccurrences 2 [1,1,3,4]) `shouldBe` 0  

    describe "substitute" $ do -- substitute -- 
        context "substitute \"\" \"\" []" $ -- BOTH EMPTY TEST
            it "should be []" $
                (substitute "" "" []) `shouldBe` []
        context "substitute 'a' 'b' \"\"" $ -- TEST WITH NONE
            it "should be []" $
                (substitute 'a' 'b' "") `shouldBe` []
        context "substitute 'a' 'b' \"aaaa\"" $ -- ALL CHARACTERS MATCH
            it "should be [b,b,b,b]" $
                (substitute 'a' 'b' "aaaa") `shouldBe` ['b','b','b','b']
        context "substitute 'a' 'b' \"book\"" $ -- NOTHING TO SUBSTITUTE
            it "should be [b,o,o,k]" $
                (substitute 'a' 'b' "book") `shouldBe` ['b','o','o','k']
        context "substitute 1 2 [1,1,3,4]" $ -- TEST WITH NUMBERS
            it "should be [2,2,3,4]" $
                (substitute 1 2 [1,1,3,4]) `shouldBe` [2,2,3,4]

    