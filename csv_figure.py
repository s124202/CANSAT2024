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

x = content[:,0]
y = content[:,1]


fig, ax = plt.subplots()
ax.scatter(x,y,label='ラベル')
ax.set_xlabel('time')
ax.set_ylabel('press[hpa]')


# ax.legend()
# ax.set_xscale('log')
# ax.set_yscale('log')
ax.set_ylim([950,1050])

# plt.savefig('.png', dpi=300)
plt.show()
