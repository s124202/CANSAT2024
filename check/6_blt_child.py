import bluetooth
import time

from src.main_const import *

def main(send):
    bd_addr = BLT_ADRESS # サーバー側のデバイスアドレスを入力
    port = 1
    timeout = 0 

    for i in range(30):
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
            if i == 29:
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