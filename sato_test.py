import red_detection
import motor

motor.setup()

THD_RED_RATIO = 80

def main():
	isReach_goal = 0
	area_ratio, angle = red_detection.detect_goal()
	
	if 0 < area_ratio < THD_RED_RATIO:
		print('Found Goal')
		motor(10, 10, 3)
	elif area_ratio == 0:
		print('Lost Goal')
		pwr_unfound = 30
		motor.motor_move(pwr_unfound, -pwr_unfound, 0.15)
		motor.motor_stop(0.5)
		isReach_goal = 1
	
	return isReach_goal

if __name__ == '__main__':
	while True:
		isReach_goal = main()

		if isReach_goal == 1:
			break