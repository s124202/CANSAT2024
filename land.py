import time

import bme280
import bmx055

def land_main():
    time_start = time.time()
    time_timeout = 15

    press_thd = 0.5
    gyr_thd = 1

    #気圧によるチェック
    press_array = [0]
    press_array.append(bme280.bme280_read()[1])
    while True:
        press_count = 0

        for i in range(5):
            press_array.pop(0)
            time.sleep(0.2)
            press_array.append(bme280.bme280_read()[1])
            print(press_array)
            press_gap = abs(press_array[0] - press_array[1])

            if press_gap < press_thd:
                press_count += 1
            else:
                break

        if press_count == 5:
            print("press_ok")
            break
        if time.time() - time_start > time_timeout:
            print("press_timeout")
            break

    #角速度によるチェック
    gyr_array = [0]
    gyr_array.append(bmx055.gyr_dataRead())
    while True:
        gyr_count = 0

        for i in range(5):
            gyr_array.pop(0)
            time.sleep(0.2)
            gyr_array.append(bmx055.gyr_dataRead())
            print(gyr_array)
            gyr_x_gap = abs(gyr_array[0][0] - gyr_array[1][0])
            gyr_y_gap = abs(gyr_array[0][1] - gyr_array[1][1])
            gyr_z_gap = abs(gyr_array[0][2] - gyr_array[1][2])

            if gyr_x_gap < gyr_thd and gyr_y_gap < gyr_thd and gyr_z_gap < gyr_thd:
                gyr_count += 1
            else:
                break

        if gyr_count == 5:
            print("gyr_ok")
            break
        if time.time() - time_start > time_timeout:
            print("gyr_timeout")
            break

if __name__ == "__main__":
    bme280.bme280_setup()
    bme280.bme280_calib_param()
    bmx055.bmx055_setup()

    try:
        land_main()

    except KeyboardInterrupt:
        print("\r\n")
    except Exception as e:
        print(e)