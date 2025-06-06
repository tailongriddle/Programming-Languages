module DailyTenSpec where

import Test.Hspec
import DailyTen

main :: IO ()
main = hspec spec 

spec :: Spec
spec = do
  
  describe "allLefts" $ do
    it "returns [] for an empty list" $
      allLefts ([] :: [Either String Int]) `shouldBe` []

    it "returns all Left values from a mixed list" $
      allLefts [Left "a", Right 1, Left "b", Right 2, Left "c"] `shouldBe` ["a", "b", "c"]

    it "returns [] when there are only Right values" $
      allLefts [Right 1, Right 2, Right 3] `shouldBe` ([] :: [Int])

    it "returns all values when all are Left" $
      allLefts [Left 10, Left 20, Left 30] `shouldBe` [10, 20, 30]


  describe "produceStringOrSum" $ do
    it "returns Left if the first argument is Left" $
      produceStringOrSum (Left "error1") (Right 10) `shouldBe` Left "error1"

    it "returns Left if the second argument is Left and the first is Right" $
      produceStringOrSum (Right 5) (Left "error2") `shouldBe` Left "error2"

    it "returns Left if both arguments are Left (first is returned)" $
      produceStringOrSum (Left "first") (Left "second") `shouldBe` Left "first"

    it "returns Right with the sum if both arguments are Right" $
      produceStringOrSum (Right 7) (Right 3) `shouldBe` Right 10

  describe "sumListOfEither" $ do
    it "returns Right 0 for an empty list" $
      sumListOfEither [] `shouldBe` (Right 0 :: Either String Integer)

    it "returns the sum for a list of only Right values" $
      sumListOfEither [Right 1, Right 2, Right 3] `shouldBe` (Right 6 :: Either String Integer)

    it "returns the first Left if it appears at the start" $
      sumListOfEither [Left "err", Right 2, Right 3] `shouldBe` Left "err"

    it "returns the first Left if it appears in the middle" $
      sumListOfEither [Right 1, Left "fail", Right 3] `shouldBe` Left "fail"

    it "returns the first Left if it appears at the end" $
      sumListOfEither [Right 1, Right 2, Left "bad"] `shouldBe` Left "bad"