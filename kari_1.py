import csv
import time

def detect_csv():
    #init(csv)
    filename = time.strftime("%m%d-%H%M%S") + ".csv"
    f = open(filename, "w")
    writer = csv.writer(f)

    i = 1

    while True:
        try:

                print(i)
                writer.writerows([i])
                f.flush()
                i += 1

        finally:
            f.close()

detect_csv()