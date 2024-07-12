#2024/07/08 shoji

from smbus import SMBus
import time
import csv


bus_number  = 1
i2c_address = 0x76	#16進数76番でi2c通信

bus = SMBus(bus_number)

digT = []	#Temperature[℃]
digP = []	#Pressure[hPa]
digH = []	#Humidity[%]
t_fine = 0.0


ACC_ADDRESS = 0x19
ACC_REGISTER_ADDRESS = 0x02
GYR_ADDRESS = 0x69
GYR_REGISTER_ADDRESS = 0x02
MAG_ADDRESS = 0x13
MAG_REGISTER_ADDRESS = 0x42

i2c = SMBus(1)


#--　ポインタ/レジスタへの書き込み　--#
def writeReg(reg_address, data):
	bus.write_byte_data(i2c_address,reg_address,data)

#--　キャリブレーションパラメータの取得　--#
def bme280_calib_param():
	'''
	'''
	calib = []

	for i in range (0x88,0x88+24):
		calib.append(bus.read_byte_data(i2c_address,i))
	calib.append(bus.read_byte_data(i2c_address,0xA1))
	for i in range (0xE1,0xE1+7):
		calib.append(bus.read_byte_data(i2c_address,i))

	digT.append((calib[1] << 8) | calib[0])
	digT.append((calib[3] << 8) | calib[2])
	digT.append((calib[5] << 8) | calib[4])
	digP.append((calib[7] << 8) | calib[6])
	digP.append((calib[9] << 8) | calib[8])
	digP.append((calib[11]<< 8) | calib[10])
	digP.append((calib[13]<< 8) | calib[12])
	digP.append((calib[15]<< 8) | calib[14])
	digP.append((calib[17]<< 8) | calib[16])
	digP.append((calib[19]<< 8) | calib[18])
	digP.append((calib[21]<< 8) | calib[20])
	digP.append((calib[23]<< 8) | calib[22])
	digH.append( calib[24] )
	digH.append((calib[26]<< 8) | calib[25])
	digH.append( calib[27] )
	digH.append((calib[28]<< 4) | (0x0F & calib[29]))
	digH.append((calib[30]<< 4) | ((calib[29] >> 4) & 0x0F))
	digH.append( calib[31] )

	for i in range(1,2):
		if digT[i] & 0x8000:
			digT[i] = (-digT[i] ^ 0xFFFF) + 1

	for i in range(1,8):
		if digP[i] & 0x8000:
			digP[i] = (-digP[i] ^ 0xFFFF) + 1

	for i in range(0,6):
		if digH[i] & 0x8000:
			digH[i] = (-digH[i] ^ 0xFFFF) + 1

#--　気圧データ読み込み　--#
def compensate_P(adc_P):
	global  t_fine
	pressure = 0.0

	v1 = (t_fine / 2.0) - 64000.0
	v2 = (((v1 / 4.0) * (v1 / 4.0)) / 2048) * digP[5]
	v2 = v2 + ((v1 * digP[4]) * 2.0)
	v2 = (v2 / 4.0) + (digP[3] * 65536.0)
	v1 = (((digP[2] * (((v1 / 4.0) * (v1 / 4.0)) / 8192)) / 8)  + ((digP[1] * v1) / 2.0)) / 262144
	v1 = ((32768 + v1) * digP[0]) / 32768

	if v1 == 0:
		return 0
	pressure = ((1048576 - adc_P) - (v2 / 4096)) * 3125
	if pressure < 0x80000000:
		pressure = (pressure * 2.0) / v1
	else:
		pressure = (pressure / v1) * 2
	v1 = (digP[8] * (((pressure / 8.0) * (pressure / 8.0)) / 8192.0)) / 4096
	v2 = ((pressure / 4.0) * digP[7]) / 8192.0
	pressure = pressure + ((v1 + v2 + digP[6]) / 16.0)

	return pressure/100

