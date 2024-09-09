#2024/07/10　sato
#2024/07/10　shoji

import purple_detection
import run_following_EM2
import stuck
from main_const import *

import bluetooth
import threading
import time

def blt_adalt():
	global send
	global receive
	global synchro

	send = 0
	receive = "0"
	synchro = 0

	while True:
		
		try:
			server_sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
			port = 1
			server_sock.bind(("",port))
			server_sock.listen(1)
			server_sock.settimeout(10)
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

			print("try reconnect")
		except:
			print("finish")
			try:
				server_sock.close()
				client_sock.close()
			except:
				pass
			break
		if synchro == 1:
			break

def blt_child():
	global send
	global receive
	global synchro
	send = 0
	receive = "0"
	synchro = 0

	bd_addr = BLT_ADRESS # サーバー側のデバイスアドレスを入力

	port = 1

	for _ in range (10):
		try:
			sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
			sock.connect((bd_addr, port))
			print("connect success")
			break
		except:
			print("try again")
			time.sleep(1)
			pass

	while True:
		if synchro == 1:
			print("synchro")
			break
		try:
			time.sleep(1)
			sock.send(str(send))
			data = sock.recv(1024)
			receive = data.decode()

		except KeyboardInterrupt:
			print("finish")
			break
		except bluetooth.btcommon.BluetoothError as err:
			print("close")
			break

	sock.close()


#下に続く並列の関数を使用
def para_adalt():
	global send
	global receive
	global synchro

	purple_area = 0

	stuck.ue_jug()

	try:
		purple_area = purple_detection.detect_para()
		print(f'purple_area : {purple_area}')

		while True:
				if PARA_THD_COVERED < purple_area:
					print("Parachute on top")
					time.sleep(PARA_SLEEP)
					run_following_EM2.motor_move_default(60, 60, 2)
				else:
					break

		if purple_area > 100:
			print("Move Backward")
			run_following_EM2.move_default(-60, -60, 2)

		else:
			print("Move Forward")
			run_following_EM2.move_default(60, 60, 2) 
	
	except:
		print("Camera died")
		run_following_EM2.move_default(60, 60, 2) 
	
	#子機のパラ回避待ち
	send = 1
	time_start = time.time()
	while True:
		confirm = receive
		if confirm == str(1):
			print("child para avoid finish")
			break
		elif time.time() - time_start > PARA_BLT_TIMEOUT:
			print("partner timeout")
			break
		else:
			print("child para avoid waiting...")
		time.sleep(3)
	synchro = 1

#下に続く並列の関数を使用
def para_child():

	global send
	global receive
	global synchro

	#親機のパラ回避待ち
	time_start = time.time()
	while True:
		confirm = receive
		if confirm == str(1):
			print("start para avoid")
			break
		elif time.time() - time_start > PARA_BLT_TIMEOUT:
			print("partner timeout")
			break
		else:
			print("adalt para avoid waiting...")
		time.sleep(3)

	purple_area = 0

	stuck.ue_jug()

	try:
		purple_area = purple_detection.detect_para()
		print(f'purple_area : {purple_area}')

		while True:
				if PARA_THD_COVERED < purple_area:
					print("Parachute on top")
					time.sleep(PARA_SLEEP)
					run_following_EM2.motor_move_default(60, 60, 2)
				else:
					break

		if purple_area > 100:
			print("Move Backward")
			run_following_EM2.move_default(-60, -60, 2)

		else:
			print("Move Forward")
			run_following_EM2.move_default(60, 60, 2) 
	
	except:
		print("Camera died")
		run_following_EM2.move_default(60, 60, 2) 

	#親機に終了報告
	send = 1
	time.sleep(5)
	synchro = 1

#パラ回避(親機)
def para_adalt_main():
	thread1 = threading.Thread(target = blt_adalt)
	thread2 = threading.Thread(target = para_adalt)

	thread1.start()
	thread2.start()

	thread1.join()
	thread2.join()

#パラ回避(子機)
def para_child_main():
	thread1 = threading.Thread(target = blt_child)
	thread2 = threading.Thread(target = para_child)

	thread1.start()
	thread2.start()

	thread1.join()
	thread2.join()

if __name__ == "__main__":
	run_following_EM2.setup()
	para_adalt_main()
