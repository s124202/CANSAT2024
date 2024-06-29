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
        data = client_sock.recv(1024)
        print("received [%s]" % data)
        count +=1

        # クライアントにデータを送信
        if count == 3:
            time.sleep(0.5)
            client_sock.send("Message from server!")
            count = 0
    except KeyboardInterrupt:
        print("finish")
        break

client_sock.close()
server_sock.close()

