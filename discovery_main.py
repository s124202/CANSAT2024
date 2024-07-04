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
            count +=1

            # クライアントにデータを送信
            if count == 3:
                time.sleep(0.5)
                client_sock.send(str(send))
                count = 0
        except KeyboardInterrupt:
            print("finish")
            break


    client_sock.close()
    server_sock.close()


def main():
    global send
    global receive
    global synchro

    #子機の発見を待つ
    while True:
        discovered = receive
        if discovered == "1":
            print("discovered")
            break
        else:
            print("waiting")
        time.sleep(3)
    
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



    else:
        send = 1
    
    #追従準備完了
    synchro = 1
    print("ready to follow")
