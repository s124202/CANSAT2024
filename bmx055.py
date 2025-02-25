#2024/07/08 shoji

from smbus import SMBus
import time
import csv

ACC_ADDRESS = 0x19
ACC_REGISTER_ADDRESS = 0x02
GYR_ADDRESS = 0x69
GYR_REGISTER_ADDRESS = 0x02
MAG_ADDRESS = 0x13
MAG_REGISTER_ADDRESS = 0x42

i2c = SMBus(1)

def bmx055_setup():
	# --- BMX055ãSetup --- #
	#Initialize ACC
	
	for i in range (5):
		try:
			i2c.write_byte_data(ACC_ADDRESS, 0x0F, 0x03)	#Acc Scale  datasheet p57
			time.sleep(0.1)
			i2c.write_byte_data(ACC_ADDRESS, 0x10, 0x0F)	#Acc PMU  datasheet p57
			time.sleep(0.1)
			i2c.write_byte_data(ACC_ADDRESS, 0x11, 0x00)	#datasheet p58
			time.sleep(0.1)
			break
		except:
			time.sleep(0.1)
			print("BMX055 Setup Error")

	#Initialize GYR
	for i in range (5):
		try:
			i2c.write_byte_data(GYR_ADDRESS, 0x0F, 0x00)	#Gyro Scale  datasheet p99
			time.sleep(0.1)
			i2c.write_byte_data(GYR_ADDRESS, 0x10, 0x07)	#Acc PMU  datasheet p100
			time.sleep(0.1)
			i2c.write_byte_data(GYR_ADDRESS, 0x11, 0x00)	#datasheet p100
			time.sleep(0.1)
			break
		except:
			time.sleep(0.1)
			print("BMX055 Setup Error")

	#Initialize MAG

	for i in range (5):
		try:
			data = i2c.read_byte_data(MAG_ADDRESS, 0x4B)	#datasheet p134
			if(data == 0):
				i2c.write_byte_data(MAG_ADDRESS, 0x4B, 0x83)
				time.sleep(0.1)
			i2c.write_byte_data(MAG_ADDRESS, 0x4B, 0x01)	#datasheet p134
			time.sleep(0.1)
			i2c.write_byte_data(MAG_ADDRESS, 0x4C, 0x38)	#datasheet p135
			time.sleep(0.1)
			i2c.write_byte_data(MAG_ADDRESS, 0x4E, 0x84)	#datasheet p137
			time.sleep(0.1)
			i2c.write_byte_data(MAG_ADDRESS, 0x51, 0x04)	#datasheet p139
			time.sleep(0.1)
			i2c.write_byte_data(MAG_ADDRESS, 0x52, 0x0F)	#datasheet p139
			time.sleep(0.1)
			break
		except:
			time.sleep(0.1)
			print("BMX055 Setup Error")

	


def acc_dataRead():
	# --- Read Acc Data --- #
	accData = [0, 0, 0, 0, 0, 0]
	value = [0.0, 0.0, 0.0]
	for i in range(6):
		for k in range (5):
			try:
				accData[i] = i2c.read_byte_data(ACC_ADDRESS, ACC_REGISTER_ADDRESS+i)
				break
			except:
				pass

	for i in range(3):
		value[i] = (accData[2*i+1] * 16) + (int(accData[2*i] & 0xF0) / 16)
		value[i] = value[i] if value[i] < 2048 else value[i] - 4096
		value[i] = value[i] * 0.0098 * 1

	return value

def gyr_dataRead():
	# --- Read Gyro Data --- "
	gyrData = [0, 0, 0, 0, 0, 0]
	value = [0.0, 0.0, 0.0]
	for i in range(6):
		for k in range (5):
			try:
				gyrData[i] = i2c.read_byte_data(GYR_ADDRESS, GYR_REGISTER_ADDRESS+i)
				break
			except:
				pass

	for i in range(3):
		value[i] = (gyrData[2*i+1] * 256) + gyrData[i]
		value[i] = value[i] - 65536 if value[i] > 32767 else value[i]
		value[i] = value[i] * 0.0038 * 16

	return value

def mag_dataRead():
	# --- Read Mag Data --- #
	magData = [0, 0, 0, 0, 0, 0, 0, 0]
	value = [0.0, 0.0, 0.0]
	for i in range(8):
		for k in range (5):
			try:
				magData[i] = i2c.read_byte_data(MAG_ADDRESS, MAG_REGISTER_ADDRESS + i)
				break
			except:
				pass

	for i in range(3):
		if i != 2:
			value[i] = ((magData[2*i+1] *256) + (magData[2*i] & 0xF8)) / 8
			if value[i] > 4095:
				value[i] = value[i] - 8192
		else:
			value[i] = ((magData[2*i+1] * 256) | (magData[2*i] & 0xF8)) / 2
			if value[i] > 16383:
				value[i] = value[i] - 32768

	return value

def bmx055_read():
	# --- Read BMX055 Data --- #
	accx, accy, accz = acc_dataRead()
	gyrx, gyry, gyrz = gyr_dataRead()
	magx, magy, magz = mag_dataRead()

	#print("[%f, %f, %f] " % (accx, accy, accz), end="")
	#print("[%f, %f, %f] " % (gyrx, gyry, gyrz), end="")
	#print("[%f, %f, %f] " % (magx, magy, magz), end="")
	#print()

	value = [accx, accy, accz, gyrx, gyry, gyrz, magx, magy, magz]

	# --- Round Data --- #
	for i in range(len(value)):
		if value[i] is not None:
			value[i] = round(value[i], 4)

	return 	value

def bmx055_csv():

	filename = "bmx055_data_" + time.strftime("%m%d-%H%M%S") + ".csv"
	f = open(filename,"w")
	writer = csv.writer(f)
	try:
<<<<<<< HEAD
		for i in range(500):
			bmxData = bmx055_read()
			print(bmxData)
			writer.writerows([[time.time(),bmxData]])
			time.sleep(0.8)
	except KeyboardInterrupt:
		print("\r\n")
		f.close()
	except Exception as e:
		print(e)
		f.close()
=======
		for i in range(300):
			bmxData = bmx055_read()
			print(bmxData)
			writer.writerows([[time.time(),bmxData]])
			time.sleep(0.1)
	except KeyboardInterrupt:
		print("\r\n")
	except Exception as e:
		print(e)
>>>>>>> 85536d0a5a4e3dc5efbf38102dfdde3499b133ba


if __name__ == '__main__':
	#bmx055_setup()
	#bmx055_csv()
	try:
		bmx055_setup()
		time.sleep(0.2)
		while 1:
			bmxData = bmx055_read()
			print(bmxData)
<<<<<<< HEAD
			time.sleep(0.8)
=======
			time.sleep(0.05)
>>>>>>> 85536d0a5a4e3dc5efbf38102dfdde3499b133ba
	except KeyboardInterrupt:
		print("\r\n")
	except Exception as e:
		print(e)