#2024/07/08 生川

#standard
import math
import time
import pigpio
import numpy as np
import traceback
import csv

RX = 15
pi = None

ELLIPSOID_GRS80 = 1  # GRS80
ELLIPSOID_WGS84 = 2  # WGS84

# Long Axis Radius and Flat Rate
GEODETIC_DATUM = {
	ELLIPSOID_GRS80: [
		6378137.0,         # [GRS80] Long Axis Radius
		1 / 298.257222101,  # [GRS80] Flat Rate
	],
	ELLIPSOID_WGS84: [
		6378137.0,         # [WGS84] Long Axis Radius
		1 / 298.257223563,  # [WGS84] Flat Rate
	],
}

# Limited times of Iteration
ITERATION_LIMIT = 1000


def open_gps():
	global pi
	if pi is None:
		pi = pigpio.pi()
	
	for i in range (5):
		try:
			pi.set_mode(RX, pigpio.INPUT)
			pi.bb_serial_read_open(RX, 9600, 8)
			break
		except pigpio.error as e:
			print("Open gps Error")
			pass


def read_gps():
	global pi

	utc = -1.0
	Lat = -1.0
	Lon = 0.0
	sHeight = 0.0
	gHeight = 0.0
	value = [0.0, 0.0, 0.0, 0.0, 0.0]

	(count, data) = pi.bb_serial_read(RX)
	if count:
		if isinstance(data, bytearray):
			gpsData = data.decode('utf-8', 'replace')

		gga = gpsData.find('$GPGGA,')
		rmc = gpsData.find('$GPRMC,')
		gll = gpsData.find('$GPGLL,')

		if gpsData[gga:gga+20].find(",0,") != -1 or gpsData[rmc:rmc+20].find("V") != -1 or gpsData[gll:gll+60].find("V") != -1:
			utc = -1.0
			Lat = 0.0
			Lon = 0.0
		else:
			utc = -2.0
			if gpsData[gga:gga+60].find(",N,") != -1 or gpsData[gga:gga+60].find(",S,") != -1:
				gpgga = gpsData[gga:gga+72].split(",")

				if len(gpgga) >= 6:
					utc = gpgga[1]
					lat = gpgga[2]
					lon = gpgga[4]
					try:
						utc = float(utc)
						Lat = round(float(lat[:2]) + float(lat[2:]) / 60.0, 6)
						Lon = round(float(lon[:3]) + float(lon[3:]) / 60.0, 6)
					except:
						utc = -2.0
						Lat = 0.0
						Lon = 0.0
					if gpgga[3] == "S":
						Lat = Lat * -1
					if gpgga[5] == "W":
						Lon = Lon * -1
				else:
					utc = -2.0
				if len(gpgga) >= 12:
					try:
						sHeight = float(gpgga[9])
						gHeight = float(gpgga[11])
					except:
						pass

			if gpsData[gll:gll+40].find("N") != -1 and utc == -2.0:
				gpgll = gpsData[gll:gll+72].split(",")

				if len(gpgll) >= 6:
					utc = gpgll[5]
					lat = gpgll[1]
					lon = gpgll[3]
					try:
						utc = float(utc)
						Lat = round(float(lat[:2]) + float(lat[2:]) / 60.0, 6)
						Lon = round(float(lon[:3]) + float(lon[3:]) / 60.0, 6)
					except:
						utc = -2.0
					if gpgll[2] == "S":
						Lat = Lat * -1
					if gpgll[4] == "W":
						Lon = Lon * -1
				else:
					utc = -2.0
			if gpsData[rmc:rmc+20].find("A") != -1 and utc == -2.0:
				gprmc = gpsData[rmc:rmc+72].split(",")

				if len(gprmc) >= 7:
					utc = gprmc[1]
					lat = gprmc[3]
					lon = gprmc[5]
					try:
						utc = float(utc)
						Lat = round(float(lat[:2]) + float(lat[2:]) / 60.0, 6)
						Lon = round(float(lon[:3]) + float(lon[3:]) / 60.0, 6)
					except:
						utc = -1.0
						Lat = 0.0
						Lon = 0.0
					if(gprmc[4] == "S"):
						Lat = Lat * -1
					if(gprmc[6] == "W"):
						Lon = Lon * -1
				else:
					utc = -1.0
					Lat = -1.0
					Lon = 0.0
			if utc == -2.0:
				utc = -1.0
				Lat = -1.0
				Lon = 0.0

	value = [utc, Lat, Lon, sHeight, gHeight]
	for i in range(len(value)):
		if not (isinstance(value[i], int) or isinstance(value[i], float)):
			value[i] = 0
	return value


def close_gps():
	global pi
	if pi is not None:
		pi.bb_serial_read_close(RX)
		pi.stop()
		pi = None


def gps_data_read():
	'''
	GPSを読み込むまでデータをとり続ける関数
	'''
	try:
		while True:
			utc, lat, lon, sHeight, gHeight = read_gps()
			print('gps reading')
			if utc != -1.0 and lat != -1.0:
				break
			time.sleep(1)
		return utc, lat, lon, sHeight, gHeight
	except KeyboardInterrupt:
		close_gps()
		print("\r\nKeyboard Intruppted, Serial Closed")


