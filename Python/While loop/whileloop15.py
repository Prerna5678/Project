i = 1
while i<7:
    if i==6:
        print(i,end='=')
    elif i%2==0:
        print(i,end='+')
    else:
        print(i,end='-')
    i = i+1
    