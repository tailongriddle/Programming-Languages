
def Permute(A, n, array, checkSet):
    num = 0

    if n == 1:
        num += 1
        array.append(A[:])
        checkSet.add(tuple(A))
        print(A)
        
    else:
        for k in range(n):
            num += Permute(A, n-1, array, checkSet)
            if n % 2 == 0:    
                A[k], A[n-1] = A[n-1], A[k]
            else:
                A[0], A[n-1] = A[n-1], A[0]
    return num

array = []
checkSet = set()

A = [1, 2, 3]
print(Permute(A, 3, array, checkSet))

A = [1, 2, 3,4]
print(Permute(A, 4, array, checkSet))
# A = [1, 2]
# print(Permute(A, 2,array, checkSet))
# A = [1, 2, 3,4,5]
# print(Permute(A, 5, array, checkSet))
# A = [1, 2, 3,4,5,6]
# print(Permute(A, 6,array, checkSet))

if len(array) != len(checkSet):
    print("FALSE")
else:
    print("TRUE")