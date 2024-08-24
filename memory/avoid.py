#2024/08/07 生川

#src
import red_detection
import motor

#const
from main_const import *


def main():
	red_area = 0

	red_area = red_detection.detect_para()
	print(f'red_area : {red_area}')

	if red_area > 100:
		print("Move Backward")
		motor.move(-20, -20, 2)

	else:
		print("Move Forward")
		motor.move(20, 20, 2)

if __name__ == '__main__':
	motor.setup()

	main()