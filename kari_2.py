#2024/07/30 生川

#standard
import time
import bluetooth

#src
import motor
import stuck

#send
#import send.mode3 as mode3

def blt():
	global send
	global receive
	global synchro

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

def main():
	aaa


if __name__ == "__main__":


	#target
	lat_test,lon_test = gps.med()

	print("移動してください")
	time.sleep(20)
	print("start")
	time.sleep(5)

	print("main")
	main(lat_test, lon_test)