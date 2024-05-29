import time

def a():
    x = 10
    while True:
        print(x)
        time.sleep(1)
        x = x + 1
        if x == 10000:
            break
    return 0

if __name__ == '__main__':
    a()
