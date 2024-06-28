import bluetooth
import time

# デバイス1のBluetoothアドレス
bd_addr = "B8:27:EB:A9:5B:64"

port = 1

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bd_addr, port))

while True:
    # データを受信
    data = sock.recv(1024)
    print("Received: ", data)

    # データを送信
    sock.send("2")
    print("Sent 2")

    time.sleep(1)

sock.close()
