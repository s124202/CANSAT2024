import bluetooth
import time

def blt():
    global send
    global receive
    global synchro

    bd_addr = "B8:27:EB:1B:C5:BF" # サーバー側のデバイスアドレスを入力
    port = 1
    while True:
        send = 0
        receive = "0"
        synchro = 0
        
        while True:
            try:
                sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                sock.connect((bd_addr, port))
                sock.settimeout(10)
                print("connect success")
                break
            except KeyboardInterrupt:
                print("finish")
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
                send += 1
                data = sock.recv(1024)
                receive = data.decode()
                print(receive)
            except KeyboardInterrupt:
                print("finish")
                break
            except bluetooth.btcommon.BluetoothError as err:
                print("close")
                break

        sock.close()
        if synchro == 1:
            break
        print("try reconnect")


if __name__ == "__main__":
    blt()