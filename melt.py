import time
import pigpio

pi = pigpio.pi()

meltPin = 11

def melt_down(meltPin, t_melt = 4.0):
	"""
	溶断回路を用いてテグスを溶断するための関数
	"""
	pi.write(meltPin, 0)
	time.sleep(1)
	pi.write(meltPin, 1)
	time.sleep(t_melt)
	pi.write(meltPin, 0)
	time.sleep(1)

if __name__ == "__main__":
	melt_down(meltPin=11, t_melt = 4.0)