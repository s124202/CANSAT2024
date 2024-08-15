#2024/07/11 生川

#standard
import time
import pigpio


meltPin = 17

def melt_down(t_melt = 3.0):
	"""
	溶断回路を用いてテグスを溶断するための関数
	"""
	pi = pigpio.pi()

	pi.write(17, 0)
	time.sleep(1)
	pi.write(17, 1)
	time.sleep(t_melt)
	pi.write(17, 0)
	time.sleep(1)

	pi.stop()


if __name__ == "__main__":
	melt_down(t_melt = 3.0)