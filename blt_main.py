import bluetooth
import time

def blt():
    global send
    global receive
    global synchro

    while True:
        send = 0
        receive = "0"
        synchro = 0
        
        try:
            server_sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            port = 3
            server_sock.bind(("",port))
            server_sock.listen(1)
            client_sock,address = server_sock.accept()
            client_sock.settimeout(10)
            print("Accepted connection from ",address)

            while True:
                if synchro == 1:
                    print("synchro")
                    break
                try:
                    data = client_sock.recv(1024)
                    receive = data.decode()
                    print(receive)
                    time.sleep(1)
                    client_sock.send(str(send))
                    send += 1
                except KeyboardInterrupt:
                    print("finish")
                    break
                except bluetooth.btcommon.BluetoothError as err:
                    print("close")
                    break
            client_sock.close()
            server_sock.close()

            print("try reconnect")
        except KeyboardInterrupt:
            print("finish")
            client_sock.close()
            server_sock.close()
            break
        if synchro == 1:
            break

if __name__ == "__main__":
    blt()