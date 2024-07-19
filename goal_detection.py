def main()
    '''
    Parameters
    ----------
    lat_dest : float
        目的地の緯度
    lon_dest : float
        目的地の経度
    thd_distance_goal : float
        画像誘導の範囲設定
    thd_red_area : float
        画面を占める赤色の割合の閾値 この割合を超えるとゴールしたと判定する
    '''

    area_ratio = 0
    angle = 0
    target_azimuth = 0
    isReach_goal = 0

    ###-----ゴールまでの距離を測定-----###
    lat_now, lon_now = gps.location()
    goal_info = gps_navigate.vincenty_inverse(lat_now, lon_now, lat_dest, lon_dest)
    distance_to_goal = goal_info['distance']
    print(f'{distance_to_goal}m')

    ###-----画像誘導モードの範囲内にいた場合の処理-----###
    if distance_to_goal <= thd_distance_goal:
        print('画像誘導モードの範囲内にいます\n画像誘導を行います')
        area_ratio, angle = TEST_detect_goal()
        mag_data = bmx055.mag_dataRead()
        mag_x, mag_y = mag_data[0], mag_data[1]
        rover_azimuth = calibration.angle(mag_x, mag_y, magx_off, magy_off)
        rover_azimuth = basics.standarize_angle(rover_azimuth)
        
        ###-----撮像した画像の中にゴールが映っていた場合の処理-----###
        if area_ratio >= thd_red_area:
            isReach_goal = 1
        elif 0 < area_ratio < thd_red_area:
            ###-----ゴールが真正面にあるときの処理-----###
            if angle == 2:
                # rover_azimuth はそのまま使用
                target_azimuth = rover_azimuth
            ###------ゴールが真正面にないときの処理------###
            ###-----目標角度を少しずらす-----###
            elif angle == 1:
                target_azimuth = rover_azimuth - 15
            elif angle == 3:
                target_azimuth = rover_azimuth + 15
                
            ###-----PID制御により前進-----###
            theta_array = [0]*5
            PID.PID_run(target_azimuth, magx_off, magy_off, theta_array=theta_array, loop_num=20)
            motor.deceleration(20, 20)
            motor.motor_stop(0.5)

        ###-----撮像した画像の中にゴールが映っていない場合の処理-----###
        elif area_ratio == 0:
            print('Lost Goal')
            pwr_unfound = 25 + add_pwr
            motor.motor_move(pwr_unfound, -pwr_unfound, 0.15)
            motor.motor_stop(0.5)
            target_azimuth = 000 #見つかっていない場合
    
    ###-----画像誘導モードの範囲外にいた場合の処理-----###
    else:
        print('ゴールから遠すぎます\nGPS誘導を行います')
        PID.drive2(lon_dest=LON_GOAL, lat_dest=LAT_GOAL, thd_distance=3, t_cal=T_CAL, loop_num=LOOP_NUM)
        target_azimuth = 000 #見つかっていない場合

    time.sleep(0.04) #9軸センサ読み取り用

    ###-----ゴールした場合の処理-----###
    if isReach_goal == 1:
        print('Goal')

    return isReach_goal