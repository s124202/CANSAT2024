import BME280

BME280.bme280_calib_param()
BME280.bme280_setup()

a = BME280.bme280_read()

print(a)