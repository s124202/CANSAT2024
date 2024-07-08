#2024/07/08 生川

#standard

#send
import send.send as send
import send.mode0 as mode0
import send.mode3 as mode3


def log(message):

    #change_mode0
    mode0.mode0_change()

    #send
    send.send_log(message)

    #change_mode3
    mode3.mode3_change()


if __name__ == '__main__':
    message = "sample"
    log(message)