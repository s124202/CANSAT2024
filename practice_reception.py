import bluetooth

# Bluetoothポート番号
port = 1

# Bluetoothソケットを作成して接続を待機
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.bind(("", port))
sock.listen(1)
print("Waiting for connection...")

while True:
        client_sock, client_info = sock.accept()
        print("Accepted connection from", client_info)
        data = client_sock.recv(1024)
        print("Received:", data)
