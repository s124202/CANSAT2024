import bluetooth
import time

def main(send): 
    try:
        server_sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        port = 1
        server_sock.bind(("",port))
        server_sock.listen(1)
<<<<<<< HEAD
        server_sock.settimeout(30)
=======
        server_sock.settimeout(10)
>>>>>>> 85536d0a5a4e3dc5efbf38102dfdde3499b133ba
        client_sock,address = server_sock.accept()
        client_sock.settimeout(10)
        print("Accepted connection from ",address)
        for i in range(15):
            try:
                data = client_sock.recv(1024)
                receive = data.decode()
                print(receive)
                time.sleep(1)
                client_sock.send(str(send))
                if receive == str(send):
                    print("synchro")
                    break
            except KeyboardInterrupt:
                print("finish")
                break
            except bluetooth.btcommon.BluetoothError as err:
                print("close")
                break
        client_sock.close()
        server_sock.close()
    except KeyboardInterrupt:
        print("finish")
        client_sock.close()
        server_sock.close()
    except:
<<<<<<< HEAD
        print("blt connect timeout")
=======
        try:
            server_sock.close()
            client_sock.close()
        except:
            pass
        print("blt connect timeout")
    
    print("correct finish")
>>>>>>> 85536d0a5a4e3dc5efbf38102dfdde3499b133ba

if __name__ == "__main__":
    main(1)