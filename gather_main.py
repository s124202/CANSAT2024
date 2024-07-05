import time
import bluetooth
import threading

import motor
import purple_detection
import gps

def blt():
    global send
    global receive
    global synchro
    send = 0
    receive = 0
    synchro = 0

    server_sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    port = 1
    server_sock.bind(("",port))
    server_sock.listen(1)

    client_sock,address = server_sock.accept()
    print("Accepted connection from ",address)

    while True:
        if synchro == 1:
            print("synchro")
            break
        try:
            data = client_sock.recv(1024)
            receive = data
            print("received" + data)
            time.sleep(1)
            client_sock.send(str(send))

        except KeyboardInterrupt:
            print("finish")
            break
        except bluetooth.btcommon.BluetoothError as err:
            print("close")
            break


    client_sock.close()
    server_sock.close()


def wait(number):
    #子機の発見を待つ
    global receive
    receive = "0"

    while True:
        confirm = receive
        print(confirm)
        if confirm == number:
            print("confirmed")
            break
        else:
            print("waiting")
        time.sleep(3)


def main():
    global send
    global receive
    global synchro

    #自身のgps取得
    main_lat,main_lon = gps.gps_float()
    time.sleep(1)

    #子機に緯度を送信
    send = main_lat

    #子機の受信報告確認
    wait(1)
    send = 0
    time.sleep(5)

    #子機に経度を送信
    send = main_lon

    #子機の受信報告確認
    wait(2)
    send = 0
    time.sleep(5)


    #子機が来るのを待つ
    wait(3)
    time.sleep(3)

    #完了
    synchro = 1
    print("success to gather")

if __name__ == "__main__":
    thread1 = threading.Thread(target = main)
    thread2 = threading.Thread(target = blt)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()