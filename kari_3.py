import bluetooth
import threading
import time

def blt_send(sock, bd_addr, port):
    sock.connect((bd_addr, port))

    for i in range (30):
        sock.send(str(i))
        time.sleep(1)

    sock.close()

def blt_receive(sock, port):
    sock.bind(("", port))
    sock.listen(1)
    client_sock, client_info = sock.accept()
    print("Accepted connection from", client_info)

    while True:
        data = client_sock.recv(1024)
        print("Received:", data)

        if data == "15":
            break

    client_sock.close()
    sock.close()

if __name__ == "__main__":
    bd_addr = "B8:27:EB:A9:5B:64"
    port_send = 3
    port_receive = 1

    sock_send = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock_receive = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    thread1 = threading.Thread(target = blt_send, args=(sock_send, bd_addr, port_send))
    thread2 = threading.Thread(target = blt_receive, args=(sock_receive, port_receive))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