def compensate_T(adc_T):
	'''
	温度データ読み込み
	'''
	global t_fine
	v1 = (adc_T / 16384.0 - digT[0] / 1024.0) * digT[1]
	v2 = (adc_T / 131072.0 - digT[0] / 8192.0) * (adc_T / 131072.0 - digT[0] / 8192.0) * digT[2]
	t_fine = v1 + v2
	temperature = t_fine / 5120.0
	return temperature

def compensate_H(adc_H):
	'''
	湿度データ読み込み
	'''
	global t_fine
	var_h = t_fine - 76800.0
	if var_h != 0:
		var_h = (adc_H - (digH[3] * 64.0 + digH[4]/16384.0 * var_h)) * (digH[1] / 65536.0 * (1.0 + digH[5] / 67108864.0 * var_h * (1.0 + digH[2] / 67108864.0 * var_h)))
	else:
		return 0
	var_h = var_h * (1.0 - digH[0] * var_h / 524288.0)
	if var_h > 100.0:
		var_h = 100.0
	elif var_h < 0.0:
		var_h = 0.0
	return var_h

#--　セットアップ　--#
def bme280_setup():
	osrs_t = 1			#Temperature oversampling x 1
	osrs_p = 1			#Pressure oversampling x 1
	osrs_h = 1			#Humidity oversampling x 1
	mode   = 3			#Normal mode
	t_sb   = 5			#Tstandby 1000ms
	filter = 0			#Filter off
	spi3w_en = 0		#3-wire SPI Disable

	ctrl_meas_reg = (osrs_t << 5) | (osrs_p << 2) | mode
	config_reg    = (t_sb << 5) | (filter << 2) | spi3w_en
	ctrl_hum_reg  = osrs_h

	writeReg(0xF2,ctrl_hum_reg)
	writeReg(0xF4,ctrl_meas_reg)
	writeReg(0xF5,config_reg)

#--　データ読み込み　--#
def bme280_read():
	try:
		data = []
		for i in range (0xF7, 0xF7+8):
			data.append(bus.read_byte_data(i2c_address,i))

		pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
		temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
		hum_raw  = (data[6] << 8)  |  data[7]

		temp = compensate_T(temp_raw)
		pres = compensate_P(pres_raw)
		hum = compensate_H(hum_raw)

		SeaLevelPres = 1013
		alt = ((temp+273.15)/0.0065)* (pow(SeaLevelPres / pres, (1/5.257)) - 1.0)
		value = [temp, pres, hum, alt]

		for i in range(len(value)):
			if value[i] is not None:
				value[i] = round(value[i], 4)
	except Exception as e:
		print(e)
		value = [0.0, 0.0, 0.0, 0.0]

	return value


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

def save_csv():

	bmx055_file = "bmx055_data_" + time.strftime("%m%d-%H%M%S") + ".csv"
	bme280_file = "bme280_data_" + time.strftime("%m%d-%H%M%S") + ".csv"
	
	f_bmx = open(bmx055_file,"w")
	writer_bmx = csv.writer(f_bmx)

	f_bme = open(bme280_file,"w")
	writer_bme = csv.writer(f_bme)

	try:
		while True:
			bmxData = bmx055_read()
			print(bmxData)
			writer_bmx.writerows([[time.time(),bmxData]])
			time.sleep(0.5)

			temp,pres,hum,alt = bme280_read()
			print("temp:" + str(temp) + "\t" + "pres:" + str(pres) + "\t" + "hum:" + str(hum) + "\t" + "alt: " + str(alt))
			writer_bme.writerows([[time.time(),pres]])
			time.sleep(0.5)

	except KeyboardInterrupt:
		print("\r\n")
		#f_bmx.close()
		#f_bme.close()

	except Exception as e:
		print(e)
		#f_bmx.close()
		#f_bme.close()

if __name__ =="__main__":

	bme280_setup()
	bme280_calib_param()
	bmx055_setup()

	save_csv()