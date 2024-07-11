#2024/07/11 shoji

import bluetooth
import time

def main(send):
    bd_addr = "B8:27:EB:1B:C5:BF" # サーバー側のデバイスアドレスを入力
    port = 1       

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