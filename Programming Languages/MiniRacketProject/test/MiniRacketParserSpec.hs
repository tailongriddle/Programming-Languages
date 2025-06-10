module MiniRacketParserSpec where


import Test.Hspec
import Parser
import Expr
import MiniRacketParser
import Error


type ParseResult = Either ErrorType (Expr, String)


expr :: Either ErrorType (a2, b) -> a2
expr (Right (e, _)) = e
expr (Left (SyntaxError msg)) = error msg
expr (Left (ParseError msg)) = error msg
expr (Left NoParse) = error "no matching parse"
expr _ = error "expr in MiniRacketParser.hs is not fully implemented yet..."


spec :: Spec
spec = do
   describe "parse literals" $ do
       it "parses number: 1235" $
           parseString "1235" `shouldBe` Right (LiteralExpr (IntValue 1235),"")
       it "parses negative numbers: -12235" $
           parseString "-12235" `shouldBe` Right (LiteralExpr (IntValue (-12235)), "")
       it "parses zero" $
           parseString "0" `shouldBe` Right (LiteralExpr (IntValue 0), "")
       it "parses negative one" $
           parseString "-1" `shouldBe` Right (LiteralExpr (IntValue (-1)), "")
       it "parses true" $
           parseString "true" `shouldBe` Right (LiteralExpr (BoolValue True), "")
       it "parses false" $
           parseString "false" `shouldBe` Right (LiteralExpr (BoolValue False), "")
       it "fails on non-literal: foo" $
           parseString "foo" `shouldSatisfy` isLeft
       it "parses number with trailing space" $
           parseString "42 " `shouldBe` Right (LiteralExpr (IntValue 42), "")
  
   describe "parse bool operations" $ do
       it "parses (or false true)" $
           parseString "(or false true)" `shouldBe` Right (BoolExpr Or [LiteralExpr (BoolValue False), LiteralExpr (BoolValue True)], "")
       it "parses (and true false)" $
           parseString "(and true false)" `shouldBe` Right (BoolExpr And [LiteralExpr (BoolValue True), LiteralExpr (BoolValue False)], "")
       it "fails on invalid bool operation" $
           parseString "(xor true false)" `shouldSatisfy` isLeft
  
   describe "parse not" $ do
       it "parses (not true)" $
           parseString "(not true)" `shouldBe` Right (NotExpr (LiteralExpr (BoolValue True)), "")
       it "parses (not false)" $
           parseString "(not false)" `shouldBe` Right (NotExpr (LiteralExpr (BoolValue False)), "")


   describe "parse comparisons" $ do
       it "parses (equal? 1 1)" $
           parseString "(equal? 1 1)" `shouldBe` Right (CompExpr Eq (LiteralExpr (IntValue 1)) (LiteralExpr (IntValue 1)), "")


   describe "parse math operations" $ do
       it "parses (+ 1 2)" $
           parseString "(+ 1 2)" `shouldBe` Right (MathExpr Add [LiteralExpr (IntValue 1), LiteralExpr (IntValue 2)], "")
       it "parses (- 5 3)" $
           parseString "(- 5 3)" `shouldBe` Right (MathExpr Sub [LiteralExpr (IntValue 5), LiteralExpr (IntValue 3)], "")
       it "parses (* 4 2)" $
           parseString "(* 4 2)" `shouldBe` Right (MathExpr Mul [LiteralExpr (IntValue 4), LiteralExpr (IntValue 2)], "")
       it "parses (div 8 2)" $
           parseString "(div 8 2)" `shouldBe` Right (MathExpr Div [LiteralExpr (IntValue 8), LiteralExpr (IntValue 2)], "")
       it "parses (mod 10 3)" $
           parseString "(mod 10 3)" `shouldBe` Right (MathExpr Mod [LiteralExpr (IntValue 10), LiteralExpr (IntValue 3)], "")
       it "fails on invalid math operation" $
           parseString "(pow 2 3)" `shouldSatisfy` isLeft


   describe "parse math expressions" $ do
       it "parses (+ 1 2)" $
           parseString "(+ 1 2)" `shouldBe` Right (MathExpr Add [LiteralExpr (IntValue 1), LiteralExpr (IntValue 2)], "")
       it "parses (+ 1 (* 2 3))" $
           parseString "(+ 1 (* 2 3))"
             `shouldBe` Right (MathExpr Add [LiteralExpr (IntValue 1), MathExpr Mul [LiteralExpr (IntValue 2), LiteralExpr (IntValue 3)]], "")
       it "parses (* (- 5 2) (div 8 2))" $
           parseString "(* (- 5 2) (div 8 2))"
             `shouldBe` Right (MathExpr Mul [MathExpr Sub [LiteralExpr (IntValue 5), LiteralExpr (IntValue 2)], MathExpr Div [LiteralExpr (IntValue 8), LiteralExpr (IntValue 2)]], "")

   describe "parse nested bool and math" $ do
        it "parses nested and/or: (and true (or false true))" $
            parseString "(and true (or false true))"
                `shouldBe` Right (BoolExpr And [LiteralExpr (BoolValue True), BoolExpr Or [LiteralExpr (BoolValue False), LiteralExpr (BoolValue True)]], "")

        it "parses nested or/and: (or (and true false) false)" $
            parseString "(or (and true false) false)"
                `shouldBe` Right (BoolExpr Or [BoolExpr And [LiteralExpr (BoolValue True), LiteralExpr (BoolValue False)], LiteralExpr (BoolValue False)], "")

        it "parses nested math: (+ 1 (* 2 3))" $
            parseString "(+ 1 (* 2 3))"
                `shouldBe` Right (MathExpr Add [LiteralExpr (IntValue 1), MathExpr Mul [LiteralExpr (IntValue 2), LiteralExpr (IntValue 3)]], "")

        it "parses nested math: (* (- 5 2) (div 8 2))" $
            parseString "(* (- 5 2) (div 8 2))"
                `shouldBe` Right (MathExpr Mul [MathExpr Sub [LiteralExpr (IntValue 5), LiteralExpr (IntValue 2)], MathExpr Div [LiteralExpr (IntValue 8), LiteralExpr (IntValue 2)]], "")
   
   describe "P2: parse negate atom" $ do
        it "parses negate atom: -x" $
            parseString "(-x)" `shouldBe` Right (MathExpr Sub [VarExpr "x"],"")
        it "parses negate atom: -test" $
            parseString "(-test)" `shouldBe` Right (MathExpr Sub [VarExpr "test"],"")
        it "parses negate atom: -name123" $
            parseString "(-name123)" `shouldBe` Right (MathExpr Sub [VarExpr "name123"],"")

   describe "P2: parse var expr" $ do
        it "parses var expr: name123" $
            parseString "(name123)" `shouldBe` Right (VarExpr "name123","")
        it "parses var expr: x" $
            parseString "(x)" `shouldBe` Right (VarExpr "x","")
        it "parses var expr: test" $
            parseString "(test)" `shouldBe` Right (VarExpr "test","")

   describe "P2: parse if expr" $ do
        it "parses if expr: if true 1 2" $
            parseString "(if true 1 2)" `shouldBe` Right (IfExpr (LiteralExpr (BoolValue True)) (LiteralExpr (IntValue 1)) (LiteralExpr (IntValue 2)),"")
        it "parses if expr: if false 1 2" $
            parseString "(if false 1 2)" `shouldBe` Right (IfExpr (LiteralExpr (BoolValue False)) (LiteralExpr (IntValue 1)) (LiteralExpr (IntValue 2)),"")
        it "parses if expr: if (or true false) (and true false) (or true false)" $
            parseString "(if (or true false) (and true false) (or true false))"
                `shouldBe` Right (IfExpr (BoolExpr Or [LiteralExpr (BoolValue True),LiteralExpr (BoolValue False)])
                                         (BoolExpr And [LiteralExpr (BoolValue True),LiteralExpr (BoolValue False)])
                                         (BoolExpr Or [LiteralExpr (BoolValue True),LiteralExpr (BoolValue False)]),"")

   describe "P2: parse let expr" $ do
        it "parses let expr: let (x 5) 5" $
            parseString "(let (x 5) 5)" `shouldBe` Right (LetExpr "x" (LiteralExpr (IntValue 5)) (LiteralExpr (IntValue 5)),"")
        it "parses let expr: let (x (+ 1 5)) (if (< 10 2) true false))" $
            parseString "(let (x (+ 1 5)) (if (< 10 2) true false)))"
                `shouldBe` Right (LetExpr "x"
                                    (MathExpr Add [LiteralExpr (IntValue 1),LiteralExpr (IntValue 5)])
                                    (IfExpr (CompExpr Lt (LiteralExpr (IntValue 10)) (LiteralExpr (IntValue 2)))
                                            (LiteralExpr (BoolValue True))
                                            (LiteralExpr (BoolValue False))),")")
 where
   isLeft (Left _) = True
   isLeft _        = False