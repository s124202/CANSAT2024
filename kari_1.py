import threading
import motor

import blt_main


def main():
    thread1 = threading.Thread(target = motor.test)
    thread2 = threading.Thread(target = blt_main.blt)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

if __name__ == "__main__":
    main()