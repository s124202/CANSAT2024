# import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['xtick.direction'] = 'in' # 目盛りの向き
plt.rcParams['ytick.direction'] = 'in' 
plt.rcParams['axes.grid'] = False # グリッドの作成
plt.rcParams['grid.linestyle']='--' # グリッドの線種
#plt.rcParams['xtick.minor.visible'] = True  # 補助目盛りの追加
#plt.rcParams['ytick.minor.visible'] = True
plt.rcParams['xtick.top'] = True  # x軸の上部目盛り
plt.rcParams['ytick.right'] = True  # y軸の右部目盛り
# plt.rcParams['figure.figsize'] = [10,6] # 比率
plt.rcParams['font.family'] = 'MS Gothic'

filename = 'bme280_save.csv'
content = np.loadtxt(filename,encoding='utf-8-sig', delimiter=',')

x = []
y1 = []
y2 = []
y3 = []


for i in range (0,300,1):
    x.append(content[i,0])

for i in range (15,150,1):
    y1.append(content[i,1])

for i in range (150,300,1):
    y2.append(content[i,1])

for i in range (445,583,1):
    y3.append(content[i,1])


fig, ax = plt.subplots()

ax.scatter(x[:len(y1)],y1,label='1周目')
ax.scatter(x[:len(y2)],y2,label='2周目')
ax.scatter(x[:len(y3)],y3,label='3周目')

ax.set_xlabel('time[s]')
ax.set_ylabel('press[hpa]')


ax.legend()
# ax.set_xscale('log')
# ax.set_yscale('log')
ax.set_ylim([1003,1008])

# plt.savefig('.png', dpi=300)
plt.show()
