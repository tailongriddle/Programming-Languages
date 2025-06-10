module Environment where

import qualified Data.List

-- Create an Empty Environment
emptyEnv :: [a]
emptyEnv = [] 

-- lookup a name in an Environment
--   Consume a name 
--   Produce Just val if the name is bound to val in the Environment
--     and Nothing if the name is not bound in the Environment
lookup :: Eq k => k -> [(k,v)] -> Maybe v
lookup = Data.List.lookup


-- bindName
--   Extend an Environment with a new name and value pair
--   In other words, bind the name to a given value
bindName :: n -> v -> [(n,v)] -> [(n,v)]
bindName name val env = (name, val) : env
