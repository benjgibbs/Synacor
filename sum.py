from itertools import permutations

nums = [2,3,5,7,9]

for perm in permutations(nums):
    sum = perm[0] + perm[1] * perm[2] ** 2 + perm[3] ** 3 - perm[4]
    if sum == 399:
        print(perm)
