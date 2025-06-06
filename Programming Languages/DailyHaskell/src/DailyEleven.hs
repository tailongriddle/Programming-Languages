module DailyEleven where

import Data.Char


-- Q1 -- firstFunctorLaw
-- type: (Eq (f a), Functor f) => f a -> Bool
-- parameters: functor
-- function that returns true if first functor law applies
-- returns Boolean representing if first functor law is followed or not 
firstFunctorLaw :: (Eq (f a), Functor f) => f a -> Bool
firstFunctorLaw functor = if fmap id functor == functor
    then True
    else False 

-- Q2 -- secondFunctorLaw
-- type: (Eq (f c), Functor f) => (b -> c) -> (a -> b) -> f a -> Bool
-- parameters: functor
-- function that returns true if second functor law applies
-- returns Boolean representing if second functor law is followed or not 
secondFunctorLaw :: (Eq (f c), Functor f) => (b -> c) -> (a -> b) -> f a -> Bool
secondFunctorLaw functiona functionb functor = if fmap (functiona . functionb) functor == (fmap functiona (fmap functionb functor))
    then True
    else False