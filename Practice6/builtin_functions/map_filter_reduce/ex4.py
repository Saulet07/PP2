from functools import reduce

nums = [1, 2, 3, 4]

prod = reduce(lambda a, b: a * b, nums)
print(prod)