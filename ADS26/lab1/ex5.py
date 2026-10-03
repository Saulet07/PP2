n=int(input());f=[]
for i in range(2,int(n**.5)+1):
 while n%i==0:f+=[i];n//=i
if n>1:f+=[n]
print(*f)