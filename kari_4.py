import bluetooth
import time

bd_addr = "B8:27:EB:A9:05:AB" # サーバー側のデバイスアドレスを入力

port = 1
sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bd_addr, port))

while True:

    try:
        time.sleep(2)
        sock.send("hello world!")
        # サーバーからのデータを受信
        data = sock.recv(1024)
        print("received [%s]" % data)
    except KeyboardInterrupt:
        print("finish")
        break

sock.close()
