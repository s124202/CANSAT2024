import bluetooth
import time

def main(send):
    bd_addr = "B8:27:EB:B3:DE:30" # サーバー側のデバイスアドレスを入力
    port = 1
    timeout = 0 

    for i in range(10):
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
            time.sleep(1)
            if i == 9:
                timeout = 1
                break
            pass
    if timeout == 1:
        print("blt connect timeout")

    for i in range(10):
        try:
            if timeout == 1:
                break
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