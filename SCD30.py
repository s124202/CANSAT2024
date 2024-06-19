#scd30_sample.py

#input : none
#output : [CO2,temp,rh(hum?)]

#config
import time
from scd30_i2c import SCD30
import csv

scd30 = SCD30()

scd30.set_measurement_interval(2)
scd30.start_periodic_measurement()

f = open("scd30_save.csv","w")
writer = csv.writer(f)

def scd30_main():

	time.sleep(2)

	while True:
		try:
			if scd30.get_data_ready():
				m = scd30.read_measurement()
				if m is not None:
					#print(f"CO2: {m[0]:.2f}ppm, temp: {m[1]:.2f}'C, rh: {m[2]:.2f}%")
					print(f"CO2: {m[0]:.2f}ppm")
					writer.writerows([[time.time(),m[0]]])
				time.sleep(2)
			else:
				time.sleep(0.2)
		except KeyboardInterrupt:
			print("\r\n")
			f.close()

if __name__ == '__main__':
	scd30_main()