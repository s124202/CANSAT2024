import time
import bluetooth
import threading
from queue import Queue

import motor
import purple_detection
import gps

def blt():
    global send
    global receive
    global synchro
    send = 0
    receive = "0"
    synchro = 0

    bd_addr = "B8:27:EB:1B:C5:BF" # サーバー側のデバイスアドレスを入力

    port = 1

    while True:
        try:
            sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            sock.connect((bd_addr, port))
            print("connect success")
            sock.settimeout(10)
            break
        except:
            print("try again")
            time.sleep(3)
            pass

    while True:
        if synchro == 1:
            print("synchro")
            break
        try:
            time.sleep(1)
            sock.send(str(send))
            data = sock.recv(1024)
            receive = data.decode()

        except KeyboardInterrupt:
            print("finish")
            break
        except bluetooth.btcommon.BluetoothError as err:
            print("close")
            break

    sock.close()


def gather(q):
    global send
    global receive
    global synchro

    receive = "0"


    #親機の緯度をもらう
    while True:
        main_lat = receive
        if main_lat != "0":
            main_lat = float(main_lat)
            break
        else:
            print("lat waiting")
        time.sleep(1)

    #緯度受信報告・bltリセット
    print(main_lat)
    send = 1
    receive = "0"
    time.sleep(5)

    #親機の経度をもらう
    while True:
        main_lon = receive
        if main_lon != "0":
            main_lon = float(main_lon)
            break
        else:
            print("lot waiting")
        time.sleep(1)
    
    #経度受信報告・bltリセット
    print(main_lon)
    send = 2
    time.sleep(5)

    #親機の元へ行く


    #親機に集合報告
    send = 3
    time.sleep(5)
    

    #完了
    synchro = 1
    print("success to gather")
    q.put([main_lat,main_lon])


def main():
    q = Queue()
    thread1 = threading.Thread(target = gather,args=(q,))
    thread2 = threading.Thread(target = blt)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    return q.get()

if __name__ == "__main__":
    lat_lon = main()
    print(lat_lon[0])
    print(lat_lon[1])