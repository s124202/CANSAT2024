import time

import release
import land
import bme280
import bmx055
import blt_child
#import para_fall_test

bme280.bme280_setup()
bme280.bme280_calib_param()
bmx055.bmx055_setup()

release.release_main()
time.sleep(1)

#blt_child.main(0)
#time.sleep(1)

land.land_main()
time.sleep(1)

blt_child.main(1)
time.sleep(1)


#para_fall_test.para_child_main()
