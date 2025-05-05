module TypeClassesSpec where


import Test.Hspec
import TypeClasses


spec :: Spec
spec = do
 describe "Vec creation" $ do -- Q1
   it "should create a Vec with a list of Double values" $ do
     let vec = Vec [1.0, 2.0, 3.0, 4.0]
     vec `shouldBe` Vec [1.0, 2.0, 3.0, 4.0]


   it "should create an empty Vec" $ do
     let vec = Vec []
     vec `shouldBe` Vec []


 describe "Vec Show instance" $ do -- Q2
   it "should display Vec [1.0, 2.0, 3.0]" $ do
     show (Vec [1.0, 2.0, 3.0]) `shouldBe` "Vec [1.0,2.0,3.0]"


   it "should display an empty Vec as Vec []" $ do
     show (Vec []) `shouldBe` "Vec []"


 describe "Vec Num instance" $ do -- Q3
   it "should add two Vecs element-wise" $ do
     Vec [1.0, 2.0] + Vec [3.0, 4.0] `shouldBe` Vec [4.0, 6.0]


   it "should subtract two Vecs element-wise" $ do
     Vec [5.0, 6.0] - Vec [3.0, 4.0] `shouldBe` Vec [2.0, 2.0]


   it "should multiply two Vecs element-wise" $ do
     Vec [2.0, 3.0] * Vec [4.0, 5.0] `shouldBe` Vec [8.0, 15.0]


   it "should compute the absolute value of a Vec" $ do
     abs (Vec [-1.0, -2.0]) `shouldBe` Vec [1.0, 2.0]


   it "should compute the signum of a Vec" $ do
     signum (Vec [-1.0, 0.0, 2.0]) `shouldBe` Vec [-1.0, 0.0, 1.0]


 describe "Vec Eq instance" $ do -- Q4
   it "should return True for equal Vecs" $ do
     Vec [1.0, 2.0] == Vec [1.0, 2.0] `shouldBe` True


   it "should return False for different Vecs" $ do
     Vec [1.0, 2.0] == Vec [2.0, 3.0] `shouldBe` False


 describe "Vec Ord instance" $ do -- Q5
   it "should compare two Vecs based on their sums" $ do
     Vec [1.0, 2.0] >= Vec [2.0, 1.0] `shouldBe` True
     Vec [1.0, 2.0] >= Vec [3.0, 1.0] `shouldBe` False


   it "should return the smaller Vec based on sum" $ do
     min (Vec [1.0, 2.0]) (Vec [3.0, 1.0]) `shouldBe` Vec [1.0, 2.0]


   it "should return the larger Vec based on sum" $ do
     max (Vec [1.0, 2.0]) (Vec [3.0, 1.0]) `shouldBe` Vec [3.0, 1.0]


 describe "VecT and magnitude" $ do -- Q6, Q7
   it "should compute the magnitude of a Vec" $ do
     magnitude (Vec [3.0, 4.0]) `shouldBe` 5.0


 describe "Vec Semigroup instance" $ do -- Q8
   it "should combine two Vecs with addition" $ do
     (Vec [1.0, 2.0] <> Vec [3.0, 4.0]) `shouldBe` Vec [4.0, 6.0]


 describe "Vec Monoid instance" $ do -- Q9
   it "should return the infinite zero Vec as mempty" $ do
     let (Vec xs) = mempty
     take 3 xs `shouldBe` [0, 0, 0]


   it "should combine two Vecs with mappend" $ do
     mappend (Vec [1.0, 2.0]) (Vec [3.0, 4.0]) `shouldBe` Vec [4.0, 6.0]


   it "should combine a list of Vecs with mconcat" $ do
     mconcat [Vec [1.0, 2.0], Vec [3.0, 4.0], Vec [5.0, 6.0]] `shouldBe` Vec [9.0, 12.0]