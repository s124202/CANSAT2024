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
        time.sleep(2)
        sock.send("hello world!")
        count += 1

        # サーバーからのデータを受信
        if count == 3:
            data = sock.recv(1024)
            print("received [%s]" % data)
            count = 0
    except KeyboardInterrupt:
        print("finish")
        break
    except bluetooth.btcommon.BluetoothError as err:
        print("close")

sock.close()
