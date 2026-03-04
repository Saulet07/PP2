x = input()
vowel = ["a", "e", "i", "o", "u", "A", "E", "I", "O", "U"]
t = any(i in vowel for i in x)
if t:
    print("Yes")
else:
    print("No")