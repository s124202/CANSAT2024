import purple_detection
import time
#aaa

PARA_THD_COVERED = 30000
PARA_TIMEOUT = 60

def main():
	try:
		purple_area = purple_detection.detect_para()

		while True:
				if PARA_THD_COVERED < purple_area:
					print("Parachute on top")
					time.sleep(PARA_TIMEOUT)
					print("Go!!!")
				else:
					break
				
		if purple_area > 100:
			print("Move Backwward")

		else:
			print("Move Forward")

	except:
		print("Go!!!!!!!!!!!!!!!")
		

if __name__ == '__main__':
	main()