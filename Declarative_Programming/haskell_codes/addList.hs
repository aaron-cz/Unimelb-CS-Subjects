iota n
    | n == 0 = []
    | n > 0 = iota (n-1) ++ [n]
