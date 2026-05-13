class Animal:
    def __init__(self):
            print("This is Amimal class")

class Dog(Animal):
    def Speak(self):
        print("This is dog")

class Cat(Animal):
    def Speak(self):
        print("This is cat")

class Cow(Animal):
    def Speak(self):
        print("This is cow")

list1=[Cow(),Dog(),Cat()]
for i in list1:
     i.Speak()