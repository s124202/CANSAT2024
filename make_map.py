import matplotlib.pyplot as plt
import numpy as np
import csv

import gps_navigate


#input
data = []
with open('run_data_0816.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        data.append({
            "latitude": float(row["latitude"]),
            "longitude": float(row["longitude"]),
            "azimuth": float(row["azimuth"])
        })

#fixed point
start = {"latitude": 40.141782, "longitude": 139.986828}
goal = {"latitude": 40.142282, "longitude": 139.987399}

#list
latitudes = [point["latitude"] for point in data]
longitudes = [point["longitude"] for point in data]
azimuths = [point["azimuth"] for point in data]

# 各地点とゴール地点の距離を計算
# distances, degrees = [gps_navigate.vincenty_inverse(point["latitude"], point["longitude"], goal["latitude"], goal["longitude"])["distance"] for point in data]
results = [gps_navigate.vincenty_inverse(point["latitude"], point["longitude"], goal["latitude"], goal["longitude"]) for point in data]
distances = [result["distance"] for result in results]
degrees = [result["azimuth1"] for result in results]

# azimuthsにdegreesを足す
adjusted_azimuths = [azimuth + degree for azimuth, degree in zip(azimuths, degrees)]

# 矢印の方向を計算
u = np.cos(np.radians(adjusted_azimuths))
v = np.sin(np.radians(adjusted_azimuths))

# グラフを作成
plt.figure(figsize=(10, 6))
#plt.scatter(latitudes, longitudes, c='blue', marker='o')
plt.plot(latitudes, longitudes, marker='o', linestyle='-', color='blue')

# 矢印を追加
plt.quiver(latitudes, longitudes, u, v, angles='xy', scale_units='xy', scale=50000, color='red')

# ゴール地点をプロット
plt.scatter(goal["latitude"], goal["longitude"], color='green', marker='x', s=100, label='Goal')
plt.text(goal["latitude"], goal["longitude"], 'GOAL', fontsize=12, ha='left', color='green')

plt.scatter(start["latitude"], start["longitude"], color='green', marker='x', s=100, label='Start')
plt.text(start["latitude"], start["longitude"], 'START', fontsize=12, ha='left', color='green')

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