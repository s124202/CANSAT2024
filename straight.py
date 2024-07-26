import time

import bmx055
import motor
import calibration
import stuck

def main(motor_pwr, move_time):
    stuck.ue_jug
    
    kp = 3
    kd = 2
    
    s_l = motor_pwr
    s_r = s_l

    magx, magy, magz = bmx055.mag_dataRead()
    theta_correct = calibration.angle(magx,magy)
    theta_correct = calibration.standarize_angle(theta_correct)
    print(theta_correct)
    theta_old = theta_correct

    for i in range (int(move_time/0.05)):
        magx, magy, magz = bmx055.mag_dataRead()
        theta = calibration.angle(magx,magy)
        theta = calibration.standarize_angle(theta)
        print(theta)
        mp = (theta_correct - theta) * kp
        md = (theta - theta_old) * kd
        m = mp - md

        m = min(m,5)
        m = max(m,-5)

        strength_l = s_l + m
        strength_r = s_r - m

        motor.motor_move(strength_l, strength_r, 0.05)
        theta_old = theta
        time.sleep(0.05)
    motor.deceleration()

def test(motor_pwr, move_time):
    kp = float(input("kp"))
    kd = float(input("kd"))

    s_l = motor_pwr
    s_r = motor_pwr

    magx, magy, magz = bmx055.mag_dataRead()
    theta_correct = calibration.angle(magx,magy)
    theta_correct = calibration.standarize_angle(theta_correct)
    print(theta_correct)
    theta_old = theta_correct

    for i in range (int(move_time/0.05)):
        magx, magy, magz = bmx055.mag_dataRead()
        theta = calibration.angle(magx,magy)
        theta = calibration.standarize_angle(theta)
        print(theta)
        mp = (theta_correct - theta) * kp
        md = (theta - theta_old) * kd
        m = mp - md

        m = min(m,5)
        m = max(m,-5)

        strength_l = s_l - m
        strength_r = s_r + m

        motor.motor_move(strength_l, strength_r, 0.05)
        theta_old = theta
        time.sleep(0.05)
    motor.deceleration(s_l, s_r)

if __name__ == "__main__":
    bmx055.bmx055_setup()
    motor.setup()

    test(motor_pwr = 30, move_time = 2)