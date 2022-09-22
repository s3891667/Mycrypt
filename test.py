# def mys(A, l, u, k):
#     if(l == u):
#         if(A[l] == k):
#             return 1
#         else:
#             return 0
#     else:
#         m = int((l+u-1)/2)
#         return mys(A, l, m, k) + mys(A, m+1, u, k)
# A = [0,1,2,3,4,5,6,7,8,9]
# print(mys(A,0,9,8))