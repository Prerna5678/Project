class stack:
    
    def __init__(self):
        self.list=[]

    def push(self,data):
        self.list.append(data)
    
    def pop(self):
        self.list.pop()
    
    def display(self):
        print(self.list)

s1=stack()
s1.push(1)
s1.push(2)
s1.push(3)
s1.push(4)
s1.push(5)
s1.pop()
s1.display()