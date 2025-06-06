module DailyTen where



-- Q1 -- allLefts
-- type: [Either a b] -> [a]
-- parameters: list of Either values
-- function that returns a list of all Left values from a list of Either values
--returns list of Left values
allLefts :: [Either a b] -> [a]
allLefts ([] :: [Either a b]) = []
allLefts (Left x : items) = x : allLefts items
allLefts (_ : items) = allLefts items

-- Q2 -- produceStringOrSum
-- type: (Either String Integer) -> (Either String Integer) -> (Either String Integer)
-- parameters: two Either types
-- function that returns first string of two parameters or sum of two integers
-- returns first string or sum 
produceStringOrSum :: (Either String Integer) -> (Either String Integer) -> (Either String Integer)
produceStringOrSum (Left x) (_) = Left x
produceStringOrSum (_) (Left y) = Left y
produceStringOrSum (Right a) (Right b) = Right (a + b)


-- Q3 -- sumListOfEither 
-- type: [Either String Integer] -> (Either String Integer)
-- parameters: list of Either types
-- function that either returns first instance of a String or a sum of all integers
-- returns first string or sum 
sumListOfEither :: [Either String Integer] -> (Either String Integer)
sumListOfEither ([] :: [Either String Integer]) = Right 0
sumListOfEither (Left a : items) = Left a
sumListOfEither (Right b : items) =
	case sumListOfEither items of
		Right sum -> Right (b + sum)
		Left str -> Left str