import time

import release
import land
import src.bme280 as bme280
import src.bmx055 as bmx055
import src.motor as motor
import blt.blt_adalt as blt_adalt
import para_fall_test

bme280.bme280_setup()
bme280.bme280_calib_param()
bmx055.bmx055_setup()
motor.setup()

#release.release_main()
#time.sleep(1)
#
#blt_adalt.main(0)
#time.sleep(1)
#
#land.land_main()
#time.sleep(1)
#
#blt_adalt.main(1)
#time.sleep(1)

para_fall_test.para_adalt_main()