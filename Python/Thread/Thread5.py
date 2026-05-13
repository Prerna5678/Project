from threading import Thread
from datetime import datetime
import time

def method1():
    for i in range(1,6):
        print("Time is now",i)
        print(datetime.now())
        time.sleep(1)

t1=Thread(target=method1)
t1.start()