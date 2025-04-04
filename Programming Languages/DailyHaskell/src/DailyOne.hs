module DailyOne where

-- Q1 --
-- type: Integer
-- parameters: four integers for each constant and x in quadratic function
-- quadratic function 
-- return: result of quadratic equation using parameters (Integer)
quadratic :: Integer -> Integer -> Integer -> Integer -> Integer
quadratic a b c x = a + (b*x) + (c*(x*x))

-- Q2 --
-- type: Integer
-- parameters: scalar Integer, tuple vector containing two Integers
-- function that scales (multiplies) a vector
-- return: result of scaling vector by an Integer (Integer)
scaleVector :: Integer -> (Integer, Integer) -> (Integer, Integer)
scaleVector s (v1,v2) = (s*v1,s*v2)

-- Q3 --
-- type: Double
-- parameters: two three-tuples of Doubles representing three-dimensional points
-- function that finds the cartesian distance between the two points
-- return: result of cartesian equation (Double)
tripleDistance :: (Double, Double, Double) -> (Double, Double, Double) -> Double
tripleDistance (x1, y1, z1) (x2, y2, z2) = sqrt (((x2-x1)*(x2-x1))+((y2-y1)*(y2-y1))+((z2-z1)*(z2-z1)))