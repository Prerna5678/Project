from threading import Thread
import time 

class Atm():
    for i in range(1,6):
        print("Welcome to ATM",i)
        time.sleep(3)

class bank():
    for i in range(1,6):
        print("Welcome to Customer",i)
        time.sleep(1)

t1=Thread(target=Atm)
t2=Thread(target=bank)
t1.start()
t2.start()