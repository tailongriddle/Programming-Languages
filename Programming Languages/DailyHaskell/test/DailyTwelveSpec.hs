module DailyTwelveSpec where

import Test.Hspec
import DailyTwelve

main :: IO ()
main = hspec spec

spec :: Spec
spec = do

  describe "firstAppLaw" $ do
    context "firstAppLaw with Just type" $ do
      it "should be True" $
        firstAppLaw (Just ('c', 35)) `shouldBe` True
    
    context "firstAppLaw with List type" $ do
      it "should be True" $
        firstAppLaw [2, 3, 5, 7, 11] `shouldBe` True

  describe "secondLeft" $ do
    it "applies (+1) to [1,2,3]" $
      secondLeft (+1) [1,2,3] `shouldBe` [2,3,4]

    it "applies show to [10,20]" $
      secondLeft show [10,20] `shouldBe` ["10","20"]

    it "applies even to [] (empty list)" $
      secondLeft even [] `shouldBe` []

  describe "secondRight" $ do
    it "applies (+1) to [1,2,3]" $
      secondRight (+1) [1,2,3] `shouldBe` [2,3,4]

    it "applies show to [10,20]" $
      secondRight show [10,20] `shouldBe` ["10","20"]

    it "applies even to [] (empty list)" $
      secondRight even [] `shouldBe` []

  describe "secondAppLaw" $ do
    it "returns True for (+1) and [1,2,3]" $
      secondAppLaw (+1) [1,2,3] `shouldBe` True

    it "returns True for show and [10,20]" $
      secondAppLaw show [10,20] `shouldBe` True

    it "returns True for even and [] (empty list)" $
      secondAppLaw even [] `shouldBe` True
  
  describe "thirdAppLaw" $ do
    it "works for [(+1), (*2)] and 3" $
      thirdAppLaw [(+1), (*2)] 3 `shouldBe` True

    it "works for [reverse, tail] and \"abc\"" $
      thirdAppLaw [reverse, tail] "abc" `shouldBe` True

    it "works for [not] and True" $
      thirdAppLaw [not] True `shouldBe` True

  describe "fourthAppLaw" $ do
    it "works for [(+1)], [(2*)], [10]" $
      fourthAppLaw [(+1)] [(2*)] [10] `shouldBe` True

    it "works for [(++\"!\")], [reverse], [\"hi\"]" $
      fourthAppLaw [(++ "!")] [reverse] ["hi"] `shouldBe` True

    it "works for [(>0)], [length], [\"abc\",\"\",\"\"]" $
      fourthAppLaw [(>0)] ([length] :: [String -> Int]) ["abc", "", ""] `shouldBe` True
