from threading import Thread,Lock
import time

class MyThread(Thread):
    def __init__(self,lock):
        super().__init__()
        self.lock=lock

    def run(self):
        with self.lock:
            print("light is green")
            time.sleep(4)
            print("light is red")

lock=Lock()
t1=MyThread(lock)
t2=MyThread(lock)
t1.start()
t2.start()