#無限にGPS取得
def gps_main():
	data_string = ""
	try:
		open_gps()
		while True:
			utc, lat, lon, sHeight, gHeight = read_gps()
			if utc == -1.0:
				if lat == -1.0:
					print("Reading gps Error")
				else:
					print("Status V")

			else:
				print("utc:" + str(utc) + "\t" + "lat:" + str(lat) + "\t" + "lon:" + str(lon) + "\t" + "sHeight: " + str(sHeight) + "\t" + "gHeight: " + str(gHeight))
				data_string = f"utc:{utc}\nlat:{lat}\nlon:{lon}\nsHeight: {sHeight}\ngHeight: {gHeight}"
			time.sleep(1)
	except KeyboardInterrupt:
		close_gps()
		print("\r\nKeyboard Intruppted, Serial Closed")
		return data_string
	except:
		close_gps()
		print(traceback.format_exc())
		return data_string


#入力secGPS取得
def gps_limit(reset_time = 100):

	time_start = time.time()
	data_string = ""

	try:
		open_gps()
		while True:
			utc, lat, lon, sHeight, gHeight = read_gps()
			if utc == -1.0:
				if lat == -1.0:
					print("Reading gps Error")
					data_string = "GPS cannot be read"
				else:
					print("Status V")
					data_string = "GPS cannot be read"

			else:
				print("utc:" + str(utc) + "\t" + "lat:" + str(lat) + "\t" + "lon:" + str(lon) + "\t" + "sHeight: " + str(sHeight) + "\t" + "gHeight: " + str(gHeight))
				data_string = f"utc:{utc}\nlat:{lat}\nlon:{lon}\nsHeight: {sHeight}\ngHeight: {gHeight}"
			time.sleep(1)

			if time.time() - time_start > reset_time:
				print("end_gps")
				break
	except KeyboardInterrupt:
		print("\r\nKeyboard Intruppted, Serial Closed")
	except:
		print(traceback.format_exc())
	finally:
		close_gps()

	return data_string


#GPS取得したらすぐにfloatでlat,lon送信
#60sec_timeout
def gps_float(reset_time=60):

	time_start = time.time()
	gps_lat = 0
	gps_lon = 0

	try:
		open_gps()
		while True:
			utc, lat, lon, sHeight, gHeight = read_gps()
			if utc == -1.0:
				if lat == -1.0:
					print("Reading gps Error")
				else:
					print("Status V")

			else:
				print("utc:" + str(utc) + "\t" + "lat:" + str(lat) + "\t" + "lon:" + str(lon) + "\t" + "sHeight: " + str(sHeight) + "\t" + "gHeight: " + str(gHeight))
				gps_lat,gps_lon = lat,lon
				break

			time.sleep(1)

			if time.time() - time_start > reset_time:
				print("end_gps")
				break
	except KeyboardInterrupt:
		print("\r\nKeyboard Intruppted, Serial Closed")
	except:
		print(traceback.format_exc())
	finally:
		close_gps()

	return gps_lat,gps_lon


#GPSを20回取得したら中央値をfloatでlat,lon送信
#60sec_timeout
def gps_med(reset_time=60):

	time_start = time.time()
	gps_lat = []
	gps_lon = []

	try:
		open_gps()
		while len(gps_lat) < 20:
			utc, lat, lon, sHeight, gHeight = read_gps()
			if utc == -1.0:
				if lat == -1.0:
					print("Reading gps Error")
				else:
					print("Status V")

			else:
				print("utc:" + str(utc) + "\t" + "lat:" + str(lat) + "\t" + "lon:" + str(lon) + "\t" + "sHeight: " + str(sHeight) + "\t" + "gHeight: " + str(gHeight))
				gps_lat.append(lat)
				gps_lon.append(lon)
			
			time.sleep(1)

			if time.time() - time_start > reset_time:
				print("end_gps")
				break

	except KeyboardInterrupt:
		print("\r\nKeyboard Intruppted, Serial Closed")
	except:
		print(traceback.format_exc())
	finally:
		close_gps()

	if len(gps_lat) == 0 or len(gps_lon) == 0:
		return None, None

	gps_lat_median = np.median(gps_lat)
	gps_lon_median = np.median(gps_lon)

	return gps_lat_median,gps_lon_median

#print無し
#GPS取得したらすぐにfloatでlat,lon送信
#60sec_timeout
def gps_location(reset_time=60):

	time_start = time.time()
	gps_lat = 0
	gps_lon = 0

	try:
		open_gps()
		while True:
			utc, lat, lon, sHeight, gHeight = read_gps()
			if utc != -1.0 and lat != -1.0:
				gps_lat,gps_lon = lat,lon
				break

			time.sleep(1)

			if time.time() - time_start > reset_time:
				print("end_gps")
				break
	except KeyboardInterrupt:
		print("\r\nKeyboard Intruppted, Serial Closed")
	except:
		print(traceback.format_exc())
	finally:
		close_gps()

	return gps_lat,gps_lon

if __name__ == '__main__':
	a,b = gps_med()
	print(a,b)