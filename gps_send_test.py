#2024/07/15 生川

#standard
import time
import traceback

#src
import src.gps as gps

#send
import send.send as send
import send.mode3 as mode3


def main(timelimit=30):

    #def
    time_start = time.time()
    result = 0

    #main
    try:
        while True:
            #change mode3
            mode3.mode3_change()

            #Get Gps
            result = gps.location()

            #send
            send.log(str(result))

            #timeout
            if time.time() - time_start > timelimit:
                print("timeout_sendProgram")
                send.log("timeout_sendProgram")
                break

    except KeyboardInterrupt:
        print("\r\nKeyboard Intruppted")
        send.log("\r\nKeyboard Intruppted")
    except:
        print(traceback.format_exc())


if __name__ == '__main__':
	main(100)