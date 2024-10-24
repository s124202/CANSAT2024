<<<<<<< HEAD
#2024/07/10 生川

#standard
import time
import pigpio


meltPin = 17


def melt_down(meltPin, t_melt):
	"""
	溶断回路を用いてテグスを溶断するための関数
	"""
	pi = pigpio.pi()

=======
import time
import pigpio

pi = pigpio.pi()

meltPin = 17

def melt_down(meltPin, t_melt = 5.0):
	"""
	溶断回路を用いてテグスを溶断するための関数
	"""
>>>>>>> 85536d0a5a4e3dc5efbf38102dfdde3499b133ba
	pi.write(meltPin, 0)
	time.sleep(1)
	pi.write(meltPin, 1)
	time.sleep(t_melt)
	pi.write(meltPin, 0)
	time.sleep(1)

<<<<<<< HEAD
	pi.stop()


=======
>>>>>>> 85536d0a5a4e3dc5efbf38102dfdde3499b133ba
if __name__ == "__main__":
	melt_down(meltPin=17, t_melt = 5.0)