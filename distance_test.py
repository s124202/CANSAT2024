import pandas as pd
from geopy.distance import geodesic

#csv読み込み
df = pd.read_csv("distance_test.csv")
for i in range(0, 904):
    iwata = ((df.at[0, 'Y_CODE']), (df.at[0, 'X_CODE']))
    destination = ((df.at[i, 'Y_CODE']), (df.at[i, 'X_CODE']))
    x = geodesic(iwata, destination).m
    df.at[0+i, 'distance'] = x  
df.to_csv("distance.csv")
