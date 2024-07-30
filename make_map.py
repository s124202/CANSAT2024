import matplotlib.pyplot as plt
import numpy as np

import gps_navigate

# サンプルデータ
data = [
    {"latitude": 35.924045, "longitude": 139.91266, "azimuth": 3.715958091904213},
    {"latitude": 35.92411, "longitude": 139.912622, "azimuth": 17.174510829165627},
    {"latitude": 35.924192, "longitude": 139.912572, "azimuth": -90.01633832991769},
    {"latitude": 35.924277, "longitude": 139.912513, "azimuth": -11.67693538236773}
]

# ゴール地点
goal = {"latitude": 35.9243106, "longitude": 139.912492} 

# 緯度と経度のリストを作成
latitudes = [point["latitude"] for point in data]
longitudes = [point["longitude"] for point in data]
azimuths = [point["azimuth"] for point in data]

# 矢印の方向を計算
u = np.cos(np.radians(azimuths))
v = np.sin(np.radians(azimuths))

# 各地点とゴール地点の距離を計算
distances = [gps_navigate.vincenty_inverse(point["latitude"], point["longitude"], goal["latitude"], goal["longitude"])["distance"] for point in data]

# グラフを作成
plt.figure(figsize=(10, 6))
#plt.scatter(latitudes, longitudes, c='blue', marker='o')
plt.plot(latitudes, longitudes, marker='o', linestyle='-', color='blue')

# 矢印を追加
plt.quiver(latitudes, longitudes, u, v, angles='xy', scale_units='xy', scale=100000, color='red')

# ゴール地点をプロット
plt.scatter(goal["latitude"], goal["longitude"], color='green', marker='x', s=100, label='Goal')
plt.text(goal["latitude"], goal["longitude"], 'GOAL', fontsize=12, ha='left', color='green')

# 各地点に距離を表示
for i, (lat, lon, dist) in enumerate(zip(latitudes, longitudes, distances)):
    plt.text(lat, lon, f'{dist:.4f}', fontsize=12, ha='right')

# グラフのラベルを設定
plt.xlabel('lat')
plt.ylabel('lon')
plt.title('graph')

# グラフを表示
plt.grid(True)
plt.show()