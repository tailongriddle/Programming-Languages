module Parser where

import Control.Applicative
import Data.Char
import Error

-- a parser is a type that contains a function that goes from a String
-- to the pair of a result of the parse and the rest of the string.
-- To make it useful for parsing though, we will
-- produce a result of the type Either String (a, String)
--    a resulting Right value will contain a successful parsing of the input
--    a resulting Left value will contain some error which occurred during parsing of the input
-- 
-- The Parser type contains a field 'parse' which contains the parsing function
-- in a particular parser (an instance of the Parser type)
-- For example:
--     parse someParser "hello" will deconstruct someParser to extract the 
--     parsing function, and then apply the parsing function to the next parameter, 
--     "hello"
newtype Parser a = P { parse :: String -> Either ErrorType (a, String) }

-- item Parser
--    the item Parser is a parser that always reads one value, 
--    removes it from the front of the input, and produces a 
--    tuple containing the value and the remaining input.
-- All other Parsers will be constructed using this Parser!
item :: Parser Char
item = P (\case 
            [] -> Left NoParse
            (x:xs) -> Right (x,xs))

-- Examples using the item parser:
-- ghci> parse item "" 
-- Left "no more input"
-- ghci> parse item "abc"
-- produces:
--    Right ('a', "bc")

-- The Parser type is a Functor
-- define fmap over a Parser by applying the given function f to the 
-- result of the parse. We assume there might be more than one answer,
-- and if so, we map over each possible answer (which is a pair)
instance Functor Parser where
    -- fmap :: (a -> b) -> Parser a -> Parser b
    fmap f p = P (\inp -> 
                case parse p inp of
                    -- note that we need Left msg -> Left msg
                    -- since we are transforming Parser a to Parser b
                    -- and left-hand side is Left :: Either String [(a, String)]
                    -- and the right-hand side is Left :: Either String [(b, String)]
                    Left msg -> Left msg
                    Right (v, out) -> Right (f v, out))


-- the Parser type is Applicative
--   This allows Parsers to be 'chained' or composed together
instance Applicative Parser where
    -- pure :: a -> Parser a
    --    this returns the parser which simply returns the value (always) 
    --      without consuming any input
    pure v = P (\inp -> Right (v, inp))
    pfuns <*> px = P (\inp -> case parse pfuns inp of
                        Left msg -> Left msg 
                        Right (g, out) -> parse (fmap g px) out)

-- Example:
--    construct a parser using applicatives
--    this will parse the first 3 characters but return only the first and 3rd elements
three :: Parser (Char, Char)
three = (pure g) <*> item <*> item <*> item 
    where g x _ z = (x, z)

 -- ghci> parse three "abcdefg"
 -- produces:
 --    Right (('a','c'), "defg")

-- the Parser type is a Monad
--   This will allow 'do' notation when writing and using Parsers
instance Monad Parser where 
    -- (>>=) :: Parser a -> (a -> Parser b) -> Parser b
    p >>= f = P (\inp -> case parse p inp of 
                    Left msg -> Left msg
                    Right (v, out) -> parse (f v) out)


-- Example
--   construct a Parser using do notation
--   This Parser behaves the same as the three parser above
threeM :: Parser (Char, Char)
threeM = do 
    x <- item 
    _ <- item 
    z <- item 
    return (x, z)

 -- ghci> parse threeM "abcdefg"
 -- produces:
 --   Right (('a','c'), "defg")

errorParse :: ErrorType -> Parser a
errorParse t = P (\_ -> Left t)

-- define a parser that fails with a given message
noParse :: Parser a
noParse = errorParse NoParse

syntaxError :: String -> Parser a
syntaxError msg = errorParse $ SyntaxError msg 

failParse :: String -> Parser a
failParse msg = errorParse $ ParseError msg

-- the Parser type is an Alternative
--   This allows the creation of a Parser which 
--   are built from other Parsers. The other Parsers
--   represent "choices" or Alternatives. If any of the Alternative
--   Parsers succeed then the overall Parser succeeds.
instance Alternative Parser where 
     -- empty :: Parser a
    empty = syntaxError "Syntax error: nothing matches. each alternative parser failed"
    -- (<|>) :: Parser a -> Parser a -> Parser a 
    p <|> q = P (\inp -> case parse p inp of 
        -- ignore these two Left cases, but not any other Left cases
                     Left NoParse -> parse q inp
                     Left (ParseError _) -> parse q inp
                     otherParse -> otherParse)
                 

