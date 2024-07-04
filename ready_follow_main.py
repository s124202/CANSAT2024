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
    receive = 0
    synchro = 0
    count = 0

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
            print("received [%s]" % data)
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


def wait():
    #子機の発見を待つ
    global receive

    while True:
        discovered = receive
        if discovered == "1":
            print("discovered")
            break
        else:
            print("waiting")
        time.sleep(3)


def main():
    global send
    global receive
    global synchro

    #子機の発見を待つ
    wait()
    
    #目的地の方向を向いて子機がいるか確認

    #+++目的地に向く+++


    find = purple_detection.main_image()
    #子機がいた場合
    if find != 0.1:
        motor.move(30,-30,0.3)
        time.sleep(1)
        motor.move(80,80,3)
        time.sleep(1)
        motor.move(-30,30,0.3)
        time.sleep(1)


    #いない場合(正しい順序になっている)
    else:
        send = 1

    #bltリセット
    time.sleep(5)
    send = 0

    #子機の発見を待つ
    wait()
    
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
