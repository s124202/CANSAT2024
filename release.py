#2024/07/08 sato
#2024/07/09 shoji
#2004/7/11 生川

import time
import bluetooth
import threading

import src.bme280 as bme280


def blt_adalt():
	global send
	global receive
	global synchro

	while True:
		send = 0
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



#1機体で気圧による放出判定
def release_alone_main():

	time_start = time.time()
	time_timeout = 300

	#閾値設定
	RELEASE_PRESS_THD = 0.2
	RELEASE_JUDGE_COUNT = 3
	RELEASE_JUDGE_TIME = 3

	press_count = 0
	press_array = [0]
	press_array.append(bme280.bme280_read()[1])

	while True:
		press_array.pop(0)
		time.sleep(RELEASE_JUDGE_TIME)
		press_array.append(bme280.bme280_read()[1])
		if press_array[0] != 0 and press_array[1] != 0:
			delta_press = press_array[1] - press_array[0]

			if delta_press > RELEASE_PRESS_THD:
				press_count += 1
			else:
				press_count = 0
		
		elif press_array[0] == 0 or press_array[1] == 0:
			print('Reading Press Again')
			press_count = 0

		print(press_array, press_count)

		if press_count == RELEASE_JUDGE_COUNT:
			print("Release Detected")
			break

		if time.time() - time_start > time_timeout:
			print("Release Timeout")
			break


#2機体で通信しながら気圧による放出判定
#下に続く並列の関数を使用
def release_together():

	global send
	global receive
	global synchro

	time_start = time.time()
	time_timeout = 300
	
	#閾値設定
	RELEASE_PRESS_THD = 0.2
	RELEASE_JUDGE_COUNT = 3
	RELEASE_JUDGE_TIME = 3

	press_count = 0
	press_array = [0]
	press_array.append(bme280.bme280_read()[1])

	while True:
		press_array.pop(0)
		time.sleep(RELEASE_JUDGE_TIME)
		press_array.append(bme280.bme280_read()[1])
		if press_array[0] != 0 and press_array[1] != 0:
			delta_press = press_array[1] - press_array[0]

			if delta_press > RELEASE_PRESS_THD:
				press_count += 1
			else:
				press_count = 0
		
		elif press_array[0] == 0 or press_array[1] == 0:
			print('Reading Press Again')
			press_count = 0

		print(press_array, press_count)

		if press_count == RELEASE_JUDGE_COUNT:
			print("Release Detected")
			break

		if time.time() - time_start > time_timeout:
			print("Release Timeout")
			break
	
	#子機と通信して放出確認
	send = 1
	time_start = time.time()
	time_timeout = 60
	while True:
		confirm = receive
		print(confirm)
		if confirm == str(1):
			print("confirmed")
			break
		elif time.time() - time_start > time_timeout:
			print("partner timeout")
			break
		else:
			print("waiting")
		time.sleep(3)  
	synchro = 1


#2機体で通信する場合はこれ(親機)
def release_adalt_main():
	thread1 = threading.Thread(target = blt_adalt)
	thread2 = threading.Thread(target = release_together)

	thread1.start()
	thread2.start()

	thread1.join()
	thread2.join()

#2機体で通信する場合はこれ(子機)
def release_child_main():
	thread1 = threading.Thread(target = blt_child)
	thread2 = threading.Thread(target = release_together)

	thread1.start()
	thread2.start()

	thread1.join()
	thread2.join()



if __name__ == "__main__":
	bme280.bme280_setup()
	bme280.bme280_calib_param()

	try:
		release_alone_main()

	except KeyboardInterrupt:
		print("\r\n")
	except Exception as e:
		print(e)