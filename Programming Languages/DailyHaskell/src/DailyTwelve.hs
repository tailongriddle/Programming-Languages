module DailyTwelve where

-- Q1 -- firstAppLaw
-- type: (Eq (f a), Applicative f) => f a -> Bool
-- parameters: applicative value
-- function that verifies if first applicative law holds (pure id <*> x = x)
-- returns true if law holds, false if not
firstAppLaw :: (Eq (f a), Applicative f) => f a -> Bool
firstAppLaw app = (pure id <*> app) == app


-- Q2a -- secondLeft
-- type: (Applicative f) => (a -> b) -> f a -> f b
-- parameters: function and applicative value
-- function that applies a function to an applicative value
-- returns the result of applying the function to the applicative value
secondLeft :: (Applicative f) => (a -> b) -> f a -> f b 
secondLeft funct val = pure funct <*> val 


-- Q2b -- secondRight
-- type: (Applicative f) => (a -> b) -> f a -> f b
-- parameters: function and applicative value
-- function that applies a function to an applicative value
-- returns the result of applying the function to the applicative value
secondRight :: (Applicative f) => (a -> b) -> f a -> f b 
secondRight funct val = fmap funct val 


-- Q2c -- secondAppLaw
-- type: (Eq b, Applicative f) => (a -> b) -> f a -> Bool
-- parameters: function and applicative value
-- function that checks if second applicative law holds for the given function and value
-- returns true if the law holds, false if not
secondAppLaw :: (Eq (f b), Applicative f) => (a -> b) -> f a -> Bool
secondAppLaw funct val = secondLeft funct val == secondRight funct val

-- Q3 -- thirdAppLaw
-- type: (Eq (f b), Applicative f) => f (a -> b) -> a -> Bool
-- parameters: applicative function and value
-- function that checks if third applicative law holds: u <*> pure y = pure ($ y) <*> u
-- returns true if law holds, false if not
thirdAppLaw :: (Eq (f b), Applicative f) => f (a -> b) -> a -> Bool
thirdAppLaw u y = (u <*> pure y) == (pure ($ y) <*> u)

-- Q4 -- fourthAppLaw
-- type: (Eq (f c), Applicative f) => f (b -> c) -> f (a -> b) -> f a -> Bool
-- parameters: applicative functions and value
-- function that checks if fourth applicative law holds: pure (.) <*> u <*> v <*> w = u <*> (v <*> w)
-- returns true if law holds, false if not
fourthAppLaw :: (Eq (f c), Applicative f) => f (b -> c) -> f (a -> b) -> f a -> Bool
fourthAppLaw u v w = (pure (.) <*> u <*> v <*> w) == (u <*> (v <*> w))