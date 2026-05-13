from threading import Thread

def method1():
    #print("Hello from thread1")
    for i in range(5):
        print("Hello from thread1",i)
def method2():
    #print("Hello from thread2")
    for i in range(5):
        print("Hello from thread2",i)

t1=Thread(target=method1)
t2=Thread(target=method2)
t1.start()
t2.start()
print(t1.name)
print(t2.name)