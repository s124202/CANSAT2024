import time

import release
import land
import bme280
import bmx055
#import para_fall_test

bme280.bme280_setup()
bme280.bme280_calib_param()
bmx055.bmx055_setup()

#release.release_adalt_main()

time.sleep(3)

land.land_child_main()

#time.sleep(3)

#para_fall_test.para_adalt_main()

