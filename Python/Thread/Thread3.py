from threading import Thread
import time

def method1():
    print("This is daemon method 1")
    print("This is daemon method 2")
    time.sleep(2)
    print("This is daemon method 3")
    print("This is daemon method 4 ")
    

t1=Thread(target=method1, daemon=False)
t1.start()