#2024/07/22 生川

#standard
import time
from scd30_i2c import SCD30


scd30 = SCD30()

scd30.set_measurement_interval(2)
scd30.start_periodic_measurement()


def scd30_main():
	time.sleep(2)

	while True:
		try:
			if scd30.get_data_ready():
				m = scd30.read_measurement()
				if m is not None:
					#print(f"CO2: {m[0]:.2f}ppm, temp: {m[1]:.2f}'C, rh: {m[2]:.2f}%")
					print(f"CO2: {m[0]:.2f}ppm")
				time.sleep(2)
			else:
				time.sleep(0.2)
		except KeyboardInterrupt:
			print("\r\n")
			break


def scd30_get():
	time.sleep(2)

	while True:
		try:
			if scd30.get_data_ready():
				m = scd30.read_measurement()
				if m is not None:
					break
				time.sleep(2)
			else:
				time.sleep(0.2)
		except KeyboardInterrupt:
			print("\r\n")

	return m[0]


if __name__ == '__main__':
	scd30_main()