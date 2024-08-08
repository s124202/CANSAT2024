import threading
from queue import Queue
import time

def time_1():
	for i in range(5):
		print(i)
		time.sleep(1)
		if i == 3:
			return
		if i == 4:
			print("dame")

def time_2(a,b,q):
	c = a + b
	q.put(c)
	return

def main():
	q = Queue()
	
	thread1 = threading.Thread(target = time_1)
	thread2 = threading.Thread(target = time_2, args=(5,6,q,))

	thread1.start()
	thread2.start()

	thread1.join()
	thread2.join()

	return q.get()

if __name__ == "__main__":
	a = main()
	print(a)