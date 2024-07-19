import egdsk

def main(x):
    c = egdsk.plus(x)
    d = c + 2
    return d

if __name__ == '__main__':
    x=2
    d = main(x)
    print(d)