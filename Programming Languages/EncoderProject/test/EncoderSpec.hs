--TEST
module EncoderSpec where

import Test.Hspec
import Encoder

main :: IO ()
main = hspec spec

spec :: Spec
spec = do
  describe "removeChar" $ do -- removeChar -- 
    context "removeChar 'x' \"\"" $ --  EMPTY TEST
      it "should be \"\"" $
        (removeChar 'x' "") `shouldBe` ""

    context "removeChar 'a' \"boaok\"" $ -- TEST WITH ONE
      it "should be \"book\"" $
        (removeChar 'a' "boaok") `shouldBe` "book"
  
    context "removeChar 'a' \"book\"" $ -- NONE TO REMOVE
      it "should be \"book\"" $
        (removeChar 'a' "book") `shouldBe` "book"

    context "removeChar 'a' \"aaaa\"" $ -- ALL CHARACTERS MATCH
      it "should be \"\"" $
        (removeChar 'a' "aaaa") `shouldBe` ""



  describe "removeWhitespace" $ do -- removeWhitespace -- 
    context "removeWhitespace \"\"" $ -- BOTH EMPTY TEST
      it "should be \"\"" $
        (removeWhitespace "") `shouldBe` ""

    context "removeWhitespace \"b \to\nok\r\"" $ -- TEST WITH ONE
      it "should be \"book\"" $
        (removeWhitespace "b \to\nok\r") `shouldBe` "book"

    context "removeWhitespace \"book\"" $ -- NOTHING TO REMOVE
      it "should be \"book\"" $
        (removeWhitespace "book") `shouldBe` "book"



  describe "removePunctuation" $ do -- removePunctuation -- 
    context "removePunctuation \"\"" $ -- BOTH EMPTY TEST
      it "should be \"\"" $
        (removePunctuation "") `shouldBe` ""

    context "removePunctuation \"{b,o.(o)[k]}\"" $ -- TEST WITH ONE
      it "should be \"book\"" $
        (removePunctuation "{b,o.(o)[k]}") `shouldBe` "book"

    context "removePunctuation \"book\"" $ -- NOTHING TO REMOVE
      it "should be \"book\"" $
        (removePunctuation "book") `shouldBe` "book"
    



  describe "charsToAscii" $ do -- charsToAscii -- 
    context "charsToAscii \"\"" $ --  EMPTY TEST
      it "should be []" $
        (charsToAscii "") `shouldBe` ([] :: [Int])

    context "charsToAscii \"abcABC\"" $ -- NORMAL TEST
      it "should be [97,98,99,65,66,67]" $
        (charsToAscii "abcABC") `shouldBe` [97,98,99,65,66,67]
      
    context "charsToAscii \"abc ABC\"" $ -- TEST WITH SPACE
      it "should be [97,98,99,32,65,66,67]" $
        (charsToAscii "abc ABC") `shouldBe` [97,98,99,32,65,66,67]
    
    context "charsToAscii \"!@#$%^&*()\"" $ -- TEST WITH PUNCTUATION
      it "should be [33,64,35,36,37,94,38,42,40,41]" $
        (charsToAscii "!@#$%^&*()") `shouldBe` [33,64,35,36,37,94,38,42,40,41]


  describe "asciiToChars" $ do -- asciiToChars -- 
    context "asciiToChars \"\"" $ --  EMPTY TEST
      it "should be []" $
        (asciiToChars ([] :: [Int])) `shouldBe` ""

    context "asciiToChars [97,98,99,65,66,67]" $ -- NORMAL TEST
      it "should be \"abcABC\"" $
        (asciiToChars [97,98,99,65,66,67]) `shouldBe` "abcABC"
    
    context "asciiToChars [97,98,99,32,65,66,67]" $ -- TEST WITH SPACE
      it "should be \"abc ABC\"" $
        (asciiToChars [97,98,99,32,65,66,67]) `shouldBe` "abc ABC"
    
    context "asciiToChars [33,64,35,36,37,94,38,42,40,41]" $ -- TEST WITH PUNCTUATION
      it "should be \"!@#$%^&*()\"" $
        (asciiToChars [33,64,35,36,37,94,38,42,40,41]) `shouldBe` "!@#$%^&*()"




  describe "shiftInts" $ do -- shiftInts -- 
    context "shiftInts 0 []" $ --  EMPTY TEST
      it "should be []" $
        (shiftInts 0 ([] :: [Int])) `shouldBe` ([] :: [Int])

    context "shiftInts 5 [0,1,2,127]" $ -- NORMAL TEST
      it "should be [5,6,7,4]" $
        (shiftInts 5 [0,1,2,127]) `shouldBe` [5,6,7,4]

    context "shiftInts 1 [0,1,2,127]" $ -- EXAMPLE TEST
      it "should be [1,2,3,0]" $
        (shiftInts 1 [0,1,2,127]) `shouldBe` [1,2,3,0]



  describe "shiftMessage" $ do -- shiftInts -- 
    context "shiftMessage 3 \"\"" $ --  EMPTY TEST W/SHIFT
      it "should be \"\"" $
        (shiftMessage 3 "") `shouldBe` ""

    context "shiftMessage 0 \"\"" $ --  EMPTY TEST 
      it "should be \"\"" $
        (shiftMessage 0 "") `shouldBe` ""

    context "shiftMessage 5 \"abcABC\"" $ -- NORMAL TEST
      it "should be \"fghFGH\"" $
        (shiftMessage 5 "abcABC") `shouldBe` "fghFGH"

    context "shiftMessage 1 \"abc ABC\"" $ -- TEST WITH SPACE
      it "should be \"bcd!BCD\"" $
        (shiftMessage 1 "abc ABC") `shouldBe` "bcd!BCD"

    context "shiftMessage -5 \"lmnLMN\"" $ -- NEGATIVE TEST
      it "should be \"ghiGHI\"" $
        (shiftMessage (-5) "lmnLMN") `shouldBe` "ghiGHI"