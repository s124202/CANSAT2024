import bme280

bme280.bme280_calib_param()
bme280.bme280_setup()

a = bme280.bme280_read()

print(a)