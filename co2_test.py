#2024/7/23 生川

#standard
import time
import csv
from scd30_i2c import SCD30

#src
import bme280
import bmx055
import co2_sensor as co2
import gps

#send
import send.mode3 as mode3
import send.send_11 as send


def main():
    #start
    print("start program")
    send.log("start program")

    time.sleep(1)

    #setup
    mode3.mode3_change()
    bmx055.bmx055_setup()
    bme280.bme280_setup()
    bme280.bme280_calib_param()
    scd30 = SCD30()
    scd30.set_measurement_interval(2)
    scd30.start_periodic_measurement()

    #const
    TIME_THD = 300

    time.sleep(1)

    #main
    start_time = time.time()
    try:
        while time.time() - start_time < TIME_THD:
            temp,pres,hum,alt = bme280.bme280_read()
            accx, accy, accz, gyrx, gyry, gyrz, magx, magy, magz = bmx055.bmx055_read()
            m_co2 = co2.scd30_get()
            lat,lon = gps.test()
            send.log(str(lat) + "," + str(lon) + "," + str(temp) + str(pres) + "," + str(hum) + "," + str(alt) + "," + str(accx) + "," + str(accy) + "," + str(accz) + "," + str(gyrx) + "," + str(gyrz) + "," + str(magx) + "," + str(magy) + "," + str(magz) + "," + str(m_co2))
            print("temp:" + str(temp) + "\t" + "pres:" + str(pres) + "\t" + "hum:" + str(hum) + "\t" + "alt: " + str(alt))
            print("accx:" + str(accx) + "\t" + "accy:" + str(accy) + "\t" + "accz:" + str(accz))
            print("gyrx:" + str(gyrx) + "\t" + "gyry:" + str(gyry) + "\t" + "gyrz:" + str(gyrz))
            print("magx:" + str(magx) + "\t" + "magy:" + str(magy) + "\t" + "magz:" + str(magz))
            print("co2:" + str(m_co2))
            print("lat:" + str(lat) + "\t" + "lon:" + str(lon))
    except KeyboardInterrupt:
        print("keyboard interrupt")
        send.log("keyboard interrupt")


if __name__ == '__main__':
    main()