#2024/07/08 生川

#standard
import time
import csv

#src
import src.gps as gps

#send
import send.mode3 as mode3
import send.send as send

#run
import run.gps_navigate as gps_navigate


def main(lat_target = 35.918468,lon_target = 139.90712):

    #初期設定
    distance_thd = 5
    lat_now = 0
    lon_now = 0
    count = 0

    try:
        while True:
            #gps_get
            lat_now,lon_now = gps.gps_float()
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
                    print("5m以内に到達")
                    break

            else: 
                count = 0

            time.sleep(1)
    
    except KeyboardInterrupt:
        print("key_interrupt")


if __name__ == '__main__':
    mode3.mode3_change()
    lat_target1,lon_target1 = gps.gps_float()
    print("wait 3sec...")
    send.log(str(lat_target1))
    send.log(str(lon_target1))
    time.sleep(3)
    main(lat_target1,lon_target1)
    send.log("finish")