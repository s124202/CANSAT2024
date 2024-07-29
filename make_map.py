import pandas as pd
import folium
import math
import matplotlib.pyplot as plt

# CSV ファイルからデータを読み込む
csv_file = "teraterm3.csv"
df = pd.read_csv(csv_file)

# 現在地の緯度経度 (例)
current_lat, current_lon = 35.924082, 139.911127

# Folium を使って地図を作成
folium_map = folium.Map(location=[current_lat, current_lon], zoom_start=10)

# 各地点をマーカーでプロット
for i, row in df.iterrows():
    folium.Marker(location=[row['緯度'], row['経度']], popup=row['地点名']).add_to(folium_map)

    # 方位角を矢印形式で表示
    azimuth = math.radians(row['方位角'])
    arrow_x = 0.01 * math.cos(azimuth)
    arrow_y = 0.01 * math.sin(azimuth)
    folium.PolyLine([(row['緯度'], row['経度']), (row['緯度'] + arrow_x, row['経度'] + arrow_y)],
                    color='blue', weight=2).add_to(folium_map)

# 地図を保存
folium_map.save('map.html')

# 方位角を矢印形式で表示
plt.figure(figsize=(8, 6))
plt.quiver(current_lon, current_lat, arrow_x, arrow_y, angles='xy', scale_units='xy', scale=1, color='b', label='Arrow')
plt.scatter(df['経度'], df['緯度'], color='r', label='Locations')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Arrow Representation of Azimuth')
plt.legend()
plt.grid(True)
plt.show()
