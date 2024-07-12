import time

import release
import land
import bme280
import bmx055
import motor
import blt_child
import para_fall_test
import melt

bme280.bme280_setup()
bme280.bme280_calib_param()
bmx055.bmx055_setup()
motor.setup()

#放出判定
release.release_main()
time.sleep(1)

#放出判定確認
blt_child.main(0)
time.sleep(1)

#着地判定
land.land_main()
time.sleep(1)

#着地判定確認
blt_child.main(1)
time.sleep(1)

#テグス溶断
print("melt start")
melt.melt_down(17,3)
time.sleep(1)

#パラ回避
para_fall_test.para_child_main()