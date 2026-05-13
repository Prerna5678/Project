from threading import Thread
import time

def method1():
    print("Thread 1")
    time.sleep(2)

def method2():
    print("Thread 2")
    time.sleep(2)

def method3():
    print("Thread 3")
    time.sleep(2)

t1=Thread(target=method1)
t1=Thread(target=method1)
t1=Thread(target=method1)

