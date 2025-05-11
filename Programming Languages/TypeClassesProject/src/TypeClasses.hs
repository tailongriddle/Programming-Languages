module TypeClasses where




-- Q1 --
data Vec = Vec [Double] -- defines new type Vec, contains list of Doubles

-- Q2 --
instance Show Vec where
   show (Vec xs) = "Vec " ++ show xs -- converts the vector to a string representation


-- Q3 --
instance Num Vec where
   (Vec xs) + (Vec ys) = Vec (zipWith (+) xs ys) -- adds two vectors
   (Vec xs) - (Vec ys) = Vec (zipWith (-) xs ys) -- subtracts two vectors
   (Vec xs) * (Vec ys) = Vec (zipWith (*) xs ys) -- multiplies two vectors
   abs (Vec xs) = Vec (map abs xs) -- absolute value of each element in the vector
   signum (Vec xs) = Vec (map signum xs) -- signum of each element in the vector
   fromInteger n = Vec (repeat (fromInteger n)) -- creates a vector of infinite length with the same value


-- Q4 --
instance Eq Vec where
   (Vec xs) == (Vec ys) = and (zipWith (==) xs ys) -- checks if two vectors are equal


-- Q5 --
instance Ord Vec where
   (Vec xs) >= (Vec ys) = foldr (+) 0 xs >= foldr (+) 0 ys -- compares sum of two vectors
   compare (Vec xs) (Vec ys) = compare (foldr (+) 0 xs) (foldr (+) 0 ys) -- compares two vectors based on sum
   min (Vec xs) (Vec ys) = if foldr (+) 0 xs < foldr (+) 0 ys then Vec xs else Vec ys -- returns vector with smaller sum
   max (Vec xs) (Vec ys) = if foldr (+) 0 xs > foldr (+) 0 ys then Vec xs else Vec ys -- returns vector with larger sum

-- Q6 --
class VecT a where
   magnitude :: VecT a => a -> Double -- defines type class


-- Q7 --
instance VecT Vec where -- defines magnitiude
   magnitude (Vec xs) = sqrt (sum (map (^2) xs)) -- magnitude of a vector

-- Q8 --
instance Semigroup Vec where -- semigroup with addition
   (Vec xs) <> (Vec ys) = Vec (zipWith (+) xs ys) -- combines two vectors with addition


-- Q9 --
instance Monoid Vec where -- monoid with zero vector
   mempty = Vec (repeat 0) -- infinite zero vector
   mappend = (<>) -- <> operator
   mconcat [] = mempty -- empty list case
   mconcat vecs = foldr mappend mempty vecs -- all vectors using mappend




