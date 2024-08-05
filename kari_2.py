#2024/07/30 生川

#standard
import time
import bluetooth
import threading

#src
import motor
import stuck

#send
#import send.mode3 as mode3

def blt():
	global send
	global receive
	global synchro

	send = 1
	receive = "0"
	synchro = 0
	
	try:
		server_sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		port = 1
		server_sock.bind(("",port))
		server_sock.listen(1)
		client_sock,address = server_sock.accept()
		client_sock.settimeout(10)
		print("Accepted connection from ",address)
		
		while True:
			if synchro == 1:
				print("synchro")
				break
			try:
				data = client_sock.recv(1024)
				receive = data.decode()
				print(receive)
				time.sleep(1)
				client_sock.send(str(send))
			except KeyboardInterrupt:
				print("finish")
				break
			except bluetooth.btcommon.BluetoothError as err:
				print("close")
				break
		client_sock.close()
		server_sock.close()
		
	except KeyboardInterrupt:
		print("finish")
		client_sock.close()
		server_sock.close()

def main():
	global send
	global receive
	global synchro
	
	send = 1
	receive = "0"

	#main
	try:
		for i in range(3):

			#子機を待たせる
			send = 1
			
			#stuck
			stuck.ue_jug()

			#cal(2sec)
			motor.move(30,-30,2)
			time.sleep(3)

			#adjust direction(3.6sec)
			for _ in range(3):
				motor.move(30,-30,0.1)
				time.sleep(0.5)
				motor.move(-30,30,0.1)
				time.sleep(0.5)
			
			#子機の発見待ち
			send = 2
			time.sleep(1)
			while (receive != str(1)):
				time.sleep(1)
			send = 0
			time.sleep(2)

			#move(2sec)
			motor.move(17,15,3)
			time.sleep(3)

	except KeyboardInterrupt:
		print("interrupt!")


if __name__ == "__main__":
	thread1 = threading.Thread(target = blt)
	thread2 = threading.Thread(target = main)

	motor.setup()
	
	thread1.start()
	thread2.start()

	thread1.join()
	thread2.join()