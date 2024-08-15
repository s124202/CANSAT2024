import serial
import time

# シリアルポートの設定
port = "/dev/serial0"  # ラズベリーパイのシリアルポート
baudrate = 9600

# シリアルポートを開く
ser = serial.Serial(port, baudrate, timeout=1)

def parse_gps(data):
    if data[0:6] == b'$GPGGA':
        s = data.decode('utf-8')
        parts = s.split(',')
        if len(parts) > 5:
            lat = float(parts[2])
            lon = float(parts[4])
            return lat, lon
    return None, None

try:
    while True:
        data = ser.readline()
        lat, lon = parse_gps(data)
        if lat and lon:
            print(f"Latitude: {lat}, Longitude: {lon}")
        time.sleep(1)
except KeyboardInterrupt:
    ser.close()
    print("プログラムを終了しました。")
