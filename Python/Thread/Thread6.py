from threading import Thread
import time

def method1():
    for i in range(1,6):
        print("Green",i)
        time.sleep(3)
    

def method2():
    for i in range(1,6):
        print("Red",i)
        time.sleep(2)

t1=Thread(target=method1)
t2=Thread(target=method2)
t1.start()
t2.start()