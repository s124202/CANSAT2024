import picamera
import time
import traceback
import os
import time

def fileName(f, ext):
	i = 0
	num = ""
	while 1:
		num = ""
		if(len(str(i)) <= 4):
			for j in range(4 - len(str(i))):
				num = num + "0"
			num = num + str(i)
		else:
			num = str(i)
		if not(os.path.exists(f + num + "." + ext)):
			break
		i = i + 1
	f = f + num + "." + ext
	return f

def Capture(path, width = 320, height = 240):
	filepath = ""
	try:
		with picamera.PiCamera() as camera:
			time.sleep(5)
			camera.rotation = 180
			camera.resolution = (width,height)	#(width,height)
			#camera.awb_mode = "sunlight"
			#camera.exposure_mode = "beach"
			filepath = fileName(path,"jpg")
			camera.capture(filepath)
	except picamera.exc.PiCameraMMALError:
		filepath = "Null"
		time.sleep(0.8)
	except:
		print(traceback.format_exc())
		time.sleep(0.1)
		filepath = "Null"

	return filepath

if __name__ == "__main__":
	try:
		photoName = Capture(" ", 320, 240)
		print(photoName)
	except KeyboardInterrupt:
		print('stop')
	except:
		print(traceback.format_exc())