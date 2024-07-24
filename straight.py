import math
import time

import bmx055
import motor
import calibration

def main():
    kp = 0.4
    kd = 3

    s_l = 30
    s_r = s_l

    magx, magy, magz = bmx055.mag_dataRead()
    theta_correct = calibration.angle(magx,magy)
    theta_correct = calibration.standarize_angle(theta_correct)
    theta_old = theta_correct

    for i in range (50):
        magx, magy, magz = bmx055.mag_dataRead()
        theta = calibration.angle(magx,magy)
        theta = calibration.standarize_angle(theta_correct)
        mp = (theta_correct - theta) * kp
        md = (theta - theta_old) * kd
        m = mp - md

        m = min(m,5)
        m = max(m,-5)

        strength_l = s_l - m
        strength_r = s_r + m

        motor.motor_move(strength_l, strength_r, 0.05)
        theta_old = theta



if __name__ == "__main__":
    bmx055.bmx055_setup()
    motor.setup()

    main()
