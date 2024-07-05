import time

import src.gps as gps
import run.gps_navigate as gps_navigate

def main():

    #目標地点設定
    lat_target = 35.91709
    lon_target = 139.90647
    distance_thd = 5

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
            print("10m以内に到達")
            break

        time.sleep(1)


if __name__ == '__main__':
	main()