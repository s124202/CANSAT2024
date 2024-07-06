import bluetooth
import time

def blt():
    bd_addr = "B8:27:EB:A9:5B:64"
    port = 1

    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((bd_addr, port))
    a = time.time()
    sock.send("1")
    print(a)
    
    sock.close()


if __name__ == "__main__":

    blt()