# 常にbluetooth通信にて受信する

import bluetooth

def main():
    # Bluetoothポート番号
    port = 1
    
    # Bluetoothソケットを作成して接続を待機
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.bind(("", port))
    sock.listen(1)
    client_sock, client_info = sock.accept()
    print("Accepted connection from", client_info)
    
    # データを受信
    while True:
        data = client_sock.recv(1024)
        print("Received:", data)
    
        if data == "15":
            break
        
    # ソケットをクローズ
    client_sock.close()
    sock.close()