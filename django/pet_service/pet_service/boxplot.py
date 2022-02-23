# -*- coding:utf-8 -*-

import folium
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import json
import csv

plt.rcParams['font.family'] = 'Malgun Gothic'

df = pd.read_csv("../data/whole_merged_data2.csv", sep=",")
column_names=list(df.columns)
gus = df['지역명'].tolist()

train_a=df['Education_Center.json'].tolist()
play_a=df['pet_cafe.json'].tolist()
train_b=df['pet_garden.json'].tolist()
train_c=df['pet_hotel.json'].tolist()
play_b=df['Pet_playground.json'].tolist()
beauty_a=df['pet_salon.json'].tolist()
shop_a=df['pet_store.json'].tolist()
together_a=df['together_cafe.json'].tolist()
together_b=df['반려동물 동반 가능 식당'].tolist()
hosp_a=df['동물약국'].tolist()
play_c=df['공원 개수'].tolist()
hosp_b=df['병원수'].tolist()
group_size = 6

label_lst = ['애견 교육 시설','애견 유치원','애견 호텔','애견 카페','반려견 놀이터','공원','동반가능 카페','동반가능 식당', '동물약국', '동물병원','애견 미용실','애견 스토어' ]
y_lst = [train_a,train_b,train_c,play_a,play_b,play_c,together_a,together_b,hosp_a,hosp_b,beauty_a,shop_a]

grp0 = list(zip(label_lst[0:3],y_lst[0:3]))
grp_color0 = ['blue' for _ in range(len(grp0))]
grp1 = list(zip(label_lst[3:6],y_lst[3:6]))
grp_color1 = ['brown' for _ in range(len(grp1))]
grp2 = list(zip(label_lst[6:8],y_lst[6:8]))
grp_color2 = ['green' for _ in range(len(grp2))]
grp3 = list(zip(label_lst[8:10],y_lst[8:10]))
grp_color3 = ['red' for _ in range(len(grp3))]
grp4 = list(zip(label_lst[10:11],y_lst[10:11]))
grp_color4 = ['purple' for _ in range(len(grp4))]
grp5 = list(zip(label_lst[11:12],y_lst[11:12]))
grp_color5 = ['pink' for _ in range(len(grp5))]

fig, (ax1, ax2) = plt.subplots(nrows=1,ncols=2,figsize=(20,8))
plt.suptitle('서울시 애견 업종별 분포')
totalcolor = grp_color0 + grp_color1 + grp_color2 + grp_color3 + grp_color4 + grp_color5

violin = ax1.violinplot(y_lst, showmeans=True)
ax1.set_xticklabels(label_lst, fontsize=8)
ax1.set_xticks(np.arange(1, 13))
for i in range(len(y_lst)):
    violin['bodies'][i].set_facecolor(totalcolor[i])
    violin['cbars'].set_edgecolor('gray')
    violin['cmaxes'].set_edgecolor('gray')
    violin['cmins'].set_edgecolor('gray')
    violin['cmeans'].set_edgecolor('gray')

boxplot = ax2.boxplot(y_lst, patch_artist=True, whiskerprops={'color':'gray'}, medianprops={'color':'gray'})
ax2.set_xticklabels(label_lst, fontsize=8)
ax2.set_xticks(np.arange(1, 13))
for patch, color in zip(boxplot['boxes'], totalcolor):
    patch.set_alpha(0.3)
    patch.set_edgecolor('gray')
    patch.set_facecolor(color)
    patch.set_linewidth(2)
plt.setp(boxplot['fliers'], markeredgecolor='black')
plt.tight_layout()
plt.show()

