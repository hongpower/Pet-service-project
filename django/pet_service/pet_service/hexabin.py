# -*- coding:utf-8 -*-

import folium
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import json
import csv


plt.rcParams['font.family'] = 'Malgun Gothic'

df = pd.read_csv("whole_merged_data.csv", sep=",")
df2 = df.sort_values('구별 총 생산')
# print(df)
# print(df2)
gus = df2['지역명'].tolist()
df_facility = df2.iloc[:,[1,2,3,4,5,6,7,8,9,10,11]]
list_GRDP = df2['구별 총 생산'].tolist()
list_population= df2['인구'].tolist()
print(list_GRDP)
print(list_population)

list_facility_tot=df_facility.sum(axis=1).tolist()
print(list_facility_tot)

# df1=pd.concat([df_GRDP,df_population,df_facility_tot], axis=1)
# print(df1)

size = np.array(list_population)/300 # 마커 사이즈 (인구)

plt.figure(figsize=(15, 8))
n = len(list_GRDP)
r = 2 * np.random.rand(n)
theta = 2 * np.pi * np.random.rand(n)
area = 200 * r**2 * np.random.rand(n)
colors = theta

hexabin = sns.jointplot(x = list_facility_tot, y=list_GRDP, kind='hex')
hexabin.set_axis_labels(xlabel='총 시설 개수', ylabel='구별 총 생산')
hexabin.fig.suptitle('Hexabin', fontsize=10, y=1.1)
plt.show()
