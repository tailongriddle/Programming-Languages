--TEST
module DailyFourSpec where

import Test.Hspec
import DailyFour

main :: IO ()
main = hspec spec

spec :: Spec
spec = do
    describe "zip3Lists" $ do -- zip3Lists -- 
        context "zip3Lists [] [] []" $ -- ALL EMPTY TEST
            it "should be []" $
                (zip3Lists ([] :: [Int]) ([] :: [Char]) ([] :: [Int])) `shouldBe` []
        context "zip3Lists [1,2,3][\'a\',\'b\',\'c\'][4,5,6]" $ -- ALL EMPTY TEST
            it "should be [(1,\'a\',4),(2,\'b\',5),(3,\'c\',6)]" $
                (zip3Lists [1,2,3] ['a','b','c'] [4,5,6]) `shouldBe` [(1,'a',4),(2,'b',5),(3,'c',6)]
        context "zip3Lists [1,2,3][\'a\',\'b\'][4.0,5.0,6.0]" $ -- EXAMPLE TEST
            it "should be [(1,\'a\',4.0),(2,\'b\',5.0),(3,\'c\',6.0)]" $
                (zip3Lists [1,2,3] ['a','b','c'] [4.0,5.0,6.0]) `shouldBe` [(1,'a',4.0),(2,'b',5.0),(3,'c',6.0)] -- TEST WITH DOUBLES

    
    describe "unzipTriples" $ do -- unzipTriples --
        context "unzipTriples []" $ -- ALL EMPTY TEST
            it "should be ([],[],[])" $
                (unzipTriples ([] :: [(Int, Char, Int)])) `shouldBe` ([], [], [])
        context "unzipTriples [(1,\'a\',4),(2,\'b\',5),(3,\'c\',6)]" $ -- NORMAL TEST
            it "should be ([1,2,3],[\'a\',\'b\',\'c\'],[4,5,6])" $
                (unzipTriples [(1,'a',4),(2,'b',5),(3,'c',6)]) `shouldBe` ([1,2,3],['a','b','c'],[4,5,6])
        context "unzipTriples [(1,\'a\',4.0),(2,\'b\',5.0),(3,\'c\',6.0)]" $ -- EXAMPLE TEST  
            it "should be ([1,2,3],[\'a\',\'b\',\'c\'],[4.0,5.0,6.0])" $
                (unzipTriples [(1,'a',4.0),(2,'b',5.0),(3,'c',6.0)]) `shouldBe` ([1,2,3],['a','b','c'],[4.0,5.0,6.0])        -- TEST WITH FLOATS

    describe "mergeSorted3" $ do -- mergeSorted3 --
        context "mergeSorted3 [] [] []" $ -- ALL EMPTY TEST
            it "should be []" $
                (mergeSorted3 ([] :: [Int]) ([] :: [Int]) ([] :: [Int])) `shouldBe` []
        context "mergeSorted3 [-1,2,3] [4,5,6] [7,8,9]" $ -- NUMERIC TEST
            it "should be [-1,2,3,4,5,6,7,8,9]" $
                (mergeSorted3 [-1,2,3] [4,5,6] [7,8,9]) `shouldBe` [-1,2,3,4,5,6,7,8,9]
        context "mergeSorted3 [\'a\',\'b\'] [\'c\',\'d\'] [\'e\',\'f\']" $ -- LETTERS TEST
            it "should be [\'a\',\'b\',\'c\',\'d\',\'e\',\'f\']" $
                (mergeSorted3 ['a','b'] ['c','d'] ['e','f']) `shouldBe` ['a','b','c','d','e','f'] 
        context "mergeSorted3 [1.0,2.0] [3.0,4.0] [5.0,6.0]" $ -- FLOATS TEST
            it "should be [1.0,2.0,3.0,4.0,5.0,6.0]" $
                (mergeSorted3 [1.0,2.0] [3.0,4.0] [5.0,6.0]) `shouldBe` [1.0,2.0,3.0,4.0,5.0,6.0]
