#2024/07/10 生川

#standard
import time

#src
import src.gps as gps

#send
import send.send as send
import send.mode0 as mode0
import send.mode3 as mode3


def main():
    #Get_Gps
    lat,lon = gps.location()
    print("lat:", lat)
    print("lon:", lon)

    #send
    send.log(str(lat))
    send.log(str(lon))

    #sleep
    time.sleep(1)

if __name__ == '__main__':
    mode3.mode3_change()
    send.log("program start")
    while True:
        main()