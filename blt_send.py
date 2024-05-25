import bluetooth

bd_addr = "14:18:C3:A4:CC:65"
port = 1

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bd_addr, port))

data = "Hello world!"
sock.send(data)

sock.close()