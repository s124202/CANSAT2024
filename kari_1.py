import bluetooth
import time

# デバイス2のBluetoothアドレス
bd_addr = "B8:27:EB:AD:E6:38"

port = 1

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bd_addr, port))

while True:
    # データを送信
    sock.send("1")
    print("Sent 1")

    # データを受信
    data = sock.recv(1024)
    print("Received: ", data)

    time.sleep(1)

sock.close()
