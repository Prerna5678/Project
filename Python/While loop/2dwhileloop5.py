i = 1
while i<=5:
        j=1
        while j<=5:
            if i==1 or i==5 or j==1 or j==5 :
                print("*",end='')
            else:
                print(" ",end='')
            j=j+1
        i=i+1
        print()