# 常にbluetooth通信にて受信する

import bluetooth
import time

def main():
    # Bluetoothポート番号
    port = 1
    
    # Bluetoothソケットを作成して接続を待機
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.bind(("", port))
    sock.listen(1)
    client_sock, client_info = sock.accept()
    print("Accepted connection from", client_info)
    
    data = client_sock.recv(1024)
    a = time.time()
    print(a)
        
    # ソケットをクローズ
    client_sock.close()
    sock.close()

if __name__ == "__main__":
    main()