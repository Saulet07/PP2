n = int(input())
gpa = {
    'A+':4.00,
    'A':3.75,
    'B+':3.50,
    'B':3.00,
    'C+':2.50,
    'C':2.00,
    'D+':1.50,
    'D':1.00,
    'F':0
}
ans = []
for _ in range(n):
    data = input().split()
    last_name = data[0]
    first_name = data[1]
    subject = int(data[2])
    total_gpa = 0
    total_credit = 0
    for i in range(subject):
        s = data[3 + i*2]
        c = int(data[4 + i*2])
        t = gpa[s]
        total = t * c
        total_gpa += total
        total_credit += c 
    sum = total_gpa / total_credit
    ans.append((sum, last_name, first_name))
ans.sort()
for sum, last_name, first_name in ans:
    print(last_name, first_name, f"{sum:.3f}")
