class Calculator:

    def __init__(self,a,b):
        self.a=a
        self.b=b

    def add(self,a,b):
        print(a+b)

    def subs(self,a,b):
        print(a-b) 
    
    def mult(self,a,b):
        print(a*b) 

    def div(self,a,b):
        print(a/b) 
    
    def display(self):
        print(self.a)
        print(self.b)

a=int(input("Enter the No. A:"))
b=int(input("Enter the No. B:"))
C1=Calculator(a,b)
C1.add(a,b)
C1.subs(a,b)
C1.mult(a,b)
C1.div(a,b)
C1.display()