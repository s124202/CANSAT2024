#2024/07/08 sato
#2024/07/09 shoji


import time
import math
import bluetooth
import threading

import bme280
import bmx055

def blt_adalt():
    global send
    global receive
    global synchro

    while True:
        send = 1
        receive = "1"
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
    send = 1
    receive = "1"
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


#1機体での着地判定
def land_alone_main():
	time_start = time.time()
	time_timeout = 300

	#閾値設定
	LAND_PRESS_THD = 0.05
	LAND_GYR_THD = 20
	LAND_ACC_THD = 0.2
	LAND_JUDGE_COUNT = 5
	LAND_JUDGE_TIME = 1

	#気圧による着地判定
	press_count = 0
	press_array = [0]
	press_array.append(bme280.bme280_read()[1])

	while True:
		press_array.pop(0)
		time.sleep(LAND_JUDGE_TIME)
		press_array.append(bme280.bme280_read()[1])
		if press_array[0] != 0 and press_array[1] != 0:
			delta_press = abs(press_array[0] - press_array[1])

			if delta_press < LAND_PRESS_THD:
				press_count += 1
			else:
				press_count = 0
		
		elif press_array[0] == 0 or press_array[1] == 0:
			print('Reading Press Again')
			press_count = 0
		
		print(press_array, press_count)
		
		if press_count == LAND_JUDGE_COUNT:
			print("Press OK")
			break

		if time.time() - time_start > time_timeout:
			print("Land Timeout")
			break
	
	#角速度による着地判定
	gyro_count = 0

	while True:
		time.sleep(LAND_JUDGE_TIME)
		bmxData = bmx055.bmx055_read()
		gyro_x = math.fabs(bmxData[3])
		gyro_y = math.fabs(bmxData[4])
		gyro_z = math.fabs(bmxData[5])

		if gyro_x < LAND_GYR_THD and gyro_y < LAND_GYR_THD and gyro_z < LAND_GYR_THD:
			gyro_count += 1
		else:
			gyro_count = 0

		print(gyro_x, gyro_y, gyro_z, gyro_count)

		if gyro_count == LAND_JUDGE_COUNT:
			print("Gyro OK")
			break

		if time.time() - time_start > time_timeout:
			print("Land Timeout")
			break
	
	#加速度(絶対値)による着地判定
	acc_count = 0
	acc_array = [0]
	bmxData = bmx055.bmx055_read()
	acc_abs = math.sqrt(bmx055[0]**2 + bmx055[1]**2 + bmx055[2]**2)
	acc_array.append(acc_abs)

	while True:
		acc_array.pop(0)
		time.sleep(LAND_JUDGE_TIME)
		bmxData = bmx055.bmx055_read()
		acc_abs = math.sqrt(bmx055[0]**2 + bmx055[1]**2 + bmx055[2]**2)
		acc_array.append(acc_abs)
		
		delta_acc = abs(acc_array[0] - acc_array[1])
		if delta_acc < LAND_ACC_THD:
			acc_count += 1
		else:
			acc_count = 0
		
		print(acc_array, acc_count)
		
		if acc_count == LAND_JUDGE_COUNT:
			print("Acceleration OK")
			break

		if time.time() - time_start > time_timeout:
			print("Land Timeout")
			break


#2機体で通信しながら着地判定
#下に続く並列の関数を使用
def land_together():

	global send
	global receive
	global synchro

	time_start = time.time()
	time_timeout = 300

	#閾値設定
	LAND_PRESS_THD = 0.05
	LAND_GYR_THD = 20
	LAND_ACC_THD = 0.2
	LAND_JUDGE_COUNT = 5
	LAND_JUDGE_TIME = 1

	#気圧による着地判定
	press_count = 0
	press_array = [0]
	press_array.append(bme280.bme280_read()[1])

	while True:
		press_array.pop(0)
		time.sleep(LAND_JUDGE_TIME)
		press_array.append(bme280.bme280_read()[1])
		if press_array[0] != 0 and press_array[1] != 0:
			delta_press = abs(press_array[0] - press_array[1])

			if delta_press < LAND_PRESS_THD:
				press_count += 1
			else:
				press_count = 0
		
		elif press_array[0] == 0 or press_array[1] == 0:
			print('Reading Press Again')
			press_count = 0
		
		print(press_array, press_count)
		
		if press_count == LAND_JUDGE_COUNT:
			print("Press OK")
			break

		if time.time() - time_start > time_timeout:
			print("Land Timeout")
			break
	
	#角速度による着地判定
	gyro_count = 0

	while True:
		time.sleep(LAND_JUDGE_TIME)
		bmxData = bmx055.bmx055_read()
		gyro_x = math.fabs(bmxData[3])
		gyro_y = math.fabs(bmxData[4])
		gyro_z = math.fabs(bmxData[5])

		if gyro_x < LAND_GYR_THD and gyro_y < LAND_GYR_THD and gyro_z < LAND_GYR_THD:
			gyro_count += 1
		else:
			gyro_count = 0

		print(gyro_x, gyro_y, gyro_z, gyro_count)

		if gyro_count == LAND_JUDGE_COUNT:
			print("Gyro OK")
			break

		if time.time() - time_start > time_timeout:
			print("Land Timeout")
			break
	
	#加速度(絶対値)による着地判定
	acc_count = 0
	acc_array = [0]
	bmxData = bmx055.bmx055_read()
	acc_abs = math.sqrt(bmx055[0]**2 + bmx055[1]**2 + bmx055[2]**2)
	acc_array.append(acc_abs)

	while True:
		acc_array.pop(0)
		time.sleep(LAND_JUDGE_TIME)
		bmxData = bmx055.bmx055_read()
		acc_abs = math.sqrt(bmx055[0]**2 + bmx055[1]**2 + bmx055[2]**2)
		acc_array.append(acc_abs)
		
		delta_acc = abs(acc_array[0] - acc_array[1])
		if delta_acc < LAND_ACC_THD:
			acc_count += 1
		else:
			acc_count = 0
		
		print(acc_array, acc_count)
		
		if acc_count == LAND_JUDGE_COUNT:
			print("Acceleration OK")
			break

		if time.time() - time_start > time_timeout:
			print("Land Timeout")
			break

	#子機と通信して放出確認
	send = 1
	time_start = time.time()
	time_timeout = 60
	while True:
		confirm = receive
		print(confirm)
		if confirm == str(2):
			print("confirmed")
			break
		elif time.time() - time_start > 60:
			print("partner timeout")
			break
		else:
			print("waiting")
		time.sleep(3)  
	synchro = 1


#2機体で通信する場合はこれ(親機)
def land_adalt_main():
    thread1 = threading.Thread(target = blt_adalt)
    thread2 = threading.Thread(target = land_together)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

#2機体で通信する場合はこれ(子機)
def release_child_main():
    thread1 = threading.Thread(target = blt_child)
    thread2 = threading.Thread(target = land_together)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

if __name__ == "__main__":
	bme280.bme280_setup()
	bme280.bme280_calib_param()
	bmx055.bmx055_setup()

	try:
		land_alone_main()

	except KeyboardInterrupt:
		print("\r\n")
	except Exception as e:
		print(e)