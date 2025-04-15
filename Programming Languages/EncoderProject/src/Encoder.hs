module Encoder where

-- F1: removeChar -- 
-- type: Char, String -> String
-- parameters: character to find, string to find in
-- removes all instances of the character from the string recursively
-- return: string with no instances of given character
removeChar :: Char -> String -> String
removeChar _ [] = []
removeChar string (a:as) = if string == a
    then 
        removeChar string as
    else 
        a : removeChar string as

-- F2: removeWhitespace -- 
-- type: String -> String
-- parameters: string result from removeChar, string with no whitespaces
-- calls removeChar for all whitespace characters in a given string by composition
-- return: string with no instances of whitespaces
removeWhitespace :: String -> String
removeWhitespace = removeChar ' '  . removeChar '\n' . removeChar '\t' . removeChar '\r' 

-- F3: removePunctuation -- 
-- type: String -> String
-- parameters: string result from removeChar, string with no punctuation
-- calls removeChar for all punctuation characters in a given string by composition
-- return: string with no instances of punctuation
removePunctuation :: String -> String
removePunctuation = removeChar ',' . removeChar '.' . removeChar '(' . removeChar ')' . removeChar '[' . removeChar ']' . removeChar '{' . removeChar '}' 

-- F4: charsToAscii -- 
-- type: String -> [Int]
-- parameters: string of characters
-- converts characters in string to list of associated ASCII values
-- return: list of associated ASCII values
charsToAscii :: String -> [Int]
charsToAscii [] = []
charsToAscii (a:as) = fromEnum a : charsToAscii as

-- F5: asciiToChars -- 
-- type: [Int] -> String
-- parameters: list of ASCII values
-- converts list of ASCII values to associated string
-- return: associated string of characters
asciiToChars :: [Int] -> String
asciiToChars [] = []
asciiToChars (a:as) = toEnum a : asciiToChars as

-- F6: shiftInts -- 
-- type: Int -> [Int] -> [Int]
-- parameters: shift value, list of ints to shift
-- shifts list of ints by value given 
-- return: shifted list of ints
shiftInts :: Int -> [Int] -> [Int]
shiftInts _ [] = []
shiftInts shift (a:as) = (a+shift) `mod` 128 : shiftInts shift as


-- F7: shiftMessage -- EXTRA CREDIT COMPOSITION !!
-- type: Int -> String -> String
-- parameters: shift value, string to shift
-- shifts string by value given
-- return: shifted string
shiftMessage :: Int -> String -> String
shiftMessage shift = asciiToChars . shiftInts shift . charsToAscii




