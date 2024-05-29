import time
import threading
import bluetooth

def increment():
    global x
    x = 0

    while True:
        time.sleep(1)
        x = x + 1
        if x == 20:
            break
    return 0


def blt():
    global x
    x = 0

    bd_addr = "B8:27:EB:A9:5B:64"
    port = 1

    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((bd_addr, port))

    while True:
        sock.send(str(x))
        time.sleep(1)

        if x == 15:
            break
    
    sock.close()


if __name__ == "__main__":

    thread1 = threading.Thread(target = increment)
    thread2 = threading.Thread(target = blt)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
