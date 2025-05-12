module DailyNine where

-- Q1 -- onlyNothing
-- type: (a -> Maybe b) -> [a] -> Bool
-- parameters: function, list
-- function that returns true if function applied to list returns only Nothing, False otherwise
-- returns True or False Bool
onlyNothing :: (a -> Maybe b) -> [a] -> Bool
onlyNothing function [] = True
onlyNothing function (item : items) = case function item of
    Just v -> False
    Nothing -> onlyNothing function items

-- Q2 -- firstAnswer
-- type: (a -> Maybe b) -> [a] -> Maybe b
-- parameters: function, list
-- function that returns Just v if not Nothing, returns Nothing otherwise
-- returns Just v or Nothing
firstAnswer :: (a -> Maybe b) -> [a] -> Maybe b
firstAnswer function [] = Nothing
firstAnswer function (item : items) = case function item of
    Just v -> Just v
    Nothing -> firstAnswer function items

-- Q3 -- allAnswers 
-- type: (a -> Maybe[b]) -> [a] -> Maybe [b]
-- parmeters: function, list
-- function that returns all Just values in a list, or returns nothing
-- returns list of Just v or nothing
allAnswers :: (a -> Maybe[b]) -> [a] -> Maybe [b]
allAnswers function list = helper list []
  where
    helper [] acc = Just acc
    helper (item : items) acc = case function item of 
        Just v -> helper items (acc ++ v) -- add v to acc
        Nothing -> Nothing

