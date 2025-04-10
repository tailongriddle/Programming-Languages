def convex_hull(S: list[Point]) -> list[Point]:
    '''
    Calculates the convex hull of a set of points using the brute force method described in class.
    S: list of points
    Return: list of points on the convex hull
    '''
    CH = []
    
  
    for i in S:
        for j in S:
            leftTurnCount = 0
            if j != i:
                for k in S:
                    if k != i or k != j:
                        if left_turn(i,j,k):
                            leftTurnCount += 1
                if leftTurnCount == 0 or leftTurnCount == len(S) - 2:
                    CH.add(i)
                    CH.add(j)
    return CH














