import bluetooth
import threading
import time


def blt_send():
    
    bd_addr = "B8:27:EB:AD:E6:38"
    port = 1

    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((bd_addr, port))

    for i in range (30):
        sock.send(str(i))
        time.sleep(1)
    
    sock.close()
    
def blt_receive():
    # Bluetoothポート番号
    port = 3
    
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

if __name__ == "__main__":
    thread1 = threading.Thread(target = blt_send)
    thread2 = threading.Thread(target = blt_receive)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()