lst=[[10,20,30],[-5,-3,0],[26,72,92]]

c1 =0
c2 =0
c3 =0

for i in range(len(lst)):
    for j in range(len(lst)):
        if lst[i][j]>0:
            c1=c1+1
        elif lst[i][j]<0:
            c2=c2+1
        else:
            c3=c3+1

print("total postive no",c1)
print("total negative no",c2)
print("total zero",c3)


