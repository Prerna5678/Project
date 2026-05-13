a=[[1,2,3],[4,5,6],[7,8,9]]
c=0
for i in a:
    for j in i:
        c=j+c
        print(j,end='')
        print(c,end='')
    print()