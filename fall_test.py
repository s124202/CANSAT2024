#2024/07/10 生川

#standard
import time

#src
import src.bme280 as bme280
import src.bmx055 as bmx055

#detection
import release
import land
import melt

#setup
bme280.bme280_setup()
bme280.bme280_calib_param()
bmx055.bmx055_setup()

#release_phase
#phase_num = 1
release.release_main()

#land_phase
#phase_num = 2
land.land_main()

#melt_phase
#phase_num = 3
melt.melt_down()

#para_avoid_phase
#phase_num = 4