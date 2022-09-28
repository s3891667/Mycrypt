def solving(array):
    newArray = []
    for num in array:
        if(abs(num) in newArray):
            continue
        else:
            newArray.append(abs(num))
    j = 0
    while j < len(newArray)-1:
        if (newArray[j] > newArray[j + 1]):
            temp = newArray[j]
            newArray[j] = newArray[j + 1]
            newArray[j + 1] = temp
            j = -1
        j += 1
    return newArray


array = [-15, -9, -6, -3, 1, 3, 6, 20]
# print(solving(array))


def mys(A, l, u, k):
    if(l == u):
        if(A[l] == k):
            return 1
        else:
            return 0
    else:
        m = int((l+u-1)/2)
        return mys(A, l, m, k) + mys(A, m+1, u, k)


A = [0, 1, 2, 8, 4, 5, 6, 7, 8, 9]
# print(mys(A, 6, 9, 8))
