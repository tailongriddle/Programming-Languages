--TEST
module DailySevenSpec where

import Test.Hspec
import DailySeven

main :: IO ()
main = hspec spec

spec :: Spec
spec = do

  describe "findLongest" $ do
    context "findLongest []" $ -- EMPTY LIST
      it "should return an empty string" $
        findLongest [] `shouldBe` ""

    context "findLongest [\"a\"]" $ -- SINGLE ELEMENT
      it "should return the single string" $
        findLongest ["a"] `shouldBe` "a"

    context "findLongest [\"a\", \"ab\", \"abc\"]" $ -- MULTIPLE ELEMENTS
      it "should return the longest string" $
        findLongest ["a", "ab", "abc"] `shouldBe` "abc"

    context "findLongest [\"hello\", \"world\", \"hi\"]" $ -- MULTIPLE ELEMENTS WITH DIFFERENT LENGTHS
      it "should return the longest string" $
        findLongest ["hello", "world", "hi"] `shouldBe` "hello"

    context "findLongest [\"same\", \"size\", \"test\"]" $ -- MULTIPLE ELEMENTS WITH SAME LENGTH
      it "should return the first longest string" $
        findLongest ["same", "size", "test"] `shouldBe` "same"

    context "findLongest [\"short\", \"longer\", \"longest\"]" $ -- MULTIPLE ELEMENTS WITH INCREASING LENGTHS
      it "should return the longest string" $
        findLongest ["short", "longer", "longest"] `shouldBe` "longest"

  describe "anyLarger" $ do
    context "anyLarger 5 []" $ -- EMPTY LIST
      it "should return False" $
        anyLarger 5 [] `shouldBe` False

    context "anyLarger 5 [1, 2, 3]" $ -- NO ELEMENT LARGER
      it "should return False" $
        anyLarger 5 [1, 2, 3] `shouldBe` False

    context "anyLarger 5 [1, 6, 3]" $ -- ONE ELEMENT LARGER
      it "should return True" $
        anyLarger 5 [1, 6, 3] `shouldBe` True

    context "anyLarger 5 [6, 7, 8]" $ -- ALL ELEMENTS LARGER
      it "should return True" $
        anyLarger 5 [6, 7, 8] `shouldBe` True

    context "anyLarger 5 [5, 5, 5]" $ -- ALL ELEMENTS EQUAL
      it "should return False" $
        anyLarger 5 [5, 5, 5] `shouldBe` False

    context "anyLarger (-1) [-2, -3, 0]" $ -- NEGATIVE AND POSITIVE NUMBERS
      it "should return True" $
        anyLarger (-1) [-2, -3, 0] `shouldBe` True

    context "anyLarger 10 [1, 2, 3, 10]" $ -- ONE ELEMENT EQUAL TO CHECK VALUE
      it "should return False" $
        anyLarger 10 [1, 2, 3, 10] `shouldBe` False
        

  describe "allNames" $ do
    context "allNames []" $ -- EMPTY LIST
      it "should return an empty string" $
        allNames [] `shouldBe` ""

    context "allNames [(\"John\", \"Doe\")]" $ -- SINGLE NAME
      it "should return the full name" $
        allNames [("John", "Doe")] `shouldBe` "John Doe "

    context "allNames [(\"John\", \"Doe\"), (\"Jane\", \"Smith\")]" $ -- MULTIPLE NAMES
      it "should return all names concatenated" $
        allNames [("John", "Doe"), ("Jane", "Smith")] `shouldBe` "John Doe Jane Smith "

    context "allNames [(\"A\", \"B\"), (\"C\", \"D\"), (\"E\", \"F\")]" $ -- MULTIPLE SHORT NAMES
      it "should return all names concatenated" $
        allNames [("A", "B"), ("C", "D"), ("E", "F")] `shouldBe` "A B C D E F "

    context "allNames [(\"\", \"Doe\"), (\"Jane\", \"\")]" $ -- EMPTY FIRST OR LAST NAME
      it "should handle empty first or last names" $
        allNames [("", "Doe"), ("Jane", "")] `shouldBe` " Doe Jane  "

