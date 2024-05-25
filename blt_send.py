import bluetooth

bd_addr = "B8:27:EB:AD:E6:38"
port = 1

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bd_addr, port))

data = "Hello world!"
sock.send(data)

sock.close()