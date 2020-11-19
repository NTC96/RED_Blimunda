import threading
import time

print("hello thread")
a=0

def thread_function(name):

	print("Thread1 " + name)
	time.sleep(1)
	print("threa_+1")
	a=1
	print(a)




x = threading.Thread(target=thread_function, args=("2",))
x.start()
print("principal_")
print(a)
time.sleep(2)
print("principal_")
print(a)