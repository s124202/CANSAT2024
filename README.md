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
## main

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
        - magx_off : x軸方向の地磁気オフセット（デフォルト0）
        - magy_off : y軸方向の地磁気オフセット（デフォルト0）
    - 返り値
        - theta : ローバーが向いてる方位角

## run/gps_navigate.py

## run/stuck.py