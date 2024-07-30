import red_detection
import motor

def main():
	red_area = 0

	red_area = red_detection.detect_para()
	print(f'red_area : {red_area}')

	if red_area > 100:
		print("Move Backward")
		motor.move(-18, -15, 2)

	else:
		print("Move Forward")
		motor.move(16, 18, 2)

if __name__ == '__main__':
	motor.setup()

	main()