-- the following will not work until you import Control.Applicative into ghci:
-- ghci> parse empty "abc"
-- produces:
--    Left (SyntaxError "Syntax error: nothing matches. each alternative parser failed")
-- ghci> parse (item <|> return 'd') "abc"
-- produces:
--    Right ('a', "bc")
-- ghci> parse (empty <|> return 'd') "abc"
-- produces:
--    Right ('d', "abc")

-- We now have three basic parsers: 
--    item - which parses the first character of a non-empty input,
--    return v - which always succeeds with the value v and does not change the input, 
--    empty - which always fails

-- Define a parser that matches a single character which 
--   satisifies a given predicate function
satisfies :: (Char -> Bool) -> Parser Char
satisfies p = do 
    x <- item 
    if p x 
        then return x 
        else failParse (show x ++ " didn't match expected character")

digit :: Parser Char 
digit = satisfies isDigit

upper :: Parser Char 
upper = satisfies isUpper

lower :: Parser Char 
lower = satisfies isLower

letter :: Parser Char 
letter = satisfies isAlpha 

alphanum :: Parser Char 
alphanum = satisfies isAlphaNum 

-- this parser parses the given character
char :: Char -> Parser Char 
char x = satisfies (== x)

space :: Parser Char 
space = satisfies isSpace

breakChar :: Parser Char
breakChar = satisfies (\x -> isSpace x || x == ')' || x == '(')

-- this parser then takes that idea and parses an entire string
string :: String -> Parser String 
string [] = return []
string (x:xs) = char x >> string xs >> return (x:xs)
-- alternatively, we can write it as 
-- string (x:xs) = 
-- do 
--   char x
--   string xs 
--   return (x:xs)

-- the next two parsers implement "many" and "some" (zeroOrMore and oneOrMore)
-- which apply the parser repeatedly until it fails, 
-- with the result values from each successful
-- parse being returned in a list

-- zeroOrMore x = oneOrMore x <|> pure []
-- some x = (pure (:)) <*> x <*> zeroOrMore x
kleeneStar :: Alternative f => f a -> f [a]
kleeneStar x = kleenePlus x <|> pure []

zeroOrMore :: Alternative f => f a -> f [a]
zeroOrMore = kleeneStar

kleenePlus :: Alternative f => f a -> f [a]
kleenePlus x = (pure (:)) <*> x <*> kleeneStar x 

oneOrMore :: Alternative f => f a -> f [a]
oneOrMore = kleenePlus

ident :: Parser String
ident = do
  x <- lower
  xs <- zeroOrMore (satisfies (\c -> isAlphaNum c || c `elem` ("?-!*/<>=" :: [Char])))
  return (x:xs)
-- parse ident "abc def"


nat :: Parser Integer 
nat = do 
    xs <- oneOrMore digit
    -- notice, if Parser.some digit fails, then return 
    -- is never called and read is never executed
    return (read xs)
-- parse nat "123 abc"

eatspace :: Parser ()
eatspace = do 
    _ <- zeroOrMore space
    return ()
-- parse eatspace "   abc"


int :: Parser Integer
int = do 
    -- try to parse a -n
    char '-'
    n <- nat 
    return (-n)
    <|> 
    -- otherwise, just parse an integer
    nat 


-- since most languages allow spacing freely, we will write a parser
-- that consumes space before and after a function 
token :: Parser a -> Parser a 
token p = do 
    eatspace 
    v <- p 
    eatspace
    return v

spacedToken :: Parser a -> Parser a
spacedToken p = do 
    eatspace 
    v <- p
    zeroOrMore breakChar 
    return v

-- now we can use token to construct parsers based on it
identifier :: Parser String 
identifier = token ident 

-- an identifier that must be followed by a space
spacedIdentifier :: Parser String
spacedIdentifier = spacedToken ident 

natural :: Parser Integer
natural = token int 

symbol :: String -> Parser String 
symbol xs = token (string xs)

-- match a symbol, but there must be a trailing space!
spacedSymbol :: String -> Parser String
spacedSymbol xs = spacedToken (string xs)

natlist :: Parser [Integer]
natlist = do 
    eatspace
    symbol "["
    n <- natural
    ns <- zeroOrMore (symbol "," >> natural)
    symbol "]"
    eatspace
    return (n:ns)