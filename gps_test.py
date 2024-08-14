import time

import gps
import gps_navigate
import send.mode3 as mode3


def main(lat_dest, lon_dest):
    lat_now, lon_now = gps.location()
    direction = gps_navigate.vincenty_inverse(lat_now, lon_now, lat_dest, lon_dest)
    distance_to_dest, target_azimuth = direction["distance"], direction["azimuth1"]

    return distance_to_dest, target_azimuth


if __name__ == "__main__":
    #setup
    mode3.mode3_change()

    #standard
    #lat_dest, lon_dest = gps.med()
    lat_dest = 40.142276
    lon_dest = 139.987388

    #init
    count = 0
    distance_array = []
    azimuth_array = []

    #main
    print("#####-----main-----#####")
    try:
        while count < 30:
            distance_to_dest, target_azimuth = main(lat_dest, lon_dest)
            distance_array.append(distance_to_dest)
            azimuth_array.append(target_azimuth)
            print("distance:", distance_to_dest, "azumith:", target_azimuth)

            count += 1

    except KeyboardInterrupt:
        print("#####-----keyboard interrupt-----#####")

    #average
    avg_distance = sum(distance_array) / len(distance_array)
    print("平均誤差:", avg_distance)