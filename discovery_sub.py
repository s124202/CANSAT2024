import time
import bluetooth

import motor
import purple_detection

def blt():
    global send
    global receive
    global synchro
    send = 0
    receive = 0
    synchro = 0
    count = 0

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
            time.sleep(2)
            sock.send(str(send))
            count += 1

            # サーバーからのデータを受信
            if count == 3:
                data = sock.recv(1024)
                receive = data
                print("received [%s]" % data)
                count = 0
        except KeyboardInterrupt:
            print("finish")
            break
        except bluetooth.btcommon.BluetoothError as err:
            print("close")
            break

    sock.close()



def main():
    global send
    global receive
    global synchro

    #周辺を見回して親機を発見する
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

    #親機の方向調整を待つ
    while True:
        discovered = receive
        if discovered == "1":
            print("adjustment finish")
            break
        else:
            print("waiting")
        time.sleep(3)

    #追従準備完了
    synchro = 1
    print("ready to follow")