import csv
import time

def detect_csv():
    filename = time.strftime("%m%d-%H%M%S") + ".csv"
    with open(filename, "w", newline='') as f:
        writer = csv.writer(f)
        i = 1
        while True:
            try:
                print(i)
                writer.writerow([i])
                f.flush()
                i += 1
                time.sleep(1)
            except KeyboardInterrupt:
                print("Process interrupted")
                break

detect_csv()
