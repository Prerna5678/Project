from threading import Thread,current_thread
import time

def method(current_bal=0,add_amt=0):
    print("Detail",current_thread().name)
    time.sleep(1)

    print(f"Your current balance is{current_bal}",current_thread().name)
    time.sleep(2)

    print(f"Final Bank Balane Amount is{current_bal + add_amt}",current_thread().name)

t1=Thread(target=method,name="First Thread",args=(10000,500))
t2=Thread(target=method,name="Second Thread",args=(15000,500))

t1.start()
t2.start()