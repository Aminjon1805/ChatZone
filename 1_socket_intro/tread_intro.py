# 1. Import threading - it allows us to speed up programs by executing multiple tasks at the same  time
#    Each task will run its own task
#    Each tread can run simultaneously and share data
#    Every thread must do smth !!!

import threading



def func_1():
    for i in range(10):
        print("ONE ")

def func_2():
    for i in range(10):
        print("TWO ")

def func_3():
    for i in range(10):
        print("THREE ")


# If we call this functions, we see first function call MUST complete before the next
# They are executed in order
# func_1()
# func_2()
# func_3()

# We can execute this functions concurrently using threads! We must have a targe for a thread
t1 = threading.Thread(target=func_1)
t2 = threading.Thread(target=func_2)
t3 = threading.Thread(target=func_3)

t1.start()
t2.start()
t3.start()

# treads used only ones

# If you want to pause the program

t1 = threading.Thread(target=func_1)
t1.start()
t1.join()
print("Threading rule !!!")
 











