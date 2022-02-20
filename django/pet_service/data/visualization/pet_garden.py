# -*- coding:utf-8 -*-

import folium
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import json

plt.rcParams['font.family'] = 'Malgun Gothic'

with open('../pet_garden.json', 'r', encoding='utf-8') as f:
    petgarden_json = json.load(f)
# print(petcafe_json)
gus = petgarden_json.keys()
# print(gus)
cnt_dict = {}
for gu in gus:
    cnt = len(petgarden_json[gu])
    cnt_dict[gu] = cnt
# print(cnt_dict)
tot = sum(cnt_dict.values())
avg = tot/len(cnt_dict)
df = pd.DataFrame.from_dict([cnt_dict])
# print(df)

b = sns.barplot(data=df,color='blue')
b.axhline(y=avg, color='red',linestyle='dashed', label="평균")
b.set_xticklabels(b.get_xticklabels(),rotation = 45)
b.set_title('애견 공원 갯수')
b_png = b.get_figure()
b_png.savefig('./foo.png')

# sns.barplot(data=cnt_dict, x='gu')
# plt.show()