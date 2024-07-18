import threading
import motor

import blt_sub


def main():
    thread1 = threading.Thread(target = motor.test)
    thread2 = threading.Thread(target = blt_sub.blt)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

if __name__ == "__main__":
    main()