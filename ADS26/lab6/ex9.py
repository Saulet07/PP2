# s = list(input())

# for i in range(len(s)):
#     for j in range(len(s) - 1):
#         if s[j] > s[j + 1]:
#             s[j], s[j + 1] = s[j + 1], s[j]
# print(" ".join(s))
s = input()
a = "".join(sorted(s))
print(a)