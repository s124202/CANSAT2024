#2024/07/08 生川

#standard
import time
import csv

#src
import gps

#run
import run.gps_navigate as gps_navigate


def main(lat_target = 35.918468,lon_target = 139.90712):

    #初期設定
    distance_thd = 2
    lat_now = 0
    lon_now = 0
    count = 0

    try:
        while True:
            #gps_get
            lat_now,lon_now = gps.gps_med()
            print("現在")
            print("緯度：" + str(lat_now) + "\t" + "経度：" + str(lon_now))

            #距離取得
            distance = gps_navigate.vincenty_inverse(lat_now, lon_now, lat_target, lon_target)
            distance_to_target = distance["distance"]
            print("目標値までの距離：" + str(distance_to_target))

            #判定
            if distance_to_target < distance_thd:
                count += 1

                if count > 2:
                    print("10m以内に到達")
                    break

                else: 
                    count = 0

            time.sleep(1)
    
    except KeyboardInterrupt:
        print("key_interrupt")


if __name__ == '__main__':
    lat_target1,lon_target1 = gps.gps_med()
    print("wait 10sec...")
    time.sleep(10)
    main(lat_target1,lon_target1)