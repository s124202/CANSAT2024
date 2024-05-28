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

        try:
            while True:
                # データを受信
                data = client_sock.recv(1024)
                print("Received:", data)
        except bluetooth.btcommon.BluetoothError as error:
            print("BluetoothError:", error)
        finally:
            # クライアントソケットをクローズ
            client_sock.close()

# ソケットをクローズ
sock.close()
