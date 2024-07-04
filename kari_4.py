import bluetooth
import time

count = 0

bd_addr = "B8:27:EB:A9:05:AB" # サーバー側のデバイスアドレスを入力

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
    try:
        data = client_sock.recv(1024)
        receive = data
        print("received [%s]" % data)
        time.sleep(1)
        client_sock.send(str(send))

    except KeyboardInterrupt:
        print("finish")
        break
    except bluetooth.btcommon.BluetoothError as err:
        print("close")
        break
        

sock.close()
