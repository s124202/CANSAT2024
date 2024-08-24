#2024/07/19 生川

#standard
import time

#src
import src.gps as gps
import src.gps_navigate as gps_navigate

#send
import src.send.mode3 as mode3
import src.send.send_11 as send_11


#無限にGPS取得してログを送る
def loop(lat_target = 35.918468,lon_target = 139.90712):

    #初期設定
    lat_now = 0
    lon_now = 0

    try:
        while True:
            #gps_get
            lat_now,lon_now = gps.location()
            print("lat:" + str(lat_now) + "\t" + "lon:" + str(lon_now))

            #距離取得
            distance = gps_navigate.vincenty_inverse(lat_now, lon_now, lat_target, lon_target)
            distance_to_target = distance["distance"]
            print("distance:" + str(distance_to_target))

            #log
            send_11.log(str(lat_now) + "," + str(lon_now) + "," + str(distance_to_target))

            time.sleep(1)

    except KeyboardInterrupt:
        print("key_interrupt")


#main
def test():
    #target
    mode3.mode3_change()
    lat_target,lon_target = gps.location()
    send_11.log("target address")
    send_11.log(str(lat_target) + "," + str(lon_target))

    #main
    send_11.log("main start")
    loop(lat_target,lon_target)


if __name__ == '__main__':
    test()