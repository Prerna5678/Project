from threading import Thread

class Mythread(Thread):
    for i in range(1,6):
        print(i)

t1=Thread(target=Mythread)
t1.start()