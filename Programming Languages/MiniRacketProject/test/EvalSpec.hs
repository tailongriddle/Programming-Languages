module EvalSpec where




import Test.Hspec
import Parser
import Expr
import MiniRacketParser


import Eval
import Error


type ParseResult = Either ErrorType (Expr, String)


spec :: Spec
spec = do
   describe "eval expressions" $ do
       it "evaluates number: 1235" $
           evalString "1235" `shouldBe` Right (IntValue 1235)
       it "evaluates negative numbers: -12235" $
           evalString "-12235" `shouldBe` Right (IntValue (-12235))
       it "evaluates zero" $
           evalString "0" `shouldBe` Right (IntValue 0)
       it "evaluates negative one" $
           evalString "-1" `shouldBe` Right (IntValue (-1))
       it "evaluates number: 42" $
           evalString "42" `shouldBe` Right (IntValue 42)
       it "evaluates true" $
           evalString "true" `shouldBe` Right (BoolValue True)
       it "evaluates false" $
           evalString "false" `shouldBe` Right (BoolValue False)
       it "fails on non-literal: foo" $
           evalString "foo" `shouldSatisfy` isLeft
       it "evaluates or false true" $
           evalString "(or false true)" `shouldBe` Right (BoolValue True)
       it "evaluates false or false" $
           evalString "(or false false)" `shouldBe` Right (BoolValue False)
       it "evaluates (and true (or false true))" $
           evalString "(and true (or false true))" `shouldBe` Right (BoolValue True)
       it "evaluates (or (and true false) false)" $
           evalString "(or (and true false) false)" `shouldBe` Right (BoolValue False)
       it "evaluates (+ 1 (* 2 3))" $
           evalString "(+ 1 (* 2 3))" `shouldBe` Right (IntValue 7)
       it "evaluates (* (- 5 2) (div 8 2))" $
           evalString "(* (- 5 2) (div 8 2))" `shouldBe` Right (IntValue 12)
       it "evaluates (+ 1 2)" $
           evalString "(+ 1 2)" `shouldBe` Right (IntValue 3)
       it "evaluates (* 2 3)" $
           evalString "(* 2 3)" `shouldBe` Right (IntValue 6)
       it "evaluates (div 6 2)" $
           evalString "(div 6 2)" `shouldBe` Right (IntValue 3)
       it "evaluates (equal? 2 2)" $
           evalString "(equal? 2 2)" `shouldBe` Right (BoolValue True)
       it "evaluates (equal? 2 3)" $
           evalString "(equal? 2 3)" `shouldBe` Right (BoolValue False)


   describe "eval nested bool and math" $ do
        it "evaluates nested and/or: (and true (or false true))" $
            evalString "(and true (or false true))"
                `shouldBe` Right (BoolValue True)
        it "evaluates nested or/and: (or (and true false) false)" $
            evalString "(or (and true false) false)"
                `shouldBe` Right (BoolValue False)
        it "evaluates nested math: (+ 1 (* 2 3))" $
            evalString "(+ 1 (* 2 3))"
                `shouldBe` Right (IntValue 7)
        it "evaluates nested math: (* (- 5 2) (div 8 2))" $
            evalString "(* (- 5 2) (div 8 2))"
                `shouldBe` Right (IntValue 12)


  where
   isLeft (Left _) = True
   isLeft _        = False








