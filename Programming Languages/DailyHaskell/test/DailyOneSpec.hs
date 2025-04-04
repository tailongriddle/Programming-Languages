
module DailyOneSpec where

import Test.Hspec
import DailyOne

main :: IO ()
main = hspec spec

spec :: Spec
spec = do
  describe "quadratic" $ do
    context "quadratic 0 0 0 1" $
      it "should be 0" $
        (quadratic 0 0 0 1) `shouldBe` 0

    context "quadratic 0 0 1 0" $
      it "should be 0" $
        (quadratic 0 0 1 0) `shouldBe` 0

    context "quadratic 0 1 0 0" $
      it "should be 0" $
        (quadratic 0 1 0 0) `shouldBe` 0

    context "quadratic 1 0 0 0" $
      it "should be 1" $
        (quadratic 1 0 0 0) `shouldBe` 1
    
    context "quadratic 1 1 1 1" $ -- ADDED ONE
      it "should be 3" $
        (quadratic 1 1 1 1) `shouldBe` 3

    context "quadratic 1 2 2 1" $ -- ADDED TWO
      it "should be 5" $
        (quadratic 1 2 2 1) `shouldBe` 5

    context "quadratic 1 2 2 2" $ -- ADDED THREE
      it "should be 7" $
        (quadratic 1 2 2 2) `shouldBe` 13

  describe "scaleVector" $ do
    context "scaleVector 5 (1,0)" $
      it "should be (5, 0)" $
        (scaleVector 5 (1, 0)) `shouldBe` (5, 0)

    context "scaleVector 10 (0,1)" $
      it "should be (0, 10)" $
        (scaleVector 10 (0, 1)) `shouldBe` (0, 10)

    context "scaleVector 0 (1,1)" $
      it "should be (0, 0)" $
        (scaleVector 0 (1, 1)) `shouldBe` (0, 0)

    context "scaleVector 3 (2,3)" $
      it "should be (6, 9)" $
        (scaleVector 3 (2, 3)) `shouldBe` (6, 9)
  
    context "scaleVector 1 (0,0)" $ -- ADDED ONE
      it "should be (0, 0)" $
        (scaleVector 1 (0, 0)) `shouldBe` (0, 0)

    context "scaleVector 3 (0,5)" $ -- ADDED TWO
      it "should be (0, 15)" $
        (scaleVector 3 (0, 5)) `shouldBe` (0, 15)

    context "scaleVector 2 (2,4)" $ -- ADDED THREE
      it "should be (4, 8)" $
        (scaleVector 2 (2, 4)) `shouldBe` (4, 8) 

  describe "tripleDistance" $ do
    context "tripleDistance (0,0,1) (0,0,0)" $
      it "should be 1.0" $
        (tripleDistance (0, 0, 1) (0, 0, 0)) `shouldBe` 1.0 

    context "tripleDistance (0,0,1) (0,0,-1)" $
      it "should be 2.0" $
        (tripleDistance (0, 0, 1) (0, 0, -1)) `shouldBe` 2.0
    context "tripleDistance (0,0,1) (0,1,0)" $ 
      it "should be (sqrt ((0 - 0)^2 + (0 - 1)^2 + (1 - 0)^2))" $
        (tripleDistance (0, 0, 1) (0, 1, 0)) `shouldBe` 
           (sqrt ((0 - 0)^2 + (0 - 1)^2 + (1 - 0)^2)) 

    context "tripleDistance (0,0,-1) (0,1,0)" $ -- ADDED ONE 
      it "should be (sqrt ((0 - 0)^2 + (0 - 1)^2 + (1 - 0)^2))" $
        (tripleDistance (0, 0, -1) (0, 1, 0)) `shouldBe` 
           (sqrt ((0 - 0)^2 + (-1 + 0)^2 + (1 - 0)^2))
    context "tripleDistance (1,1,1) (1,1,1)" $ -- ADDED TWO 
      it "should be (sqrt ((1 - 1)^2 + (-1 + 1)^2 + (1 - 1)^2))" $
        (tripleDistance (1, -1, 1) (1, -1, 1)) `shouldBe` 
           (sqrt ((1 - 1)^2 + (-1 + 1)^2 + (1 - 1)^2))
    context "tripleDistance (0,0,0) (0,0,0)" $ -- ADDED THREE 
      it "should be 0.0" $
        (tripleDistance (1, -1, 1) (1, -1, 1)) `shouldBe` 0.0
