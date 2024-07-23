# プログラム一覧

## receive
- config_gui.pyw : 設定反映用
- hexdump.py : なんか必要らしい
- PySimpleGUI.py : GUI設定用
- receive.py : 受信用

## run
- calibration.py : キャリブレーション用
- gps_navigate.py : 走行用GPS用
- stuck.py : スタック用

## send

## sorce
- bme280.py
- bmx055.py
- co2_sensor.py
- gps.py
- motor.py
- voc_index.py

## main
- gps_send.py
- pid_run.py
- co2_test.py
- voc_test.py
- melt.py

# 使用方法
## receive/config_gui.pyw
- receive用基板をつないだ状態で起動する。
- open>getで設定確認、変更したらset param
- 設定は基本的に、
    - チャネル：0
    - アドレス：ここを端末番号にして管理

## receive/receive.py
- 11行目のCOMの値をつながっているCOM番号に変更して実行
- TeraTermなら繋ぐだけで大丈夫。実行する必要すらないよ

## run/calibration.py
- cal(l, r, n) : キャリブレーション用
    - 引数
        - l : 左タイヤの出力
        - r : 右タイヤの出力
        - n : 回数（1回 0.03sec）
    - 返り値
        - magx_off : x軸方向の地磁気オフセット
        - magy_off : y軸方向の地磁気オフセット

- angle(magx, magy, magx_off=0, magy_off=0) : ローバー自身の方位角取得
    - 引数
        - magx : 現在のx軸方向の地磁気
        - magy : 現在のy軸方向の地磁気
        - magx_off : x軸方向の地磁気オフセット（デフォルト 0）
        - magy_off : y軸方向の地磁気オフセット（デフォルト 0）
    - 返り値
        - theta : ローバーが向いてる方位角

## run/gps_navigate.py
- vincenty_inverse(lat1, lon1, lat2, lon2, ellipsoid=None) : 目的地までの距離取得
    - 引数
        - lat1 : 始点の緯度
        - lon1 : 始点の経度
        - lat2 : 終点の緯度
        - lon2 : 終点の経度
        - ellipsoid : 楕円体（デフォルト None）
    - 返り値
        - 'distance' : 距離
        - 'azimuth1' : 方位角（始点>終点）
        - 'azimuth2' : 方位角（終点>始点）

## run/stuck.py
- ue_ jug() : ローバーの状態を確認
    - 引数：なし
    - 返り値：なし
    - 補足
        - 向きが正常ならそのまま抜ける
        - 向きが上下逆なら戻す方向にモーターを回す

- stuck_jug(lat1, lon1, lat2, lon2, thd=1.0) : スタック判定用
    - 引数
        - lat1 : 始点の緯度
        - lon1 : 始点の経度
        - lat2 : 終点の緯度
        - lon2 : 終点の経度
        - thd : しきい値（デフォルト 1.0）
    - 返り値
        - bool : スタック判定でFalse

- stuck_avoid()
    - 引数 : なし
    - 返り値 : なし
    - 補足
        - 