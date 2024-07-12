import time

import land
import bme280
import bmx055
import motor
import blt_adalt
import para_fall_test
import melt

bme280.bme280_setup()
bme280.bme280_calib_param()
bmx055.bmx055_setup()
motor.setup()

#着地判定
land.land_main()
time.sleep(1)

#着地判定確認
blt_adalt.main(1)
time.sleep(1)

#テグス溶断
print("melt start")
melt.melt_down(17,3)
time.sleep(1)

#パラ回避
para_fall_test.para_adalt_main()