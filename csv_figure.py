import numpy as np
import matplotlib.pyplot as plt
import csv

filename = 'bme280_save.csv'
content = np.loadtxt(filename,encoding='utf-8-sig', delimiter=',')

x = content[:,0]
y = content[:,1]

plt.plot(x,y)
plt.show()
