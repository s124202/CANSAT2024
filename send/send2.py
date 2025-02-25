#2024/07/08 生川
#target=11

#standard
import serial
import sys
import argparse
import time

#send
import send.hexdump as hexdump
import send.mode0 as mode0
import send.mode3 as mode3
#import hexdump
#import mode0
#import mode3


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("serial_port", default="/dev/ttyAMA0", nargs='?')
    parser.add_argument("-b", "--baud", default="9600")
    parser.add_argument("-m", "--model", default="E220-900JP")
    parser.add_argument("-p", "--payload_length")
    parser.add_argument("-a", "--ascii_text")
    parser.add_argument("-f", "--fixed_mode", action="store_true", default=True)
    parser.add_argument("--target_address", default="11")
    parser.add_argument("--target_channel", default="0")

    args = parser.parse_args()

    return args


def send_log(result=None):
    args = get_args()

    if args.model == "E220-900JP":
        if args.fixed_mode:
            if (args.target_address != None) and (args.target_channel != None):
                t_addr = int(args.target_address)
                t_addr_H = t_addr >> 8
                t_addr_L = t_addr & 0xFF
                t_ch = int(args.target_channel)
                payload = bytes([t_addr_H, t_addr_L, t_ch])
            else:
                print("INVALID")
                return
        else:
            payload = bytes([])

        if result != None:
            payload += result.encode('utf-8')  # resultをバイト形式にエンコードして追加

        if args.payload_length != None:
            count = int(args.payload_length) // 256
            if count > 0:
                payload = payload + bytes(range(256))
                for i in range(count - 1):
                    payload = payload + bytes(range(256))
                payload = payload + bytes(range(int(args.payload_length) % 256))
            else:
                payload = payload + bytes(range(int(args.payload_length)))
        elif args.ascii_text != None:
            payload = payload + args.ascii_text.encode('utf-8')
        elif result == None:
            with open('ascii_data.txt', 'rb') as f:
                payload = payload + f.read()

        print("serial port:")
        print(args.serial_port)
        print("周波数：")
        print(920.6 + int(args.target_channel) * 0.2)

        print("send data hex dump:")
        hexdump.hexdump(payload, result='print')

        with serial.Serial(args.serial_port, int(args.baud), timeout=None) as ser:
            while True:
                if ser.out_waiting == 0:
                    break
            ser.write(payload)
            ser.flush()
            print("SENT")

    else:
        print("INVALID")
        return


#mode変更含む
def log(message):

    #change_mode0
    mode0.mode0_change()

    #send
    send_log(message)

    #change_mode3
    #mode3.mode3_change()


if __name__ == "__main__":
    message = "sample"
    log("sample")
