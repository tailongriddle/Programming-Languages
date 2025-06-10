module Error where

-- There are two kinds of errors, type errors and evaluation errors.
-- A type error denotes that during evaluation evaluated an incorrect type was found
--   (For example, a string operand is used in a mathematical addition). 
-- An evaluation error denotes that some other error occurred during evaluation.
--   (i.e. not enough parameters for a function call).
-- Both kinds of errors have an associated message describing the cause of the error.
-- NoEval denotes that no evaluation occurred.

data ErrorType = 
      TypeError String 
    | EvalError String 
    | SyntaxError String
    | ParseError String
    | EvalNotImplemented    -- the evaluation of this expression has not been implemented
    | NoParse               -- indicates a failure to parse (e.g. there was not a match)
    | NoEval                -- indicates that evaluation cannot proceed any further (e.g. there was not a match)
    | NoSymbol String 
    deriving (Show, Eq)
