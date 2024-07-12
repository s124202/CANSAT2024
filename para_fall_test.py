#2024/07/10　sato
#2024/07/10　shoji
#2024/07/13 生川

import para_avoidance
import src.motor as motor

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
		except KeyboardInterrupt:
			print("finish")
			client_sock.close()
			server_sock.close()
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

	bd_addr = "B8:27:EB:1B:C5:BF" # サーバー側のデバイスアドレスを入力

	port = 1

	while True:
		try:
			sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
			sock.connect((bd_addr, port))
			print("connect success")
			break
		except:
			print("try again")
			time.sleep(3)
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
	#print("Improving the rover's posture")
	#stuck.correct_posture()

	print("#####-----Parachute Avoid Sequence: Start-----#####")

	print("Para Avoid Start")

	check_count = 0 #パラ回避用のカウンター
	red_area = 0
	PARA_THD_COVERED = 255000

	red_area = para_avoidance.detect_para()
	print(f'red_area : {red_area}')

	while True:
		if PARA_THD_COVERED < red_area:
			print("Parachute on top")
			motor.move(80, 80, 5)
		else:
			break

	if red_area > 1000:
		print("Move Backward")
		motor.move(-60, -60, 5) #徐々に減速するはず
		#motor.motor_stop(0.2)
	else:
		print("Move Forward")
		motor.move(60, 60, 5) #徐々に減速するはず
		#motor.motor_stop(0.2)
	
	#子機のパラ回避待ち
	send = 1
	time_start = time.time()
	time_timeout = 120
	while True:
		confirm = receive
		print(confirm)
		if confirm == str(1):
			print("child para avoid finish")
			break
		elif time.time() - time_start > time_timeout:
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
	time_timeout = 120
	while True:
		confirm = receive
		print(confirm)
		if confirm == str(1):
			print("start para avoid")
			break
		elif time.time() - time_start > time_timeout:
			print("partner timeout")
			break
		else:
			print("adalt para avoid waiting...")
		time.sleep(3)

	#print("Improving the rover's posture")
	#stuck.correct_posture()

	print("#####-----Parachute Avoid Sequence: Start-----#####")

	print("Para Avoid Start")

	check_count = 0 #パラ回避用のカウンター
	red_area = 0
	PARA_THD_COVERED = 255000

	red_area = para_avoidance.detect_para()
	print(f'red_area : {red_area}')

	while True:
		if PARA_THD_COVERED < red_area:
			print("Parachute on top")
			motor.move(80, 80, 5)
		else:
			break

	if red_area > 1000:
		print("Move Backward")
		motor.move(-60, -60, 5) #徐々に減速するはず
		#motor.motor_stop(0.2)
	else:
		print("Move Forward")
		motor.move(60, 60, 5) #徐々に減速するはず
		#motor.motor_stop(0.2)

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
	motor.setup()
	para_adalt_main()