import bluetooth
import time

count = 0

server_sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)

port = 1
server_sock.bind(("",port))
server_sock.listen(1)

client_sock,address = server_sock.accept()
print("Accepted connection from ",address)

while True:
    try:
        time.sleep(1)
        sock.send(str(send))
        data = sock.recv(1024)
        receive = data
        print("received [%s]" % data)

    except KeyboardInterrupt:
        print("finish")
        break
    except bluetooth.btcommon.BluetoothError as err:
        print("close")
        break

client_sock.close()
server_sock.close()

