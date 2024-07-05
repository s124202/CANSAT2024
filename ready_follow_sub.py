import time
import bluetooth
import threading

import motor
import purple_detection

def blt():
    global send
    global receive
    global synchro
    send = 0
    receive = "0"
    synchro = 0

    bd_addr = "B8:27:EB:A9:05:AB" # サーバー側のデバイスアドレスを入力

    port = 1

    while True:
        try:
            sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            sock.connect((bd_addr, port))
            print("connect success")
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
            print("received" + receive)

        except KeyboardInterrupt:
            print("finish")
            break
        except bluetooth.btcommon.BluetoothError as err:
            print("close")
            break

    sock.close()

def look_around():
    #周辺を見回して親機を発見する
    global send
    count = 0

    while True:
        find = purple_detection.main_image()
        if find != 0.1:
            count += 1
            time.sleep(0.1)
            if count == 3:
                print("discover main")
                send = 1
                break
            continue

        motor.move(30,-30,0.3)
        time.sleep(1)

def main():
    global send
    global receive
    global synchro

    #周辺を見回して親機を発見する
    look_around()

    #親機の方向調整を待つ
    while True:
        discovered = receive
        if discovered == "1":
            print("adjustment finish")
            break
        else:
            print("waiting")
        time.sleep(3)

    #bltリセット
    time.sleep(5)
    send = 0

    #周辺を見回して親機を発見する
    look_around()

    #追従準備完了
    synchro = 1
    print("ready to follow")

if __name__ == "__main__":
    thread1 = threading.Thread(target = main)
    thread2 = threading.Thread(target = blt)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()