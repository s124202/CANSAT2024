import time

import release
import land
import bme280

bme280.bme280_setup()
bme280.bme280_calib_param()

release.release_main()
time.sleep(2)
land.land_main()