module DailyElevenSpec where

import Test.Hspec
import DailyEleven
import Data.Char


f :: Maybe Integer -> Maybe Integer
f mx = fmap (+1) mx

g :: Maybe Integer -> Maybe Integer
g mx = fmap (*2) mx

main :: IO ()
main = hspec spec

spec :: Spec
spec = do 

  describe "firstFunctorLaw" $ do
    context "firstFunctorLaw with Just type" $ do
      it "should be True" $
        firstFunctorLaw (Just ('c', 35)) `shouldBe` True

    context "firstFunctorLaw with list type" $ do
      it "should be True" $
        firstFunctorLaw [2, 3, 5, 7, 11] `shouldBe` True
    

  describe "secondFunctorLaw" $ do
    context "secondFunctorLaw with isAlpha and fst applied to Just ('c', 35)" $ do
      it "should be True" $
        secondFunctorLaw isAlpha fst (Just ('c', 35)) `shouldBe` True

    context "secondFunctorLaw with chr and (+96) applied to [2,3,5,7,11]" $ do
      it "should be True" $
        secondFunctorLaw chr (+96) [2,3,5,7,11] `shouldBe` True



  describe "firstFunctorLaw for Either String (Maybe Integer)" $ do
    context "with Left value" $
      it "should be True" $
        firstFunctorLaw (Left "err" :: Either String (Maybe Integer)) `shouldBe` True

    context "with Right Nothing" $
      it "should be True" $
        firstFunctorLaw (Right Nothing :: Either String (Maybe Integer)) `shouldBe` True

    context "with Right (Just k)" $
      it "should be True" $
        firstFunctorLaw (Right (Just 42) :: Either String (Maybe Integer)) `shouldBe` True

  describe "secondFunctorLaw for Either String (Maybe Integer)" $ do
    context "with Left value" $
      it "should be True" $
        secondFunctorLaw f g (Left "err" :: Either String (Maybe Integer)) `shouldBe` True

    context "with Right Nothing" $
      it "should be True" $
        secondFunctorLaw f g (Right Nothing :: Either String (Maybe Integer)) `shouldBe` True

    context "with Right (Just k)" $
      it "should be True" $
        secondFunctorLaw f g (Right (Just 42) :: Either String (Maybe Integer)) `shouldBe` True