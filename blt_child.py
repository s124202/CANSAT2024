import bluetooth
import time

from main_const import *

def main(send,timeout_count=30):
    bd_addr = BLT_ADRESS # サーバー側のデバイスアドレスを入力
    port = 1

    for i in range(timeout_count):
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
            time.sleep(2)
            if i == timeout_count - 1:
                print("blt connect timeout")
                return
            pass

    for i in range(5):
        try:
            time.sleep(1)
            sock.send(str(send))
            data = sock.recv(1024)
            receive = data.decode()
            print(receive)
            if receive == str(send):
                print("synchro")
                break
        except KeyboardInterrupt:
            print("finish")
            break
        except bluetooth.btcommon.BluetoothError as err:
            print("close")
            break
    sock.close()


if __name__ == "__main__":
    main(1)