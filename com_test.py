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
    #change_mode3
    #mode3.mode3_change()

    #Get_Gps
    result = gps.location()
    print("gps:", result)

    #change_mode0
    #mode0.mode0_change()

    #sleep
    #print("wait 3sec...")
    #time.sleep(3)

    #send
    send.send_log(str(result))

    #sleep
    print("wait 1sec...")
    time.sleep(1)

if __name__ == '__main__':
    while True:
        main()